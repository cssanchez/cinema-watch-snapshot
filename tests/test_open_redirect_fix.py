import pytest
from pathlib import Path

def test_redirect_logic_is_secure():
    movies_index = Path("docs/movies/index.html")
    screenings_index = Path("docs/screenings/index.html")

    for path in [movies_index, screenings_index]:
        content = path.read_text(encoding="utf-8")

        # Check that URL API is used
        assert "new URL('/cinema-watch-snapshot/', window.location.origin)" in content
        assert "url.search = window.location.search" in content
        assert "window.location.replace(url.toString())" in content

        # Check that it doesn't use the vulnerable pattern anymore
        assert "const target = `/cinema-watch-snapshot/${query}#" not in content
        assert "window.location.replace(target);" not in content
