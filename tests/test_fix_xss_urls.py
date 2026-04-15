import os
from pathlib import Path
from fix_xss_urls import process_file

def test_injects_sanitize_url(tmp_path):
    html_content = """
    <script>
      function mapStaticRows(rows) {
        return (Array.isArray(rows) ? rows : []).map((row) => ({
          movie_href: String(row.movie_href || ''),
          venue_href: String(row.venue_href || ''),
          provider: String(row.provider || '')
        }));
      }

      function mapApiRows(rows) {
        return (Array.isArray(rows) ? rows : []).map((row) => ({
          movie_href: String(row.movie_href || ''),
          venue_href: String(row.venue_href || (row.provider && row.venue_key ? `/venues/${row.provider}/${row.venue_key}` : '')),
          provider: String(row.provider || '')
        }));
      }
    </script>
    """

    test_file = tmp_path / "test.html"
    test_file.write_text(html_content, encoding="utf-8")

    # Run the processor
    assert process_file(test_file) == True

    result = test_file.read_text(encoding="utf-8")

    # Check that the sanitizer function was injected
    assert "function sanitizeUrl(url) {" in result
    assert "if (lower.startsWith('javascript:')" in result

    # Check that mapStaticRows uses the sanitizer
    assert "movie_href: sanitizeUrl(row.movie_href)," in result
    assert "venue_href: sanitizeUrl(row.venue_href)," in result

    # Check that mapApiRows uses the sanitizer
    assert "venue_href: sanitizeUrl(row.venue_href || (row.provider && row.venue_key ? `/venues/${row.provider}/${row.venue_key}` : ''))," in result

    # Processing again shouldn't modify the file
    assert process_file(test_file) == False
