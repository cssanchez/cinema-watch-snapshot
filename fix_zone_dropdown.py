#!/usr/bin/env python3
"""Patch the Zone dropdown to use URL params, localStorage fallback, and keep selection persistent."""

from pathlib import Path
import re

DOCS_ROOT = Path(__file__).parent / 'docs'
SCRIPT_PATTERN = re.compile(
    r"const storageKey = 'cinema-watch-location';\n.*?window\.CinemaWatchLocations\s*=\s*\{\s*init:\s*initHomepageLocation\s*\};\n",
    re.S,
)

NEW_SCRIPT = """const storageKey = 'cinema-watch-location';
      const locationSearchParam = 'location';

      function getUrlLocation() {
        const params = new URLSearchParams(window.location.search || '');
        return params.get(locationSearchParam) || '';
      }

      function updateUrlLocation(key) {
        const url = new URL(window.location.href);
        const params = url.searchParams;
        if (key) {
          params.set(locationSearchParam, key);
        } else {
          params.delete(locationSearchParam);
        }
        url.search = params.toString();
        history.replaceState(null, '', url.toString());
      }

      let cachedButtons = null;
      let cachedPanels = null;
      let availableKeys = null;

      function setHomepageLocation(root, key, { persist = true, updateUrl = true } = {}) {
        if (!cachedButtons) {
          cachedButtons = Array.from(root.querySelectorAll('[data-location-target]'));
          cachedPanels = Array.from(root.querySelectorAll('[data-location-panel]'));
          availableKeys = new Set([
            ...cachedPanels.map((panel) => panel.dataset.locationPanel || ''),
            ...cachedButtons.map((button) => button.dataset.locationTarget || ''),
          ]);
        }

        const buttons = cachedButtons;
        const panels = cachedPanels;

        let nextKey = key && availableKeys.has(key) ? key : '';
        if (!nextKey) {
          const activeButton = buttons.find((button) => button.getAttribute('aria-pressed') === 'true');
          nextKey = activeButton?.dataset.locationTarget || '';
        }
        if (!nextKey && buttons.length > 0) {
          nextKey = buttons[0].dataset.locationTarget || '';
        }
        if (!nextKey) {
          return '';
        }

        for (const button of buttons) {
          const pressed = button.dataset.locationTarget === nextKey;
          button.setAttribute('aria-pressed', pressed ? 'true' : 'false');
        }
        for (const panel of panels) {
          panel.hidden = panel.dataset.locationPanel !== nextKey;
        }

        const activeLabel = root.querySelector('.nav-location-active');
        if (activeLabel) {
          const activeBtn = buttons.find((b) => b.dataset.locationTarget === nextKey);
          if (activeBtn) {
            const span = activeBtn.querySelector('span');
            if (span) activeLabel.textContent = span.textContent;
          }
        }

        if (persist) {
          if (nextKey) {
            window.localStorage.setItem(storageKey, nextKey);
          } else {
            window.localStorage.removeItem(storageKey);
          }
        }

        if (updateUrl) {
          updateUrlLocation(nextKey);
        }

        return nextKey;
      }

      function initHomepageLocation(root = document) {
        const urlKey = getUrlLocation();
        const savedKey = window.localStorage.getItem(storageKey) || '';
        const initialKey = urlKey || savedKey;
        const resolvedKey = setHomepageLocation(root, initialKey, { persist: false, updateUrl: false });

        if (resolvedKey && !urlKey) {
          updateUrlLocation(resolvedKey);
        }
      }

      document.addEventListener('click', (event) => {
        const toggle = event.target.closest('[data-location-dropdown-toggle]');
        if (toggle) {
          event.preventDefault();
          const menu = document.querySelector('.nav-location-menu');
          if (menu) {
            const expanded = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', !expanded);
            menu.hidden = expanded;
          }
          return;
        }

        if (!event.target.closest('[data-location-dropdown]')) {
          const toggleBtn = document.querySelector('[data-location-dropdown-toggle]');
          const menuBox = document.querySelector('.nav-location-menu');
          if (toggleBtn && menuBox) {
            toggleBtn.setAttribute('aria-expanded', 'false');
            menuBox.hidden = true;
          }
        }

        const button = event.target.closest('[data-location-target]');
        if (!(button instanceof HTMLButtonElement)) {
          return;
        }
        event.preventDefault();
        setHomepageLocation(document, button.dataset.locationTarget || '');
        
        const menuToClose = document.querySelector('.nav-location-menu');
        const toggleToClose = document.querySelector('[data-location-dropdown-toggle]');
        if (menuToClose && toggleToClose) {
          menuToClose.hidden = true;
          toggleToClose.setAttribute('aria-expanded', 'false');
        }
      });

      initHomepageLocation(document);
      window.CinemaWatchLocations = { init: initHomepageLocation };
"""


def fix_zone_dropdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "const storageKey = 'cinema-watch-location';" not in content:
        return False

    modified_content, count = SCRIPT_PATTERN.subn(NEW_SCRIPT, content)
    if count == 0 or modified_content == content:
        return False

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    return True


def find_html_files():
    return sorted(DOCS_ROOT.rglob('index.html'))


def main():
    files = find_html_files()
    print(f"Found {len(files)} HTML files to process")

    fixed_count = 0
    failed_count = 0

    for file_path in files:
        try:
            if fix_zone_dropdown(file_path):
                relative_path = file_path.relative_to(DOCS_ROOT)
                print(f"  [+] Fixed {relative_path}")
                fixed_count += 1
            else:
                relative_path = file_path.relative_to(DOCS_ROOT)
                print(f"  [-] No changes needed for {relative_path}")
        except Exception as e:
            relative_path = file_path.relative_to(DOCS_ROOT)
            print(f"  [E] Error processing {relative_path}: {e}")
            failed_count += 1

    print(f"\nSummary: {fixed_count} fixed, {failed_count} errors")
    return failed_count == 0


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
