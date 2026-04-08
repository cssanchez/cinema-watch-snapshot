#!/usr/bin/env python3
"""Fix zone dropdown to allow unselected state across all HTML files."""

from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def fix_zone_dropdown(file_path):
    """Replace old setHomepageLocation with new robust version."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if this file has the old problematic pattern
    if 'buttons[0]?.dataset.locationTarget' not in content:
        return False
    
    # Make sequential string replacements to fix the function
    modified_content = content
    
    # 1. Fix the line that forces default to first button
    modified_content = modified_content.replace(
        "nextKey = activeButton?.dataset.locationTarget || buttons[0]?.dataset.locationTarget || '';",
        "if (activeButton) {\n            nextKey = activeButton.dataset.locationTarget || '';\n          }"
    )
    
    # 2. Remove the early return guard that prevents unselected state
    modified_content = modified_content.replace(
        "        if (!nextKey) {\n          return;\n        }\n\n",
        ""
    )
    
    # 3. Update panel visibility logic to handle empty selection
    modified_content = modified_content.replace(
        "          panel.hidden = panel.dataset.locationPanel !== nextKey;",
        "          panel.hidden = nextKey ? panel.dataset.locationPanel !== nextKey : true;"
    )
    
    # 4. Update label logic for unselected state
    modified_content = modified_content.replace(
        "        if (activeLabel && buttons.length > 0) {",
        "        if (activeLabel) {"
    )
    
    # 5. Add proper handling for empty nextKey in label
    modified_content = modified_content.replace(
        "          const activeBtn = buttons.find((b) => b.dataset.locationTarget === nextKey);\n          if (activeBtn) {\n            const span = activeBtn.querySelector('span');\n            if (span) activeLabel.textContent = span.textContent;\n          }",
        "          if (nextKey) {\n            const activeBtn = buttons.find((b) => b.dataset.locationTarget === nextKey);\n            if (activeBtn) {\n              const span = activeBtn.querySelector('span');\n              if (span) activeLabel.textContent = span.textContent;\n            }\n          } else {\n            activeLabel.textContent = 'Zone';\n          }"
    )
    
    # 6. Fix localStorage to only persist when actually selected
    modified_content = modified_content.replace(
        "        if (persist) {\n          window.localStorage.setItem(storageKey, nextKey);\n        }",
        "        if (persist) {\n          if (nextKey) {\n            window.localStorage.setItem(storageKey, nextKey);\n          } else {\n            window.localStorage.removeItem(storageKey);\n          }\n        }"
    )
    
    if modified_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        return True
    
    return False

def find_html_files():
    """Find all HTML files in docs directory."""
    return sorted(DOCS_ROOT.rglob('index.html'))

def main():
    """Fix zone dropdown in all HTML files."""
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
                # Don't print "no changes needed" to reduce clutter
        except Exception as e:
            relative_path = file_path.relative_to(DOCS_ROOT)
            print(f"  [E] Error processing {relative_path}: {e}")
            failed_count += 1
    
    print(f"\nSummary: {fixed_count} fixed, {failed_count} errors")
    return failed_count == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

def find_html_files():
    """Find all HTML files in docs directory."""
    return sorted(DOCS_ROOT.rglob('index.html'))

def main():
    """Fix zone dropdown in all HTML files."""
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
