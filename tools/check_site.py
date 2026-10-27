#!/usr/bin/env python3
"""Check the built site: every relative href/src resolves inside site/, and every data file is JSON.

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
        for url in LINK.findall(page.read_text(encoding='utf-8')):
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or url.startswith(('#', 'mailto:', 'data:')):
                continue
            target = (page.parent / unquote(parts.path)).resolve()
            if site not in target.parents and target != site:
                errors.append(f'{page.relative_to(site)}: {url} leaves the site')
            elif not target.exists():
                errors.append(f'{page.relative_to(site)}: {url} not found')
    data = sorted(site.glob('data/*.json')) + [site / 'site.json']
    for path in data:
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            errors.append(f'{path.relative_to(site)}: {exc}')
    for line in errors:
        print(f'✗ {line}')
    if errors:
        return 1
    print(f'✓ {len(pages)} pages, {len(data)} JSON files, all relative links resolve')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else 'site')))
