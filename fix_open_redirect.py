import os
import re
from pathlib import Path

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        modified = False

        # Target 1: const targetUrl = `${homePath}${hash || ''}`;
        old_target1 = r"const targetUrl = `\$\{homePath\}\$\{hash \|\| ''\}`;(\s+if \(window\.CineVicioLiveNav\?\.load\) \{\s+window\.CineVicioLiveNav\.load\(targetUrl\);\s+return;\s+\}\s+window\.location\.assign\(targetUrl\);)"
        new_target1 = r"""let targetUrl;
        try {
          const parsedUrl = new URL(`${homePath}${hash || ''}`, window.location.origin);
          if (parsedUrl.origin !== window.location.origin) throw new Error('Invalid origin');
          targetUrl = parsedUrl.href;
        } catch (e) {
          targetUrl = '/';
        }\1"""

        if re.search(old_target1, content):
            content = re.sub(old_target1, new_target1, content)
            modified = True

        # Target 2: const targetUrl = `${homePath}#cartelera`;
        old_target2 = r"const targetUrl = `\$\{homePath\}#cartelera`;(\s+if \(window\.CineVicioLiveNav\?\.load\) \{\s+window\.CineVicioLiveNav\.load\(targetUrl\);\s+\} else \{\s+window\.location\.assign\(targetUrl\);\s+\})"
        new_target2 = r"""let targetUrl;
            try {
              const parsedUrl = new URL(`${homePath}#cartelera`, window.location.origin);
              if (parsedUrl.origin !== window.location.origin) throw new Error('Invalid origin');
              targetUrl = parsedUrl.href;
            } catch (e) {
              targetUrl = '/';
            }\1"""

        if re.search(old_target2, content):
            content = re.sub(old_target2, new_target2, content)
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    docs_dir = "docs"
    count = 0
    for p in Path(docs_dir).rglob('*.html'):
        if process_file(p):
            count += 1
    print(f"Patched {count} files")

if __name__ == "__main__":
    main()
