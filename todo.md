# AI Infra Monitor — To-Do

Operational backlog for the public hub. Add items as they surface; check them off or delete when done.

## Open

- [ ] **Align the capacity page with MacroGauge's `/capacity`, so the two sites never disagree.**
  The hub page now uses MacroGauge's layout, but it still renders the private notebook's
  `neocloud-capacity.json`, which has drifted from MacroGauge's `config/capacity.json` since the
  one-off port (`macrogauge/scripts/port_neocloud_config.py`). Goal: one dataset, one set of
  rules, the same numbers on both sites. Snapshot of the gaps on 2026-10-26 (hub capacity curated
  2026-10-25, priced 2026-10-26; MacroGauge curated 2026-10-21, priced 2026-10-23). *Added 2026-10-26.*
  1. **Pick one source of truth.** Recommended: MacroGauge's `config/capacity.json` (plus
     `power_deals.json`), with the hub export reading MacroGauge's published `capacity.json`
     instead of the notebook's copy, and the notebook tracker synced from it or retired.
     Whichever side wins, the other stops being hand-edited.
  2. **Reconcile the 17 of 18 shared companies whose figures conflict**, field by field against
     the filings. Don't assume either side is current: the notebook carries some later filings
     (CRWV and ORCL research is dated 2026-10-25). Hub value → MacroGauge value:
     - Capacity (MW): ORCL con 750 → 5,000, plan 2,150 → 0 · CRWV con 700 → 1,200, plan
       2,240 → 1,500 · NBIS con 778 → 1,000, plan 2,700 → 3,800 · BTDR con 207 → 349, plan
       1,298 → 1,143 · IREN con 330 → 530, plan 730 → 530 · KEEL con 350 → 18, plan 224 → 110 ·
       CORZ op 485 → 437, con 637 → 663, plan 1,540 → 1,400 · WYFI and BTBT op 32 → 50, con
       23 → 3, plan 200 → 120 · DOCN op 70 → 85, con 65 → 50 · MARA plan 600 → 100 · APLD plan
       250 → 0 · GLXY plan 830 → 0 · WULF plan 1,450 → 1,320
     - Net debt ($B): CRWV 46.55 → 29.8 · ORCL 132.07 → 89.0 · CIFR 1.57 → 4.6 · RIOT 0.90 →
       0.29 · MARA 2.63 → 2.0 · APLD 3.11 → 2.7 · BTDR 1.46 → 1.3 · CORZ 3.0 → 2.5 · DOCN
       −0.32 → 0.15 · IREN 1.81 → 1.7 · KEEL 0.32 → 0.26 · WULF 2.7 → 2.6 · AKAM 3.02 → 2.95 ·
       WYFI 0.18 → 0.25 · BTBT 0.28 → 0.35
     - Backlog ($B): BTDR 7.6 → 4.7 · GLXY 18 → 13.5 · IREN 19.4 → 16.5 · APLD 36.2 → 36 ·
       CRWV 104.2 → 104 · BTBT 0.921 → 0.933
     - Only HUT matches on every field.
  3. **Settle one net-debt convention.** Most of the large gaps are a difference in method, not
     in the facts. The hub's CRWV and ORCL figures include operating leases; MacroGauge uses
     funded debt for hyperscalers and finance leases (not operating leases) for neoclouds. Write
     the rule once and apply it to every row on both sites.
  4. **Close the coverage gap.** MacroGauge tracks 29 companies; the hub tracks 19. The hub lacks
     AMZN, GOOGL, MSFT, META, BABA, TCEHY, BIDU, OpenAI/Stargate, xAI, DLR and EQIX. The hub's
     SPCX (SpaceX: Colossus / xAI) has no MacroGauge row, and MacroGauge's XAI row covers the
     same capacity: keep one and de-duplicate.
  5. **Use one rule for withholding EV per MW.** MacroGauge withholds it with an `ev_note` for
     AKAM (CDN and security business), MARA (no AI MW energized, no AI lease) and EQIX. The hub
     currently plots AKAM at about $362M per MW and MARA at about $35M per MW. Port `ev_note` and
     the private-builder rule to the hub.
  6. **Carry everything MacroGauge shows** once the data is shared: the Filed / Estimate badge
     (10 MacroGauge rows are estimates), the power-deals table (33 deals, curated 2026-10-17),
     the NVDA-vs-the-field tile, MacroGauge's headline (hyperscaler share of operating capacity),
     the full site map (137 mapped sites on MacroGauge vs 51 on the hub) and the tenant list (37
     vs 38 deals).
  7. **Fix the leftover wording.** Rename the data role `benchmark` to `hyperscaler` at the
     source (the hub relabels it for display today), and update ORCL's curator note, which still
     opens "hyperscaler benchmark — scale calibration only".
  8. **Match the pricing cadence.** MacroGauge reprices every weekday morning; the hub is priced
     only when it is exported. Either show MacroGauge's priced date on the hub, or add the
     scheduled quote refresh from the hub plan's Phase 3.
  9. **Guard it.** Add a parity check that diffs the hub's `site/data/neocloud-capacity.json`
     against MacroGauge's published `capacity.json` (companies, MW, net debt, backlog, roles,
     withheld rules) and fails CI on any difference.

- [ ] **Audit the other three hub pages for overlap with MacroGauge.** Check the financing
  ledger, demand monitor and ETF atlas against any MacroGauge page that publishes the same
  figures (issuer debt, hyperscaler capex, ETF holdings), and list each conflict the way the
  capacity item above does. Nothing has been compared yet. *Added 2026-10-26.*
