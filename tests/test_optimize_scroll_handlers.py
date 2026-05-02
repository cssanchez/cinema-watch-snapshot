import pytest
from pathlib import Path
import optimize_scroll_handlers

@pytest.fixture
def temp_docs_dir(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    # Mocking optimize_scroll_handlers.DOCS_ROOT
    original_docs_root = optimize_scroll_handlers.DOCS_ROOT
    optimize_scroll_handlers.DOCS_ROOT = docs_dir
    yield docs_dir
    optimize_scroll_handlers.DOCS_ROOT = original_docs_root

def test_replaces_getActiveHomeSections(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
      function getActiveHomeSections() {
        const visiblePanel = getVisibleLocationPanel();
        const specials = visiblePanel?.querySelector('[data-front-specials="true"]')
          || document.querySelector('[data-front-specials="true"]');
        const movies = visiblePanel?.querySelector('[data-front-movies="true"]')
          || document.querySelector('[data-front-movies="true"]');
        return {
          cartelera: _getCartelera(),
          specials: specials instanceof HTMLElement ? specials : null,
          movies: movies instanceof HTMLElement ? movies : null,
        };
      }
    """, encoding="utf-8")

    optimize_scroll_handlers.process_file(test_html)
    content = test_html.read_text(encoding="utf-8")

    assert "let _lastVisiblePanel = undefined;" in content
    assert "let _lastActiveSections = null;" in content
    assert "if (_lastVisiblePanel === visiblePanel && _lastActiveSections) {" in content
    assert "_lastVisiblePanel = visiblePanel;" in content
    assert "_lastActiveSections = {" in content

def test_replaces_syncTopNavState(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
      function syncTopNavState() {
        const path = window.location.pathname || '/';
        const params = new URLSearchParams(window.location.search || '');
        const category = (params.get('category') || '').toLowerCase();
        const focusParam = (params.get('focus') || '').toLowerCase();
    """, encoding="utf-8")

    optimize_scroll_handlers.process_file(test_html)
    content = test_html.read_text(encoding="utf-8")

    assert "let _lastSearch = null;" in content
    assert "let _cachedCategory = '';" in content
    assert "let _cachedFocusParam = '';" in content
    assert "if (_lastSearch !== currentSearch) {" in content
    assert "_lastSearch = currentSearch;" in content

def test_idempotency(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_content = """
      function getActiveHomeSections() {
        const visiblePanel = getVisibleLocationPanel();
        const specials = visiblePanel?.querySelector('[data-front-specials="true"]')
          || document.querySelector('[data-front-specials="true"]');
        const movies = visiblePanel?.querySelector('[data-front-movies="true"]')
          || document.querySelector('[data-front-movies="true"]');
        return {
          cartelera: _getCartelera(),
          specials: specials instanceof HTMLElement ? specials : null,
          movies: movies instanceof HTMLElement ? movies : null,
        };
      }
    """
    test_html.write_text(test_content, encoding="utf-8")

    # First pass
    optimize_scroll_handlers.process_file(test_html)
    content_after_first_pass = test_html.read_text(encoding="utf-8")

    # Second pass
    optimize_scroll_handlers.process_file(test_html)
    content_after_second_pass = test_html.read_text(encoding="utf-8")

    assert content_after_first_pass == content_after_second_pass
