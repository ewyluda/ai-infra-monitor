# AI Infra Monitor — To-Do

Operational backlog for the public hub. Add items as they surface; check them off or delete when done.

## Open

- [ ] **Carry the notebook's newer capacity figures into MacroGauge's `config/capacity.json`.**
  The hub's capacity page now renders MacroGauge's published `capacity.json` (source of truth since
  2026-10-26), so a figure that is newer in the private notebook only reaches either site once it is
  in MacroGauge's config. Verify each against the cited filing before editing. Comparison done
  2026-10-26: notebook capacity curated 2026-10-25, MacroGauge 2026-10-21, field change dates from
  git history on both sides. *Added 2026-10-26.*
  - **Done 2026-10-27 in MacroGauge
    [PR #141](https://github.com/ewyluda/macrogauge/pull/141)** (reaches the sites at the first
    daily publish after merge):
    - IREN backlog $16.5B → **$19.4B**, checked against the FY26 10-K ($5.1B RPO + $11.4B lease
      contracts at 6/30, plus $2.8B of July contracts).
    - Net-debt convention written into MacroGauge's curation rules and the /capacity method note:
      all consolidated debt (project notes included) less unrestricted cash; restricted cash and
      operating leases never count; post-quarter financings stay re-pull notes. Applied to every
      row it changes: HUT 0.0 → 7.4, APLD 2.7 → 3.4, BTDR 1.3 → 1.4, RIOT 0.29 → 0.37,
      KEEL 0.26 → 0.31; WYFI and MARA basis text only.
  - **Already in MacroGauge before this pass (wave 1, 2026-10-26):** BTDR's ~$2.9B AI-cloud
    backlog stays out of `bk` by its GPU-cloud rule (so the notebook's $7.6B is a method
    difference); BTDR A102 is dated Q1 2027; NBIS's AIB 50 MW site is in.
  - **Still open, gated on Q3 filings:**
    - CORZ operational 437 → **~485 MW** (Dalton Ph II +48 MW per a 10/13 company post): confirm
      in the Q3 10-Q (11/5).
    - NBIS: the $3.5B Citi term loan (10/22) and a net-debt re-pull at Q3 (reported 10/27).
    - GLXY at its Q3 re-pull (10/27): add the Helios II notes under the new convention.
  - **Still open, decisions:** finance leases for landlord and operator rows. Neoclouds count
    them, but IREN ($0.24B), DOCN (~$0.41B) and APLD ($0.05B) leave them out; settle it at the
    Q3 re-pulls.
  - **Keep MacroGauge's figure (method difference, or MacroGauge is newer):**
    - CRWV net debt 46.55 vs **29.8**: the notebook includes $16.3B of operating leases;
      MacroGauge excludes them on purpose (its basis fix). CRWV plan 2,240 vs **1,500**: the
      notebook adds India 240 MW and splits construction / planned differently; MacroGauge holds
      the total at the 4.2 GW contracted and lists India as secured.
    - CIFR, APLD and BTDR net debt now follow the written convention (restricted cash not netted).
    - MARA plan 600 vs **100**: the notebook counts Long Ridge (up to 600 MW), still awaiting
      FERC; MacroGauge excludes it until the deal closes.
    - ORCL, KEEL, DOCN, RIOT, AKAM, WULF plan, IREN capacity and net debt, NBIS plan, BTBT and
      WYFI operational / construction / net debt, CORZ plan and net debt, APLD plan, GLXY plan:
      MacroGauge changed these more recently (Aug–Oct, including the critical-IT re-basing).
    - SPCX: MacroGauge's XAI row covers the same capacity and was refreshed from SpaceX's Q3
      results. Drop the notebook's SPCX row.
  - **Check before deciding:** WYFI / BTBT plan (200 vs 120; both trace to the 9/14 deck, so check
    gross vs critical-IT; Q3 11/12) and GLXY backlog ($18B vs $13.5B; MacroGauge says the Q2
    release did not restate it, so find the notebook's source; Q3 10/27).
  - **After PR #141 publishes:** flip the notebook financing ledger's per-issuer basis to match
    (`nd_cash_includes_restricted` off for APLD, BTDR, WYFI, KEEL, RIOT, MARA; HUT onto
    consolidated debt incl. the River Bend and Beacon Point notes), re-sync, and re-export the hub.
    Until then the ledger's reconciliation shows APLD (+$0.70B) and HUT (+$7.40B) as "disagree".
    BTDR, KEEL and RIOT move $53–76M, inside the tolerance, so a missed flip there goes unflagged
    (overlap audit F4).
  - Once carried, retire the notebook's `neocloud-capacity.json` as a source or sync it from
    MacroGauge, and rename its `benchmark` role and ORCL's "hyperscaler benchmark" note.

- [ ] **Match the pricing cadence.** MacroGauge reprices every weekday morning; the hub takes
  MacroGauge's prices at export time. A scheduled export (hub plan, Phase 3 follow-up) keeps the
  hub within a day. *Added 2026-10-26.*

- [ ] **Resolve the MacroGauge overlap conflicts.** Listed in
  `docs/reviews/2026-10-27-macrogauge-overlap-audit.md` (IDs below). *Added 2026-10-27.*
  - **MacroGauge config, one PR:** NBIS 0.50% 2030 converts $3.0B → **$3.45B** in
    `issuer_bonds.json` (F2; the $450M option was exercised, 8/24 6-K). WULF `bk` 32 → **27** per
    the Q2 investor deck (D6).
  - **At the Q3 re-pulls:** GLXY net debt (F1) and contracted revenue on both sites (D7; hub >$15B,
    MacroGauge $13.5B, notebook capacity $18B). The Nebius $3.5B Citi bridge goes into the /rates
    note and NBIS `ndflag` (F3).
  - **Notebook, then re-export:** refresh the lab register from Anthropic's S-1 (D1–D5: Azure,
    AWS, Google Cloud, SpaceX/xAI, Broadcom TPU leases). Note IREN's $2.8B July contracts (D8),
    mark Meta–Nebius $27B as an upper bound (D10), source or drop Akamai's extra $1.8B (D11), and
    fix the Volta row's 0.133 GW against 121 IT MW (D12).

- [ ] **Polish the visuals on every page of the site.** Covers the landing page and all five
  dashboards (capacity tracker, financing ledger, demand monitor, ETF atlas, trade layer index).
  Keep one cohesive style across pages. Remove no visuals; update or enhance them with elegant,
  tasteful interactions: hover tooltips, click interactions (select, filter, drill in), smooth
  transitions, and sortable table headers where sorting makes sense. Use the design skills and
  plugins that help (`frontend-design`, `ui-ux-pro-max`, `dataviz`, `design:design-critique`,
  `design:accessibility-review`). Do this before the README GIFs and the showcase video, so they
  capture the finished pages. *Added 2026-10-27.*

- [ ] **Replace the README screenshots with GIFs that scroll and interact with each page.** The six
  static PNGs in `docs/img/` (landing page plus five dashboards) show only the top of each page.
  Record a short GIF per page that scrolls through its best content and exercises its features
  (view tabs, hovers and tooltips, filters, toggles), then swap each `<img>` in `README.md` and keep
  the alt text accurate. Script the capture so it can be rerun after redesigns, and keep each GIF
  small enough to load quickly on GitHub. *Added 2026-10-27.*

- [ ] **Later: make a 90-second showcase video of the hub.** Model it on the Solution for Sandra
  gala video (`Code & Projects/Solution for sandra/video/` in Google Drive): a storyboard table of
  timed scenes and captions, a scripted browser capture (`capture.mjs`), original generated music
  (`music.py`), and a `build.sh` that encodes 1920×1080, 30 fps H.264 + AAC. Captions carry the
  message, no voice, scene cuts on the beat. Do this after the README GIFs. Embed the finished
  video on the home page (`site/index.html`) if it can be done without weighing the page down.
  *Added 2026-10-27.*

## Done

- [x] **Audited the other hub pages for overlap with MacroGauge.** The financing ledger and demand
  monitor were checked against MacroGauge's `capacity.json` and `rates.json`: 4 ledger conflicts
  and 12 demand conflicts, with capex, most backlog, and the MW cross-check in agreement. The ETF
  atlas has no overlap. See `docs/reviews/2026-10-27-macrogauge-overlap-audit.md`. *2026-10-27.*

- [x] **Financing ledger and demand monitor read MacroGauge's capacity data.** `financing_ledger_refresh.py`
  and `ai_demand_refresh.py` now read MacroGauge's published `capacity.json`; the ledger's net-debt
  comparison follows MacroGauge's per-issuer convention with a sourced principal-basis column, and the
  financing audit's findings are remediated in the notebook and pinned by `tools/check_financing.py`. See
  `docs/reviews/2026-10-27-financing-ledger-audit.md`. *2026-10-27.*

- [x] **Capacity page source of truth is MacroGauge.** The hub export reads MacroGauge's published
  `capacity.json` and renders it with a port of MacroGauge's `/capacity` page: 29 companies,
  Filed / Estimate badges, withheld EV per MW with reasons, the NVDA tile, power deals and the full
  site map. A test fails if the hub's published figures differ from MacroGauge's. *2026-10-26.*
