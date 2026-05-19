import pytest
import os
import shutil
from pathlib import Path
import optimize_dom_array_from

@pytest.fixture
def temp_docs_dir(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    # Mocking optimize_dom_array_from.DOCS_ROOT
    optimize_dom_array_from.DOCS_ROOT = docs_dir
    return docs_dir

def test_replaces_getVisibleLocationPanel(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
      function getVisibleLocationPanel() {
        return Array.from(document.querySelectorAll('[data-location-panel]'))
          .find((panel) => panel instanceof HTMLElement && !panel.hidden) || null;
      }
    """)

    optimize_dom_array_from.process_file(test_html)
    content = test_html.read_text()

    assert "Array.from" not in content
    assert "for (let i = 0; i < panels.length; i++)" in content

def test_replaces_getActiveHomeSections(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
      function getActiveHomeSections() {
        const visiblePanel = Array.from(document.querySelectorAll('[data-location-panel]'))
          .find((panel) => panel instanceof HTMLElement && !panel.hidden);
        return visiblePanel;
      }
    """)

    optimize_dom_array_from.process_file(test_html)
    content = test_html.read_text()

    assert "Array.from" not in content
    assert "const visiblePanel = getVisibleLocationPanel();" in content

def test_replaces_scrollToSpecialRooms(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
        target = Array.from(document.querySelectorAll('[data-front-specials="true"]'))
          .find((section) => {
            if (!(section instanceof HTMLElement)) {
              return false;
            }
            const panel = section.closest('[data-location-panel]');
            return !(panel instanceof HTMLElement) || !panel.hidden;
          });
    """)

    optimize_dom_array_from.process_file(test_html)
    content = test_html.read_text()

    assert "Array.from" not in content
    assert "const specials = document.querySelectorAll('[data-front-specials=\"true\"]');" in content
    assert "target = undefined;" in content

def test_replaces_scrollToMoviesSection(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
        target = Array.from(document.querySelectorAll('[data-front-movies="true"]'))
          .find((section) => {
            if (!(section instanceof HTMLElement)) {
              return false;
            }
            const panel = section.closest('[data-location-panel]');
            return !(panel instanceof HTMLElement) || !panel.hidden;
          });
    """)

    optimize_dom_array_from.process_file(test_html)
    content = test_html.read_text()

    assert "Array.from" not in content
    assert "const movies = document.querySelectorAll('[data-front-movies=\"true\"]');" in content
    assert "target = undefined;" in content


def test_replaces_initFrontBoards(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
      function initFrontBoards(root = document) {
        const locationKeys = new Set(
          Array.from(root.querySelectorAll('[data-front-board-location]'))
            .map((element) => element.getAttribute('data-front-board-location') || '')
            .filter(Boolean)
        );
        for (const locationKey of locationKeys) {
          setFrontBoard(root, locationKey, '');
        }
      }
    """)

    optimize_dom_array_from.process_file(test_html)
    content = test_html.read_text()

    assert "Array.from" not in content
    assert "const elements = root.querySelectorAll('[data-front-board-location]');" in content
    assert "const locationKeys = new Set();" in content
    assert "if (val) locationKeys.add(val);" in content


def test_replaces_syncActiveQuickBoardPresets(temp_docs_dir):
    test_html = temp_docs_dir / "test.html"
    test_html.write_text("""
      function syncActiveQuickBoardPresets(root = document) {
        const locationKeys = new Set(
          Array.from(root.querySelectorAll('form[data-front-advanced-form="true"]'))
            .map((form) => form instanceof HTMLFormElement ? String(form.dataset.frontLocationKey || '').trim() : '')
            .filter(Boolean)
        );
        for (const locationKey of locationKeys) {
          syncBoardPreset(root, locationKey, '', { force: false });
        }
      }
    """)

    optimize_dom_array_from.process_file(test_html)
    content = test_html.read_text()

    assert "Array.from" not in content
    assert "const forms = root.querySelectorAll('form[data-front-advanced-form=\"true\"]');" in content
    assert "const locationKeys = new Set();" in content
    assert "if (val) locationKeys.add(val);" in content
