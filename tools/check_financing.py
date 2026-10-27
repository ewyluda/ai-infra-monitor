#!/usr/bin/env python3
"""Check financing-ledger data, embedded parity, calculations and the October 27 audit fixes.

Run with: python3 tools/check_financing.py
Requires Node for executing the page's actual calculation functions; no network.
Regression fixtures are from docs/reviews/2026-10-27-financing-ledger-audit.md.
"""
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
L = json.loads((SITE / 'data/neocloud-financing-ledger.json').read_text())
C = json.loads((SITE / 'data/capacity.json').read_text())
html = (SITE / 'neocloud-financing-ledger.html').read_text()
checks = 0


def check(condition, message):
    global checks
    checks += 1
    assert condition, message


def equal(actual, expected, message, tol=1e-6):
    check(actual is not None and math.isclose(actual, expected, abs_tol=tol), f'{message}: {actual} != {expected}')


embedded = json.loads(html.split('/*FIN-DATA-START*/')[1].split('/*FIN-DATA-END*/')[0])
check(embedded == L, 'Embedded HTML data differs from standalone JSON')
code = 'const LED = ' + json.dumps(L) + ';\n'
code += html[html.index('/* ---------- base helpers'):html.index('/* ---------- end base helpers ---------- */')]
code += '''
const I=LED.instruments, sum=w=>Object.values(w).reduce((s,b)=>s+Object.values(b).reduce((a,c)=>a+c,0),0);
const pick=(t,s)=>I.filter(r=>r.t===t&&r.name.includes(s));
const wall=maturityWall(I,true,true), money=maturityWall(I,true,true,true);
console.log(JSON.stringify({
  totals:totals(I), totals_bd:totals(I,false), wall, wall_bd:maturityWall(I,false,true), near:nearTerm(wall),
  peak:peakWindow(wall,PEAK_YEARS), com:commitments(I), recon:reconciliation(), puts:holderPuts(I,'2027-12-31'),
  accretion:accretion(I), moneyness:moneyness(I),
  magnetar:maturityWall(pick('CRWV','Magnetar'),true,true),
  crwv_converts:maturityWall(I.filter(r=>r.t==='CRWV'),true,true),
  converts_only:sum(maturityWall(I.filter(r=>r.type==='convert'),true,true)),
  splits:LED.companies.filter(c=>c.filed_ladder).map(c=>{const s=ladderSplit(c);
    return {t:c.t,left:s.left,after:s.after,late:s.late.length,bullets:s.bullets.length};}),
  iceland:maturityWall(pick('WYFI','Iceland'),false,true), btc_loan:maturityWall(pick('BTDR','BIT Bitcoin Loan'),false,true),
}));
'''
result = subprocess.run(['node'], input=code, text=True, capture_output=True, check=True)
A = json.loads(result.stdout)
cos = {c['t']: c for c in L['companies']}
rows = L['instruments']
debt = [r for r in rows if r.get('category', 'lease' if r['type'] == 'lease' else 'financial_debt') == 'financial_debt']


def row(t, needle):
    hits = [r for r in rows if r['t'] == t and needle in r['name']]
    check(len(hits) == 1, f'{t} {needle}: expected one row')
    return hits[0]


def wall_total(w):
    return sum(sum(b.values()) for b in w.values())


# Totals reproduce independently from the stored rows.
pf_debt = sum(r['drawn_m'] or 0 for r in debt)
equal(A['totals']['debt'], pf_debt, 'Pro-forma financial debt')
equal(A['totals']['converts'], sum(r['drawn_m'] or 0 for r in debt if r['type'] == 'convert'), 'Convert principal')
check(abs(wall_total(A['wall']) - pf_debt) <= 5, 'Maturity wall reconciles to financial debt within filed-ladder rounding')
check(abs(wall_total(A['wall_bd']) - A['totals_bd']['debt']) <= 5, 'Balance-date wall reconciles to balance-date debt')
equal(A['converts_only'], A['totals']['converts'], 'A converts-only selection carries every convert at full principal')

# F03: bullets keep their principal at contractual maturity inside a filed ladder.
equal(A['crwv_converts']['2031']['convert'], 2587.5, 'CRWV 1.75% 2031 converts at full principal')
equal(A['crwv_converts']['2032']['convert'], 4000.0, 'CRWV 1.75% 2032 converts at full principal')
for s in A['splits']:
    check(all(a >= -0.5 for _, a in s['left']) and s['after'] >= -0.5, f'{s["t"]}: ladder period smaller than its bullets')
    check(s['after'] <= 0.5 or s['late'] > 0, f'{s["t"]}: ladder remainder has no amortizing row to carry it')

# F02: filed principal schedules are captured and tie to balance-date principal.
for t in ('CRWV', 'WULF', 'CIFR', 'IREN', 'APLD', 'HUT'):
    lad = cos[t].get('filed_ladder')
    check(bool(lad), f'{t}: filed principal ladder captured')
    total = sum(lad['years'].values()) + lad['after']['amount_m']
    covered = [r for r in debt if r['t'] == t and (not (r.get('as_of') and r['as_of'] > cos[t]['balance_date']) or 'drawn_bd_m' in r)]
    bd = sum((r['drawn_bd_m'] or 0) if 'drawn_bd_m' in r else (r['drawn_m'] or 0) for r in covered)
    check(abs(total - bd) <= 1.0, f'{t}: ladder {total} vs balance-date principal {bd}')
check(row('CORZ', '7.75% Senior Secured Notes').get('schedule') == [['2029', 189.75], ['2030', 379.5], ['2031-05-15', 2730.75]],
      'CORZ secured-note schedule')

# F05: one reporting basis per view.
equal(A['totals_bd']['debt'], 92548.343, 'Balance-date financial debt', 1e-3)

# F06: a partial selection does not inject an issuer's whole ladder.
equal(wall_total(A['magnetar']), 189.0, 'Magnetar search wall')
check(set(A['magnetar']) == {'2029'}, 'Magnetar sits at its own maturity only')

# F07 / F09: WhiteFiber repayments and non-revolving availability; Riot letters of credit.
equal(row('WYFI', 'B. Riley Facility')['drawn_m'], 0.0, 'B. Riley note repaid 2026-08-24')
equal(row('WYFI', 'Delayed Draw Term Loan')['drawn_m'], 30.0, 'Bit Digital DDTL after the 2026-09-23 repayment')
check(row('WYFI', 'Delayed Draw Term Loan')['available_m'] <= 20.0, 'Non-revolving DDTL availability')
equal(row('RIOT', '$50 Million Revolving')['available_m'], 0.557, 'Riot revolver after letters of credit')
check(sum(o['available'] for o in A['com'].values()) <= 15390.667 + 1e-6, 'Available undrawn bound')

# F08: Bitdeer September asset-loan balance; bitcoin loan stays at its last valued balance.
equal(row('BTDR', 'BIT Assets Collateralized Loan')['drawn_m'], 423.3, 'Bitdeer asset loan at 2026-09-29')
equal(row('BTDR', 'BIT Bitcoin Loan')['drawn_m'], 144.6, 'Bitdeer bitcoin loan at its June valuation')

# F10 / F11 / F01: cash scopes and bridges.
recon = {r['t']: r for r in A['recon']}
equal(recon['BTBT']['pf_nd'], 172.501, 'Bit Digital parent net debt on parent cash', 1e-3)
equal(cos['CIFR']['cash_m'], 831.829, 'Cipher unrestricted cash')
check('net cash by' not in cos['CIFR']['reconciliation_note'], 'Cipher narrative does not double-count restricted cash')
bridge = {(t, p['amount_m']) for t in ('BTDR', 'GLXY', 'MARA') for p in cos[t]['pro_forma_cash']}
check({('BTDR', 58.0), ('GLXY', -25.4), ('MARA', -100.0)} <= bridge, 'Disclosed post-quarter cash movements')

# F12: no maturity is guessed from text that names more than one year.
for r in rows:
    if len(set(re.findall(r'(?<!\d)20\d\d(?!\d)', r.get('maturity') or ''))) > 1:
        check(bool(r.get('final_maturity')), f'{r["t"]} {r["name"]}: final_maturity')
check(set(A['iceland']) == {'2028'}, 'WhiteFiber Iceland loan at its unextended 2028 maturity')
check(set(A['btc_loan']) == {'2027'}, 'Bitdeer bitcoin loan in the period ending June 2027')

# F13 / F14.
check('parent' in row('IREN', 'Mackenzie')['recourse'], 'IREN Mackenzie parent payment guarantee')
equal(row('CRWV', 'DDTL 2.0 Facility')['committed_m'] + row('CRWV', 'DDTL 2.1 Facility')['committed_m'], 8000.0,
      'CoreWeave DDTL 2.0/2.1 combined capacity')

# F04: the comparison is bound to the published capacity snapshot.
tr = L['tracker']
check(tr['published_at'] == C['published_at'], 'Tracker snapshot is the published capacity.json')
check(tr['quote_as_of'] == C['priced_date'], 'Tracker price date')
cap = {c['t']: c for c in C['companies']}
for t, v in tr['rows'].items():
    check((v['px'], v['nd'], v['ndflag']) == (cap[t]['px'], cap[t]['nd'], cap[t]['ndflag']), f'{t}: tracker row parity')
for t, co in cos.items():
    check(not co.get('tracker_to_principal_m') or bool(co.get('tracker_to_principal_note')), f'{t}: principal bridge sourced')
check(not row('CRWV', 'Operating lease liabilities')['nd_include'], 'CoreWeave net debt excludes operating leases, as published')

# L01 / L02 / L03: puts, accretion and settlement beside the wall.
equal(sum(p['amount_m'] for p in A['puts']), 989.1, 'Holder puts exercisable through 2027 (stored rounding)', 1e-6)
equal(A['accretion'], 2302.295, 'Accretion above stored principal', 1e-3)
settle = {m['name']: m['settlement'] for m in A['moneyness'] if m['t'] == 'WULF'}
check(settle['2.75% convertible senior notes due 2030'] == settle['1.00% convertible senior notes due 2031'] == 'cash principal',
      'TeraWulf cash-principal settlement')

manifest = json.loads((SITE / 'site.json').read_text())
check(next(p['as_of'] for p in manifest['pages'] if p['file'] == 'neocloud-financing-ledger.html') == L['as_of'],
      'Financing manifest date')

print(f'✓ {checks} financing checks: data parity, calculations, filed schedules and audit regressions')
print(json.dumps({'debt_m': A['totals']['debt'], 'debt_balance_date_m': A['totals_bd']['debt'],
                  'due_by_end_next_year_m': A['near'], 'holder_puts_m': sum(p['amount_m'] for p in A['puts']),
                  'peak': A['peak'], 'available_m': sum(o['available'] for o in A['com'].values()),
                  'disagree': [r['t'] for r in A['recon'] if r['status'] == 'disagree']}, indent=2))
