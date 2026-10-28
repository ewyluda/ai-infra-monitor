#!/usr/bin/env python3
"""Check the built site: every relative href/src resolves inside site/, site.json is JSON, no data
files are published (the site serves pages, not data), and every page carries the TDM reservation.

    python3 tools/check_site.py [SITE_DIR]

Stdlib only. Exits 1 on any failure.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK = re.compile(r'''(?<![\w-])(?:href|src)\s*=\s*["']([^"'$`{]+)["']''')


def main(site):
    site = site.resolve()
    errors = []
    pages = sorted(site.rglob('*.html'))
    for page in pages:
        text = page.read_text(encoding='utf-8')
        if '<meta name="tdm-reservation" content="1"' not in text:
            errors.append(f'{page.relative_to(site)}: no tdm-reservation meta')
        for url in LINK.findall(text):
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or url.startswith(('#', 'mailto:', 'data:')):
                continue
            target = (page.parent / unquote(parts.path)).resolve()
            if site not in target.parents and target != site:
                errors.append(f'{page.relative_to(site)}: {url} leaves the site')
            elif not target.exists():
                errors.append(f'{page.relative_to(site)}: {url} not found')
    for path in sorted(site.rglob('*.json')):
        if path != site / 'site.json':
            errors.append(f'{path.relative_to(site)}: data file published')
    try:
        json.loads((site / 'site.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        errors.append(f'site.json: {exc}')
    for line in errors:
        print(f'✗ {line}')
    if errors:
        return 1
    print(f'✓ {len(pages)} pages, all relative links resolve, no data files, TDM reservation on every page')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else 'site')))
