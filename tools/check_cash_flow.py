#!/usr/bin/env python3
"""Check the cash-flow page's data and calculations, read from the pages' embedded data.

Run with: python3 tools/check_cash_flow.py
Requires Node for executing the page's actual calculation functions; no network.
The page's capex must agree with the demand monitor's release-checked capex for every quarter both carry.
"""
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
html = (SITE / 'ai-cash-flow-monitor.html').read_text()
D = json.loads(html.split('/*AI-CASH-FLOW-DATA-START*/')[1].split('/*AI-CASH-FLOW-DATA-END*/')[0])
DEMAND = json.loads((SITE / 'ai-demand-monitor.html').read_text()
                    .split('/*AI-DEMAND-DATA-START*/')[1].split('/*AI-DEMAND-DATA-END*/')[0])
checks = 0


def check(condition, message):
    global checks
    checks += 1
    assert condition, message


def close(a, b):
    return (a is None and b is None) or (a is not None and b is not None and math.isclose(a, b, abs_tol=1e-9))


# Independent Python implementation of the page's method.
def q_index(q):
    return int(q[:4]) * 4 + int(q[5]) - 1


def q_name(i):
    return f'{i // 4}Q{i % 4 + 1}'


def to_usd(c, r):
    if c['currency'] == 'USD':
        return 1.0
    fx = D['fx'][c['currency']]
    v = fx['q'].get(r['q'])
    return None if v is None else (1 / v if fx['quote'] == 'per_usd' else v)


def ttm(c, q):
    by_q = {r['q']: r for r in c['quarters']}
    rows = [by_q.get(q_name(i)) for i in range(q_index(q) - 3, q_index(q) + 1)]
    if any(r is None or to_usd(c, r) is None for r in rows):
        return None
    ocf = sum(r['ocf'] * to_usd(c, r) for r in rows)
    capex = sum(r['capex'] * to_usd(c, r) for r in rows)
    return {'ocf': ocf, 'capex': capex, 'fcf': ocf - capex}


companies = {c['t']: c for c in D['companies']}
last = max(q_index(r['q']) for c in D['companies'] for r in c['quarters'])
quarters = [q_name(i) for i in range(q_index(D['start_q']), last + 1)]

# Data contract.
for g in D['groups']:
    for t in g['tickers']:
        check(t in companies, f'{g["name"]}: {t} has no company row')
check('NVDA' in D['groups'][0]['tickers'] and 'NVDA' in D['groups'][1]['tickers'], 'Nvidia belongs to both groups')
for c in D['companies']:
    qs = [r['q'] for r in c['quarters']]
    check(qs == sorted(set(qs), key=q_index), f'{c["t"]}: quarters ordered and unique')
    for r in c['quarters']:
        check(all(isinstance(r[k], (int, float)) and math.isfinite(r[k]) for k in ('ocf', 'capex')),
              f'{c["t"]} {r["q"]}: operating cash flow and capex present')
        check(r['capex'] >= 0, f'{c["t"]} {r["q"]}: capex is a positive outflow')
        check(to_usd(c, r) is not None, f'{c["t"]} {r["q"]}: has a {c["currency"]} rate')
        check(r['filed'][:10] <= D['as_of'], f'{c["t"]} {r["q"]}: filed by the pull date')
    check(c['cik'], f'{c["t"]}: has a CIK for its SEC link')

# Cross-page: the capex line is the demand monitor's, quarter for quarter.
shared = 0
for dc in DEMAND['capex']['companies']:
    if dc['t'] not in companies:
        continue
    mine = {r['q']: r['capex'] for r in companies[dc['t']]['quarters']}
    for r in dc['quarters']:
        if r.get('capex') is not None and r['q'] in mine:
            shared += 1
            check(abs(mine[r['q']] - r['capex']) <= 0.01, f'{dc["t"]} {r["q"]}: capex {mine[r["q"]]} vs demand {r["capex"]}')
check(shared >= 20, f'cash-flow and demand pages share {shared} capex quarters')

# The page's own functions, run in Node, must match the Python method above.
code = 'const D = ' + json.dumps(D) + ';\n'
code += html[html.index('const qIndex'):html.index('/* ---------- presentation ---------- */')]
code += '''
const out = {groups: D.groups.map(g => ({id: g.id, series: groupSeries(g), latest: latestComplete(g)})),
  ttm: Object.fromEntries(D.companies.map(c => [c.t, {q: latestTtmQ(c), v: latestTtmQ(c) ? ttm(c, latestTtmQ(c)) : null}]))};
console.log(JSON.stringify(out));
'''
page = json.loads(subprocess.run(['node', '-e', code], check=True, capture_output=True, text=True).stdout)
for g, pg in zip(D['groups'], page['groups']):
    for q, s in zip(quarters, pg['series']):
        parts = [p for p in (ttm(companies[t], q) for t in g['tickers']) if p]
        check(s['q'] == q and s['reported'] == len(parts) and s['n'] == len(g['tickers']), f'{g["name"]} {q}: reporting count')
        for k in ('ocf', 'capex', 'fcf'):
            check(close(s[k], sum(p[k] for p in parts)), f'{g["name"]} {q}: TTM {k}')
    done = [s for s in pg['series'] if s['reported'] == s['n']]
    check(pg['latest'] and pg['latest']['q'] == done[-1]['q'], f'{g["name"]}: latest complete quarter')
for t, v in page['ttm'].items():
    py = ttm(companies[t], v['q'])
    for k in ('ocf', 'capex', 'fcf'):
        check(close(v['v'][k], py[k]), f'{t} {v["q"]}: TTM {k}')

print(f'✓ cash flow: {checks} checks, {len(D["companies"])} companies, {shared} capex quarters reconcile with the demand monitor')
