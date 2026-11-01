from pathlib import Path
import html

import pandas as pd


OUT = Path("outputs/visuals")
OUT.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "MATCH": "#2E7D32",
    "Yes": "#2E7D32",
    "Partially": "#F9A825",
    "No": "#C62828",
    "PASS": "#2E7D32",
    "REVIEW": "#F9A825",
    "Partial": "#F9A825",
    "Medium": "#1565C0",
    "Unknown": "#607D8B",
}


def save_bar(path, title, counts, ylabel):
    counts = {str(k): int(v) for k, v in counts.items()}
    width, height = 900, 520
    margin_left, margin_top, margin_bottom = 110, 80, 95
    plot_width = width - margin_left - 60
    plot_height = height - margin_top - margin_bottom
    max_value = max(counts.values()) if counts else 1
    gap = 40
    bar_width = (plot_width - gap * (len(counts) - 1)) / max(len(counts), 1)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="38" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700" fill="#263238">{html.escape(title)}</text>',
        f'<text x="24" y="{margin_top + plot_height / 2}" transform="rotate(-90 24 {margin_top + plot_height / 2})" text-anchor="middle" font-family="Arial" font-size="16" fill="#455A64">{html.escape(ylabel)}</text>',
        f'<line x1="{margin_left}" y1="{margin_top + plot_height}" x2="{margin_left + plot_width}" y2="{margin_top + plot_height}" stroke="#B0BEC5" stroke-width="2"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_height}" stroke="#B0BEC5" stroke-width="2"/>',
    ]

    for index, (label, value) in enumerate(counts.items()):
        x = margin_left + index * (bar_width + gap)
        bar_height = plot_height * value / max_value
        y = margin_top + plot_height - bar_height
        color = PALETTE.get(label, "#607D8B")
        parts.extend(
            [
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" rx="6" fill="{color}"/>',
                f'<text x="{x + bar_width / 2:.1f}" y="{y - 12:.1f}" text-anchor="middle" font-family="Arial" font-size="20" font-weight="700" fill="#263238">{value}</text>',
                f'<text x="{x + bar_width / 2:.1f}" y="{margin_top + plot_height + 38}" text-anchor="middle" font-family="Arial" font-size="16" fill="#263238">{html.escape(label)}</text>',
            ]
        )

    parts.append("</svg>")
    Path(path).write_text("\n".join(parts), encoding="utf-8")


def save_metric_availability(path, validation):
    match_count = int((validation["Validation_Status"].astype(str).str.upper() == "MATCH").sum())
    total = len(validation)
    proxy = match_count / total if total else 0
    rows = [
        ("Proxy precision", f"Yes: {proxy:.1%}", f"{match_count}/{total} LLM rules marked MATCH in validation sheet"),
        ("True precision", "Only if labels are reviewed", "Need clear false-positive labels for every extracted rule"),
        ("Recall", "Not yet", "Need a complete manual/gold list of all expected Part M WC/shower rules"),
        ("Accuracy", "Not recommended yet", "Needs TP, FP, TN, FN; rule extraction rarely has meaningful true negatives"),
    ]

    width, height = 1100, 430
    xs = [40, 250, 500]
    col_widths = [210, 250, 580]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="42" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700" fill="#263238">Accuracy / Precision Visuals: What Is Defensible With Current Data</text>',
        '<rect x="40" y="75" width="1020" height="45" fill="#263238"/>',
    ]

    for x, text in zip(xs, ["Metric", "Can you show it?", "Why"]):
        parts.append(
            f'<text x="{x + 12}" y="104" font-family="Arial" font-size="16" font-weight="700" fill="#ffffff">{text}</text>'
        )

    y = 120
    for index, row in enumerate(rows):
        fill = "#F7FAFC" if index % 2 == 0 else "#FFFFFF"
        parts.append(f'<rect x="40" y="{y}" width="1020" height="70" fill="{fill}" stroke="#CFD8DC"/>')
        for x, col_width, text in zip(xs, col_widths, row):
            parts.append(
                f'<foreignObject x="{x + 12}" y="{y + 12}" width="{col_width - 20}" height="52">'
                f'<div xmlns="http://www.w3.org/1999/xhtml" style="font-family:Arial;font-size:15px;color:#263238;line-height:1.25;">{html.escape(text)}</div>'
                "</foreignObject>"
            )
        y += 70

    parts.append("</svg>")
    Path(path).write_text("\n".join(parts), encoding="utf-8")


def main():
    validation = pd.read_excel("outputs/llm_vs_manual_validation.xlsx")
    rules = pd.read_excel("outputs/focused_llm_partm_rules_wc_shower.xlsx")
    compliance = pd.read_excel("outputs/automated_compliance_results.xlsx")
    mapping = pd.read_excel("outputs/llm_rule_to_ifc_check_mapping.xlsx")

    save_bar(
        OUT / "01_validation_status.svg",
        "LLM Rule Extraction Validation Against Manual Topics",
        validation["Validation_Status"].fillna("Unknown").value_counts(),
        "Number of LLM-extracted rules",
    )
    save_bar(
        OUT / "02_automatable_coverage.svg",
        "Automatability of Extracted Part M Rules",
        rules["automatable"].fillna("Unknown").value_counts(),
        "Number of rules",
    )
    save_bar(
        OUT / "03_compliance_results.svg",
        "Prototype Automated Compliance Results",
        compliance["Result"].fillna("Unknown").value_counts(),
        "Number of checks",
    )
    save_bar(
        OUT / "04_mapping_confidence.svg",
        "Confidence of LLM Rule to IFC Check Mapping",
        mapping["Confidence"].fillna("Unknown").value_counts(),
        "Mapped rules",
    )
    save_metric_availability(OUT / "05_metric_availability.svg", validation)

    for path in sorted(OUT.glob("*.svg")):
        print(path.resolve())


if __name__ == "__main__":
    main()
