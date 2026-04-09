#!/usr/bin/env python3
"""
Performance Optimization: Cache repeated DOM queries that run in UI interaction loops
This script modifies the HTML files in docs/ to cache the result of document.querySelector
and document.querySelectorAll for elements that don't change at runtime (static site).
"""

import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

def optimize_dom_queries(content):
    original = content

    # 1. getScreeningsLink
    content = re.sub(
        r"function getScreeningsLink\(\) \{\s*return document\.querySelector\('\[data-nav-link=\"screenings\"\]'\);\s*\}",
        "let _cachedScreeningsLink = null;\n      function getScreeningsLink() {\n        if (!_cachedScreeningsLink) _cachedScreeningsLink = document.querySelector('[data-nav-link=\"screenings\"]');\n        return _cachedScreeningsLink;\n      }",
        content
    )
    content = content.replace(
        "const screeningsLink = document.querySelector('[data-nav-link=\"screenings\"]');",
        "const screeningsLink = getScreeningsLink();"
    )

    # 2. syncTopNavState document.querySelectorAll('[data-nav-link]')
    if "let _cachedNavLinks = null;" not in content:
        content = content.replace(
            "function syncTopNavState() {",
            "let _cachedNavLinks = null;\n      function syncTopNavState() {",
            1
        )
        content = content.replace(
            "document.querySelectorAll('[data-nav-link]').forEach((link) => {",
            "if (!_cachedNavLinks) _cachedNavLinks = document.querySelectorAll('[data-nav-link]');\n        _cachedNavLinks.forEach((link) => {"
        )

    # 3. syncToolbarZoneSummaries & closeToolbarZones document.querySelectorAll('.toolbar-zone')
    if "let _cachedToolbarZones = null;" not in content:
        content = content.replace(
            "function closeToolbarZones(except = null) {",
            "let _cachedToolbarZones = null;\n      function closeToolbarZones(except = null) {",
            1
        )
        content = content.replace(
            "document.querySelectorAll('.toolbar-zone[open]').forEach((element) => {",
            "if (!_cachedToolbarZones) _cachedToolbarZones = document.querySelectorAll('.toolbar-zone');\n        _cachedToolbarZones.forEach((element) => {\n          if (!element.hasAttribute('open')) return;"
        )
        content = content.replace(
            "document.querySelectorAll('.toolbar-zone').forEach((element) => {",
            "if (!_cachedToolbarZones) _cachedToolbarZones = document.querySelectorAll('.toolbar-zone');\n        _cachedToolbarZones.forEach((element) => {"
        )

    # 4. syncActiveQuickBoardPresets document.querySelectorAll('form[data-front-advanced-form="true"]')
    # Fix the bug identified in code review: maintain the root scope, rather than assuming document
    if "let _cachedAdvancedForms = null;" not in content:
        content = content.replace(
            "function syncActiveQuickBoardPresets(root = document) {",
            "let _cachedAdvancedForms = null;\n      function syncActiveQuickBoardPresets(root = document) {",
            1
        )
        content = content.replace(
            "Array.from(root.querySelectorAll('form[data-front-advanced-form=\"true\"]'))",
            "Array.from(root === document ? (_cachedAdvancedForms || (_cachedAdvancedForms = root.querySelectorAll('form[data-front-advanced-form=\"true\"]'))) : root.querySelectorAll('form[data-front-advanced-form=\"true\"]'))"
        )
        content = content.replace(
            "document.querySelectorAll('form[data-front-advanced-form=\"true\"]').forEach((form) => {",
            "if (!_cachedAdvancedForms) _cachedAdvancedForms = document.querySelectorAll('form[data-front-advanced-form=\"true\"]');\n        _cachedAdvancedForms.forEach((form) => {"
        )

    # 5. applyTranslations scope.querySelectorAll('[data-i18n-source]')
    # Fix the bug identified in code review: uses 'root' instead of 'scope' occasionally
    if "let _cachedI18nSources = null;" not in content:
        content = content.replace(
            "function applyTranslations(root = document) {",
            "let _cachedI18nSources = null;\n      let _cachedLanguageOptions = null;\n      let _cachedI18nPlaceholders = null;\n      function applyTranslations(root = document) {",
            1
        )
        content = content.replace(
            "scope.querySelectorAll('[data-i18n-source]').forEach((element) => {",
            "const sources = scope === document ? (_cachedI18nSources || (_cachedI18nSources = scope.querySelectorAll('[data-i18n-source]'))) : scope.querySelectorAll('[data-i18n-source]');\n        sources.forEach((element) => {"
        )
        content = content.replace(
            "scope.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {",
            "const placeholders = scope === document ? (_cachedI18nPlaceholders || (_cachedI18nPlaceholders = scope.querySelectorAll('[data-i18n-placeholder]'))) : scope.querySelectorAll('[data-i18n-placeholder]');\n        placeholders.forEach((element) => {"
        )
        content = content.replace(
            "document.querySelectorAll('[data-language-option]').forEach((button) => {",
            "if (!_cachedLanguageOptions) _cachedLanguageOptions = document.querySelectorAll('[data-language-option]');\n        _cachedLanguageOptions.forEach((button) => {"
        )

    return content, content != original

def main():
    files = list(DOCS_ROOT.rglob('*.html'))
    processed_count = 0
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, changed = optimize_dom_queries(content)

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            processed_count += 1
            print(f"Patched: {file_path.relative_to(DOCS_ROOT)}")

    print(f"\nDone! Patched {processed_count} files out of {len(files)} total HTML files.")

if __name__ == '__main__':
    main()
