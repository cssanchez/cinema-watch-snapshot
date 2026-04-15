import pytest
from pathlib import Path
import re
from optimize_split_listing_tokens import process_file

def test_optimize_split_listing_tokens(tmp_path):
    docs_dir = tmp_path / 'docs'
    docs_dir.mkdir()

    html_file = docs_dir / 'index.html'

    html_content = """      function splitListingTokens(value) {
        const text = String(value || '').trim();
        if (!text) return [];
        const normalized = text
          .replaceAll('•', '|')
          .replaceAll('·', '|')
          .replaceAll('/', '|')
          .replaceAll(' - ', '|');
        return normalized
          .split('|')
          .map((part) => part.trim().replace(/\\s+/g, ' '))
          .filter(Boolean);
      }"""

    html_file.write_text(html_content, encoding='utf-8')

    assert process_file(html_file) == True

    result = html_file.read_text(encoding='utf-8')
    assert "const _splitListingTokensCache = new Map();" in result
    assert "if (_splitListingTokensCache.has(text)) return [..._splitListingTokensCache.get(text)];" in result
    assert "if (_splitListingTokensCache.size > 2000) _splitListingTokensCache.clear();" in result
    assert "_splitListingTokensCache.set(text, result);" in result
