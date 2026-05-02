import pytest
from pathlib import Path
import fix_security_xss

def test_process_file_no_match(tmp_path):
    file_path = tmp_path / "index.html"
    content = "<html><body>No changes needed</body></html>"
    file_path.write_text(content, encoding="utf-8")

    assert fix_security_xss.process_file(file_path) is False
    assert file_path.read_text(encoding="utf-8") == content

def test_process_file_movie_href(tmp_path):
    file_path = tmp_path / "index.html"
    content = "<div>{escapeHtml(item.movie_href)}</div>"
    file_path.write_text(content, encoding="utf-8")

    assert fix_security_xss.process_file(file_path) is True
    new_content = file_path.read_text(encoding="utf-8")
    assert "escapeHtml(sanitizeUrl(item.movie_href))" in new_content
    # Since we didn't have const _escapeHtmlCache =, sanitizeUrl definition wasn't injected yet in this test case
    # but the usage was updated.

def test_process_file_venue_href(tmp_path):
    file_path = tmp_path / "index.html"
    content = "<div>{escapeHtml(item.venue_href)}</div>"
    file_path.write_text(content, encoding="utf-8")

    assert fix_security_xss.process_file(file_path) is True
    new_content = file_path.read_text(encoding="utf-8")
    assert "escapeHtml(sanitizeUrl(item.venue_href))" in new_content

def test_process_file_inject_definition(tmp_path):
    file_path = tmp_path / "index.html"
    content = "const _escapeHtmlCache = new Map();"
    file_path.write_text(content, encoding="utf-8")

    assert fix_security_xss.process_file(file_path) is True
    new_content = file_path.read_text(encoding="utf-8")
    assert "function sanitizeUrl(url)" in new_content
    assert "const _escapeHtmlCache =" in new_content

def test_process_file_idempotency(tmp_path):
    file_path = tmp_path / "index.html"
    content = "const _escapeHtmlCache = new Map();"
    file_path.write_text(content, encoding="utf-8")

    # First run
    assert fix_security_xss.process_file(file_path) is True
    first_run_content = file_path.read_text(encoding="utf-8")

    # Second run
    assert fix_security_xss.process_file(file_path) is False
    assert file_path.read_text(encoding="utf-8") == first_run_content

def test_process_file_full_patch(tmp_path):
    file_path = tmp_path / "index.html"
    content = """
    <script>
    const _escapeHtmlCache = new Map();
    function render() {
        return `<div>${escapeHtml(item.movie_href)}</div><div>${escapeHtml(item.venue_href)}</div>`;
    }
    </script>
    """
    file_path.write_text(content, encoding="utf-8")

    assert fix_security_xss.process_file(file_path) is True
    new_content = file_path.read_text(encoding="utf-8")

    assert "function sanitizeUrl(url)" in new_content
    assert "escapeHtml(sanitizeUrl(item.movie_href))" in new_content
    assert "escapeHtml(sanitizeUrl(item.venue_href))" in new_content
    assert "const _escapeHtmlCache =" in new_content
