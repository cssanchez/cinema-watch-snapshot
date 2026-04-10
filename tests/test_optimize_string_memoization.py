from optimize_string_memoization import (
    RE_NORMALIZE_SOURCE,
    RE_NORMALIZE_SOURCE_REPLACEMENT,
    RE_CANONICAL_LANGUAGE,
    RE_CANONICAL_LANGUAGE_REPLACEMENT,
    RE_CANONICAL_FORMAT,
    RE_CANONICAL_FORMAT_REPLACEMENT,
    RE_FOLD_TEXT,
    RE_FOLD_TEXT_REPLACEMENT,
    RE_TRANSLATE_SOURCE,
    RE_TRANSLATE_SOURCE_REPLACEMENT
)

def test_normalize_source_replacement():
    original = r"function normalizeSource(value) { return String(value ?? '').replace(/\s+/g, ' ').trim(); }"
    result = RE_NORMALIZE_SOURCE.sub(lambda m: RE_NORMALIZE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_normalizeSourceCache.set" in result
    assert r"const result = strValue.replace(/\s+/g, ' ').trim();" in result

def test_canonical_language_replacement():
    original = r"function canonicalLanguage(value) { const text = foldText(value); if (!text) return ''; if (text.includes('subti')) return 'subtitulado'; if (['espanol', 'español', 'castellano', 'doblada'].includes(text)) return 'espanol'; return text; }"
    result = RE_CANONICAL_LANGUAGE.sub(lambda m: RE_CANONICAL_LANGUAGE_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_canonicalLanguageCache.set" in result

def test_canonical_format_replacement():
    original = r"function canonicalFormat(value) { return foldText(value).replace(/\s+/g, ''); }"
    result = RE_CANONICAL_FORMAT.sub(lambda m: RE_CANONICAL_FORMAT_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_canonicalFormatCache.set" in result

def test_fold_text_replacement():
    original = r"function foldText(value) { return String(value ?? '') .normalize('NFD') .replace(/[\u0300-\u036f]/g, '') .toLowerCase() .trim(); }"
    result = RE_FOLD_TEXT.sub(lambda m: RE_FOLD_TEXT_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_foldTextCache.set" in result

def test_translate_source_replacement():
    original = r"function translateSource(value, language = currentLanguage) { const key = normalizeSource(value); if (language === 'en') { return key; } return sourceTranslations[language]?.[key] || key; }"
    result = RE_TRANSLATE_SOURCE.sub(lambda m: RE_TRANSLATE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), original)
    assert "_translateSourceCache.set" in result
