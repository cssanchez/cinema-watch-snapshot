import re

with open('fix_zone_dropdown.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = """      function setHomepageLocation(root, key, { persist = true, updateUrl = true } = {}) {
        const buttons = Array.from(root.querySelectorAll('[data-location-target]'));
        const panels = Array.from(root.querySelectorAll('[data-location-panel]'));
        const availableKeys = new Set([
          ...panels.map((panel) => panel.dataset.locationPanel || ''),
          ...buttons.map((button) => button.dataset.locationTarget || ''),
        ]);"""

new_func = """      let cachedButtons = null;
      let cachedPanels = null;
      let cachedKeys = null;

      function setHomepageLocation(root, key, { persist = true, updateUrl = true } = {}) {
        if (!cachedButtons) {
          cachedButtons = Array.from(root.querySelectorAll('[data-location-target]'));
          cachedPanels = Array.from(root.querySelectorAll('[data-location-panel]'));
          cachedKeys = new Set([
            ...cachedPanels.map((panel) => panel.dataset.locationPanel || ''),
            ...cachedButtons.map((button) => button.dataset.locationTarget || ''),
          ]);
        }

        const buttons = cachedButtons;
        const panels = cachedPanels;
        const availableKeys = cachedKeys;"""

new_content = content.replace(old_func, new_func)

if new_content != content:
    with open('fix_zone_dropdown.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched fix_zone_dropdown.py")
else:
    print("Could not find block to patch")
