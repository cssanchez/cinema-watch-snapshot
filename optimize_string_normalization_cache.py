#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

RE_FOLD_TEXT = re.compile(
    r"function foldText\(value\)\s*\{\s*return String\(value \?\? ''\)\s*\.normalize\('NFD'\)\s*\.replace\(/\[\\u0300-\\u036f\]/g, ''\)\s*\.toLowerCase\(\)\s*\.trim\(\);\s*\}",
    re.MULTILINE
)
RE_FOLD_TEXT_REPLACEMENT = (
    "const _foldTextCache = new Map();\n"
    "      // Memoize foldText to avoid redundant NFD normalization overhead in client-side filtering\n"
    "      function foldText(value) {\n"
    "        if (_foldTextCache.size > 2000) _foldTextCache.clear();\n"
    "        const strValue = String(value ?? '');\n"
    "        if (_foldTextCache.has(strValue)) return _foldTextCache.get(strValue);\n"
    "        const result = strValue.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase().trim();\n"
    "        _foldTextCache.set(strValue, result);\n"
    "        return result;\n"
    "      }"
)

RE_CANONICAL_LANGUAGE = re.compile(
    r"function canonicalLanguage\(value\)\s*\{\s*const text = foldText\(value\);\s*if \(!text\) return '';\s*if \(text\.includes\('subti'\)\) return 'subtitulado';\s*if \(\['espanol', 'español', 'castellano', 'doblada'\]\.includes\(text\)\) return 'espanol';\s*return text;\s*\}",
    re.MULTILINE
)
RE_CANONICAL_LANGUAGE_REPLACEMENT = (
    "const _canonicalLanguageCache = new Map();\n"
    "      // Memoize canonicalLanguage to prevent redundant O(N) evaluations in client-side loops\n"
    "      function canonicalLanguage(value) {\n"
    "        if (_canonicalLanguageCache.size > 2000) _canonicalLanguageCache.clear();\n"
    "        const strValue = String(value ?? '');\n"
    "        if (_canonicalLanguageCache.has(strValue)) return _canonicalLanguageCache.get(strValue);\n"
    "        const text = foldText(strValue);\n"
    "        let result = text;\n"
    "        if (!text) result = '';\n"
    "        else if (text.includes('subti')) result = 'subtitulado';\n"
    "        else if (['espanol', 'español', 'castellano', 'doblada'].includes(text)) result = 'espanol';\n"
    "        _canonicalLanguageCache.set(strValue, result);\n"
    "        return result;\n"
    "      }"
)

RE_CANONICAL_FORMAT = re.compile(
    r"function canonicalFormat\(value\)\s*\{\s*return foldText\(value\)\.replace\(/\\s\+/g, ''\);\s*\}",
    re.MULTILINE
)
RE_CANONICAL_FORMAT_REPLACEMENT = (
    "const _canonicalFormatCache = new Map();\n"
    "      // Memoize canonicalFormat to prevent redundant O(N) regex evaluation\n"
    "      function canonicalFormat(value) {\n"
    "        if (_canonicalFormatCache.size > 2000) _canonicalFormatCache.clear();\n"
    "        const strValue = String(value ?? '');\n"
    "        if (_canonicalFormatCache.has(strValue)) return _canonicalFormatCache.get(strValue);\n"
    "        const result = foldText(strValue).replace(/\\s+/g, '');\n"
    "        _canonicalFormatCache.set(strValue, result);\n"
    "        return result;\n"
    "      }"
)

RE_SPLIT_LISTING_TOKENS = re.compile(
    r"function splitListingTokens\(value\)\s*\{\s*const text = String\(value \|\| ''\)\.trim\(\);\s*if \(!text\) return \[\];\s*const normalized = text\s*\.replaceAll\('•', '\|'\)\s*\.replaceAll\('·', '\|'\)\s*\.replaceAll\('/', '\|'\)\s*\.replaceAll\(' - ', '\|'\);\s*return normalized\s*\.split\('\|'\)\s*\.map\(\(part\) => part\.trim\(\)\.replace\(/\\s\+/g, ' '\)\)\s*\.filter\(Boolean\);\s*\}",
    re.MULTILINE
)
RE_SPLIT_LISTING_TOKENS_REPLACEMENT = (
    "const _splitListingTokensCache = new Map();\n"
    "      // Memoize splitListingTokens to avoid redundant string splitting and formatting across identical tokens\n"
    "      function splitListingTokens(value) {\n"
    "        if (_splitListingTokensCache.size > 2000) _splitListingTokensCache.clear();\n"
    "        const strValue = String(value || '').trim();\n"
    "        if (!strValue) return [];\n"
    "        if (_splitListingTokensCache.has(strValue)) return [..._splitListingTokensCache.get(strValue)];\n"
    "        const normalized = strValue.replaceAll('•', '|').replaceAll('·', '|').replaceAll('/', '|').replaceAll(' - ', '|');\n"
    "        const result = normalized.split('|').map((part) => part.trim().replace(/\\s+/g, ' ')).filter(Boolean);\n"
    "        _splitListingTokensCache.set(strValue, result);\n"
    "        return [...result];\n"
    "      }"
)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    content = RE_FOLD_TEXT.sub(lambda m: RE_FOLD_TEXT_REPLACEMENT, content)
    content = RE_CANONICAL_LANGUAGE.sub(lambda m: RE_CANONICAL_LANGUAGE_REPLACEMENT, content)
    content = RE_CANONICAL_FORMAT.sub(lambda m: RE_CANONICAL_FORMAT_REPLACEMENT, content)
    content = RE_SPLIT_LISTING_TOKENS.sub(lambda m: RE_SPLIT_LISTING_TOKENS_REPLACEMENT, content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = list(DOCS_ROOT.rglob('*.html'))
    processed_count = 0
    for file_path in files:
        if process_file(file_path):
            processed_count += 1
            print(f"Patched: {file_path.relative_to(DOCS_ROOT)}")

    print(f"\\nDone! Patched {processed_count} files out of {len(files)} total HTML files.")

if __name__ == '__main__':
    main()
