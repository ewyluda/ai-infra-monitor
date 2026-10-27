# Neocloud financing ledger — data and calculation audit

Review date: **2026-10-27** (America/New_York). Outcome: **Needs revision**.

This is an audit-only record. No production code, published page, or live dataset was changed for this review or report. Proposed corrections below have **not** been applied. Dollar amounts are USD; tables marked `$M` use millions. Findings describe the captured October 27 page, whose research date was October 25 and stock-price date was October 26. They are not assertions about balances after that snapshot.

## Scope and snapshot

- Target: [Neocloud Financing Ledger](https://ewyluda.github.io/ai-infra-monitor/neocloud-financing-ledger.html). The original request's displayed link text named the demand monitor, but its destination was this financing page.
- Examined all **125 records**, **15 issuers**, and **five views**: ledger, maturity wall, drawn/available, convert moneyness, and net-debt reconciliation. There are 116 financial-debt rows and nine excluded-claim rows; 44 outstanding convertible series have priced moneyness calculations.
- Independently recomputed aggregate amounts, maturity calculations, all 44 conversion classifications, and all 15 reconciliation calculations. Tested representative issuer, class, search, and pro-forma control states in the rendered desktop page.
- Checked core principal, cash, coupon, conversion, and maturity disclosures for every issuer against primary sources. This is **partial source verification**, not certification of every covenant, incorporated exhibit, rating, or undisclosed current balance. Mobile rendering was not verified.
- Reviewed repository snapshot: [`9e1b20c1b272b6c1af0ec3d3895aa76c2fd86640`](https://github.com/ewyluda/ai-infra-monitor/commit/9e1b20c1b272b6c1af0ec3d3895aa76c2fd86640). The live HTML and JSON matched that snapshot and the local financing files byte for byte at the start and end of the review.

| Reviewed file | SHA-256 |
| --- | --- |
| `site/neocloud-financing-ledger.html` | `936cf8071ff2090de436ed8ab61f0bcd254c6b3648985bf5fc57534b2b2aef4c` |
| `site/data/neocloud-financing-ledger.json` | `1d9d19b49d8225be3972cd0ccee7840f103cd2dc09080a44ca28abf1acbb766c` |

Immutable evidence: [HTML at reviewed commit][review-html], [financing JSON at reviewed commit][review-json], [capacity tracker JSON at reviewed commit][capacity-json]. The reproduction below reads those Git objects directly, so later live-data changes do not silently alter its inputs.

Severity is relative to this dashboard: **High** materially changes its debt, liquidity, maturity, or comparison interpretation; **Medium** changes a meaningful component or control; **Lower** is disclosure/label cleanup. These are review priorities, not trading recommendations.

## Findings and proposed corrections

### F01 — High: CIFR narrative double-counts restricted cash and reverses net debt into net cash

**Location:** CIFR reconciliation explanation.

The narrative starts with $4,020.3M cash, then subtracts approximately $3,728M restricted cash again to claim approximately $1.7B net cash. The starting amount already includes $3,188.452M current restricted cash. [CIFR's Q2 balance sheet and cash-flow reconciliation][cifr-q2] show:

| Cash component | $M |
| --- | ---: |
| Unrestricted cash | 831.829 |
| Current restricted cash | 3,188.452 |
| Subtotal already used as cash | 4,020.281 |
| Noncurrent restricted cash | 539.506 |
| All cash, including all restricted cash | 4,559.787 |
| Debt principal | 6,015.500 |
| Debt less all cash | **1,455.713 net debt** |

The narrative double-count is **$3,188.452M**. The displayed numerical row separately uses a disclosed convention that excludes noncurrent restricted cash; that policy is distinct from the provably incorrect narrative.

**Proposed correction:** State the cash components once and recompute the explanation on an explicitly named basis. Do not describe the company as net cash on this calculation.

### F02 — High: maturity wall omits available filed repayment schedules

**Location:** overview maturity chart, maturity-wall view, and near-term/peak callouts.

Most issuers fall back to final maturity even where primary filings provide earlier principal payments. Relative to the full disclosed balance-date intervals, the following **$754.522M** of through-2027 payments are absent:

| Issuer | Disclosed interval and principal ($M) | Captured through 2027 ($M) | Missing relative to interval ($M) | Evidence |
| --- | --- | ---: | ---: | --- |
| WULF | Remaining 2026: 13.850; 2027: 222.890 | 0 | 236.740 | [Q2 principal maturity table][wulf-q2] |
| CIFR | Remaining 2026: 18.476; 2027: 217.105 | 0 | 235.581 | [Q2 Note 14][cifr-q2] |
| IREN | Fiscal year ending June 2027: 177.362 | 0 | 177.362 | [FY2026 debt maturity table][iren-fy26] |
| APLD | Remaining fiscal year ending May 2027: 108.739 | 3.900 | At least 104.839 | [August 2026 quarterly maturity table][apld-q1] |

Some interval payments may already have occurred after the reporting dates. Fiscal years must be mapped to calendar intervals, not relabeled as calendar years. Consequently this is evidence of missing schedules, **not** proof that current unpaid near-term debt should simply increase by $754.522M.

Later-year examples are also material. [CORZ's filing][corz-q2] schedules $189.750M in 2029 and $379.500M in 2030, while the page places its entire $3,300M secured note at 2031. [HUT's filing][hut-q2] schedules $86.389M in 2028, $100.634M in 2029, and $237.971M in 2030; the page places all $7,500M of the project notes at 2042. These HUT payments total $424.994M.

The page already discloses that final-maturity fallback makes near-term amounts a floor. That disclosure is useful, but the missing schedules are available. **BTDR's asset-loan amortization is already encoded ($373.5M in 2027 and $142.1M in 2028); it is not a missing-schedule finding.**

**Proposed correction:** Capture the available schedules, preserve fiscal-period boundaries, and reconcile them to the selected balance-date or pro-forma principal before rebuilding the maturity metrics.

### F03 — High: CoreWeave allocation reduces known bullet convertible principal

**Location:** maturity chart's 2031/2032 allocations and instrument/moneyness colors.

The implementation proportionally allocates the filed $14,896M after-2030 bucket across $21,554.5M of late-final-maturity instruments. Its factor is `14896 / 21554.5 = 0.691085388202`. This reduces known bullet obligations:

| CRWV series | Outstanding principal ($M) | Allocated by page ($M) | Difference ($M) |
| --- | ---: | ---: | ---: |
| 1.75% due December 2031 | 2,587.500 | 1,788.183442 | 799.316558 |
| 1.75% due October 2032 | 4,000.000 | 2,764.341553 | 1,235.658447 |
| Total | 6,587.500 | 4,552.524995 | **2,034.975005** |

Both original offering disclosures explicitly state that there is no sinking fund: [2031 issuance][crwv-2031], [2032 issuance][crwv-2032]. Aggregate debt remains approximately unchanged, but principal is attributed to the wrong instruments and timing. The chart's convertible-colored total is therefore understated.

**Proposed correction:** Reserve known bullet principal at contractual maturity first. Allocate only the residual filed schedule across amortizing facilities, then reconcile the complete schedule. Implementation evidence: reviewed HTML `maturityWall`, lines 189–203.

### F04 — High: net-debt reconciliation uses a different tracker snapshot and basis

**Location:** net-debt reconciliation comparison values and match/disagree labels.

The financing page's embedded `tracker.rows` differs from the linked public capacity tracker's `nd` values for **12 of 15 issuers**. This is not merely different stock-price dates. [Public tracker][capacity-page] and [reviewed tracker data][capacity-json]:

| Issuer | Financing comparison ($B) | Public capacity tracker ($B) |
| --- | ---: | ---: |
| CRWV | 46.552 | 29.800 |
| APLD | 3.110 | 2.700 |
| CORZ | 3.000 | 2.500 |
| WULF | 2.700 | 2.600 |
| CIFR | 1.570 | 4.600 |
| IREN | 1.810 | 1.700 |
| KEEL | 0.320 | 0.260 |
| RIOT | 0.900 | 0.290 |
| BTDR | 1.460 | 1.300 |
| WYFI | 0.180 | 0.250 |
| BTBT | 0.280 | 0.350 |
| MARA | 2.630 | 2.000 |

NBIS ($0.5B), GLXY ($3.9B), and HUT ($0B) agree. The CRWV public card was also checked in the browser: it shows $29.8B and excludes operating leases, whereas financing compares a lease-inclusive $46.552B and marks it a match.

**Proposed correction:** Bind the comparison to the actual published tracker snapshot and show any basis conversion explicitly. Do not simply replace numbers without reconciling financial debt, lease treatment, cash scope, and reporting period.

### F05 — Medium: disabling pro forma mixes historical and updated balances

**Location:** ledger, drawn/available, and convert-moneyness views.

Turning off the pro-forma control filters rows, but these views still use `drawn_m` for retained rows instead of consistently using `drawn_bd_m`. Six issuers are affected:

| Issuer | Displayed less balance-date debt ($M) |
| --- | ---: |
| NBIS | -800.000 |
| CRWV | +1,200.000 |
| CIFR | -165.900 |
| WYFI | -185.489 |
| RIOT | -200.000 |
| MARA | -150.000 |
| Total | **-301.389** |

Browser reproduction: ledger, all issuers/classes, pro forma off gives **109 rows and $92,246.954M** debt rather than **$92,548.343M** balance-date debt. CRWV alone gives 19 rows and **$36,750.5M**, rather than **$35,550.5M**. Offsetting errors obscure individual issuer differences.

**Proposed correction:** Centralize the selected reporting-basis amount and use it consistently in rows, totals, commitments, moneyness sizing, and dated availability. Evidence: `filtered` lines 258–260, `totals` lines 214–217, `commitments` lines 219–225, `moneyness` lines 227–233, and `renderLedger` lines 348–369 of [reviewed HTML][review-html].

### F06 — Medium: maturity search injects an entire issuer repayment ladder

**Location:** maturity-wall search.

Browser reproduction: select CRWV, all classes, pro forma on, then search `Magnetar`. Only the **$189M** instrument matches, but the chart/table total is **$20,655M**, including **$10,597M** due on demand or through 2027. The implementation adds the full issuer's 2026–2030 ladder whenever any eligible row enters that issuer's pool.

**Proposed correction:** Attribute schedules to instruments or disable the full-issuer ladder when the instrument selection is partial. A filtered chart must reconcile to the selected population. Evidence: `maturityWall` lines 194–203 and `renderWall` lines 373–383 of [reviewed HTML][review-html].

### F07 — Medium: WhiteFiber retains $50M of retired loans

**Location:** WYFI ledger and debt/cash rollforward.

The ledger retains $20M owed to B. Riley and $60M to Bit Digital. The [October 21 proxy][wyfi-proxy] states that $20M was repaid on August 24 and $30M on September 23, leaving $30M outstanding. These repayments precede the page's research cutoff.

Correcting this item alone reduces WYFI gross debt from **$466.05M to $416.05M**. The cash bridge must also include repayments and any actual fee/interest cash; it is wrong to infer that net debt automatically falls $50M. The embedded tracker note already mentions these repayments, making the instrument rows internally stale.

**Proposed correction:** Update outstanding balances and the matching cash movements together, retaining their event dates and source.

### F08 — Medium: Bitdeer ignores disclosed September loan balances

**Location:** BIT asset-loan and bitcoin-loan rows.

The BIT asset-loan row remains **$515.6M**, although [the same filing's subsequent-events note][btdr-h1] gives **$423.3M** outstanding on September 29: a **$92.3M component overstatement**. The bitcoin borrowing increased from **1,953.84 BTC to 3,669 BTC** by September 29, while the row retains June's $144.6M valuation. No updated dollar valuation was established.

The separate August $45M one-week facility must not simply be added to the September aggregate. Its continued outstanding status is not established.

**Proposed correction:** Use the disclosed September asset-loan balance, distinguish original currency from dollar valuation for bitcoin borrowings, and retain unknown values as unknown. No exact corrected BTDR or cohort debt total is claimed here.

### F09 — Medium: available credit is overstated by at least $35.143M

**Location:** drawn/available view, ledger availability, overview availability KPI.

| Facility | Page available ($M) | Supported available ($M) | Overstatement ($M) |
| --- | ---: | ---: | ---: |
| RIOT $50M revolver | 15.700 | 0.557 | 15.143 |
| WYFI $100M nonrevolving DDTL | 40.000 | At most 20.000 | At least 20.000 |

[RIOT Note 11][riot-q2] reconciles $34.272M drawn + $15.171M letters of credit + $0.557M available = $50M. WYFI had $80M cumulative advances; its [agreement's Advance definition and assignment provisions][wyfi-ddtl] count advances whether or not outstanding. The funded $20M assignment to B. Riley did not create new capacity, and repayment does not replenish a nonrevolving commitment.

Correcting these two items alone moves the available total from **$15,425.810M to at most $15,390.667M**. Other availability uncertainties remain; this is not a certified current liquidity total.

**Proposed correction:** Deduct letters of credit and apply each facility's contractual revolving/nonrevolving rules.

### F10 — Medium: BTBT debt and cash scopes do not match

**Location:** BTBT net-debt reconciliation.

The page uses **$200M debt excluding WYFI** but subtracts **$83.555M consolidated cash including WYFI**. [BTBT Q2][btbt-q2] continues to consolidate WYFI; [WYFI Q2][wyfi-q2] reports $56.056M cash. The ex-WYFI residual is therefore `83.555 - 56.056 = 27.499`, producing `200 - 27.499 = 172.501` net debt, rather than the displayed approximately $116.4M.

The $27.499M residual is not a separately filed legal-parent balance sheet. The supported finding is the mismatch in consolidation scope, not a claim of fully reconstructed standalone parent accounts.

**Proposed correction:** Match debt and cash populations. If measuring external cohort funding, also state and apply the intercompany-elimination policy for WYFI's debt to BTBT; issuer-level gross obligations and external funding are different measures.

### F11 — Medium: pro-forma cash bridges omit known transactions

**Location:** BTDR, GLXY, and MARA reconciliation cash bridges.

| Issuer | Omitted cash movement | Evidence |
| --- | --- | --- |
| BTDR | +$58M net ATM proceeds, July 1–September 29 | [H1 Note 24][btdr-h1] |
| GLXY | -$25.4M repurchases, August 6–10 | [Q2 Note 24, PDF p. 51][glxy-q2] |
| MARA | -$100M utility security deposit posted September 21 | [Amendment 8-K, Item 1.01][mara-deposit] |

For MARA, under the page's cash-only convention, this single change would move pro-forma cash from $1,021.3M to $921.3M and net debt from $2,025.9M to $2,125.9M, before other unknown movements. The deposit is withdrawable subject to conditions; no subsequent withdrawal was established.

**Proposed correction:** Incorporate disclosed cash movements consistently. Continue labeling the result an event-based bridge, not actual current cash; capex, operating cash flows, and other intervening movements are not fully reconstructed.

### F12 — Medium: free-text parsing selects the wrong maturity year

**Location:** maturity chart.

`maturityYear` takes the last four-digit year in the text. Two confirmed cases:

| Instrument | Text meaning | Page bucket | Supported treatment |
| --- | --- | --- | --- |
| BTDR $144.6M bitcoin loan | `2027-06 (all due within 12 months of 2026-06-30)` | 2026 | Preserve the period ending June 2027; exact contractual date is not disclosed by this description |
| WYFI $18M Iceland loan | Initial March 25, 2028 maturity, optional extension to 2030 | 2030 | Use unextended 2028 maturity unless exercise is evidenced |

Evidence: [BTDR H1][btdr-h1], [WYFI Q2 Note 10][wyfi-q2], and `maturityYear` at line 177 of [reviewed HTML][review-html]. WYFI's quarterly amortization also needs its own schedule rather than a single terminal bucket.

**Proposed correction:** Store contractual maturity, reporting date, optional extension, and amortization schedule as separate structured fields.

### F13 — Medium: IREN Mackenzie recourse classification omits a parent payment guarantee

**Location:** IREN $2.4B Mackenzie facility's `recourse: spv` label and guarantee description.

[IREN FY2026 Item 9B][iren-fy26] expressly says IREN Limited unconditionally guarantees borrower payment obligations. It distinguishes that guarantee from performance obligations and does not pledge parent assets. No parent asset pledge does not mean no parent payment recourse.

**Proposed correction:** Describe the parent payment guarantee explicitly and distinguish it from collateral security and performance/completion guarantees. Current draws remain undisclosed; this finding does not increase recorded debt automatically.

### F14 — Medium: CoreWeave historical commitments overlap by $2.6B

**Location:** DDTL 2.0/2.1 committed amounts and unresolved-overlap note.

The rows show $7,600M plus $3,000M, or $10,600M. [CoreWeave's Q3 2025 release][crwv-q325] describes only **$400M incremental capacity** to create the $3,000M tranche, incorporating $2,600M existing capacity. Combined historical capacity is **$8,000M**, not $10,600M.

**Proposed correction:** Model the amended facility/tranche relationship and eliminate overlapping commitment capacity. Draw periods are closed, so this finding does not change the current drawn-debt or available-capacity totals.

## Material interpretation limits and unresolved inputs

These are distinguished from confirmed arithmetic/source errors. Do not convert uncertainties into invented corrections.

### L01 — Early holder puts are additional conditional liquidity exposure

The final-maturity wall does not surface approximately **$989.124M** that holders can require to be repaid in 2027:

| Issuer/series | Principal ($M) | First relevant holder put |
| --- | ---: | --- |
| MARA March 2030 | 632.540 | December 1, 2027 |
| MARA June 2031 | 291.584 | June 4, 2027 |
| BTDR December 2029 | 65.000 | December 6, 2027 |

[MARA Note 13][mara-q2] classifies the June 2031 series as current because of its first put. [BTDR's note terms][btdr-h1] support the December put. These are optional holder rights, not unconditional scheduled maturities. A liquidity view should show earliest put dates separately. The dataset rounds the two MARA balances to $632.5M/$291.6M, producing $989.1M from stored inputs.

Additional checked puts include BTDR $375M in July 2029 and $400M in November 2029; WYFI $31.85M in February 2029 and $310M in September 2030; BTBT $150M in October 2028; and CIFR $850M in November 2030. Sources: [BTDR][btdr-h1], [WYFI August issuance][wyfi-aug], [BTBT][btbt-q2], [CIFR October issuance][cifr-oct].

### L02 — Original principal is not total cash redemption value

The wall excludes **$2,302.295M** of NBIS terminal accretion based on stored outstanding principal and maturity cash ratios. The page expressly discloses its original-principal convention, so this is not an undisclosed formula error. It limits interpretation of the chart as cash owed at maturity.

The conversion break-even formula is appropriate for the reviewed Nebius terms because conversion shares are defined per original principal. Sources: [June 2025 prospectus][nbis-jun25], [September 2025 terms][nbis-sep25], [August 2026 terms][nbis-aug-pricing].

### L03 — Conversion moneyness does not determine cash-principal settlement

WULF's **$500M 2030** and **$1,000M 2031** convertible series require cash for principal upon conversion; shares may cover the excess conversion value. They are respectively ITM and near break-even under the page's inputs, yet price recovery does not eliminate their cash-principal obligation. The approximately 85% OTM calculation is correct as moneyness, but is not itself a measure of principal requiring cash settlement. [2030 terms][wulf-2030], [2031 terms][wulf-2031], [2030 indenture section 14.02(a)][wulf-indent].

**Proposed clarification:** Separate price/strike status from cash, share, or combination settlement requirements and holder conversion eligibility.

### L04 — Current revolver availability remains conditional

- **WULF:** $326M is $400M commitment less $74M July letters of credit. The [October amendment][wulf-oct] does not establish current draws, current letters of credit, or satisfaction/removal of the earlier $75M pre-commencement cap. Treat the amount as conditional arithmetic, not independently verified October liquidity.
- **CIFR:** the $166.9M figure deducts $33.1M letters of credit from $200M, but the [June filing][cifr-q2] describes a $50M pre-commencement borrowing cap. Later availability could be higher; the review did not establish whether the commencement condition had been met at the asserted date.

### L05 — Nebius exchange settlement is an assumption, not a verified completed event

The ledger deducts $800M and describes the exchange as completed August 20. The [pricing announcement][nbis-aug-pricing] describes agreements entered into and settlement expected August 24. The [closing announcement][nbis-aug-close] confirms the new notes but continues to describe exchange agreements. The ledger's open-item list itself acknowledges that settlement was not independently confirmed. Retain a clearly labeled pro-forma assumption until completion is established; do not assert the debt remains outstanding either.

### L06 — Cohort and net-debt definitions need explicit boundaries

The cohort includes a WYFI liability to BTBT. That is a real issuer obligation but not external funding for the combined cohort. Different issuer net-debt conventions also treat leases, restricted cash, and nonrecourse projects differently. These differences are disclosed in part and are not automatically errors; aggregate or cross-issuer comparisons need a common named basis and intercompany policy. HUT's exclusion of project debt from parent net debt does not mean that debt is absent from the gross-debt ledger.

## Additional lower-priority findings and resolved open items

1. **APLD preferred terms are incomplete.** The $1,825M preferred row omits the minimum 1.80× invested-capital liquidation preference, rising to 2.00× for specified IPO/drag-along outcomes. October 6, 2032 is a forced-sale-process right, not an ordinary debt maturity; the row already partly qualifies it as an expected valuation date. Do not reclassify it as debt without a separate policy decision. [FY2026 10-K][apld-fy26].
2. **APLD completion-guarantee uncertainty is stale.** The same filing explicitly describes parent completion guarantees for the $2.35B 2030 and $2.15B 2031 project notes. [FY2026 10-K][apld-fy26].
3. **MARA August funding is disclosed, not merely inferred.** Q2 Item 5 expressly says the $450M Coinbase and $300M Two Prime loans were fully drawn. [MARA Q2][mara-q2]. This resolves funding-status uncertainty, not all later repayment/current-balance questions.
4. **WYFI RBC guarantors are available in the executed exhibit.** The agreement names Enovum MLT entities and 1504950 B.C. ULC; WhiteFiber Inc. is not listed. The current SPV classification is supported, and the open-item wording should be updated. [Credit agreement, Guarantors definition and security provisions][wyfi-rbc].
5. **RIOT finance-lease liability is expressly zero.** Q2 Note 12 describes the asset but no remaining finance-lease liability; `null`/undisclosed wording is unnecessary. [RIOT Q2][riot-q2].
6. **GLXY's apparent loan discrepancy is a scope difference.** $427.377M is in the GDH LP operating-partnership financials (Note 23); $286.715M is in GDI consolidated financials/Note 16. Calling it an unexplained MD&A discrepancy misses the different entities. Exact eliminations were not reconstructed. [GLXY Q2][glxy-q2].
7. **Moneyness bubble areas are not strictly proportional.** The minimum radius of four pixels makes the small $6.6M CIFR series approximately 21 times the area implied by strict principal proportionality. Label the minimum-size treatment or change the visual encoding. The `px/conv` column actually displays `px / conv - 1`, a percentage premium/discount, not the raw ratio. Evidence: `renderMoney` in [reviewed HTML][review-html].

## Checks that passed, and what passing means

The following are arithmetic results **from the stored inputs**, not corrected economic totals:

| Measure | Recomputed value |
| --- | ---: |
| Financial debt, pro forma ($M) | 108,840.154 |
| Financial debt, balance date ($M) | 92,548.343 |
| Convertible principal ($M) | 44,971.350 |
| Convertible principal more than 20% below maturity break-even ($M) | 38,172.550 |
| That principal as a share of all priced converts | 84.881930% |
| Displayed peak three-year window | 2030–2032 |
| Principal in displayed peak window ($M) | 65,211.750 |
| Peak as a share of stored financial debt | 59.91516% |
| Displayed demand/through-2027 principal ($M) | 12,104.200 |
| Reported available capacity ($M) | 15,425.810 |
| Commitments with undisclosed draws ($M) | 7,248.000 |
| Excluded claims ($M) | 20,947.815 |

All 44 moneyness classifications and all 15 reconciliation formulas/tolerance classifications agree with the implementation when supplied the same inputs. The wall exceeds stored financial debt by $0.5M because of the filed rounded CoreWeave ladder; this is not a material finding. No duplicate issuer/instrument names, missing source-URL fields, unknown issuer keys, or invalid/negative numeric amount fields were found. Source-link presence does not prove source validity or completeness.

All 15 October 26 stock-price inputs were independently compared with FMP daily closes during the review and matched. That is a recorded external-data check; the provider responses were not archived in the repository, and the offline reproduction does not independently re-fetch market data.

## Coverage and remaining verification gaps

The source review covered core fields for every issuer but did not certify every contract clause. These named limitations should survive any remediation handoff:

| Issuer | Core evidence checked | Remaining material limits |
| --- | --- | --- |
| NBIS | Q2 balances; eight convert series; accretion; August issuance; July/October facilities | Bridge/ABF draws, full covenants, exchange settlement, separately confirmed June-2025 original-balance history |
| CRWV | Q2 principal table, cash/leases, conversion terms; newer DDTL agreements; August draws; September convert | Older DDTL contractual margins, full exhibits, post-August movements, ratings, approximately $375M FMP classification residual |
| APLD | August balances, revolver/LC reconciliation, three secured issues, convert, Texas financing, preferred terms | Legacy-loan detail partly from May, $18.5M promissory terms and small residual, full redemption/covenant terms |
| CORZ | Q2 principal/cash, convert terms, secured-note schedule, August revolver, Polaris transaction | Purchase adjustment/current revolver use, unrestricted-cash allocation inference, independent proof of no capped calls |
| IREN | Six converts, cash, DDTL/USPP, leases, Mackenzie guarantee | Other-debt terms, Mackenzie draw, residual $400M in broader announcement, full unpublished covenant ratios |
| WULF | Four notes, cash, deferred consideration, revolver terms/amendment, July LCs; cash conversion settlement | Current draws/LCs/commencement, some project cash events, full capped-call terms |
| CIFR | Q2 debt/cash/schedule/revolver cap; October convert and remaining old principal | Actual October issuance expenses, current revolver availability, exhaustive collateral exhibits |
| GLXY | Q2 debt/cash/Helios I; Helios II issuance description; exact exchangeable dates; subsequent buybacks | Helios II indenture fetch unavailable, detailed amortization, current Helios I draws and trading-loan coupons |
| HUT | Q2 cash/debt, project-note schedules, FalconX/TZRC; Two Prime; September JPM terms | Full Two Prime recourse/collateral beyond filing description, ratings |
| BTDR | H1 loan/convert/cash terms; puts; September asset/BTC balances; ATM and land cash flows | September BTC dollar valuation, complete loan repayment bridge, continued August short-facility status |
| WYFI | Q2 cash/debt; DDTL agreement/draws/repayments; Iceland; RBC exhibit; August convert/exchange | Latest RBC draw/FX, additional Iceland draws, repayment fee/interest cash |
| KEEL | Q2 cash, two converts, June guarantee terms, small loan balances | Small-loan coupon/maturity details not reconstructed from older filings; no material checked-field discrepancy found |
| RIOT | Q2 debt/cash/revolver LCs, 10-K convert/CPACE terms, September retirement, August bridge | Post-August small-revolver renewal, $573M bridge draw, repayment cash/collateral allocation |
| MARA | Q2 cash and five converts/puts; August loan funding; September deposit | Long Ridge closing status, subsequent deposit withdrawal, 2032 capped-call confirmation |
| BTBT | Q2 cash/consolidation, convert/put, Galaxy collateral loan | Formal standalone parent cash, intercompany cohort policy |

No complete corrected cohort debt, net-debt, liquidity, or maturity total is supplied: several corrections offset each other, reporting dates differ, and some current balances remain undisclosed. Apply supported event-level changes together and recalculate dependent views only in a separately authorized implementation task.

## Recorded browser reproductions

These observations were made on the unchanged live page. The report preserves the controls and resulting values; screenshots and browser-session state are not required by the offline calculation below and were not committed.

| Check | Control state | Observed result |
| --- | --- | --- |
| Five main views | Navigate ledger, maturity, drawn/available, moneyness, reconciliation | All rendered on desktop; findings concern values/meaning rather than failure to load |
| Historical basis | Ledger; all issuers/classes; pro forma off | 109 rows; $92.25B displayed (unrounded $92,246.954M) |
| Historical CRWV | Ledger; CRWV; all classes; pro forma off | 19 rows; $36.75B instead of $35.5505B |
| Partial maturity search | Maturity; CRWV; all classes; pro forma on; search `Magnetar` | $189M matching instrument but $20.655B wall and $10.597B near-term |
| Public comparison | Capacity tracker; search/expand CRWV | $29.8B net debt, excluding operating leases; financing comparison uses $46.552B |

## Supporting numerical appendices

The tables and reproduction code below preserve the evidence needed to inspect the calculations without modifying live inputs. A local rerun at the reviewed Git object is appropriate; no network access or site refresh is necessary.

### A. Issuer inputs, prices, and primary balance-date filings

| Issuer | Rows | Balance date | October 26 close ($) | Primary filing |
| --- | ---: | --- | ---: | --- |
| NBIS | 12 | 2026-06-30 | 153.27 | [6-K (2026-08-12)](https://www.sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d2.htm) |
| CRWV | 21 | 2026-06-30 | 55.19 | [10-Q (2026-08-12)](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm) |
| APLD | 11 | 2026-08-31 | 17.83 | [10-Q (2026-10-07)](https://www.sec.gov/Archives/edgar/data/1144879/000114487926000059/apld-20260831.htm) |
| CORZ | 4 | 2026-06-30 | 13.51 | [10-Q (2026-07-28)](https://www.sec.gov/Archives/edgar/data/1839341/000183934126000014/core-20260630.htm) |
| IREN | 11 | 2026-06-30 | 25.43 | [10-K (2026-08-27)](https://www.sec.gov/Archives/edgar/data/1878848/000187884826000052/iren-20260630.htm) |
| WULF | 6 | 2026-06-30 | 11.98 | [10-Q (2026-08-05)](https://www.sec.gov/Archives/edgar/data/1083301/000108330126000166/wulf-20260630.htm) |
| CIFR | 9 | 2026-06-30 | 7.71 | [10-Q (2026-08-04)](https://www.sec.gov/Archives/edgar/data/1819989/000181998926000041/cifr-20260630.htm) |
| GLXY | 6 | 2026-06-30 | 15.68 | [10-Q (2026-08-10)](https://www.sec.gov/Archives/edgar/data/1859392/000185939226000091/glxy-20260630.htm) |
| HUT | 7 | 2026-06-30 | 62.97 | [10-Q (2026-08-04)](https://www.sec.gov/Archives/edgar/data/1964789/000110465926090025/hut-20260630x10q.htm) |
| BTDR | 9 | 2026-06-30 | 7.085 | [6-K (H1-2026 interim financial statements, Ex. 99.1) (2026-09-29)](https://www.sec.gov/Archives/edgar/data/1899123/000121390026104638/ea030647301ex99-1.htm) |
| WYFI | 7 | 2026-06-30 | 9.52 | [10-Q (2026-08-12)](https://www.sec.gov/Archives/edgar/data/2042022/000121390026088026/ea0300877-10q_whitefiber.htm) |
| KEEL | 4 | 2026-06-30 | 2.18 | [10-Q (2026-08-10)](https://www.sec.gov/Archives/edgar/data/1812477/000181247726000023/keel-20260630.htm) |
| RIOT | 6 | 2026-06-30 | 12.59 | [10-Q (2026-08-10)](https://www.sec.gov/Archives/edgar/data/1167419/000110465926093448/riot-20260630x10q.htm) |
| MARA | 10 | 2026-06-30 | 6.84 | [10-Q (2026-08-06)](https://www.sec.gov/Archives/edgar/data/1507605/000150760526000022/mara-20260630.htm) |
| BTBT | 2 | 2026-06-30 | 0.8389 | [10-Q (2026-08-13)](https://www.sec.gov/Archives/edgar/data/1710350/000121390026088709/ea0300693-10q_bitdigital.htm) |

### B. Reconciliation from stored inputs

These results reproduce the page. A `match` status is the page's tolerance result, not an audit endorsement of the cash scope, source snapshot, or assumptions. Net-debt conventions differ by issuer. Amounts are $M.

| Issuer | Balance-date net debt | Pro-forma net debt | Embedded tracker | Comparison basis | Page status |
| --- | ---: | ---: | ---: | --- | --- |
| NBIS | 484.200 | -245.800 | 500.000 | balance | match |
| CRWV | 46,551.500 | 47,180.700 | 46,552.000 | balance | match |
| APLD | 3,043.390 | 3,043.390 | 3,110.000 | balance | match |
| CORZ | 2,615.300 | 2,939.600 | 3,000.000 | pro_forma | match |
| IREN | 1,810.050 | 1,810.050 | 1,810.000 | balance | match |
| WULF | 2,696.400 | 2,696.400 | 2,700.000 | balance | match |
| CIFR | 1,995.200 | 1,940.300 | 1,570.000 | balance | disagree |
| GLXY | 2,520.057 | 6,027.057 | 3,900.000 | balance | disagree |
| HUT | 1.500 | 1.500 | 0.000 | balance | match |
| BTDR | 1,445.470 | 1,545.470 | 1,460.000 | pro_forma | match |
| WYFI | 259.239 | 191.050 | 180.000 | pro_forma | match |
| KEEL | 334.237 | 334.237 | 320.000 | balance | match |
| RIOT | 382.300 | 382.300 | 900.000 | pro_forma | disagree |
| MARA | 2,025.900 | 2,025.900 | 2,630.000 | pro_forma | disagree |
| BTBT | 116.400 | 116.400 | 280.000 | balance | consolidated |

### C. All 44 convertible moneyness calculations

Break-even is conversion price × maturity cash ratio; status is ITM at/above break-even, near from 20% below up to break-even, and OTM more than 20% below. Cash settlement requirements are a separate question (L03). Principal is $M and prices are dollars.

| Issuer | Series | Principal | Conversion price | Maturity break-even | Price vs. break-even | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| NBIS | 2.00% convertible notes due June 2029 (post-exchange remainder; 120% at maturity) | 89.600 | 51.4500 | 61.7400 | 148.2507% | ITM |
| NBIS | 3.00% convertible notes due June 2031 (post-exchange remainder; 125% at maturity) | 90.000 | 51.4500 | 64.3125 | 138.3207% | ITM |
| IREN | 3.50% convertible senior notes due 2029 | 233.400 | 13.6400 | 13.6400 | 86.4370% | ITM |
| APLD | 2.75% Convertible Senior Notes due 2030 | 450.000 | 9.7500 | 9.7500 | 82.8718% | ITM |
| CIFR | 1.75% convertible senior notes due 2030 | 6.600 | 4.4500 | 4.4500 | 73.2584% | ITM |
| IREN | 3.25% convertible senior notes due 2030 | 212.300 | 16.8100 | 16.8100 | 51.2790% | ITM |
| WULF | 2.75% convertible senior notes due 2030 | 500.000 | 8.4800 | 8.4800 | 41.2736% | ITM |
| CORZ | 3.00% Convertible Senior Notes due 2029 | 460.000 | 11.0000 | 11.0000 | 22.8182% | ITM |
| WULF | 1.00% convertible senior notes due 2031 | 1,000.000 | 12.4300 | 12.4300 | -3.6203% | near |
| NBIS | 1.00% convertible senior notes due 2030 (accrete to 115%) | 1,581.250 | 138.7500 | 159.5625 | -3.9436% | near |
| NBIS | 2.75% convertible senior notes due 2032 (accrete to 115%) | 1,581.250 | 138.7500 | 159.5625 | -3.9436% | near |
| RIOT | 0.75% convertible senior notes due 2030 | 594.400 | 14.8600 | 14.8600 | -15.2759% | near |
| BTDR | 5.00% convertible senior notes due 2032 (February 2026 notes) | 375.000 | 9.9250 | 9.9250 | -28.6146% | OTM |
| NBIS | 2.625% convertible senior notes due 2033 (accrete to 120%) | 1,750.000 | 180.3100 | 216.3720 | -29.1637% | OTM |
| NBIS | 1.25% convertible senior notes due 2031 (accrete to 120%) | 2,587.500 | 183.2200 | 219.8640 | -30.2887% | OTM |
| GLXY | 2.500% Exchangeable Senior Notes due 2029 (GDH LP) | 402.500 | 23.8100 | 23.8100 | -34.1453% | OTM |
| WULF | 0.00% convertible senior notes due 2032 | 1,025.000 | 19.9400 | 19.9400 | -39.9198% | OTM |
| CORZ | 0.00% Convertible Senior Notes due 2031 | 625.000 | 22.4900 | 22.4900 | -39.9289% | OTM |
| CRWV | 2.875% Convertible Senior Notes due 2033 - post-quarter | 4,200.000 | 97.8500 | 97.8500 | -43.5973% | OTM |
| CRWV | 1.75% Convertible Senior Notes due 2031 | 2,587.500 | 107.8000 | 107.8000 | -48.8033% | OTM |
| CIFR | 0.00% convertible senior notes due 2032 (October 2026) | 850.000 | 15.3100 | 15.3100 | -49.6408% | OTM |
| IREN | 0.25% convertible senior notes due 2032 | 1,150.000 | 51.4000 | 51.4000 | -50.5253% | OTM |
| IREN | 1.00% convertible senior notes due 2033 (June) | 1,150.000 | 51.4000 | 51.4000 | -50.5253% | OTM |
| CIFR | 0.00% convertible senior notes due 2031 | 1,300.000 | 16.0300 | 16.0300 | -51.9027% | OTM |
| GLXY | 3.00% Exchangeable Senior Notes due 2026 (GDH LP) | 445.000 | 33.3400 | 33.3400 | -52.9694% | OTM |
| CRWV | 1.75% Convertible Senior Notes due 2032 | 4,000.000 | 119.6000 | 119.6000 | -53.8545% | OTM |
| BTDR | 4.875% convertible senior notes due 2031 (June 2025 notes) | 375.000 | 15.8750 | 15.8750 | -55.3701% | OTM |
| NBIS | 0.50% convertible senior notes due 2030 (accrete to 110%) | 3,450.000 | 313.4600 | 344.8060 | -55.5489% | OTM |
| BTDR | 5.25% convertible senior notes due 2029 (November 2024 notes) | 65.000 | 15.9500 | 15.9500 | -55.5799% | OTM |
| BTDR | 4.00% convertible senior notes due 2031 (November 2025 notes) | 400.000 | 17.7700 | 17.7700 | -60.1294% | OTM |
| NBIS | 4.50% convertible senior notes due 2034 (accrete to 125%) | 2,300.000 | 324.6500 | 405.8125 | -62.2313% | OTM |
| WYFI | 4.50% convertible senior notes due 2031 (2031 Notes) | 31.850 | 25.9100 | 25.9100 | -63.2574% | OTM |
| MARA | 2.125% convertible senior notes due 2031 (September 2031 Notes) | 300.000 | 18.8900 | 18.8900 | -63.7904% | OTM |
| IREN | 1.00% convertible senior notes due 2033 (December) | 3,000.000 | 73.0700 | 73.0700 | -65.1978% | OTM |
| MARA | 0.00% convertible senior notes due 2032 (August 2032 Notes) | 1,025.000 | 20.2600 | 20.2600 | -66.2389% | OTM |
| KEEL | 1.375% convertible senior notes due 2031 (2025 Convertible Notes; issuer Bitfarms Ltd., Keel co-obligor) | 588.000 | 6.8600 | 6.8600 | -68.2216% | OTM |
| IREN | 0.00% convertible senior notes due 2031 | 1,000.000 | 85.6300 | 85.6300 | -70.3025% | OTM |
| KEEL | 1.250% convertible senior notes due 2032 (2026 Convertible Notes) | 458.000 | 7.4100 | 7.4100 | -70.5803% | OTM |
| WYFI | 5.00% convertible senior notes due 2032 | 310.000 | 33.8400 | 33.8400 | -71.8676% | OTM |
| GLXY | 0.50% Exchangeable Senior Notes due 2031 (GDH LP) | 1,300.000 | 55.7600 | 55.7600 | -71.8795% | OTM |
| MARA | 0.00% convertible senior notes due 2030 (March 2030 Notes) | 632.500 | 25.9100 | 25.9100 | -73.6009% | OTM |
| BTBT | 4.00% convertible senior notes due 2030 (2030 Notes) - BTBT-level | 150.000 | 4.1600 | 4.1600 | -79.8341% | OTM |
| MARA | 0.00% convertible senior notes due 2031 (June 2031 Notes) | 291.600 | 34.5800 | 34.5800 | -80.2198% | OTM |
| MARA | 1.00% convertible senior notes due 2026 (December 2026 Notes) | 48.100 | 76.1700 | 76.1700 | -91.0201% | OTM |

### D. Displayed maturity wall

This reproduces the existing allocation and therefore includes the identified timing/classification defects. Amounts are $M.

| Bucket | Principal |
| --- | ---: |
| demand | 50.000000 |
| 2026 | 5,116.700000 |
| 2027 | 6,937.500000 |
| 2028 | 6,585.527000 |
| 2029 | 5,011.940000 |
| 2030 | 18,099.050000 |
| 2031 | 33,174.658866 |
| 2032 | 13,938.041134 |
| 2033 | 10,100.000000 |
| 2034 | 2,300.000000 |
| 2035 | 5.000000 |
| 2042 | 7,500.000000 |
| undated | 22.237000 |

### E. Offline reproduction

Run the Python block below from this repository (Python 3 standard library; Git required). It reads immutable Git objects, checks their hashes, independently computes the key results, and prints JSON. It does not write files, fetch sources, refresh data, or execute the page JavaScript. Assertions verify the recorded outcomes, including the defects; passing does not mean the page is correct. The filing-value corrections near the end are explicitly transcribed evidence, not independently fetched observations.

```python
import collections
import hashlib
import json
import math
import re
import subprocess

REV = '9e1b20c1b272b6c1af0ec3d3895aa76c2fd86640'
def archived(path):
    return subprocess.check_output(['git', 'show', f'{REV}:{path}'])

raw = archived('site/data/neocloud-financing-ledger.json')
html = archived('site/neocloud-financing-ledger.html')
assert hashlib.sha256(raw).hexdigest() == '1d9d19b49d8225be3972cd0ccee7840f103cd2dc09080a44ca28abf1acbb766c'
assert hashlib.sha256(html).hexdigest() == '936cf8071ff2090de436ed8ab61f0bcd254c6b3648985bf5fc57534b2b2aef4c'
j = json.loads(raw)
rows = j['instruments']
cos = {c['t']: c for c in j['companies']}
debt = lambda r: r.get('category', 'lease' if r['type'] == 'lease' else 'financial_debt') == 'financial_debt'
pf_row = lambda r: bool(r.get('as_of') and r['as_of'] > cos[r['t']]['balance_date'])
current = lambda r: r['drawn_m'] or 0
balance = lambda r: (r['drawn_bd_m'] or 0) if 'drawn_bd_m' in r else (0 if pf_row(r) else current(r))
def year(text):
    years = re.findall(r'(?<!\d)(20\d\d)(?!\d)', text or '')
    return int(years[-1]) if years else None
def bucket(text):
    if re.search(r'\bon demand\b|\brecallable\b', text or '', re.I):
        return 'demand'
    return str(year(text)) if year(text) else 'undated'
def display_wall(selected, pro_forma=True):
    # Independent translation of the displayed policy, not a corrected schedule.
    wall = collections.defaultdict(float)
    pools = collections.defaultdict(list)
    for r in selected:
        if not debt(r):
            continue
        if cos[r['t']].get('filed_ladder') and not pf_row(r):
            pools[r['t']].append(r)
            continue
        amount = current(r) if pro_forma else balance(r)
        if not amount:
            continue
        schedule = r.get('schedule') or []
        total = sum(x[1] for x in schedule)
        if total:
            for when, part in schedule:
                wall[bucket(when)] += amount * part / total
        else:
            wall[bucket(r.get('maturity'))] += amount
    for ticker, selected_rows in pools.items():
        ladder = cos[ticker]['filed_ladder']
        for when, amount in ladder['years'].items():
            wall[when] += amount
        after = ladder.get('after')
        if after:
            late = [r for r in selected_rows if (year(r.get('maturity')) or 0) >= after['from']]
            total = sum(balance(r) for r in late)
            for r in late:
                if total:
                    wall[bucket(r['maturity'])] += after['amount_m'] * balance(r) / total
    return dict(wall)

converts = [r for r in rows if debt(r) and r['type'] == 'convert' and current(r) and r['conv_price']]
status = lambda r: 'ITM' if j['tracker']['rows'][r['t']]['px'] >= r['conv_price'] * (r.get('maturity_cash_ratio') or 1) else ('near' if j['tracker']['rows'][r['t']]['px'] >= .8 * r['conv_price'] * (r.get('maturity_cash_ratio') or 1) else 'OTM')
pf_debt = sum(current(r) for r in rows if debt(r))
bd_debt = sum(balance(r) for r in rows if debt(r))
convert_debt = sum(current(r) for r in converts)
otm = sum(current(r) for r in converts if status(r) == 'OTM')
available = sum(r.get('available_m') or 0 for r in rows if debt(r) and r['drawn_m'] is not None)
unknown = sum((r.get('committed_m') if r.get('committed_m') is not None else r.get('face_m')) or 0 for r in rows if debt(r) and r['drawn_m'] is None)
off_rows = [r for r in rows if not pf_row(r) or 'drawn_bd_m' in r]
wall = display_wall(rows)
near = sum(wall.get(k, 0) for k in ['demand', '2026', '2027'])
years = sorted(int(k) for k in wall if k.isdigit())
peak = max(((y, sum(wall.get(str(z), 0) for z in range(y, y + 3))) for y in years), key=lambda x: x[1])
magnetar = [r for r in rows if r['t'] == 'CRWV' and 'magnetar' in json.dumps(r).lower()]
mag_wall = display_wall(magnetar)
late = [r for r in rows if debt(r) and r['t'] == 'CRWV' and not pf_row(r) and (year(r.get('maturity')) or 0) >= 2031]
factor = cos['CRWV']['filed_ladder']['after']['amount_m'] / sum(balance(r) for r in late)
reconciliation = []
for t, c in cos.items():
    selected = [r for r in rows if r['t'] == t and r['nd_include']]
    cash = (c.get('cash_m') or 0) + ((c.get('restricted_cash_m') or 0) if c.get('nd_cash_includes_restricted') else 0)
    pf_cash = cash + sum(x['amount_m'] for x in c.get('pro_forma_cash', []))
    bd_nd = sum(balance(r) for r in selected) - cash
    pf_nd = sum(current(r) for r in selected) - pf_cash
    tracker = j['tracker']['rows'][t]['nd'] * 1000
    target = pf_nd if c.get('tracker_compare') == 'pro_forma' else bd_nd
    tolerance = max(150, .03 * max(abs(tracker), abs(target)))
    label = 'match' if abs(tracker - target) <= tolerance else 'disagree'
    if c.get('tracker_basis') == 'consolidated':
        label = 'consolidated'
    reconciliation.append(dict(t=t, bd_nd=bd_nd, pf_nd=pf_nd, tracker_nd=tracker, status=label))

result = {
    'records': len(rows), 'issuers': len(cos), 'converts': len(converts),
    'pf_debt_m': pf_debt, 'bd_debt_m': bd_debt,
    'convert_m': convert_debt, 'otm_m': otm, 'otm_pct': 100 * otm / convert_debt,
    'available_m': available, 'undisclosed_commitments_m': unknown,
    'excluded_claims_m': sum(current(r) for r in rows if not debt(r)),
    'display_wall_m': wall, 'display_wall_minus_debt_m': sum(wall.values()) - pf_debt,
    'display_near_m': near, 'display_peak': peak,
    'pf_off_displayed_m': sum(current(r) for r in off_rows if debt(r)),
    'pf_off_errors_m': {t: sum(current(r) for r in off_rows if debt(r) and r['t'] == t) - sum(balance(r) for r in rows if debt(r) and r['t'] == t) for t in cos},
    'magnetar_selected_m': sum(current(r) for r in magnetar if debt(r)),
    'magnetar_display_wall_m': sum(mag_wall.values()),
    'magnetar_display_near_m': sum(mag_wall.get(k, 0) for k in ['demand', '2026', '2027']),
    'crwv_tail_factor': factor,
    'crwv_convert_misallocation_m': 6587.5 * (1 - factor),
    'nbis_accretion_m': sum(current(r) * ((r.get('maturity_cash_ratio') or 1) - 1) for r in rows if debt(r)),
    'reconciliation': reconciliation,
    # Below are transcribed filing values, not independently re-fetched by this script.
    'cifr_all_cash_m': 831.829 + 3188.452 + 539.506,
    'cifr_net_debt_all_cash_m': 6015.5 - (831.829 + 3188.452 + 539.506),
    'omitted_schedule_intervals_m': 13.850 + 222.890 + 18.476 + 217.105 + 177.362 + 108.739 - 3.9,
    'available_after_two_corrections_m': available - (15.7 - .557) - (40 - 20),
    'btbt_ex_wyfi_net_debt_m': 200 - (83.555 - 56.056),
    '2027_put_principal_m': 632.540 + 291.584 + 65,
}
for key, expected in {
    'pf_debt_m': 108840.154, 'bd_debt_m': 92548.343, 'convert_m': 44971.350,
    'otm_m': 38172.550, 'available_m': 15425.810, 'undisclosed_commitments_m': 7248,
    'display_near_m': 12104.2, 'pf_off_displayed_m': 92246.954,
    'magnetar_selected_m': 189, 'magnetar_display_wall_m': 20655,
    'magnetar_display_near_m': 10597, 'crwv_convert_misallocation_m': 2034.9750052193276,
    'nbis_accretion_m': 2302.295, 'cifr_net_debt_all_cash_m': 1455.713,
    'omitted_schedule_intervals_m': 754.522, 'available_after_two_corrections_m': 15390.667,
    'btbt_ex_wyfi_net_debt_m': 172.501, '2027_put_principal_m': 989.124,
}.items():
    assert math.isclose(result[key], expected, abs_tol=1e-6), (key, result[key], expected)
assert (len(rows), len(cos), len(converts)) == (125, 15, 44)
assert peak[0] == 2030 and math.isclose(peak[1], 65211.75, abs_tol=1e-6)
print(json.dumps(result, indent=2))
```

Verification when preparing this report: the full block executed successfully, including all assertions. The independent results also agreed with a separate execution of the page's base JavaScript helpers for default totals, maturity wall, moneyness, and reconciliation.


## Primary-source references

References identify the relevant filing or contract, with sections called out in the findings. A document being listed does not mean every incorporated exhibit was verified.

[review-html]: https://github.com/ewyluda/ai-infra-monitor/blob/9e1b20c1b272b6c1af0ec3d3895aa76c2fd86640/site/neocloud-financing-ledger.html
[review-json]: https://github.com/ewyluda/ai-infra-monitor/blob/9e1b20c1b272b6c1af0ec3d3895aa76c2fd86640/site/data/neocloud-financing-ledger.json
[capacity-json]: https://github.com/ewyluda/ai-infra-monitor/blob/9e1b20c1b272b6c1af0ec3d3895aa76c2fd86640/site/data/capacity.json
[capacity-page]: https://ewyluda.github.io/ai-infra-monitor/neocloud-capacity-tracker.html
[cifr-q2]: https://www.sec.gov/Archives/edgar/data/1819989/000181998926000041/cifr-20260630.htm
[cifr-oct]: https://www.sec.gov/Archives/edgar/data/1819989/000119312526424297/d313847d8k.htm
[wulf-q2]: https://www.sec.gov/Archives/edgar/data/1083301/000108330126000166/wulf-20260630.htm
[wulf-oct]: https://www.sec.gov/Archives/edgar/data/1083301/000162828026067100/wulf-20261023.htm
[wulf-2030]: https://investors.terawulf.com/news-events/press-releases/detail/92/terawulf-inc-announces-upsize-and-pricing-of-425-million-convertible-notes-offering
[wulf-2031]: https://investors.terawulf.com/news-events/press-releases/detail/116/terawulf-inc-announces-upsize-and-pricing-of-850-million-convertible-notes-offering
[wulf-indent]: https://investors.terawulf.com/sec-filings/all-sec-filings/content/0000950142-24-002636/eh240549125_ex0401.htm
[iren-fy26]: https://www.sec.gov/Archives/edgar/data/1878848/000187884826000052/iren-20260630.htm
[apld-q1]: https://www.sec.gov/Archives/edgar/data/1144879/000114487926000059/apld-20260831.htm
[apld-fy26]: https://www.sec.gov/Archives/edgar/data/1144879/000114487926000048/apld-20260531.htm
[corz-q2]: https://www.sec.gov/Archives/edgar/data/1839341/000183934126000014/core-20260630.htm
[hut-q2]: https://www.sec.gov/Archives/edgar/data/1964789/000110465926090025/hut-20260630x10q.htm
[crwv-2031]: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000105/crwv-20251208.htm
[crwv-2032]: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000164/crwv-20260409.htm
[crwv-q325]: https://www.sec.gov/Archives/edgar/data/1769628/000176962825000059/coreweave3q25earningspress.htm
[wyfi-proxy]: https://www.sec.gov/Archives/edgar/data/2042022/000121390026111410/ea0308982-01.htm
[wyfi-ddtl]: https://www.sec.gov/Archives/edgar/data/2042022/000121390026061575/ea029228001ex10-1.htm
[wyfi-q2]: https://www.sec.gov/Archives/edgar/data/2042022/000121390026088026/ea0300877-10q_whitefiber.htm
[wyfi-aug]: https://www.sec.gov/Archives/edgar/data/2042022/000121390026092599/ea0302925-8k_white.htm
[wyfi-rbc]: https://www.sec.gov/Archives/edgar/data/2042022/000121390026088026/ea030087701ex10-2.htm
[btdr-h1]: https://www.sec.gov/Archives/edgar/data/1899123/000121390026104638/ea030647301ex99-1.htm
[riot-q2]: https://www.sec.gov/Archives/edgar/data/1167419/000110465926093448/riot-20260630x10q.htm
[btbt-q2]: https://www.sec.gov/Archives/edgar/data/1710350/000121390026088709/ea0300693-10q_bitdigital.htm
[glxy-q2]: https://investor.galaxy.com/static-files/828a6f22-b8eb-4390-bd2f-e67d73312b6b
[mara-q2]: https://www.sec.gov/Archives/edgar/data/1507605/000150760526000022/mara-20260630.htm
[mara-deposit]: https://www.sec.gov/Archives/edgar/data/1507605/000095014226002607/eh260835247_8k.htm
[nbis-jun25]: https://www.sec.gov/Archives/edgar/data/1513845/000110465925065768/tm2519765-1_424b7.htm
[nbis-sep25]: https://www.sec.gov/Archives/edgar/data/1513845/000141057825002149/tm2525503d8_ex99-2.htm
[nbis-aug-pricing]: https://www.sec.gov/Archives/edgar/data/1513845/000110465926098924/tm2623617d1_ex99-1.htm
[nbis-aug-close]: https://www.sec.gov/Archives/edgar/data/1513845/000110465926100347/tm2623863d1_ex99-1.htm
