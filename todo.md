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
    [PR #141](https://github.com/ewyluda/macrogauge/pull/141)** (merged and published on
    MacroGauge 2026-10-27 09:21 ET by a manual run; on the hub since the 2026-10-27 export):
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
    - NBIS: the $3.5B Citi 364-day secured bridge (signed 10/17, 6-K 10/22) and a net-debt
      re-pull at Q3 (reported 10/27).
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
  - **Done 2026-10-27, notebook `321cf7c` and the hub export:** the financing ledger follows the
    convention. `nd_cash_includes_restricted` is off for APLD, BTDR, WYFI, KEEL, RIOT and MARA;
    HUT counts the River Bend and Beacon Point notes, with a $96.7M carrying-to-principal bridge.
    Reconciliation on the 10-27 publish: 13 match, GLXY disagrees (F1), BTBT structural.
  - Once carried, retire the notebook's `neocloud-capacity.json` as a source or sync it from
    MacroGauge, and rename its `benchmark` role and ORCL's "hyperscaler benchmark" note.

- [ ] **Resolve the MacroGauge overlap conflicts.** Listed in
  `docs/reviews/2026-10-27-macrogauge-overlap-audit.md` (IDs below). *Added 2026-10-27.*
  - **Done 2026-10-27 in MacroGauge [PR #142](https://github.com/ewyluda/macrogauge/pull/142)**
    (merged after the 09:21 run; MacroGauge publishes it 2026-10-28, the hub at the export after
    that): NBIS 0.50% 2030 converts $3.0B → **$3.45B** in `issuer_bonds.json` (F2; the $450M
    option was exercised, 8/24 6-K). WULF `bk` 32 → **27** per the Q2 investor deck (D6).
  - **Done 2026-10-27, notebook `353bcc1` and the hub export:** lab register restated from
    Anthropic's S-1 (D1–D5; also Nscale $44.6B, Lambda $34.9B of $41.3B, AMD >$20B spend note); the
    Broadcom $125.2B is the 2026 lease alone, $161.2B all leases. IREN July contracts noted (D8),
    Meta–Nebius sized at the $12B dedicated (D10), Volta at 121 IT MW (D12).
  - **Next export (after MacroGauge's 2026-10-28 publish):** the scheduled export should pick up
    PR #142's WULF backlog 27 on the capacity page with no manual step; confirm it did.
  - **Done 2026-10-27, lab register sweep since 10-01:** three rows added, `labs_as_of` moved to
    2026-10-27 (live at the next scheduled export). Anthropic–EverWind Nova Scotia lease (10/16,
    95 MW first phase; secondary, since only the press names Anthropic). The Broadcom-arranged
    $63B SPV (10/26), a financing of Anthropic's existing Broadcom lease, not a new commitment.
    SpaceX's ~$40B Apollo GPU finance lease (10/26 8-K). Not added, still talks: a second
    Anthropic–Nscale deal, OpenAI's UAE-led round, Broadcom financing for OpenAI chips.
  - **Done 2026-10-27, owner chose backfill:** the 6/9 Broadcom–Apollo–Blackstone $35B tranche for
    Anthropic is a financing row like 10/26 (the joint release, plus Broadcom's 10-Q: $29B maximum
    backstop on 5-year leases). Neither release says whether the 10/26 $63B includes it.
  - **MacroGauge to source or drop:** the AKAM edge's extra $1.8B (D11). Akamai's 9/24 release
    states $11.6B committed plus up to $9B more, with no $1.8B; the hub's $11.6B stands.
  - **At the Q3 re-pulls:** GLXY net debt (F1) and contracted revenue on both sites (D7; hub >$15B,
    MacroGauge $13.5B, notebook capacity $18B). The Nebius $3.5B Citi bridge goes into the /rates
    note and NBIS `ndflag` (F3).

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

- [x] **Matched the pricing cadence.** A scheduled export runs hourly from 09:15 to 22:15 ET and acts
  only when MacroGauge has published something the hub doesn't show yet. It re-syncs the ledger
  and demand monitor, rebuilds the site, runs every check CI runs, and pushes only if all of them
  pass; any failure pushes nothing. The capacity page and the ledger's quotes follow MacroGauge
  within the hour. The ETF atlas and layer index prices still refresh by hand. First unattended
  publish expected after MacroGauge's 2026-10-28 run. *2026-10-27.*

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
