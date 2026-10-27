#!/usr/bin/env python3
"""Check demand data, embedded parity, arithmetic, bounds and capacity provenance.

Run with: python3 tools/check_demand.py
Requires Node for executing the page's actual calculation functions; no network.
Historical regression fixtures are from the October 27, 2026 source audit.
"""
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
D = json.loads((SITE / 'data/ai-demand-monitor.json').read_text())
capacity_path = SITE / 'data/capacity.json'
C = json.loads(capacity_path.read_text())
html = (SITE / 'ai-demand-monitor.html').read_text()
checks = 0


def check(condition, message):
    global checks
    checks += 1
    assert condition, message


def equal(actual, expected, message):
    check((actual is None and expected is None) or
          (actual is not None and expected is not None and
           math.isclose(actual, expected, abs_tol=1e-9)), message)


embedded = json.loads(html.split('/*AI-DEMAND-DATA-START*/')[1]
                     .split('/*AI-DEMAND-DATA-END*/')[0])
check(embedded == D, 'Embedded HTML data differs from standalone JSON')
code = 'const D = ' + json.dumps(D) + ';\n'
code += html[html.index('const HYPER'):html.index('/* ---------- header ---------- */')]
code += '''
const bound = {fy:"FY2026",kind:"full_year",low:25,high:null,qualifier:"over"};
const point = {...bound,low:50,high:50,qualifier:null};
const pair = (a,b) => ({quarters:[{q:"2025Q2",call_date:"2025-06-11",guide:a},
  {q:"2026Q1",call_date:"2026-03-10",guide:b,fy_actual:{fy:"FY2026",value:55}}]});
console.log(JSON.stringify({
  company:D.capex.companies.map(c=>({t:c.t,qoq:qoqSeries(c),ttm:ttm(c),runRate:runRate(c),guides:guideRevisions(c)})),
  ttm:cohortTtm(),runRate:cohortRunRate(),totals:cohortQuarterTotals(),yoy:cohortYearOnYear(),
  latest:latestGuides(),progress:guideProgress(),ratio:capexPerContractedGw(),
  bounds:{mid:guideMid(bound),text:guideText(bound),
    first:guideRevisions(pair(bound,point)).FY2026,
    last:guideRevisions(pair(point,bound)).FY2026,
    finite:guideRevisions(pair({...point,low:30,high:40},point)).FY2026,
    latest:(()=>{ const row=D.capex.companies.find(c=>c.t==="ORCL").quarters.slice(-1)[0], saved=row.guide;
      row.guide={...saved,low:95,high:null,qualifier:"over"};
      try { return guideProgress().find(p=>p.t==="ORCL"); } finally { row.guide=saved; } })()}
}));
'''
result = subprocess.run(['node'], input=code, text=True, capture_output=True, check=True)
actual = json.loads(result.stdout)
companies = {c['t']:c for c in D['capex']['companies']}
hyperscalers = [c for c in companies.values() if c['cohort'] == 'hyperscaler']

for computed in actual['company']:
    company = companies[computed['t']]
    quarters = company['quarters']
    tags = [q['q'] for q in quarters]
    check(tags == sorted(set(tags)), f'{company["t"]}: duplicate or unordered quarters')
    for i, row in enumerate(quarters):
        expected = None if i == 0 else (row['capex'] - quarters[i-1]['capex']) / quarters[i-1]['capex']
        equal(computed['qoq'][i][2], expected, f'{company["t"]} {row["q"]}: q/q')
        check(row['as_of'] >= row['period_end'], f'{company["t"]} {row["q"]}: disclosure precedes period end')
    equal(computed['ttm'], sum(q['capex'] for q in quarters[-4:]), f'{company["t"]}: TTM')
    equal(computed['runRate'], quarters[-1]['capex'] * 4, f'{company["t"]}: run rate')
    for fy, series in computed['guides'].items():
        stated = [q['guide'] for q in quarters if q.get('guide',{}).get('fy') == fy
                  and q['guide'].get('kind','full_year') == 'full_year']
        def midpoint(guide):
            if guide.get('qualifier'):
                return None
            values = [guide[k] for k in ('low','high') if guide.get(k) is not None]
            return sum(values) / len(values)
        expected = None
        if len(stated) > 1 and midpoint(stated[0]) is not None and midpoint(stated[-1]) is not None:
            expected = midpoint(stated[-1]) - midpoint(stated[0])
        equal(series['revision'], expected, f'{company["t"]} {fy}: guide revision')
        if series['actual'] is not None:
            last = midpoint(stated[-1]) if stated else None
            equal(series['vs_actual'], series['actual']-last if last is not None else None,
                  f'{company["t"]} {fy}: actual vs guide')

equal(actual['ttm'],sum(sum(q['capex'] for q in c['quarters'][-4:]) for c in hyperscalers),'Cohort TTM')
equal(actual['runRate'],4*sum(c['quarters'][-1]['capex'] for c in hyperscalers),'Cohort run rate')
for q, total, count in actual['totals']:
    values = [r['capex'] for c in hyperscalers for r in c['quarters'] if r['q'] == q]
    equal(total,sum(values),q+': cohort sum')
    equal(count,len(values),q+': reporting count')
yoy = actual['yoy']
equal(yoy['ratio'],yoy['total']/yoy['prior_total'],'Cohort YoY')
for progress in actual['progress']:
    company = companies[progress['t']]
    fy = progress['fy']
    rows = [r for r in company['quarters'] if
            (r['period_end'][:4] == fy[2:] if fy.startswith('CY') else r['fiscal'][2:4] == fy[-2:])]
    spent = sum(r[company['headline']['field']] for r in rows)
    equal(progress['spent'],spent,progress['t']+': guidance basis spend')
    equal(progress['quarters'],len(rows),progress['t']+': guidance quarter count')
    equal(progress['pace'],progress['mid']*len(rows)/4,progress['t']+': linear pace')
    equal(progress['implied_per_q'],(progress['mid']-spent)/(4-len(rows)),progress['t']+': remaining pace')

# Bounded guidance must not silently become a point estimate or a zero.
equal(actual['bounds']['mid'],None,'A lower bound has no midpoint')
check(actual['bounds']['text'] == '>25','Keep strict floor visible')
equal(actual['bounds']['first']['revision'],None,'No revision from a floor')
equal(actual['bounds']['last']['revision'],None,'No revision to a floor')
equal(actual['bounds']['last']['vs_actual'],None,'No exact actual comparison to a floor')
equal(actual['bounds']['finite']['revision'],15,'Closed-range midpoint revision')
equal(actual['bounds']['finite']['vs_actual'],5,'Actual vs finite guide')
check(len(actual['bounds']['first']['path']) == 2,'Do not drop the bounded first guide')
equal(actual['bounds']['latest']['move'],None,'No exact latest move to an open-ended guide')
equal(actual['bounds']['latest']['pace'],None,'No midpoint pace for an open-ended guide')
equal(actual['bounds']['latest']['implied_per_q'],None,'No implied remaining spend for a floor')

# The published capacity input must reproduce the retained constituent snapshot.
cc = D['capacity_crosscheck']
check(cc['source'] == 'data/capacity.json','Capacity source link')
check(cc['source_sha256'] == hashlib.sha256(capacity_path.read_bytes()).hexdigest(),'Capacity snapshot source changed; reconcile before publishing')
check(cc['source_published_at'] == C['published_at'],'Capacity publication date')
check(cc['capacity_as_of'] == C['as_of_curated'],'Capacity curation date')
selected = [r for r in C['tenants'] if r[1] in cc['deduped_tickers']]
check(len(selected) == len(cc['tenants']),'Capacity tenant snapshot row count')
for source, row in zip(selected,cc['tenants']):
    check(source == [row['tenant'],row['operator'],row['mw'],row['note']],'Tenant source parity')
    reason = 'undisclosed' if source[2] is None else 'inferred' if 'MW inferred' in source[3] else None
    check(row['exclusion_reason'] == reason and row['included'] == (reason is None),'Tenant inclusion classification')
selected_companies = [{k:c[k] for k in ('t','op','con','plan')} for c in C['companies'] if c['t'] in cc['deduped_tickers']]
check(cc['companies'] == selected_companies,'Operator snapshot parity')
for k in ('op','con','plan'):
    equal(cc[k+'_mw'],sum(c[k] for c in selected_companies),k+': operator total')
equal(cc['tenant_contracted_mw'],sum(r['mw'] for r in cc['tenants'] if r['included']),'Included tenant MW')
equal(cc['tenants_counted'],sum(r['included'] for r in cc['tenants']),'Included tenant count')
equal(cc['tenants_undisclosed_mw'],sum(r['exclusion_reason']=='undisclosed' for r in cc['tenants']),'Undisclosed tenant count')
equal(cc['tenants_inferred_mw'],sum(r['exclusion_reason']=='inferred' for r in cc['tenants']),'Inferred tenant count')
equal(cc['inferred_mw_excluded'],sum(r['mw'] for r in cc['tenants'] if r['exclusion_reason']=='inferred'),'Excluded inferred MW')
equal(actual['ratio'],actual['runRate']/(cc['tenant_contracted_mw']/1000),'Run rate per included GW')

# Source-audited historical fixtures: catch a future export overwriting these fixes.
def quarter(t, q):
    return next(r for r in companies[t]['quarters'] if r['q'] == q)

equal(quarter('CRWV','2024Q4')['capex'],3.498,'CoreWeave comparative cash capex')
check(quarter('CRWV','2024Q4')['as_of']=='2026-02-26','CoreWeave comparative disclosure date')
equal(quarter('NBIS','2025Q1')['capex'],0.5439,'Nebius Q1 comparative cash capex')
check(quarter('NBIS','2025Q1')['as_of']=='2026-05-13','Nebius comparative disclosure date')
equal(quarter('NBIS','2025Q2')['capex'],0.5106,'Nebius Q2 capex')
equal(quarter('AMZN','2024Q4')['cash_capex_mgmt'],27.834-1.782,'Amazon baseline net cash capex')
equal(quarter('AMZN','2024Q4')['fin_lease'],0.445,'Amazon baseline lease additions')
equal(quarter('AMZN','2024Q4')['fin_lease_principal'],0.333,'Amazon baseline principal')
equal(quarter('META','2024Q4')['fin_lease_principal'],0.411,'Meta baseline principal')
contracted = {c['t']:c for c in D['contracted']['companies']}
galaxy = next(r for r in contracted['GLXY']['quarters'] if r['q']=='2025Q1')
check(galaxy['value']==13 and galaxy['qualifier']=='over','Galaxy combined lease floor')
galaxy_later = next(r for r in contracted['GLXY']['quarters'] if r['q']=='2026Q1')
check(galaxy_later['report_date']==galaxy_later['as_of']=='2026-05-04','Galaxy source date')
nbis_rpo = next(r for r in contracted['NBIS']['quarters'] if r['q']=='2025Q4')
check(nbis_rpo['report_date']==nbis_rpo['as_of']=='2026-04-30','Nebius annual RPO source date')
nbis_q1 = next(r for r in contracted['NBIS']['quarters'] if r['q']=='2026Q1')
check(nbis_q1['src'].endswith('nbis-20260331xex99d2.htm'),'Nebius RPO exhibit')
sb = next(r for r in D['lab_commitments'] if r['date']=='2026-01-09' and r['lab']=='OpenAI')
equal(sb['usd_b'],0.5,'OpenAI-only equity contribution')
check(any(r.get('transcript_src') for r in D['lab_commitments'] if r['date']=='2025-12-11'),'Broadcom supporting transcript')
manifest = json.loads((SITE/'site.json').read_text())
check(next(p['as_of'] for p in manifest['pages'] if p['file']=='ai-demand-monitor.html') == D['as_of'],'Demand manifest date')

print(f'✓ {checks} demand checks: data parity, source fixtures, calculations, bounds and capacity snapshot')
print(json.dumps({'ttm_b':actual['ttm'],'run_rate_b':actual['runRate'],'yoy':actual['yoy'],
                  'contracted_mw':cc['tenant_contracted_mw'],'run_rate_per_gw':actual['ratio'],
                  'latest_guides_raised':sum(g['move'] is not None and g['move']>0 for g in actual['latest']),
                  'guidance_progress':[{k:p[k] for k in ('t','fy','spent','mid','quarters','implied_per_q')} for p in actual['progress']]},indent=2))
