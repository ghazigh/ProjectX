"""Prompts and the response schema for the article pipeline.

The system prompt is the stable, reusable instruction set — it carries a
cache_control breakpoint so that, once it (or a longer house-style guide
appended to it) crosses the model's minimum cacheable size, repeated runs
reuse it at ~0.1x input cost. The per-article brief is volatile and goes in
the user turn, after the cached prefix.
"""

SYSTEM_PROMPT = """\
You are a senior SEO content writer and editor. You produce publish-ready, \
genuinely useful long-form articles that rank — without resorting to keyword \
stuffing, filler, or AI boilerplate.

Operating principles:
- Write for the reader first, the search engine second. Follow Google's \
helpful-content guidance and E-E-A-T (experience, expertise, authoritativeness, \
trustworthiness). Content that only exists to rank gets demoted.
- Use the primary keyword naturally: in the title, the first ~100 words, at \
least one H2, the meta description, and the slug. Aim for a natural density \
(roughly 0.5%-1.5%) — never force it. Weave secondary keywords in where they \
genuinely fit.
- Structure for scannability: a compelling intro that states the value, \
descriptive H2/H3 subheadings, short paragraphs, bullet/numbered lists where \
they help, and a clear conclusion. Use markdown (## and ###) for headings.
- Be concrete and specific. Prefer examples, steps, numbers, and definitions \
over vague claims. Do not invent statistics, studies, prices, or quotes — if a \
specific figure would strengthen a point, describe what to cite and mark it so \
the client can verify and insert a real source.
- Match the requested tone, audience, and word count. Calibrate depth to the \
topic; do not pad to hit a number.
- Suggest internal links (as descriptive anchor-text ideas the client maps to \
their own pages) and a few authoritative external link targets (by type/name, \
not fabricated URLs).
- Write a concise FAQ section targeting real long-tail questions a reader would \
search, suitable for FAQ schema.

You always return your output strictly as JSON matching the provided schema. \
Do not include commentary outside the JSON.\
"""

# Flat JSON schema (no recursion, additionalProperties:false on every object,
# every property required) per structured-output constraints.
ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "SEO title tag, ideally <= 60 characters, includes the primary keyword.",
        },
        "meta_description": {
            "type": "string",
            "description": "Meta description, ideally 140-155 characters, includes the primary keyword and a hook.",
        },
        "slug": {
            "type": "string",
            "description": "URL slug, lowercase, hyphen-separated, includes the primary keyword.",
        },
        "primary_keyword": {"type": "string"},
        "secondary_keywords": {
            "type": "array",
            "items": {"type": "string"},
        },
        "article_markdown": {
            "type": "string",
            "description": "Full article body in markdown. Use ## and ### for headings. Do NOT repeat the H1 title here.",
        },
        "faqs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                },
                "required": ["question", "answer"],
                "additionalProperties": False,
            },
        },
        "internal_link_ideas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Descriptive anchor-text ideas for links to the client's own related pages.",
        },
        "external_link_ideas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Types or names of authoritative sources worth citing (not fabricated URLs).",
        },
        "image_alt_suggestions": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "title",
        "meta_description",
        "slug",
        "primary_keyword",
        "secondary_keywords",
        "article_markdown",
        "faqs",
        "internal_link_ideas",
        "external_link_ideas",
        "image_alt_suggestions",
    ],
    "additionalProperties": False,
}


def build_brief(*, topic, primary_keyword, secondary_keywords, word_count, tone, audience, extra_notes):
    """Render the per-article brief sent as the user turn."""
    secondary = ", ".join(secondary_keywords) if secondary_keywords else "(none specified — choose 3-6 relevant ones)"
    notes = extra_notes.strip() if extra_notes else "(none)"
    return (
        f"Write an SEO article.\n\n"
        f"Topic: {topic}\n"
        f"Primary keyword: {primary_keyword}\n"
        f"Secondary keywords: {secondary}\n"
        f"Target word count: ~{word_count} words\n"
        f"Tone: {tone}\n"
        f"Target audience: {audience}\n"
        f"Additional notes: {notes}\n"
    )
