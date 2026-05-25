"""Command-line entry point for the content/SEO engine.

Usage:
    python -m content_engine.cli "How to compost at home" \\
        --keyword "home composting" \\
        --secondary "compost bin,kitchen scraps" \\
        --words 1500 --tone "friendly, practical" \\
        --audience "beginner gardeners"
"""

from __future__ import annotations

import argparse
import os
import sys

import anthropic

from .pipeline import ArticleBrief, generate_article
from .seo import analyze


def _slugify_fallback(text: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "article"


def _render_markdown(data: dict, seo_report_md: str) -> str:
    parts = [
        "---",
        f'title: "{data["title"]}"',
        f'description: "{data["meta_description"]}"',
        f'slug: "{data["slug"]}"',
        f'primary_keyword: "{data["primary_keyword"]}"',
        f'secondary_keywords: {data["secondary_keywords"]}',
        "---",
        "",
        f"# {data['title']}",
        "",
        data["article_markdown"].strip(),
        "",
    ]

    if data.get("faqs"):
        parts.append("## Frequently asked questions")
        parts.append("")
        for faq in data["faqs"]:
            parts.append(f"### {faq['question']}")
            parts.append("")
            parts.append(faq["answer"])
            parts.append("")

    parts.append("---")
    parts.append("")
    parts.append("## Optimization notes (for the editor — remove before publishing)")
    parts.append("")
    parts.append("**Internal link ideas:**")
    for item in data.get("internal_link_ideas", []):
        parts.append(f"- {item}")
    parts.append("")
    parts.append("**External sources to cite (verify before inserting):**")
    for item in data.get("external_link_ideas", []):
        parts.append(f"- {item}")
    parts.append("")
    parts.append("**Image alt-text ideas:**")
    for item in data.get("image_alt_suggestions", []):
        parts.append(f"- {item}")
    parts.append("")
    parts.append(seo_report_md)
    parts.append("")
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an SEO-optimized article with Claude.")
    parser.add_argument("topic", help="The article topic / working title.")
    parser.add_argument("--keyword", "-k", required=True, help="Primary target keyword.")
    parser.add_argument("--secondary", "-s", default="", help="Comma-separated secondary keywords.")
    parser.add_argument("--words", "-w", type=int, default=1500, help="Target word count (default 1500).")
    parser.add_argument("--tone", "-t", default="clear, professional, helpful", help="Desired tone.")
    parser.add_argument("--audience", "-a", default="general readers researching the topic", help="Target audience.")
    parser.add_argument("--notes", "-n", default="", help="Extra instructions for this article.")
    parser.add_argument("--model", "-m", default=None, help="Override the model (default from env or opus-4-7).")
    parser.add_argument("--out-dir", "-o", default="output", help="Directory to write the article to.")
    args = parser.parse_args(argv)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key,", file=sys.stderr)
        print("then `export $(grep -v '^#' .env | xargs)` or use a tool like python-dotenv.", file=sys.stderr)
        return 1

    secondary = [s.strip() for s in args.secondary.split(",") if s.strip()]
    brief = ArticleBrief(
        topic=args.topic,
        primary_keyword=args.keyword,
        secondary_keywords=secondary,
        word_count=args.words,
        tone=args.tone,
        audience=args.audience,
        extra_notes=args.notes,
    )

    kwargs = {"model": args.model} if args.model else {}
    try:
        result = generate_article(brief, **kwargs)
    except anthropic.AuthenticationError:
        print("Error: invalid ANTHROPIC_API_KEY.", file=sys.stderr)
        return 1
    except anthropic.APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        return 1

    data = result.data
    report = analyze(
        title=data["title"],
        meta_description=data["meta_description"],
        slug=data["slug"],
        primary_keyword=data["primary_keyword"],
        article_markdown=data["article_markdown"],
    )

    slug = data.get("slug") or _slugify_fallback(args.topic)
    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, f"{slug}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(_render_markdown(data, report.render()))

    print(f"Wrote {out_path}")
    print(f"SEO score: {report.score}/100  |  {report.word_count} words  |  "
          f"reading ease {report.reading_ease}  |  density {report.primary_density}%")
    print(f"Model: {result.model}  |  est. cost: ${result.estimated_cost_usd}  |  "
          f"out tokens: {result.usage.output_tokens}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
