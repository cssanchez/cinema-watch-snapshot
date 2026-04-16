#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_ROOT = Path(__file__).parent / 'docs'

# Define regex patterns globally, precompiled to prevent recompiling overhead in loops
# Note: we update the replacements to include the size constraint as per requirements.
RE_NORMALIZE_SOURCE = re.compile(
    r"function normalizeSource\(value\)\s*\{\s*return String\(value \?\? ''\)\.replace\(/\\s\+/g, ' '\)\.trim\(\);\s*\}",
    re.MULTILINE
)
RE_NORMALIZE_SOURCE_REPLACEMENT = """const _normalizeSourceCache = new Map();
      function normalizeSource(value) {
        const strValue = String(value ?? '');
        if (_normalizeSourceCache.has(strValue)) return _normalizeSourceCache.get(strValue);
        const result = strValue.replace(/\\\\s+/g, ' ').trim();
        if (_normalizeSourceCache.size > 2000) _normalizeSourceCache.clear();
        _normalizeSourceCache.set(strValue, result);
        return result;
      }"""

RE_CANONICAL_LANGUAGE = re.compile(
    r"function canonicalLanguage\(language\)\s*\{\s*return normalizeSource\(language\)\.toLowerCase\(\);\s*\}",
    re.MULTILINE
)
RE_CANONICAL_LANGUAGE_REPLACEMENT = """const _canonicalLanguageCache = new Map();
      function canonicalLanguage(language) {
        const strLanguage = String(language ?? '');
        if (_canonicalLanguageCache.has(strLanguage)) return _canonicalLanguageCache.get(strLanguage);
        const result = normalizeSource(strLanguage).toLowerCase();
        if (_canonicalLanguageCache.size > 2000) _canonicalLanguageCache.clear();
        _canonicalLanguageCache.set(strLanguage, result);
        return result;
      }"""

RE_CANONICAL_FORMAT = re.compile(
    r"function canonicalFormat\(format\)\s*\{\s*const normalized = normalizeSource\(format\)\.toLowerCase\(\);\s*return\s*normalized === '2d' \|\| normalized === '3d'\s*\? normalized\s*: '2d';\s*\}",
    re.MULTILINE
)
RE_CANONICAL_FORMAT_REPLACEMENT = """const _canonicalFormatCache = new Map();
      function canonicalFormat(format) {
        const strFormat = String(format ?? '');
        if (_canonicalFormatCache.has(strFormat)) return _canonicalFormatCache.get(strFormat);
        const normalized = normalizeSource(strFormat).toLowerCase();
        const result = normalized === '2d' || normalized === '3d' ? normalized : '2d';
        if (_canonicalFormatCache.size > 2000) _canonicalFormatCache.clear();
        _canonicalFormatCache.set(strFormat, result);
        return result;
      }"""

RE_FOLD_TEXT = re.compile(
    r"function foldText\(text\)\s*\{\s*return normalizeSource\(text\)\s*\.toLowerCase\(\)\s*\.normalize\('NFD'\)\s*\.replace\(/\[\\u0300-\\u036f\]/g, ''\);\s*\}",
    re.MULTILINE
)
RE_FOLD_TEXT_REPLACEMENT = """const _foldTextCache = new Map();
      function foldText(text) {
        const strText = String(text ?? '');
        if (_foldTextCache.has(strText)) return _foldTextCache.get(strText);
        const result = normalizeSource(strText)
          .toLowerCase()
          .normalize('NFD')
          .replace(/[\\\\u0300-\\\\u036f]/g, '');
        if (_foldTextCache.size > 2000) _foldTextCache.clear();
        _foldTextCache.set(strText, result);
        return result;
      }"""

# Below are exact string replacements for the specific functions that actually exist in docs/index.html etc

ESCAPE_HTML_ORIG = """      function escapeHtml(value) {
        return String(value ?? '')
          .replaceAll('&', '&amp;')
          .replaceAll('<', '&lt;')
          .replaceAll('>', '&gt;')
          .replaceAll('"', '&quot;')
          .replaceAll("'", '&#39;');
      }"""

ESCAPE_HTML_NEW = """const _escapeHtmlCache = new Map();
      function escapeHtml(value) {
        const strValue = String(value ?? '');
        if (_escapeHtmlCache.has(strValue)) return _escapeHtmlCache.get(strValue);
        const result = strValue
          .replaceAll('&', '&amp;')
          .replaceAll('<', '&lt;')
          .replaceAll('>', '&gt;')
          .replaceAll('"', '&quot;')
          .replaceAll("'", '&#39;');
        if (_escapeHtmlCache.size > 2000) _escapeHtmlCache.clear();
        _escapeHtmlCache.set(strValue, result);
        return result;
      }"""

FOLD_TEXT_ORIG_2 = """      function foldText(value) {
        return String(value ?? '')
          .normalize('NFD')
          .replace(/[\\u0300-\\u036f]/g, '')
          .toLowerCase()
          .trim();
      }"""

FOLD_TEXT_NEW_2 = """const _foldTextCache = new Map();
      function foldText(value) {
        const strValue = String(value ?? '');
        if (_foldTextCache.has(strValue)) return _foldTextCache.get(strValue);
        const result = strValue
          .normalize('NFD')
          .replace(/[\\u0300-\\u036f]/g, '')
          .toLowerCase()
          .trim();
        if (_foldTextCache.size > 2000) _foldTextCache.clear();
        _foldTextCache.set(strValue, result);
        return result;
      }"""

CANONICAL_LANGUAGE_ORIG_2 = """      function canonicalLanguage(value) {
        const text = foldText(value);
        if (!text) return '';
        if (text.includes('subti')) return 'subtitulado';
        if (['espanol', 'español', 'castellano', 'doblada'].includes(text)) return 'espanol';
        return text;
      }"""

CANONICAL_LANGUAGE_NEW_2 = """const _canonicalLanguageCache = new Map();
      function canonicalLanguage(value) {
        const strValue = String(value ?? '');
        if (_canonicalLanguageCache.has(strValue)) return _canonicalLanguageCache.get(strValue);
        const text = foldText(strValue);
        let result = text;
        if (!text) result = '';
        else if (text.includes('subti')) result = 'subtitulado';
        else if (['espanol', 'español', 'castellano', 'doblada'].includes(text)) result = 'espanol';
        if (_canonicalLanguageCache.size > 2000) _canonicalLanguageCache.clear();
        _canonicalLanguageCache.set(strValue, result);
        return result;
      }"""

CANONICAL_FORMAT_ORIG_2 = """      function canonicalFormat(value) {
        return foldText(value).replace(/\\s+/g, '');
      }"""



BUILD_ROW_DETAIL_TOKENS_ORIG_2 = """      function buildRowDetailTokens(row) {
        const provider = String(row?.provider || '').trim();
        const providerName = String(row?.provider_name || '').trim();
        const venueName = String(row?.venue_name || '').trim();
        const venueLabel = venueShortLabel(provider, venueName);
        const listingTokens = splitListingTokens(row?.listing_label || '');
        const experience = String(row?.experience || '').trim();
        const formatLabel = String(row?.format_label || '').trim();
        const language = String(row?.language || '').trim();

        const venueFolded = foldText(venueName);
        const venueLabelFolded = foldText(venueLabel);
        const experienceFolded = canonicalFormat(experience);
        const formatFolded = canonicalFormat(formatLabel);
        const languageFolded = canonicalLanguage(language);
        const blockedExact = new Set([
          foldText(provider),
          foldText(providerName),
          venueFolded,
          venueLabelFolded,
          experienceFolded,
          formatFolded,
          languageFolded,
        ].filter(Boolean));
        const blockedContains = [venueFolded, venueLabelFolded].filter(Boolean);

        const detailTokens = [];
        const seen = new Set();

        const appendToken = (value) => {
          const cleaned = String(value || '').trim().replace(/\\s+/g, ' ');
          const folded = foldText(cleaned);
          if (!cleaned || !folded || seen.has(folded)) return;
          detailTokens.push(cleaned);
          seen.add(folded);
        };

        if (experience) {
          if (!venueFolded || !venueFolded.includes(experienceFolded)) {
            appendToken(experience);
          }
        }
        if (formatLabel && canonicalFormat(formatLabel) !== canonicalFormat(experience)) {
          appendToken(formatLabel);
        }
        if (language) {
          appendToken(language);
        }

        for (const token of listingTokens) {
          const folded = foldText(token);
          if (!folded || blockedExact.has(folded)) continue;
          if (folded.length >= 4 && blockedContains.some((candidate) => candidate.includes(folded))) continue;
          appendToken(token);
        }

        return detailTokens;
      }"""

BUILD_ROW_DETAIL_TOKENS_NEW_2 = """// ⚡ Bolt Optimization: Memoize buildRowDetailTokens to avoid redundant string allocations and sets creation for recurring rows.
const _buildRowDetailTokensCache = new Map();
      function buildRowDetailTokens(row) {
        // Use a composite key representing the row identity to cache tokens
        const key = [
          row?.provider || '',
          row?.provider_name || '',
          row?.venue_name || '',
          row?.listing_label || '',
          row?.experience || '',
          row?.format_label || '',
          row?.language || ''
        ].join('|');

        if (_buildRowDetailTokensCache.has(key)) {
            return [..._buildRowDetailTokensCache.get(key)];
        }

        const provider = String(row?.provider || '').trim();
        const providerName = String(row?.provider_name || '').trim();
        const venueName = String(row?.venue_name || '').trim();
        const venueLabel = venueShortLabel(provider, venueName);
        const listingTokens = splitListingTokens(row?.listing_label || '');
        const experience = String(row?.experience || '').trim();
        const formatLabel = String(row?.format_label || '').trim();
        const language = String(row?.language || '').trim();

        const venueFolded = foldText(venueName);
        const venueLabelFolded = foldText(venueLabel);
        const experienceFolded = canonicalFormat(experience);
        const formatFolded = canonicalFormat(formatLabel);
        const languageFolded = canonicalLanguage(language);
        const blockedExact = new Set([
          foldText(provider),
          foldText(providerName),
          venueFolded,
          venueLabelFolded,
          experienceFolded,
          formatFolded,
          languageFolded,
        ].filter(Boolean));
        const blockedContains = [venueFolded, venueLabelFolded].filter(Boolean);

        const detailTokens = [];
        const seen = new Set();

        const appendToken = (value) => {
          const cleaned = String(value || '').trim().replace(/\\s+/g, ' ');
          const folded = foldText(cleaned);
          if (!cleaned || !folded || seen.has(folded)) return;
          detailTokens.push(cleaned);
          seen.add(folded);
        };

        if (experience) {
          if (!venueFolded || !venueFolded.includes(experienceFolded)) {
            appendToken(experience);
          }
        }
        if (formatLabel && canonicalFormat(formatLabel) !== canonicalFormat(experience)) {
          appendToken(formatLabel);
        }
        if (language) {
          appendToken(language);
        }

        for (const token of listingTokens) {
          const folded = foldText(token);
          if (!folded || blockedExact.has(folded)) continue;
          if (folded.length >= 4 && blockedContains.some((candidate) => candidate.includes(folded))) continue;
          appendToken(token);
        }

        if (_buildRowDetailTokensCache.size > 2000) _buildRowDetailTokensCache.clear();
        _buildRowDetailTokensCache.set(key, detailTokens);
        return [...detailTokens];
      }"""
CANONICAL_FORMAT_NEW_2 = """const _canonicalFormatCache = new Map();
      function canonicalFormat(value) {
        const strValue = String(value ?? '');
        if (_canonicalFormatCache.has(strValue)) return _canonicalFormatCache.get(strValue);
        const result = foldText(strValue).replace(/\\s+/g, '');
        if (_canonicalFormatCache.size > 2000) _canonicalFormatCache.clear();
        _canonicalFormatCache.set(strValue, result);
        return result;
      }"""


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Legacy regexes
    content = RE_NORMALIZE_SOURCE.sub(lambda m: RE_NORMALIZE_SOURCE_REPLACEMENT.replace('\\\\', '\\'), content)
    content = RE_CANONICAL_LANGUAGE.sub(lambda m: RE_CANONICAL_LANGUAGE_REPLACEMENT, content)
    content = RE_CANONICAL_FORMAT.sub(lambda m: RE_CANONICAL_FORMAT_REPLACEMENT, content)
    content = RE_FOLD_TEXT.sub(lambda m: RE_FOLD_TEXT_REPLACEMENT.replace('\\\\', '\\'), content)

    # New direct replacements
    content = content.replace(ESCAPE_HTML_ORIG, ESCAPE_HTML_NEW)
    content = content.replace(FOLD_TEXT_ORIG_2, FOLD_TEXT_NEW_2)
    content = content.replace(CANONICAL_LANGUAGE_ORIG_2, CANONICAL_LANGUAGE_NEW_2)
    content = content.replace(CANONICAL_FORMAT_ORIG_2, CANONICAL_FORMAT_NEW_2)
    content = content.replace(BUILD_ROW_DETAIL_TOKENS_ORIG_2, BUILD_ROW_DETAIL_TOKENS_NEW_2)

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
