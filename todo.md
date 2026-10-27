# AI Infra Monitor — To-Do

Operational backlog for the public hub. Add items as they surface; check them off or delete when done.

## Open

- [ ] **Carry the notebook's newer capacity figures into MacroGauge's `config/capacity.json`.**
  The hub's capacity page now renders MacroGauge's published `capacity.json` (source of truth since
  2026-10-26), so a figure that is newer in the private notebook only reaches either site once it is
  in MacroGauge's config. Verify each against the cited filing before editing. Comparison done
  2026-10-26: notebook capacity curated 2026-10-25, MacroGauge 2026-10-21, field change dates from
  git history on both sides. *Added 2026-10-26.*
  - **Carry (the notebook cites later evidence):**
    - IREN backlog $16.5B → **$19.4B**: FY26 10-K (6/30) RPO $5.1B + lease TCV $11.4B, plus
      $2.8B of July contracts. MacroGauge's own note says its 16.5 is "prior TCV basis, not
      restated FY26".
    - BTDR backlog $4.7B → **$7.6B**: adds the ~$2.9B AI-cloud contract backlog from the Sept ops
      update (10/19) to the $4.7B Tydal lease. MacroGauge's backlog text already names the $2.9B
      but `bk` leaves it out, so decide whether AI-cloud contract revenue counts as backlog. Also
      from 10/19: A102 ready-for-service slipped Nov '26 → Q1 '27; move that tranche.
    - CORZ operational 437 → **~485 MW** (construction −48): Dalton Ph II +48 MW billing per a
      company post on 10/13, not yet in a filing. Confirm in the Q3 10-Q (due 11/5) first;
      MacroGauge's note still expects Dalton Ph II end-2026 to early 2027.
    - NBIS: the AIB 50 MW 12-year colocation deal (binding, 9/30) and the $3.5B Citi term loan
      (10/22) are not in MacroGauge's row. Add them to the note and sites; re-pull net debt at Q3.
  - **Keep MacroGauge's figure (method difference, or MacroGauge is newer):**
    - CRWV net debt 46.55 vs **29.8**: the notebook includes $16.3B of operating leases;
      MacroGauge excludes them on purpose (its basis fix). CRWV plan 2,240 vs **1,500**: the
      notebook adds India 240 MW and splits construction / planned differently; MacroGauge holds
      the total at the 4.2 GW contracted and lists India as secured.
    - CIFR (1.57 vs **4.6**), APLD (3.11 vs **2.7**), BTDR (1.46 vs **1.3**) net debt: same filing,
      different restricted-cash netting. Settle the convention once (see below).
    - MARA plan 600 vs **100**: the notebook counts Long Ridge (up to 600 MW), still awaiting
      FERC; MacroGauge excludes it until the deal closes.
    - ORCL, KEEL, DOCN, RIOT, AKAM, WULF plan, IREN capacity and net debt, NBIS plan, BTBT and
      WYFI operational / construction / net debt, CORZ plan and net debt, APLD plan, GLXY plan:
      MacroGauge changed these more recently (Aug–Oct, including the critical-IT re-basing).
    - SPCX: MacroGauge's XAI row covers the same capacity and was refreshed from SpaceX's Q3
      results. Drop the notebook's SPCX row.
  - **Check before deciding:** WYFI / BTBT plan (200 vs 120; both trace to the 9/14 deck, so check
    gross vs critical-IT) and GLXY backlog ($18B vs $13.5B; MacroGauge says the Q2 release did not
    restate it, so find the notebook's source).
  - **Write the net-debt convention down** (operating leases, restricted cash, pro forma for
    post-quarter deals) in MacroGauge's methodology, and apply it to every row.
  - Once carried, retire the notebook's `neocloud-capacity.json` as a source or sync it from
    MacroGauge, and rename its `benchmark` role and ORCL's "hyperscaler benchmark" note.

- [ ] **Point the financing ledger and demand monitor at MacroGauge's capacity data.** Both hub
  pages still embed figures from the notebook's capacity file, so they now disagree with the hub's
  own capacity page. The ledger's net-debt reconciliation and tracker snapshot use notebook net debt
  and quotes (CRWV $46.6B there vs $29.8B on the capacity page; quotes 10-26 vs MacroGauge's 10-23).
  The demand monitor's capacity cross-check uses notebook totals (1,335 MW operational, 6,323 MW
  tenant-contracted, as of 10-25). Have `financing_ledger_refresh.py` and `ai_demand_refresh.py`
  read MacroGauge's `capacity.json`. *Added 2026-10-26.*

- [ ] **Match the pricing cadence.** MacroGauge reprices every weekday morning; the hub takes
  MacroGauge's prices at export time. A scheduled export (hub plan, Phase 3 follow-up) keeps the
  hub within a day. *Added 2026-10-26.*

- [ ] **Audit the other hub pages for overlap with MacroGauge.** Check the financing ledger,
  demand monitor and ETF atlas against any MacroGauge page that publishes the same figures (issuer
  debt, hyperscaler capex, ETF holdings), and list each conflict. *Added 2026-10-26.*

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

- [x] **Capacity page source of truth is MacroGauge.** The hub export reads MacroGauge's published
  `capacity.json` and renders it with a port of MacroGauge's `/capacity` page: 29 companies,
  Filed / Estimate badges, withheld EV per MW with reasons, the NVDA tile, power deals and the full
  site map. A test fails if the hub's published figures differ from MacroGauge's. *2026-10-26.*
