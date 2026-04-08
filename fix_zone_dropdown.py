#!/usr/bin/env python3
"""Simplify zone dropdown - always keep a zone selected, no empty state."""

from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def fix_zone_dropdown(file_path):
    """Simplify setHomepageLocation to always have a zone selected."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if this file needs fixing (has the placeholder "Zone" logic)
    if "activeLabel.textContent = 'Zone';" not in content:
        return False
    
    # Replace the problematic logic where it sets the placeholder
    modified_content = content.replace(
        """        const activeLabel = root.querySelector('.nav-location-active');
        if (activeLabel) {
          if (nextKey) {
            const activeBtn = buttons.find((b) => b.dataset.locationTarget === nextKey);
            if (activeBtn) {
              const span = activeBtn.querySelector('span');
              if (span) activeLabel.textContent = span.textContent;
            }
          } else {
            activeLabel.textContent = 'Zone';
          }
        }""",
        """        const activeLabel = root.querySelector('.nav-location-active');
        if (activeLabel) {
          const activeBtn = buttons.find((b) => b.dataset.locationTarget === nextKey);
          if (activeBtn) {
            const span = activeBtn.querySelector('span');
            if (span) activeLabel.textContent = span.textContent;
          }
        }"""
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
    
    for file_path in files:
        try:
            if fix_zone_dropdown(file_path):
                relative_path = file_path.relative_to(DOCS_ROOT)
                print(f"  [+] Cleaned {relative_path}")
                fixed_count += 1
        except Exception as e:
            relative_path = file_path.relative_to(DOCS_ROOT)
            print(f"  [E] Error: {relative_path}: {e}")
    
    print(f"\nSummary: {fixed_count} cleaned")
    return True

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
