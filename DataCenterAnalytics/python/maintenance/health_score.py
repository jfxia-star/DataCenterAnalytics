# ============================================================
# Maintenance Agent: Dashboard Health Score
# ============================================================

import os

# ------------------------------------------------------------
# Helper: Read audit report lines
# ------------------------------------------------------------
def read_report(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

# ------------------------------------------------------------
# 1. Field Coverage Score (0–20)
# ------------------------------------------------------------
def compute_field_score():
    lines = read_report("docs/field-usage-report.md")
    unused = sum(1 for l in lines if "UNUSED FIELD" in l)
    missing_desc = sum(1 for l in lines if "Missing Description" in l)

    score = 20 - (0.5 * unused) - (0.5 * missing_desc)
    return max(0, score)

# ------------------------------------------------------------
# 2. Measure Hygiene Score (0–25)
# ------------------------------------------------------------
def compute_measure_score():
    lines = read_report("docs/measure-hygiene-report.md")
    unused = sum(1 for l in lines if "UNUSED MEASURE" in l)
    missing_desc = sum(1 for l in lines if "Missing Description" in l)
    naming_issues = sum(1 for l in lines if "Naming Issue" in l)

    score = 25 - unused - missing_desc - naming_issues
    return max(0, score)

# ------------------------------------------------------------
# 3. Visual Complexity Score (0–20)
# ------------------------------------------------------------
def compute_visual_score():
    lines = read_report("docs/visual-complexity-report.md")
    complexity_values = []

    for l in lines:
        if "Complexity Score:" in l:
            try:
                val = int(l.split("Complexity Score:")[1].strip())
                complexity_values.append(val)
            except:
                pass

    total_complexity = sum(complexity_values)
    score = 20 - min(20, total_complexity / 5)
    return max(0, score)

# ------------------------------------------------------------
# 4. Slicer Governance Score (0–15)
# ------------------------------------------------------------
def compute_slicer_score():
    lines = read_report("docs/slicer-coverage-report.md")

    unused = sum(1 for l in lines if "Unused Slicers" in l and ":" in l)
    unfiltered = sum(1 for l in lines if "Visuals Not Affected" in l and ":" in l)
    redundant = sum(1 for l in lines if "Slicer Redundancy" in l and ":" in l)
    overloaded = sum(1 for l in lines if "Slicer Overload" in l and ":" in l)

    score = 15 - (2 * unused) - (1 * unfiltered) - (1 * redundant) - (2 * overloaded)
    return max(0, score)

# ------------------------------------------------------------
# 5. Python Quality Score (0–20)
# ------------------------------------------------------------
def compute_python_score():
    lines = read_report("docs/python-script-audit-report.md")

    missing_doc = sum(1 for l in lines if "Docstring: False" in l)
    syntax_errors = sum(1 for l in lines if "Syntax OK: False" in l)
    imports = sum(len(l.split("Imports:")[1].split(",")) for l in lines if "Imports:" in l)
    line_count = sum(int(l.split("Lines:")[1].split("|")[0].strip()) for l in lines if "Lines:" in l)

    score = 20 - (2 * missing_doc) - (5 * syntax_errors) - (1 * imports) - (0.1 * line_count)
    return max(0, score)

# ------------------------------------------------------------
# 6. Compute Final Health Score
# ------------------------------------------------------------
def compute_health_score():
    field_score = compute_field_score()
    measure_score = compute_measure_score()
    visual_score = compute_visual_score()
    slicer_score = compute_slicer_score()
    python_score = compute_python_score()

    total = field_score + measure_score + visual_score + slicer_score + python_score

    return {
        "FieldScore": field_score,
        "MeasureScore": measure_score,
        "VisualScore": visual_score,
        "SlicerScore": slicer_score,
        "PythonScore": python_score,
        "HealthScore": total
    }

# ------------------------------------------------------------
# 7. Generate Health Score Report
# ------------------------------------------------------------
def generate_report(scores):
    path = "docs/dashboard-health-score.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Maintenance Agent: Dashboard Health Score\n\n")
        f.write("## Component Scores\n")
        f.write("```\n")
        for k, v in scores.items():
            f.write(f"{k}: {v}\n")
        f.write("```\n\n")
        f.write(f"## Final Dashboard Health Score: **{scores['HealthScore']} / 100**\n")

    print(f"Health score report generated at {path}")

# ------------------------------------------------------------
# 8. Main Execution
# ------------------------------------------------------------
def run_health_score():
    print("Running Maintenance Agent: Dashboard Health Score...\n")
    scores = compute_health_score()
    generate_report(scores)
    print("Health scoring complete.")

if __name__ == "__main__":
    run_health_score()