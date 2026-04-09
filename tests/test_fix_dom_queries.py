import pytest
from pathlib import Path
import re

from fix_dom_queries import optimize_dom_queries

def test_optimize_dom_queries():
    sample_content = """
    <script>
      function getScreeningsLink() {
        return document.querySelector('[data-nav-link="screenings"]');
      }
      function doThing() {
        const screeningsLink = document.querySelector('[data-nav-link="screenings"]');
      }
      function syncTopNavState() {
        document.querySelectorAll('[data-nav-link]').forEach((link) => {
        });
      }
      function closeToolbarZones(except = null) {
        document.querySelectorAll('.toolbar-zone[open]').forEach((element) => {
        });
        document.querySelectorAll('.toolbar-zone').forEach((element) => {
        });
      }
      function syncActiveQuickBoardPresets(root = document) {
        const forms = Array.from(root.querySelectorAll('form[data-front-advanced-form="true"]'));
        document.querySelectorAll('form[data-front-advanced-form="true"]').forEach((form) => {
        });
      }
      function applyTranslations(root = document) {
        root.querySelectorAll('[data-i18n-source]').forEach((element) => {
        });
        root.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
        });
        document.querySelectorAll('[data-language-option]').forEach((button) => {
        });
      }
    </script>
    """
    new_content, changed = optimize_dom_queries(sample_content)
    assert changed is True

    # Assert caching logic introduced
    assert "let _cachedScreeningsLink = null;" in new_content
    assert "const screeningsLink = getScreeningsLink();" in new_content
    assert "let _cachedNavLinks = null;" in new_content
    assert "let _cachedToolbarZones = null;" in new_content
    assert "let _cachedAdvancedForms = null;" in new_content
    assert "let _cachedI18nSources = null;" in new_content
    assert "let _cachedLanguageOptions = null;" in new_content
    assert "let _cachedI18nPlaceholders = null;" in new_content

    # Validate that `if (!cachedVar) cachedVar = ...` logic is present
    assert "if (!_cachedNavLinks) _cachedNavLinks = document.querySelectorAll('[data-nav-link]');" in new_content
