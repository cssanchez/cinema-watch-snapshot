import re

with open('docs/screenings/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# 1. getScreeningsLink
c1 = re.sub(
    r"function getScreeningsLink\(\) \{\s*return document\.querySelector\('\[data-nav-link=\"screenings\"\]'\);\s*\}",
    "let _cachedScreeningsLink = null;\n      function getScreeningsLink() {\n        if (!_cachedScreeningsLink) _cachedScreeningsLink = document.querySelector('[data-nav-link=\"screenings\"]');\n        return _cachedScreeningsLink;\n      }",
    content
)
c2 = c1.replace(
    "const screeningsLink = document.querySelector('[data-nav-link=\"screenings\"]');",
    "const screeningsLink = getScreeningsLink();"
)

# 2. syncTopNavState document.querySelectorAll('[data-nav-link]')
c3 = c2.replace(
    "function syncTopNavState() {",
    "let _cachedNavLinks = null;\n      function syncTopNavState() {",
    1
)
c4 = c3.replace(
    "document.querySelectorAll('[data-nav-link]').forEach((link) => {",
    "if (!_cachedNavLinks) _cachedNavLinks = document.querySelectorAll('[data-nav-link]');\n        _cachedNavLinks.forEach((link) => {"
)

# 3. syncToolbarZoneSummaries & closeToolbarZones document.querySelectorAll('.toolbar-zone')
c5 = c4.replace(
    "function closeToolbarZones(except = null) {",
    "let _cachedToolbarZones = null;\n      function closeToolbarZones(except = null) {",
    1
)
c6 = c5.replace(
    "document.querySelectorAll('.toolbar-zone[open]').forEach((element) => {",
    "if (!_cachedToolbarZones) _cachedToolbarZones = document.querySelectorAll('.toolbar-zone');\n        _cachedToolbarZones.forEach((element) => {\n          if (!element.hasAttribute('open')) return;"
)
c7 = c6.replace(
    "document.querySelectorAll('.toolbar-zone').forEach((element) => {",
    "if (!_cachedToolbarZones) _cachedToolbarZones = document.querySelectorAll('.toolbar-zone');\n        _cachedToolbarZones.forEach((element) => {"
)

# 4. syncActiveQuickBoardPresets document.querySelectorAll('form[data-front-advanced-form="true"]')
c8 = c7.replace(
    "function syncActiveQuickBoardPresets(root = document) {",
    "let _cachedAdvancedForms = null;\n      function syncActiveQuickBoardPresets(root = document) {",
    1
)
c9 = c8.replace(
    "Array.from(root.querySelectorAll('form[data-front-advanced-form=\"true\"]'))",
    "Array.from(root === document ? (_cachedAdvancedForms || (_cachedAdvancedForms = root.querySelectorAll('form[data-front-advanced-form=\"true\"]'))) : root.querySelectorAll('form[data-front-advanced-form=\"true\"]'))"
)
c10 = c9.replace(
    "document.querySelectorAll('form[data-front-advanced-form=\"true\"]').forEach((form) => {",
    "if (!_cachedAdvancedForms) _cachedAdvancedForms = document.querySelectorAll('form[data-front-advanced-form=\"true\"]');\n        _cachedAdvancedForms.forEach((form) => {"
)

# 5. applyTranslations document.querySelectorAll('[data-i18n-source]')
c11 = c10.replace(
    "function applyTranslations(root = document) {",
    "let _cachedI18nSources = null;\n      let _cachedLanguageOptions = null;\n      let _cachedI18nPlaceholders = null;\n      function applyTranslations(root = document) {",
    1
)
c12 = c11.replace(
    "scope.querySelectorAll('[data-i18n-source]').forEach((element) => {",
    "const sources = scope === document ? (_cachedI18nSources || (_cachedI18nSources = scope.querySelectorAll('[data-i18n-source]'))) : scope.querySelectorAll('[data-i18n-source]');\n        sources.forEach((element) => {"
)
c13 = c12.replace(
    "scope.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {",
    "const placeholders = scope === document ? (_cachedI18nPlaceholders || (_cachedI18nPlaceholders = scope.querySelectorAll('[data-i18n-placeholder]'))) : scope.querySelectorAll('[data-i18n-placeholder]');\n        placeholders.forEach((element) => {"
)
c14 = c13.replace(
    "document.querySelectorAll('[data-language-option]').forEach((button) => {",
    "if (!_cachedLanguageOptions) _cachedLanguageOptions = document.querySelectorAll('[data-language-option]');\n        _cachedLanguageOptions.forEach((button) => {"
)

print(c14 != original)
