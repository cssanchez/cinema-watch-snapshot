import pytest
from pathlib import Path
import fix_open_redirect

def test_fix_open_redirect(tmp_path):
    # Setup test file
    test_file = tmp_path / "test.html"
    original_content = """
      function navigateHomeHash(hash) {
        const homePath = getHomePath();
        const relativePath = relativePathFromHome(window.location.pathname || '/', homePath);
        if (relativePath === '/') {
          if (!hash) {
            setHomeAndScrollTop();
            return;
          }
          if (hash === '#peliculas') {
            setHomeAndScrollMovies();
            return;
          }
          if (hash === '#salas-especiales') {
            setHomeAndScrollSpecialRooms();
            return;
          }
          setHomeAndScrollCartelera();
          return;
        }
        const targetUrl = `${homePath}${hash || ''}`;
        if (window.CineVicioLiveNav?.load) {
          window.CineVicioLiveNav.load(targetUrl);
          return;
        }
        window.location.assign(targetUrl);
      }
"""
    test_file.write_text(original_content, encoding='utf-8')

    # Process file
    result = fix_open_redirect.process_file(test_file)

    assert result == True

    patched_content = test_file.read_text(encoding='utf-8')
    assert "let targetUrl;" in patched_content
    assert "try {" in patched_content
    assert "const parsedUrl = new URL(`${homePath}${hash || ''}`, window.location.origin);" in patched_content
    assert "if (parsedUrl.origin !== window.location.origin) throw new Error('Invalid origin');" in patched_content
    assert "const targetUrl = `${homePath}${hash || ''}`" not in patched_content

def test_fix_open_redirect_cartelera(tmp_path):
    test_file = tmp_path / "test2.html"
    original_content = """
          if (relativePath !== '/') {
            const targetUrl = `${homePath}#cartelera`;
            if (window.CineVicioLiveNav?.load) {
              window.CineVicioLiveNav.load(targetUrl);
            } else {
              window.location.assign(targetUrl);
            }
          }
"""
    test_file.write_text(original_content, encoding='utf-8')

    result = fix_open_redirect.process_file(test_file)
    assert result == True

    patched_content = test_file.read_text(encoding='utf-8')
    assert "let targetUrl;" in patched_content
    assert "try {" in patched_content
    assert "const parsedUrl = new URL(`${homePath}#cartelera`, window.location.origin);" in patched_content
    assert "if (parsedUrl.origin !== window.location.origin) throw new Error('Invalid origin');" in patched_content
    assert "const targetUrl = `${homePath}#cartelera`" not in patched_content
