#!/usr/bin/env python3
"""
Implement 6 UX/Security improvements to cinema listing website.
This script processes all HTML files in docs/ and applies transformations.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Configuration
DOCS_ROOT = str(Path(__file__).parent / "docs")
ENCODING = "utf-8"

# Pre-compiled Regex Patterns
RE_FRESHNESS_FONT = re.compile(r'(\.front-freshness strong\s*\{[^}]*?)font-family:\s*var\(--heading-font\)(.*?)font-size:\s*1\.1rem', flags=re.DOTALL)
RE_FRESHNESS_PADDING = re.compile(r'(\.front-freshness\s*\{[^}]*?)padding:\s*0\.9rem\s*1rem', flags=re.DOTALL)
RE_FRESHNESS_BG = re.compile(r'(\.front-freshness\s*\{[^}]*?)background:\s*rgba\(255,\s*255,\s*255,\s*0\.035\)', flags=re.DOTALL)

RE_DATE_GROUP = re.compile(r'(\n    )(<section class="front-date-group">)')
RE_STYLE_CLOSING = re.compile(r'(\s*)</style>')
RE_SEE_ALL_LINK = re.compile(r'<a class="text-link" ([^>]*)>See all</a>', flags=re.IGNORECASE)

RE_SOLD_PERCENT = re.compile(r'(\d+)%\s*sold')
RE_SCREENING_ROW_FULL = re.compile(r'<div class="front-screening-row">.*?</div>\s*</div>', flags=re.DOTALL)

RE_DATE_GROUP_FULL = re.compile(r'<section class="front-date-group">(?:[^<]|<(?!/section))*</section>', flags=re.DOTALL)
RE_SCREENING_ROW_OPEN = re.compile(r'<div class="front-screening-row"')
RE_SHOWN_COUNT = re.compile(r'(>)(\d+)(\s+shown<)')

def find_all_html_files(root_path: str) -> List[str]:
    """Find all HTML files in the docs directory."""
    html_files = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return sorted(html_files)


def transform_1_demote_freshness(content: str) -> str:
    """
    Demote freshness card prominence:
    - Change font-size from 1.1rem to 0.9rem in .front-freshness strong
    - Change font-family from heading-font to ui-font
    - Remove/reduce background opacity
    - Reduce padding
    """
    # Find and replace the .front-freshness CSS rule
    replacement = r'\1font-family: var(--ui-font)\2font-size: 0.9rem'
    content = RE_FRESHNESS_FONT.sub(replacement, content)

    # Also reduce padding in .front-freshness from 0.9rem 1rem to 0.6rem 0.8rem
    replacement_padding = r'\1padding: 0.6rem 0.8rem'
    content = RE_FRESHNESS_PADDING.sub(replacement_padding, content)

    # Remove or reduce background opacity
    replacement_bg = r'\1background: rgba(255, 255, 255, 0.02)'
    content = RE_FRESHNESS_BG.sub(replacement_bg, content)

    return content


def transform_2_add_time_context(content: str) -> str:
    """
    Add time context label before each screening group.
    Insert: <div class="screening-time-context" ...>Coming up</div>
    before: <section class="front-date-group">
    """
    time_context_html = (
        '<div class="screening-time-context" style="display:flex; align-items:center; gap:0.5rem; '
        'padding:1rem; color:var(--accent); font-size:0.95rem;"><span style="color:var(--muted);">'
        'Coming up</span></div>\n    '
    )

    # Replace all occurrences of <section class="front-date-group"> with the context label + section
    replacement = r'\1' + time_context_html.rstrip('\n    ') + r'\n    \2'
    content = RE_DATE_GROUP.sub(replacement, content)

    return content


def transform_3_truncation_signal(content: str) -> str:
    """
    Convert text-based "See all" links to pill-style buttons.
    Also add CSS for .button-see-all
    """
    # First, add CSS for button-see-all if not already present
    if '.button-see-all' not in content:
        css_rule = (
            '\n\n    .button-see-all {\n'
            '      display: inline-block;\n'
            '      padding: 0.5rem 1rem;\n'
            '      border-radius: var(--radius-lg);\n'
            '      background: var(--accent);\n'
            '      color: var(--bg);\n'
            '      font-size: 0.85rem;\n'
            '      font-weight: 500;\n'
            '      text-decoration: none;\n'
            '      cursor: pointer;\n'
            '      transition: opacity 0.2s;\n'
            '    }\n'
            '\n'
            '    .button-see-all:hover {\n'
            '      opacity: 0.8;\n'
            '    }'
        )

        # Insert CSS before the closing </style> tag
        content = RE_STYLE_CLOSING.sub(css_rule + r'\n  </style>', content)

    # Convert <a class="text-link" href="..." data-i18n-source>See all</a>
    # to <a class="button-see-all" href="..." data-i18n-source>See all</a>
    replacement = r'<a class="button-see-all" \1>See all</a>'
    content = RE_SEE_ALL_LINK.sub(replacement, content)

    return content


def extract_sold_percentage(screening_text: str) -> float:
    """Extract sold percentage from screening metadata text."""
    match = re.search(r'(\d+)%\s*sold', screening_text)
    if match:
        return float(match.group(1))
    return 0.0

def transform_4_occupancy_highlight(content: str) -> str:
    """
    Add screening-high-occupancy class to rows with >= 50% sold.
    Also add CSS for .screening-high-occupancy
    """
    # First, add CSS if not already present
    if '.screening-high-occupancy' not in content:
        css_rule = (
            '\n\n    .screening-high-occupancy {\n'
            '      background: rgba(240, 139, 101, 0.15);\n'
            '      border-left: 3px solid var(--warm);\n'
            '    }'
        )
        content = RE_STYLE_CLOSING.sub(css_rule + r'\n  </style>', content)

    # Find all front-screening-row elements and check if they have >= 50% sold
    def replace_row(match):
        row_html = match.group(0)
        # Check if this row contains sold percentage >= 50%
        sold_percent = extract_sold_percentage(row_html)
        if sold_percent >= 50:
            # Add class to the div
            row_html = row_html.replace(
                '<div class="front-screening-row">',
                '<div class="front-screening-row screening-high-occupancy">'
            )
        return row_html

    # Match front-screening-row divs
    # Secure fix for ReDoS: replaced nested quantifiers with a non-greedy match.
    # The structure is <div class="front-screening-row">...<div class="front-screening-copy">...</div></div>
    content = RE_SCREENING_ROW_FULL.sub(replace_row, content)

    return content


def transform_5_count_format(content: str) -> str:
    """
    Change "X shown" to "X of Y shown" where Y is inferred from context.
    For each section, count the actual screening rows and use that as Y.
    """
    def replace_shown_count(match):
        # match contains a front-date-group section
        section = match.group(0)

        # Count the front-screening-row elements in this section
        row_count = len(RE_SCREENING_ROW_OPEN.findall(section))

        # Replace "X shown" with "X of Y shown" where Y is the row count
        # More targeted approach: find and replace within the section
        section = RE_SHOWN_COUNT.sub(
            lambda m: m.group(1) + m.group(2) +
            f' of {row_count}' + m.group(3),
            section
        )

        return section

    # Match each front-date-group section
    content = RE_DATE_GROUP_FULL.sub(replace_shown_count, content)

    return content


def transform_6_add_csp(content: str) -> str:
    """
    Add Content-Security-Policy meta tag to prevent XSS attacks.
    """
    csp_tag = '  <meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\'; style-src \'self\' \'unsafe-inline\'; img-src \'self\' data:; connect-src \'self\'; font-src \'self\'; object-src \'none\'; base-uri \'self\'; form-action \'self\';">\n'
    if 'http-equiv="Content-Security-Policy"' not in content:
        if '<meta charset="utf-8">\n' in content:
            content = content.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + csp_tag)
        elif '<head>\n' in content:
            content = content.replace('<head>\n', '<head>\n' + csp_tag)
    return content

def process_file(file_path: str) -> Tuple[bool, int]:
    """
    Process a single HTML file applying all 6 transformations.
    Returns (success, changes_made)
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding=ENCODING) as f:
            content = f.read()

        original_content = content

        # Apply transformations in order
        content = transform_1_demote_freshness(content)
        content = transform_2_add_time_context(content)
        content = transform_3_truncation_signal(content)
        content = transform_4_occupancy_highlight(content)
        content = transform_5_count_format(content)

        content = transform_6_add_csp(content)
        
        # Check if changes were made
        changes_made = 1 if content != original_content else 0

        # Write back the file
        with open(file_path, 'w', encoding=ENCODING) as f:
            f.write(content)

        return True, changes_made

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0


def main():
    """Main entry point."""
    print("Cinema UX Improvements Automation")
    print("=" * 60)

    # Find all HTML files
    html_files = find_all_html_files(DOCS_ROOT)
    print(f"Found {len(html_files)} HTML files to process")

    # Process each file
    success_count = 0
    failure_count = 0
    files_changed = 0

    for i, file_path in enumerate(html_files, 1):
        rel_path = os.path.relpath(file_path, DOCS_ROOT)
        success, changes = process_file(file_path)

        if success:
            success_count += 1
            if changes:
                files_changed += 1
                print(f"[{i}/{len(html_files)}] {rel_path}")
        else:
            failure_count += 1
            print(f"ERROR [{i}/{len(html_files)}] {rel_path}")

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Total files: {len(html_files)}")
    print(f"  Processed successfully: {success_count}")
    print(f"  Files modified: {files_changed}")
    print(f"  Errors: {failure_count}")
    print("\nTransformations applied:")
    print("  1. Demoted freshness card prominence")
    print("  2. Added time context labels")
    print("  3. Converted See all links to pill buttons")
    print("  4. Added occupancy highlights for 50%+ sold")
    print("  5. Updated count display format to 'X of Y'")
    print("  6. Added Content-Security-Policy meta tag")


if __name__ == "__main__":
    main()
