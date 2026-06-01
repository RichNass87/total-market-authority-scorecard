import gradio as gr

CATEGORIES = [
    ("legal", "Legal and Factual Clarity", "Business name, location, category, contact details, registration/licensing facts, and factual identity are clear and consistent."),
    ("entity", "Entity Clarity", "Public platforms can identify the business as one connected entity across profiles, website, proof assets, and owner/team signals."),
    ("role", "Role Clarity", "The business has a specific role in the customer's decision beyond a generic service label."),
    ("language", "Language Ownership", "The business uses specific, repeatable language that defines its method, standard, or point of view."),
    ("proof", "Proof Alignment", "Reviews, photos, case studies, videos, posts, and proof assets support the role the business claims."),
    ("platform", "Platform Agreement", "Website, Google Business Profile, social profiles, directories, marketplaces, and proof assets reinforce the same identity."),
    ("website", "Website Brain", "The website organizes identity, decisions, proof, definitions, FAQs, case studies, owner authority, and conversion paths."),
    ("machine", "Machine Readability and Schema Discipline", "Headings, metadata, internal links, visible summaries, structured facts, and schema make the business easier to parse."),
    ("owner", "Owner / Team Entity Strength", "Owner, founder, leadership, and team are publicly connected to the business standards, proof, process, and authority framework."),
    ("behavior", "Behavioral Confirmation", "Customers, reviews, calls, questions, engagement, and platform behavior confirm that the market understands the business frame."),
]


def interpret_total(score: int) -> str:
    if score < 300:
        return "Present but unclear"
    if score < 500:
        return "Basic presence"
    if score < 700:
        return "Organized but incomplete"
    if score < 850:
        return "Trusted in pockets"
    if score < 950:
        return "Hard to ignore"
    return "Market-explainable under pressure"


def recommendation_for(label: str) -> str:
    mapping = {
        "Legal and Factual Clarity": "Audit name, address, phone, service area, licensing, categories, and public factual identity across every public surface.",
        "Entity Clarity": "Connect website, profiles, owner/team bios, citations, social platforms, proof assets, and datasets/tools into one recognizable entity pattern.",
        "Role Clarity": "Write a one-sentence authority statement that explains who you help, what decision you clarify, and what risk you reduce.",
        "Language Ownership": "Name the method, standard, checklist, scorecard, or operating principle that makes the business easier to remember and repeat.",
        "Proof Alignment": "Create proof assets that match the claimed role: case studies, photos with context, review themes, before/after evidence, and process documentation.",
        "Platform Agreement": "Rewrite public profile descriptions so Google Business Profile, website, social, review sites, directories, and author assets reinforce the same idea.",
        "Website Brain": "Build pages that explain decisions, definitions, proof, process, FAQs, team standards, and next steps instead of only listing services.",
        "Machine Readability and Schema Discipline": "Improve H1s, metadata, internal links, summaries, structured facts, schema, and visible page content without hiding claims in code only.",
        "Owner / Team Entity Strength": "Create owner and team pages that connect the people to the business standard, method, proof, and customer decision logic.",
        "Behavioral Confirmation": "Track whether calls, reviews, questions, engagement, and customer language prove that the market understands the frame.",
    }
    return mapping.get(label, "Improve this layer with clearer proof and platform alignment.")


def build_scorecard(business_name, industry, market, authority_sentence, notes, *scores):
    scores = [int(s) for s in scores]
    total = sum(scores)
    grade = interpret_total(total)
    scored = [(CATEGORIES[i][1], scores[i], CATEGORIES[i][2]) for i in range(len(CATEGORIES))]
    strongest = sorted(scored, key=lambda x: x[1], reverse=True)[:3]
    weakest = sorted(scored, key=lambda x: x[1])[:3]

    report = f"""
# Total Market Authority Scorecard™

## Business

**Business:** {business_name or 'Not provided'}  
**Industry:** {industry or 'Not provided'}  
**Market:** {market or 'Not provided'}

## Total Score

# {total} / 1000

**Interpretation:** {grade}

## Authority Sentence

{authority_sentence or 'No authority sentence entered yet.'}

## Category Scores

| Category | Score | What It Measures |
|---|---:|---|
"""
    for label, score, description in scored:
        report += f"| {label} | {score}/100 | {description} |\n"

    report += "\n## Strongest Layers\n"
    for label, score, _ in strongest:
        report += f"- **{label}: {score}/100**\n"

    report += "\n## Weakest Layers\n"
    for label, score, _ in weakest:
        report += f"- **{label}: {score}/100** — {recommendation_for(label)}\n"

    report += "\n## Recommended Next Moves\n"
    for label, score, _ in weakest:
        report += f"1. **Improve {label}:** {recommendation_for(label)}\n"

    if notes:
        report += f"\n## Notes Entered\n\n{notes}\n"

    report += """
---

## Important Disclaimer

This scorecard is educational and directional. It is not an official ranking factor, platform score, SEO guarantee, AI visibility guarantee, advertising recommendation, legal opinion, or financial advice. Search engines, AI systems, social platforms, marketplaces, review platforms, and advertising platforms can change at any time.
"""
    return report


with gr.Blocks(title="Total Market Authority Scorecard") as demo:
    gr.Markdown("""
# Total Market Authority Scorecard™

A public scoring framework for measuring local business legibility, AI visibility, platform agreement, proof alignment, and market verifiability.

Score each layer from **0 to 100**. The tool returns a **1000-point Total Market Authority score**, an interpretation, strongest layers, weakest layers, and recommended next moves.
""")

    with gr.Row():
        business_name = gr.Textbox(label="Business Name", placeholder="Example: Inspector Roofing and Restoration")
        industry = gr.Textbox(label="Industry", placeholder="Example: Roofing and Restoration")
        market = gr.Textbox(label="Primary Market", placeholder="Example: Alpharetta, GA / North Atlanta")

    authority_sentence = gr.Textbox(
        label="One-Sentence Authority Statement",
        placeholder="Example: We help homeowners make inspection-first roofing decisions through documentation, evidence, and claim verifiability.",
        lines=3,
    )

    sliders = []
    for _, label, description in CATEGORIES:
        sliders.append(gr.Slider(0, 100, value=50, step=5, label=label, info=description))

    notes = gr.Textbox(label="Optional Notes", lines=4, placeholder="Add proof assets, missing items, platform issues, or business context.")

    button = gr.Button("Generate Scorecard", variant="primary")
    output = gr.Markdown()

    button.click(
        fn=build_scorecard,
        inputs=[business_name, industry, market, authority_sentence, notes] + sliders,
        outputs=output,
    )

    gr.Markdown("""
---
Created by Richard Nasser. Based on the Total Market Authority™ framework.
""")

if __name__ == "__main__":
    demo.launch()
