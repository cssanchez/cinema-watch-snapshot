import pytest
from pathlib import Path
import fix_zone_dropdown

def test_fix_zone_dropdown_no_storage_key(tmp_path):
    file_path = tmp_path / "index.html"
    file_path.write_text("<div>No storage key here</div>", encoding="utf-8")

    assert fix_zone_dropdown.fix_zone_dropdown(file_path) is False
    assert file_path.read_text(encoding="utf-8") == "<div>No storage key here</div>"

def test_fix_zone_dropdown_with_storage_key_no_match(tmp_path):
    file_path = tmp_path / "index.html"
    content = "const storageKey = 'cinema-watch-location';\nconsole.log('different script');"
    file_path.write_text(content, encoding="utf-8")

    assert fix_zone_dropdown.fix_zone_dropdown(file_path) is False
    assert file_path.read_text(encoding="utf-8") == content

def test_fix_zone_dropdown_successful_patch(tmp_path):
    file_path = tmp_path / "index.html"
    old_script = """const storageKey = 'cinema-watch-location';
function oldInit() {}
window.CinemaWatchLocations = { init: initHomepageLocation };
"""
    content = f"<html><body><script>{old_script}</script></body></html>"
    file_path.write_text(content, encoding="utf-8")

    assert fix_zone_dropdown.fix_zone_dropdown(file_path) is True
    new_content = file_path.read_text(encoding="utf-8")
    assert old_script not in new_content
    assert fix_zone_dropdown.NEW_SCRIPT in new_content

def test_find_html_files(tmp_path, monkeypatch):
    monkeypatch.setattr(fix_zone_dropdown, "DOCS_ROOT", tmp_path)

    # Create some dummy files
    (tmp_path / "index.html").touch()
    d1 = tmp_path / "dir1"
    d1.mkdir()
    (d1 / "index.html").touch()
    (d1 / "other.html").touch()
    d2 = tmp_path / "dir2"
    d2.mkdir()
    (d2 / "index.html").touch()

    expected = sorted([
        tmp_path / "index.html",
        d1 / "index.html",
        d2 / "index.html"
    ])

    result = fix_zone_dropdown.find_html_files()
    assert result == expected
