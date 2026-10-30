/* AI Infra Monitor shared kit: sortable table headers and one tooltip for the dashboards.
   hub_export.py injects this file and a per-page #aim-config; the notebook's own pages never load it.
   Progressive enhancement only: each page renders as before, and the kit re-applies itself when a
   page re-renders a table (filters, toggles), so the reader's sort survives.

   config.sort: [{table: selector, skip: [col indexes], group: row selector that splits the body into
   segments sorted separately, attach: row selector that travels with the row above it,
   unit: 'tbody' when each record is its own <tbody>}]
   config.tips: selector for elements whose title (attribute or SVG <title>) shows in the shared tooltip.
   config.clamp: [{sel: long-text elements shown at a few lines, lines: N, all: element an Expand-all
   toggle follows; specs naming the same element share one toggle}]: nothing is removed; Show more
   appears only where the text overflows.
   config.label: selector for tables whose body cells take their column's head as data-aim-label, for a
   page style that stacks each row's cells (rows with a spanning cell are not records and are skipped). */
(() => {
  const cfg = JSON.parse(document.getElementById('aim-config')?.textContent || '{}');
  const NULLS = new Set(['', '—', '–', '-', 'n/a', 'na', 'n.a.', 'none']);
  const SCALE = { K: 1e3, M: 1e6, B: 1e9, T: 1e12, GW: 1e3, MW: 1 };
  const state = new Map(); // spec index -> {col, dir}
  let seq = 0;

  function key(cell) {
    if (!cell) return null;
    if (cell.dataset.sort != null) {
      const n = Number(cell.dataset.sort);
      return cell.dataset.sort === '' ? null : Number.isFinite(n) ? n : cell.dataset.sort;
    }
    // The first rendered line only: a cell's sub-line (basis, q/q change, site count) is not its value.
    const raw = (cell.innerText || cell.textContent).split('\n')[0].replace(/\s+/g, ' ').trim();
    const t = raw.replace(/[‐‑–]/g, '-').replace(/−/g, '-');
    if (NULLS.has(t.toLowerCase())) return null;
    if (/^\d{4}-\d{2}(-\d{2})?\b/.test(t)) return t.slice(0, 10); // ISO dates sort as text
    const m = t.match(/^[<>~≈]?\s*([-+]?)\s*\$?\s*(\d[\d,]*\.?\d*|\.\d+)\s*(GW|MW|[KMBT](?![a-z]))?/);
    if (m) return (m[1] === '-' ? -1 : 1) * parseFloat(m[2].replace(/,/g, '')) * (SCALE[m[3]] || 1);
    return raw.toLowerCase();
  }

  const lead = u => u[0].tagName === 'TBODY' ? u[0].rows[0] : u[0];

  function units(table, spec) {
    if (spec.unit === 'tbody') return [[...table.tBodies].map(b => [b])];
    const segs = [[]];
    for (const body of table.tBodies) for (const row of body.rows) {
      if (spec.group && row.matches(spec.group)) { segs.push([]); continue; }
      const seg = segs[segs.length - 1];
      if (spec.attach && row.matches(spec.attach) && seg.length) seg[seg.length - 1].push(row);
      else seg.push([row]);
    }
    return segs.filter(s => s.length);
  }

  function apply(table, spec, i) {
    const st = state.get(i);
    const segs = units(table, spec);
    segs.flat().forEach(u => { if (!u[0].dataset.aimI) u[0].dataset.aimI = ++seq; });
    const ths = headCells(table);
    ths.forEach((th, c) => {
      if (!th.querySelector('.aim-sort')) return;
      th.setAttribute('aria-sort', st && st.col === c && st.dir ? (st.dir > 0 ? 'ascending' : 'descending') : 'none');
    });
    for (const seg of segs) {
      const keyed = seg.map(u => ({ u, k: st && st.dir ? key(lead(u)?.cells[st.col]) : null, i: +u[0].dataset.aimI }));
      keyed.sort((a, b) => {
        if (!st || !st.dir) return a.i - b.i;
        if (a.k === null || b.k === null) return (a.k === null) - (b.k === null) || a.i - b.i;
        const d = typeof a.k === 'number' && typeof b.k === 'number' ? a.k - b.k : String(a.k).localeCompare(String(b.k));
        return d * st.dir || a.i - b.i;
      });
      const parent = seg[0][0].parentNode, anchor = [...parent.children].filter(el => seg.some(u => u.includes(el))).at(-1).nextSibling;
      const frag = document.createDocumentFragment();
      keyed.forEach(({ u }) => u.forEach(el => frag.append(el)));
      parent.insertBefore(frag, anchor);
    }
  }

  function headCells(table) {
    const head = table.tHead;
    return head && head.rows.length ? [...head.rows[head.rows.length - 1].cells] : [];
  }

  function numericColumn(table, spec, c) {
    let num = 0, txt = 0;
    units(table, spec).flat().forEach(u => {
      const k = key(lead(u)?.cells[c]);
      if (typeof k === 'number' || (typeof k === 'string' && /^\d{4}-\d{2}/.test(k))) num++; else if (k !== null) txt++;
    });
    return num >= txt;
  }

  function enhance(table, spec, i) {
    headCells(table).forEach((th, c) => {
      if (th.querySelector('.aim-sort') || (spec.skip || []).includes(c) || th.colSpan > 1 || !th.textContent.trim()) return;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = /right|end/.test(getComputedStyle(th).textAlign) ? 'aim-sort aim-sort-r' : 'aim-sort'; // icon on the inner side
      btn.append(...th.childNodes);
      const ind = document.createElement('span');
      ind.className = 'aim-sort-ind';
      ind.setAttribute('aria-hidden', 'true');
      btn.append(ind);
      th.append(btn);
      btn.addEventListener('click', () => {
        const st = state.get(i);
        const first = numericColumn(table, spec, c) ? -1 : 1; // numbers and dates: largest first
        const dir = !st || st.col !== c || !st.dir ? first : st.dir === first ? -first : 0;
        state.set(i, { col: c, dir });
        quiet(() => apply(table, spec, i));
      });
    });
  }

  let observer;
  function quiet(fn) { observer && observer.disconnect(); try { fn(); } finally { observe(); } }
  /* ---------- clamp: long notes at a few lines, Show more per note, Expand all per register ---------- */
  const expandAll = new Map(); // Expand-all anchor (or spec index) -> every note open
  const sizer = new ResizeObserver(entries => entries.forEach(en => fit(en.target)));
  function fit(el) {
    const open = el.classList.contains('aim-open'), more = el.nextElementSibling;
    const over = el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1;
    el.classList.toggle('aim-cut', over && !open);
    if (more && more.classList.contains('aim-more')) more.hidden = !open && !over;
  }
  function setOpen(el, open) {
    el.classList.toggle('aim-open', open);
    const more = el.nextElementSibling;
    if (more && more.classList.contains('aim-more')) { more.textContent = open ? 'Show less' : 'Show more'; more.setAttribute('aria-expanded', open); }
    fit(el);
  }
  function clampScan() {
    const specs = cfg.clamp || [];
    specs.forEach((spec, i) => {
      const group = spec.all || i, anchor = spec.all && document.querySelector(spec.all);
      if (anchor && ![...document.querySelectorAll('.aim-all')].some(b => b.dataset.aimAll === spec.all)) {
        const all = document.createElement('button');
        all.type = 'button';
        all.className = 'aim-all';
        all.dataset.aimAll = spec.all;
        all.setAttribute('aria-pressed', 'false');
        all.textContent = 'Expand all notes';
        all.addEventListener('click', () => {
          const open = !expandAll.get(group);
          expandAll.set(group, open);
          all.setAttribute('aria-pressed', open);
          all.textContent = open ? 'Collapse all notes' : 'Expand all notes';
          specs.filter(sp => sp.all === spec.all).forEach(sp => document.querySelectorAll(sp.sel).forEach(el => setOpen(el, open)));
        });
        anchor.after(all);
      }
      document.querySelectorAll(spec.sel).forEach(el => {
        if (el.classList.contains('aim-clamp')) return;
        el.classList.add('aim-clamp');
        if ((spec.lines || 3) === 1) el.classList.add('aim-clamp-1'); // one line truncates with an ellipsis; no fade
        el.style.setProperty('--aim-lines', spec.lines || 3);
        const more = document.createElement('button');
        more.type = 'button';
        more.className = 'aim-more';
        more.hidden = true;
        more.addEventListener('click', e => { e.stopPropagation(); setOpen(el, !el.classList.contains('aim-open')); });
        el.after(more);
        setOpen(el, !!expandAll.get(group));
        sizer.observe(el);
      });
    });
  }

  /* ---------- label: each body cell carries its column's head, for a stacked phone layout ---------- */
  function label(table) {
    const heads = headCells(table).map(th => th.textContent.replace(/[▲▼]/g, '').trim());
    for (const body of table.tBodies) for (const row of body.rows) {
      if ([...row.cells].some(cell => cell.colSpan > 1)) continue;
      [...row.cells].forEach((cell, c) => { if (heads[c] && cell.dataset.aimLabel !== heads[c]) cell.dataset.aimLabel = heads[c]; });
    }
  }

  function scan() {
    clampScan();
    if (cfg.label) document.querySelectorAll(cfg.label).forEach(label);
    (cfg.sort || []).forEach((spec, i) => document.querySelectorAll(spec.table).forEach(table => {
      const fresh = units(table, spec).flat().some(u => !u[0].dataset.aimI);
      const bare = headCells(table).some((th, c) => !(spec.skip || []).includes(c) && th.colSpan === 1 && th.textContent.trim() && !th.querySelector('.aim-sort'));
      if (fresh || bare) { enhance(table, spec, i); apply(table, spec, i); }
    }));
  }
  function observe() { observer && observer.observe(document.body, { childList: true, subtree: true }); }
  // Observer callbacks run before the next paint, so a re-rendered table never shows unsorted.
  observer = new MutationObserver(() => quiet(scan));

  /* ---------- tooltip: one element, follows the pointer, also opens on keyboard focus ---------- */
  const tip = document.createElement('div');
  tip.className = 'aim-tip';
  tip.id = 'aim-tip';
  tip.setAttribute('role', 'tooltip');
  tip.hidden = true;
  let host = null, stash = null;

  function tipText(el) {
    const t = el.getAttribute('title') ?? el.querySelector(':scope > title')?.textContent;
    return t && t.trim() ? t : null;
  }
  function place(x, y) {
    const pad = 12, w = tip.offsetWidth, h = tip.offsetHeight;
    let left = x + 14, top = y + 16;
    if (left + w + pad > innerWidth) left = Math.max(pad, x - w - 14);
    if (top + h + pad > innerHeight) top = Math.max(pad, y - h - 14);
    tip.style.transform = `translate(${Math.round(left)}px,${Math.round(top)}px)`;
  }
  function show(el, x, y) {
    if (host !== el) hide();
    const text = host === el ? tip.textContent : tipText(el);
    if (!text) return;
    if (host !== el) {
      host = el;
      // Hold the native title back while ours is open; it returns on leave, so assistive tech keeps it.
      const node = el.querySelector(':scope > title');
      stash = node ? { node } : { attr: el.getAttribute('title') };
      if (node) node.remove(); else el.removeAttribute('title');
      tip.textContent = text;
      tip.hidden = false;
      el.setAttribute('aria-describedby', 'aim-tip');
    }
    place(x, y);
    tip.classList.add('on');
  }
  function hide() {
    if (!host) return;
    if (stash.node) host.prepend(stash.node); else if (stash.attr != null) host.setAttribute('title', stash.attr);
    host.removeAttribute('aria-describedby');
    host = stash = null;
    tip.classList.remove('on');
    tip.hidden = true;
  }
  function tipHost(target) {
    if (!cfg.tips || !(target instanceof Element)) return null;
    if (host && host.isConnected && host.contains(target)) return host; // its title is stashed while open
    const el = target.closest(cfg.tips);
    return el && tipText(el) ? el : null;
  }

  function init() {
    document.body.append(tip);
    document.addEventListener('pointermove', e => {
      const el = tipHost(e.target);
      if (el) show(el, e.clientX, e.clientY); else hide();
    }, { passive: true });
    document.addEventListener('focusin', e => {
      const el = tipHost(e.target);
      if (!el) return hide();
      const r = el.getBoundingClientRect();
      show(el, r.left, r.bottom - 8);
    });
    document.addEventListener('focusout', hide);
    document.addEventListener('scroll', hide, { passive: true, capture: true });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') hide(); });
    scan();
    observe();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
