# Hub pages vs MacroGauge — overlap audit

Review date: **2026-10-27** (America/New_York). Scope: the financing ledger, demand monitor and ETF atlas,
checked against every MacroGauge dataset that publishes the same figures. The capacity page is out of
scope because it already renders MacroGauge's `capacity.json` and a test pins parity.

This is an audit-only record. No published page or dataset was changed. Fixes go where each figure is
generated: MacroGauge's `config/` (by PR), or the private notebook followed by a hub re-export. Editing the
hub's JSON directly would be overwritten by the next export.

## Snapshot

| Side | Version |
| --- | --- |
| Hub | `acf0a88` (main). Ledger and demand monitor read MacroGauge's capacity publish of 2026-10-26T12:49:10Z (curated 10-21, priced 10-23) |
| MacroGauge published | `origin/main` `23866ad9`, daily publish 2026-10-27T12:49:12Z (curated 10-26, priced 10-26) |
| MacroGauge pending | [PR #141](https://github.com/ewyluda/macrogauge/pull/141) head `634ccf15` (net-debt convention, IREN backlog), not merged at review time |

## Where the pages overlap

| Hub page | MacroGauge dataset (page) | Shared figures |
| --- | --- | --- |
| Financing ledger | `capacity.json` (/capacity) | Issuer net debt, the instruments and post-quarter financings named in each `ndflag`, share prices |
| Financing ledger | `rates.json` from `config/issuer_bonds.json` (/rates) | CRWV 9.625% 2032 notes, NBIS 0.50% 2030 converts, loan margins in the table note |
| Demand monitor | `capacity.json` (/capacity) | Contracted backlog (`bk`), hyperscaler and neocloud capex in `econ`, op/con/plan MW, tenant edges and lab deal sizes |
| ETF atlas | none | MacroGauge publishes no ETF prices, holdings or fund data, and none of the six fund tickers appears in its published data or config (its DRAM series is memory spot pricing, not the Roundhill fund) |

MacroGauge's `news.json` is a syndicated headline tape, not curated figures, so it was read for context only.

## Method

- **Net debt:** ran the ledger page's own `reconciliation()` (extracted the same way as
  [`tools/check_financing.py`](../../tools/check_financing.py)) three times, swapping the tracker rows for the
  hub snapshot, MacroGauge's 10-27 publish, and PR #141's config. Moneyness was rerun on the 10-26 prices.
- **Text claims:** every `ndflag` figure for the 15 ledger issuers was compared with the ledger's instrument rows.
- **Demand:** compared each contracted-backlog series, capex quarter and guide with MacroGauge's `bk` and `econ`
  text; the capacity cross-check (MW per operator, 25 tenant rows) field by field; and the 54 lab commitments
  with MacroGauge's 40 tenant edges.
- **Sources opened for this audit:** Nebius pricing and closing releases (8/19, 8/24), Nebius Citi 6-K (10/22),
  TeraWulf Q2 investor deck. Everything else compares the two published datasets. Anthropic S-1 figures below are
  as MacroGauge quotes them; the S-1 itself was not opened.

## Conflicts

**Action** names the side that should change. Confirmed = checked against a primary source in this audit.

### Financing ledger

| # | Figure | Hub | MacroGauge | Status | Action |
| --- | --- | --- | --- | --- | --- |
| F1 | GLXY net debt | $2.52B at 6/30 (principal $3,415.8M − cash $895.7M); $6.05B pro forma with the $3,507M Helios II notes. Flagged **disagree** by $1.53B | $3.9B, "pre-notes basis". The value came over unsourced in the 7/21 notebook port and has never changed; it does not reproduce from the Q2 10-Q on any pre-notes basis (carrying $3,262.8M − cash $895.7M = $2.37B) | Confirmed from both datasets and MacroGauge's git history | MacroGauge: re-derive at the GLXY Q3 re-pull (already in the to-do). Ledger needs no change |
| F2 | NBIS 0.50% converts due 2030, size | $3,450M | /rates shows **$3.00B** (pricing release 8/19). MacroGauge's own capacity `ndflag` says $3.45B | **Confirmed:** the 8/24 closing release says the initial purchasers' $450M option was exercised in full | MacroGauge: `config/issuer_bonds.json` amount → 3.45, cite the 8/24 6-K |
| F3 | Nebius loans | $3.5B Citi 364-day secured bridge, signed 10/17, Term SOFR + 2.75% stepping to 3.50%, drawn amount undisclosed | /rates note: "plus a secured term loan at SOFR + 2.50%" (the $775M facility only); capacity `ndflag` silent | **Confirmed** from the 10/22 6-K. MacroGauge text predates it (`issuer_bonds.json` curated 10-08) | MacroGauge: add the bridge to the /rates note and NBIS `ndflag` at the Q3 re-pull |
| F4 | Net debt after PR #141 publishes | APLD and HUT on the old basis | APLD 2.7 → 3.4, HUT 0.0 → 7.4; BTDR, KEEL, RIOT move $0.05–0.08B | Reproduced: APLD **disagree +$0.70B**, HUT **disagree +$7.40B**; BTDR (+$55M), KEEL (+$53M), RIOT (+$76M) stay inside the max($150M, 3%) tolerance | Notebook: flip every flag the to-do lists after the publish. Only APLD and HUT trip the check, so a missed BTDR, KEEL or RIOT flip would go unflagged |

**Agree:** the other 13 issuers match within tolerance on MacroGauge's 10-27 publish (BTBT differs by
construction: parent vs consolidated). Every `ndflag` figure checked against ledger rows agrees, including
IREN DDTL $413M of $1.5B and USPP $525M of $2.1B, HUT's $3.25B and $4.25B project notes, CIFR's $850M
converts and $165.9M exchange, WYFI's $198.15M exchanged notes, BTDR's $423.3M asset loan, and MARA's
"+$600M" (the ledger's $750M less the $150M line it refinances). CRWV's 9.625% 2032 notes match ($1.25B;
MacroGauge dates the 6/11 pricing, the ledger the 6/18 closing). The hub's tracker snapshot is one publish
behind, but no issuer's net debt changed between the two publishes, and no convert changes moneyness
status on the newer prices.

### Demand monitor

| # | Figure | Hub | MacroGauge | Status | Action |
| --- | --- | --- | --- | --- | --- |
| D1 | Anthropic–Microsoft Azure | $30B, up to 1 GW (11/18/25 announcement) | At least $44.9B, Nov 2026–May 2033, amended Feb and Oct 2026 (Anthropic S-1, 10/26) | Hub predates the S-1 (`labs_as_of` 10-01) | Notebook: refresh from the S-1 |
| D2 | Anthropic–AWS | >$100B, up to 5 GW, 10 yrs | At least $110.0B, May 2026–Apr 2036 (S-1) | As D1 | As D1 |
| D3 | Anthropic–Google Cloud | ~$200B (press, secondary) | At least ~$114.5B GCP, Apr 2026–Jul 2033, plus an estimated $125–150B of TPU compute 2028–31 (S-1) | As D1 | Replace the press row with the S-1 figures |
| D4 | Anthropic–SpaceX/xAI | >0.3 GW, no dollar size | Up to $120.5B into 2029, ~$3.1B/month at full delivery; 500 MW inferred (S-1) | As D1 | As D1 |
| D5 | Anthropic Broadcom TPU leases | $125.2B (Reuters on IPO materials) | ~$161.2B rent (S-1) | As D1 | As D1 |
| D6 | WULF contracted revenue | $27B (Q2 investor deck, 8/5) | $32B, unsourced since the 7/21 notebook port | **Confirmed:** the Q2 deck says "~$27B+ contracted revenue" | MacroGauge: `bk` → 27 with the deck as source |
| D7 | GLXY contracted lease revenue | >$15B (Q1 recap, 5/4) | ~$13.5B (15-yr), unsourced since the 7/21 port; the notebook capacity row says $18B | Three values; GLXY reported Q3 on 10/27 | Both: take the Q3 figure at the GLXY re-pull |
| D8 | IREN contracted backlog | $16.6B at 6/30 (10-K) | $16.5B now (a prior TCV basis, by its own note); **$19.4B** after PR #141 (adds $2.8B of July contracts) | Date difference, both correct for their date | Notebook: add the July contracts as a post-period note, or the Q3 point when IREN reports |
| D9 | NBIS backlog | $37.5B RPO (Q2 6-K) | >$40B customer commitments (Q2 letter) | Different measures, both labeled | None |
| D10 | Meta–Nebius (Mar 2026) | $27B | $12B dedicated, "up-to-$27B incl. conditional take-up" | The hub's $27B includes the conditional $15B (its note says so) | Notebook: mark the row as an upper bound |
| D11 | Anthropic–Akamai | $11.6B, 7 yrs | ~$13.4B ($1.8B edge inference + $11.6B CPU expansion) | MacroGauge adds a $1.8B deal the hub lacks; not sourced in this audit | Check the $1.8B source, then add a row or drop it |
| D12 | Anthropic–Volta (Bitdeer Norway) | 0.133 GW | 121 MW (Bitdeer's Tydal lease) | The hub's own note also says 121 IT MW | Notebook: use 0.121 or state the basis of 0.133 |

**Agree:** every capex quarter and guide MacroGauge states (MSFT FY26 $145.3B incl. finance leases, CY26 ~$175B,
Q1 FY27 >$50B; GOOGL Q2 $44.9B and $195–205B; AMZN ~$220B; ORCL FY26 $55.7B, FY27 Q1 $28.5B, $90–95B;
NBIS Q2 $5.7B); backlog for ORCL $664B, CRWV $104B, APLD $36B, CORZ $24B; the capacity cross-check
(14 operators' op/con/plan MW and all 25 tenant rows) is identical to MacroGauge's 10-27 publish and to PR #141;
OpenAI–Oracle ($300B, 4.5 GW), OpenAI–CoreWeave ($22.4B over three contracts), Meta–CoreWeave ($14.2B + $21B),
Anthropic–TeraWulf ($19B, 401 MW) and Anthropic–Lambda ($35B, ~350 MW).

**Coverage, not conflict:** MacroGauge publishes CRWV's FY26 capex guide ($35–39B); the hub carries no capex
guides for the neocloud buyers.

### ETF atlas

No overlap. The atlas publishes fund metadata, holdings weights and ETF price returns. Fifteen holdings
(APLD, CIFR, CORZ, CRWV, DLR, EQIX, GLXY, HUT, IREN, KEEL, NBIS, ORCL, RIOT, WULF, WYFI) are MacroGauge
capacity companies, but the atlas publishes no company-level figure for them.

## Not covered

- The Anthropic S-1 was not opened; D1–D5 compare the hub with MacroGauge's reading of it.
- GLXY's Q3 release (10/27) was not read, so D7 and F1 have no corrected value yet.
- The trade layer index was out of scope. It shares FMP quotes and market caps with MacroGauge's `capacity.json`
  for some tickers, at different quote dates.
