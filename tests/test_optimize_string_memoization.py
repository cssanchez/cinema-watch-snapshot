from optimize_string_memoization import (
    RE_NORMALIZE_SOURCE,
    RE_NORMALIZE_SOURCE_REPLACEMENT,
    RE_CANONICAL_LANGUAGE,
    RE_CANONICAL_LANGUAGE_REPLACEMENT,
    RE_CANONICAL_FORMAT,
    RE_CANONICAL_FORMAT_REPLACEMENT,
    RE_FOLD_TEXT,
    RE_FOLD_TEXT_REPLACEMENT
)

def test_normalize_source_replacement():
    original = r"function normalizeSource(value) { return String(value ?? '').replace(/\s+/g, ' ').trim(); }"
    result = RE_NORMALIZE_SOURCE.sub(lambda m: RE_NORMALIZE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_normalizeSourceCache.set" in result
    assert r"const result = strValue.replace(/\s+/g, ' ').trim();" in result

def test_canonical_language_replacement():
    original = r"function canonicalLanguage(language) { return normalizeSource(language).toLowerCase(); }"
    result = RE_CANONICAL_LANGUAGE.sub(lambda m: RE_CANONICAL_LANGUAGE_REPLACEMENT, original)
    assert "_canonicalLanguageCache.set" in result
    assert "const result = normalizeSource(strLanguage).toLowerCase();" in result

def test_canonical_format_replacement():
    original = r"function canonicalFormat(format) { const normalized = normalizeSource(format).toLowerCase(); return normalized === '2d' || normalized === '3d' ? normalized : '2d'; }"
    result = RE_CANONICAL_FORMAT.sub(lambda m: RE_CANONICAL_FORMAT_REPLACEMENT, original)
    assert "_canonicalFormatCache.set" in result
    assert "normalized === '2d' || normalized === '3d' ? normalized : '2d';" in result

def test_fold_text_replacement():
    original = r"function foldText(text) { return normalizeSource(text).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }"
    result = RE_FOLD_TEXT.sub(lambda m: RE_FOLD_TEXT_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_foldTextCache.set" in result
    assert r"replace(/[\u0300-\u036f]/g, '');" in result
