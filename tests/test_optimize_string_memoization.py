from optimize_string_memoization import (
    RE_NORMALIZE_SOURCE,
    RE_NORMALIZE_SOURCE_REPLACEMENT,
    RE_CANONICAL_LANGUAGE,
    RE_CANONICAL_LANGUAGE_REPLACEMENT,
    RE_CANONICAL_FORMAT,
    RE_CANONICAL_FORMAT_REPLACEMENT,
    RE_FOLD_TEXT,
    RE_FOLD_TEXT_REPLACEMENT,
    ESCAPE_HTML_ORIG,
    ESCAPE_HTML_NEW,
    FOLD_TEXT_ORIG_2,
    FOLD_TEXT_NEW_2,
    CANONICAL_LANGUAGE_ORIG_2,
    CANONICAL_LANGUAGE_NEW_2,
    CANONICAL_FORMAT_ORIG_2,
    CANONICAL_FORMAT_NEW_2
)

def test_normalize_source_replacement():
    original = r"function normalizeSource(value) { return String(value ?? '').replace(/\s+/g, ' ').trim(); }"
    result = RE_NORMALIZE_SOURCE.sub(lambda m: RE_NORMALIZE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_normalizeSourceCache.set" in result
    assert r"const result = strValue.replace(/\s+/g, ' ').trim();" in result
    assert "if (_normalizeSourceCache.size > 2000) _normalizeSourceCache.clear();" in result

def test_canonical_language_replacement():
    original = r"function canonicalLanguage(language) { return normalizeSource(language).toLowerCase(); }"
    result = RE_CANONICAL_LANGUAGE.sub(lambda m: RE_CANONICAL_LANGUAGE_REPLACEMENT, original)
    assert "_canonicalLanguageCache.set" in result
    assert "const result = normalizeSource(strLanguage).toLowerCase();" in result
    assert "if (_canonicalLanguageCache.size > 2000) _canonicalLanguageCache.clear();" in result

def test_canonical_format_replacement():
    original = r"function canonicalFormat(format) { const normalized = normalizeSource(format).toLowerCase(); return normalized === '2d' || normalized === '3d' ? normalized : '2d'; }"
    result = RE_CANONICAL_FORMAT.sub(lambda m: RE_CANONICAL_FORMAT_REPLACEMENT, original)
    assert "_canonicalFormatCache.set" in result
    assert "normalized === '2d' || normalized === '3d' ? normalized : '2d';" in result
    assert "if (_canonicalFormatCache.size > 2000) _canonicalFormatCache.clear();" in result

def test_fold_text_replacement():
    original = r"function foldText(text) { return normalizeSource(text).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }"
    result = RE_FOLD_TEXT.sub(lambda m: RE_FOLD_TEXT_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_foldTextCache.set" in result
    assert r"replace(/[\u0300-\u036f]/g, '');" in result
    assert "if (_foldTextCache.size > 2000) _foldTextCache.clear();" in result

def test_new_replacements_exact_match():
    # Make sure our source strings match the new output properly
    assert "if (_escapeHtmlCache.size > 2000) _escapeHtmlCache.clear();" in ESCAPE_HTML_NEW
    assert "if (_foldTextCache.size > 2000) _foldTextCache.clear();" in FOLD_TEXT_NEW_2
    assert "if (_canonicalLanguageCache.size > 2000) _canonicalLanguageCache.clear();" in CANONICAL_LANGUAGE_NEW_2
    assert "if (_canonicalFormatCache.size > 2000) _canonicalFormatCache.clear();" in CANONICAL_FORMAT_NEW_2
