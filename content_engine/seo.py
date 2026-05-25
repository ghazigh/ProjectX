"""Lightweight on-page SEO analysis — runs locally, no API calls.

Gives each generated article a quick objective scorecard the client can see:
word count, keyword placement, density, readability, and structure checks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


_WORD_RE = re.compile(r"[A-Za-z0-9']+")
_SENTENCE_RE = re.compile(r"[.!?]+")


def _words(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def _count_syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def flesch_reading_ease(text: str) -> float:
    words = _words(text)
    sentences = [s for s in _SENTENCE_RE.split(text) if s.strip()]
    n_words = len(words)
    n_sentences = max(len(sentences), 1)
    n_syllables = sum(_count_syllables(w) for w in words)
    if n_words == 0:
        return 0.0
    score = 206.835 - 1.015 * (n_words / n_sentences) - 84.6 * (n_syllables / n_words)
    return round(score, 1)


def keyword_density(text: str, keyword: str) -> float:
    words = _words(text)
    if not words or not keyword.strip():
        return 0.0
    kw_words = _words(keyword)
    if not kw_words:
        return 0.0
    joined = " ".join(words)
    needle = " ".join(kw_words)
    occurrences = joined.count(needle)
    return round(100.0 * occurrences * len(kw_words) / len(words), 2)


@dataclass
class SeoReport:
    word_count: int
    heading_count: int
    reading_ease: float
    primary_density: float
    checks: list[tuple[str, bool]] = field(default_factory=list)

    @property
    def score(self) -> int:
        if not self.checks:
            return 0
        passed = sum(1 for _, ok in self.checks if ok)
        return round(100 * passed / len(self.checks))

    def render(self) -> str:
        lines = [
            "## SEO report",
            "",
            f"- Score: {self.score}/100",
            f"- Word count: {self.word_count}",
            f"- Headings (H2/H3): {self.heading_count}",
            f"- Flesch reading ease: {self.reading_ease} "
            f"({_ease_label(self.reading_ease)})",
            f"- Primary keyword density: {self.primary_density}%",
            "",
            "### Checks",
        ]
        for label, ok in self.checks:
            lines.append(f"- [{'x' if ok else ' '}] {label}")
        return "\n".join(lines)


def _ease_label(score: float) -> str:
    if score >= 70:
        return "easy"
    if score >= 50:
        return "moderate"
    return "hard — consider shorter sentences"


def analyze(*, title: str, meta_description: str, slug: str, primary_keyword: str, article_markdown: str) -> SeoReport:
    kw = primary_keyword.lower().strip()
    body_words = _words(article_markdown)
    headings = re.findall(r"^#{2,3}\s", article_markdown, flags=re.MULTILINE)
    first_chunk = " ".join(body_words[:100])

    density = keyword_density(article_markdown, primary_keyword)
    ease = flesch_reading_ease(article_markdown)

    checks = [
        ("Primary keyword in title", kw in title.lower()),
        ("Primary keyword in meta description", kw in meta_description.lower()),
        ("Primary keyword in slug", kw.replace(" ", "-") in slug.lower() or kw in slug.lower()),
        ("Primary keyword in first 100 words", kw in first_chunk),
        ("Title length <= 60 chars", len(title) <= 60),
        ("Meta description 120-160 chars", 120 <= len(meta_description) <= 160),
        ("At least 3 subheadings", len(headings) >= 3),
        ("Keyword density 0.3%-2.0% (not stuffed)", 0.3 <= density <= 2.0),
        ("Reading ease >= 50", ease >= 50),
        ("Body >= 600 words", len(body_words) >= 600),
    ]

    return SeoReport(
        word_count=len(body_words),
        heading_count=len(headings),
        reading_ease=ease,
        primary_density=density,
        checks=checks,
    )
