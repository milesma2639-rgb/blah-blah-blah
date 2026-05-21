import html
import re
import sys
from pathlib import Path

ROOT = Path('game-repos')
ROOT.mkdir(exist_ok=True)
raw = sys.stdin.read().replace('──', '\n')
pattern = re.compile(r"([^:\n]+?)\s*:\s*([^\n]*?\.html?)", re.IGNORECASE)

seen = set()
count = 0
for name, file_name in pattern.findall(raw):
    name = ' '.join(name.strip().split())
    file_name = file_name.strip()

    if not name or name.lower().startswith('note'):
        continue

    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    if not slug:
        continue

    base = slug
    suffix = 2
    while slug in seen:
        slug = f"{base}-{suffix}"
        suffix += 1
    seen.add(slug)

    repo_dir = ROOT / slug
    repo_dir.mkdir(parents=True, exist_ok=True)

    (repo_dir / 'README.md').write_text(
        f"# {name}\n\nSource file: `{file_name}`\n",
        encoding='utf-8',
    )

    safe_title = html.escape(name)
    (repo_dir / file_name).write_text(
        (
            '<!doctype html>\n'
            '<html lang="en">\n'
            '<head>\n'
            '  <meta charset="utf-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'  <title>{safe_title}</title>\n'
            '</head>\n'
            '<body>\n'
            f'  <h1>{safe_title}</h1>\n'
            '</body>\n'
            '</html>\n'
        ),
        encoding='utf-8',
    )

    count += 1

(ROOT / 'README.md').write_text(
    f"# Game Repositories\n\nGenerated {count} repositories from provided list.\n",
    encoding='utf-8',
)
print(count)
