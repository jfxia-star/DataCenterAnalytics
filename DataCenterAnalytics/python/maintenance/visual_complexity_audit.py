# ============================================================
# Maintenance Agent: Visual Complexity Audit
# ============================================================

import os
import json

# ------------------------------------------------------------
# 1. Load PBIX metadata
# ------------------------------------------------------------
def load_pbix_metadata():
    metadata_path = os.path.join("docs", "pbix_metadata.json")

    if not os.path.exists(metadata_path):
        print("PBIX metadata file not found. Please create docs/pbix_metadata.json")
        return {}

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        return metadata
    except Exception as e:
        print(f"Error reading metadata file: {e}")
        return {}

# ------------------------------------------------------------
# 2. Compute visual complexity score
# ------------------------------------------------------------
def compute_complexity(visual):
    fields = visual.get("fields", [])
    measures = visual.get("measures", [])
    uses_python = visual.get("python_visual", False)
    slicers = visual.get("slicers", [])

    score = 0

    # Field complexity
    score += len(fields)

    # Measure complexity
    score += len(measures) * 2

    # Python visuals add complexity
    if uses_python:
        score += 5

    # Slicer dependencies
    score += len(slicers)

    return score

# ------------------------------------------------------------
# 3. Build visual complexity summary
# ------------------------------------------------------------
def build_visual_summary(pbix_metadata):
    visuals = pbix_metadata.get("visuals", [])
    summary = []

    for v in visuals:
        summary.append({
            "name": v.get("name", "Unnamed Visual"),
            "field_count": len(v.get("fields", [])),
            "measure_count": len(v.get("measures", [])),
            "uses_python": v.get("python_visual", False),
            "slicer_count": len(v.get("slicers", [])),
            "complexity_score": compute_complexity(v)
        })

    return summary

# ------------------------------------------------------------
# 4. Generate audit report
# ------------------------------------------------------------
def generate_report(summary):
    report_path = os.path.join("docs", "visual-complexity-report.md")

    with open(report_path, "w") as f:
        f.write("# Maintenance Agent: Visual Complexity Audit\n\n")

        f.write("## Visual Complexity Summary\n")
        f.write("```\n")
        for item in summary:
            f.write(
                f"{item['name']} | "
                f"Fields: {item['field_count']} | "
                f"Measures: {item['measure_count']} | "
                f"Python: {item['uses_python']} | "
                f"Slicers: {item['slicer_count']} | "
                f"Complexity Score: {item['complexity_score']}\n"
            )
        f.write("```\n\n")

    print(f"Visual complexity report generated at {report_path}")

# ------------------------------------------------------------
# 5. Main execution
# ------------------------------------------------------------
def run_visual_complexity_audit():
    print("Running Maintenance Agent: Visual Complexity Audit...\n")

    pbix_metadata = load_pbix_metadata()
    summary = build_visual_summary(pbix_metadata)

    generate_report(summary)

    print("Audit complete.")

if __name__ == "__main__":
    run_visual_complexity_audit()