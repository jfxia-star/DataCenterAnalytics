# ============================================================
# Maintenance Agent: Measure Hygiene Audit
# ============================================================

import os
import json

# ------------------------------------------------------------
# 1. Load measures metadata
# ------------------------------------------------------------
def load_measures_metadata():
    metadata_path = os.path.join("docs", "measures_metadata.json")

    if not os.path.exists(metadata_path):
        print("Measures metadata file not found. Please create docs/measures_metadata.json")
        return {}

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        return metadata
    except Exception as e:
        print(f"Error reading measures metadata: {e}")
        return {}

# ------------------------------------------------------------
# 2. Identify unused measures
# ------------------------------------------------------------
def get_unused_measures(measures):
    unused = []

    for m in measures:
        used_in = m.get("used_in_visuals", [])
        if not used_in:
            unused.append(m["name"])

    return unused

# ------------------------------------------------------------
# 3. Identify naming issues
# ------------------------------------------------------------
def check_measure_naming(measures):
    issues = []

    for m in measures:
        name = m["name"]

        if (" " in name) or (name != name.lower()):
            issues.append(name)

    return issues

# ------------------------------------------------------------
# 4. Identify missing descriptions
# ------------------------------------------------------------
def get_missing_descriptions(measures):
    missing = []

    for m in measures:
        desc = m.get("description", "")
        if not desc or desc.strip() == "":
            missing.append(m["name"])

    return missing

# ------------------------------------------------------------
# 5. Identify redundant measures
# ------------------------------------------------------------
def get_redundant_measures(measures):
    redundant = []
    expressions_seen = {}

    for m in measures:
        expr = m.get("expression", "").strip()
        name = m["name"]

        if expr in expressions_seen:
            redundant.append((name, expressions_seen[expr]))
        else:
            expressions_seen[expr] = name

    return redundant

# ------------------------------------------------------------
# 6. Prefix consistency audit
# ------------------------------------------------------------
def check_prefix_consistency(measures):
    prefixes = ["total_", "avg_", "max_", "min_", "peak_", "generation_", "facility_", "temperature_"]
    inconsistent = []

    for m in measures:
        name = m["name"]
        if not any(name.startswith(p) for p in prefixes):
            inconsistent.append(name)

    return inconsistent

# ------------------------------------------------------------
# 7. Semantic category audit
# ------------------------------------------------------------
def categorize_measure(measure):
    name = measure["name"]

    if "demand" in name:
        return "Demand"
    if "generation" in name:
        return "Generation"
    if "temperature" in name or "tmax" in name or "tmin" in name or "tavg" in name:
        return "Climate"
    if "facility" in name or "sqft" in name:
        return "Facility"
    if "grid" in name:
        return "Grid"

    return "Uncategorized"

# ------------------------------------------------------------
# 8. Expression complexity scoring
# ------------------------------------------------------------
def measure_complexity(measure):
    expr = measure["expression"].lower()

    if "sum(" in expr:
        return "Low"
    if "average(" in expr or "max(" in expr or "min(" in expr:
        return "Medium"
    if "divide(" in expr or "-" in expr or "+" in expr:
        return "High"

    return "Unknown"

# ------------------------------------------------------------
# 9. Description quality scoring
# ------------------------------------------------------------
def description_quality(measure):
    desc = measure.get("description", "").strip()

    if desc == "":
        return "Missing"
    if len(desc.split()) < 4:
        return "Weak"
    return "Good"

# ------------------------------------------------------------
# 10. Build measure quality summary
# ------------------------------------------------------------
def build_measure_quality_summary(measures):
    summary = []

    for m in measures:
        summary.append({
            "name": m["name"],
            "category": categorize_measure(m),
            "complexity": measure_complexity(m),
            "description_quality": description_quality(m),
            "used": len(m.get("used_in_visuals", [])) > 0
        })

    return summary

# ------------------------------------------------------------
# 11. Generate audit report
# ------------------------------------------------------------
def generate_report(unused, naming_issues, missing_desc, redundant, prefix_issues, quality_summary):
    report_path = os.path.join("docs", "measure-hygiene-report.md")

    with open(report_path, "w") as f:
        f.write("# Maintenance Agent: Measure Hygiene Audit\n\n")

        f.write("## Unused Measures\n```\n")
        for m in unused:
            f.write(f"{m}\n")
        f.write("```\n\n")

        f.write("## Naming Issues\n```\n")
        for m in naming_issues:
            f.write(f"{m}\n")
        f.write("```\n\n")

        f.write("## Missing Descriptions\n```\n")
        for m in missing_desc:
            f.write(f"{m}\n")
        f.write("```\n\n")

        f.write("## Redundant Measures\n```\n")
        for pair in redundant:
            f.write(f"{pair[0]} duplicates {pair[1]}\n")
        f.write("```\n\n")

        f.write("## Prefix Consistency Issues\n```\n")
        for m in prefix_issues:
            f.write(f"{m}\n")
        f.write("```\n\n")

        f.write("## Measure Quality Summary\n```\n")
        for item in quality_summary:
            f.write(
                f"{item['name']} | "
                f"Category: {item['category']} | "
                f"Complexity: {item['complexity']} | "
                f"Description: {item['description_quality']} | "
                f"Used: {item['used']}\n"
            )
        f.write("```\n\n")

    print(f"Measure hygiene report generated at {report_path}")

# ------------------------------------------------------------
# 12. Main execution
# ------------------------------------------------------------
def run_measure_hygiene_audit():
    print("Running Maintenance Agent: Measure Hygiene Audit...\n")

    metadata = load_measures_metadata()
    measures = metadata.get("measures", [])

    unused = get_unused_measures(measures)
    naming_issues = check_measure_naming(measures)
    missing_desc = get_missing_descriptions(measures)
    redundant = get_redundant_measures(measures)
    prefix_issues = check_prefix_consistency(measures)
    quality_summary = build_measure_quality_summary(measures)

    generate_report(unused, naming_issues, missing_desc, redundant, prefix_issues, quality_summary)

    print("Audit complete.")

if __name__ == "__main__":
    run_measure_hygiene_audit()