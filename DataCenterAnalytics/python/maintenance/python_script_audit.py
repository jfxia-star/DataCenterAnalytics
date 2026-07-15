# ============================================================
# Maintenance Agent: Python Script Audit
# ============================================================

import os
import ast

# ------------------------------------------------------------
# 1. Find Python visual scripts
# ------------------------------------------------------------
def find_python_visual_scripts():
    visuals_dir = os.path.join("python", "visuals")
    scripts = []

    if not os.path.exists(visuals_dir):
        print("Python visuals directory not found: python/visuals")
        return scripts

    for fname in os.listdir(visuals_dir):
        if fname.endswith(".py"):
            scripts.append(os.path.join(visuals_dir, fname))

    return scripts

# ------------------------------------------------------------
# 2. Analyze a single Python script
# ------------------------------------------------------------
def analyze_script(path):
    info = {
        "path": path,
        "exists": True,
        "syntax_ok": True,
        "imports": [],
        "has_docstring": False,
        "line_count": 0
    }

    if not os.path.exists(path):
        info["exists"] = False
        info["syntax_ok"] = False
        return info

    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception:
        info["syntax_ok"] = False
        return info

    info["line_count"] = len(source.splitlines())

    try:
        tree = ast.parse(source)
    except SyntaxError:
        info["syntax_ok"] = False
        return info

    # Module-level docstring
    if ast.get_docstring(tree):
        info["has_docstring"] = True

    # Imports
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    info["imports"] = sorted(set(imports))

    return info

# ------------------------------------------------------------
# 3. Build Python script audit summary
# ------------------------------------------------------------
def build_python_script_summary():
    scripts = find_python_visual_scripts()
    summary = []

    for script in scripts:
        summary.append(analyze_script(script))

    return summary

# ------------------------------------------------------------
# 4. Generate audit report
# ------------------------------------------------------------
def generate_report(summary):
    report_path = os.path.join("docs", "python-script-audit-report.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Maintenance Agent: Python Script Audit\n\n")

        f.write("## Python Visual Script Summary\n")
        f.write("```\n")
        for item in summary:
            f.write(
                f"{os.path.basename(item['path'])} | "
                f"Exists: {item['exists']} | "
                f"Syntax OK: {item['syntax_ok']} | "
                f"Docstring: {item['has_docstring']} | "
                f"Lines: {item['line_count']} | "
                f"Imports: {', '.join(item['imports'])}\n"
            )
        f.write("```\n\n")

    print(f"Python script audit report generated at {report_path}")

# ------------------------------------------------------------
# 5. Main execution
# ------------------------------------------------------------
def run_python_script_audit():
    print("Running Maintenance Agent: Python Script Audit...\n")

    summary = build_python_script_summary()
    generate_report(summary)

    print("Audit complete.")

if __name__ == "__main__":
    run_python_script_audit()