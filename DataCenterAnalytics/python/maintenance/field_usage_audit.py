# ============================================================
# Maintenance Agent: Field Usage Audit
# ============================================================

import os
import json
import pandas as pd

# ------------------------------------------------------------
# 1. Load curated datasets from ../data_processed
# ------------------------------------------------------------
def load_datasets():
    processed_dir = os.path.join("..", "data_processed")
    datasets = {}

    if not os.path.exists(processed_dir):
        print(f"Processed data folder not found: {processed_dir}")
        return datasets

    for file in os.listdir(processed_dir):
        if file.endswith(".csv"):
            path = os.path.join(processed_dir, file)
            try:
                df = pd.read_csv(path)
                datasets[file] = df
            except Exception as e:
                print(f"Error loading {file}: {e}")

    return datasets

# ------------------------------------------------------------
# 2. Load PBIX metadata (exported manually to docs/pbix_metadata.json)
# ------------------------------------------------------------
def load_pbix_metadata():
    metadata_path = os.path.join("docs", "pbix_metadata.json")

    if not os.path.exists(metadata_path):
        print("PBIX metadata file not found. Please export metadata to docs/pbix_metadata.json")
        return {}

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        return metadata
    except Exception as e:
        print(f"Error reading metadata file: {e}")
        return {}

# ------------------------------------------------------------
# 3. Identify fields used in visuals
# ------------------------------------------------------------
def get_used_fields(pbix_metadata):
    used_fields = set()

    visuals = pbix_metadata.get("visuals", [])
    for visual in visuals:
        fields = visual.get("fields", [])
        for field in fields:
            used_fields.add(field)

    return used_fields

# ------------------------------------------------------------
# 4. Identify unused fields
# ------------------------------------------------------------
def get_unused_fields(datasets, used_fields):
    unused = {}

    for name, df in datasets.items():
        df_fields = set(df.columns)
        unused_fields = df_fields - used_fields
        unused[name] = sorted(list(unused_fields))

    return unused

# ------------------------------------------------------------
# 5. Identify naming inconsistencies
# ------------------------------------------------------------
def check_naming_consistency(datasets):
    issues = []

    for name, df in datasets.items():
        for col in df.columns:
            if (" " in col) or (col != col.lower()):
                issues.append((name, col))

    return issues

# ------------------------------------------------------------
# 6. Generate audit report (Markdown)
# ------------------------------------------------------------
def generate_report(used_fields, unused_fields, naming_issues):
    report_path = os.path.join("docs", "maintenance-report.md")

    with open(report_path, "w") as f:
        f.write("# Maintenance Agent: Field Usage Audit\n\n")

        f.write("## Used Fields\n")
        f.write("```\n")
        for field in sorted(list(used_fields)):
            f.write(f"{field}\n")
        f.write("```\n\n")

        f.write("## Unused Fields by Dataset\n")
        for dataset, fields in unused_fields.items():
            f.write(f"### {dataset}\n")
            f.write("```\n")
            for field in fields:
                f.write(f"{field}\n")
            f.write("```\n\n")

        f.write("## Naming Issues\n")
        if naming_issues:
            f.write("```\n")
            for issue in naming_issues:
                f.write(f"Dataset: {issue[0]}, Field: {issue[1]}\n")
            f.write("```\n")
        else:
            f.write("No naming issues detected.\n")

    print(f"Audit report generated at {report_path}")

# ------------------------------------------------------------
# 7. Main execution
# ------------------------------------------------------------
def run_field_usage_audit():
    print("Running Maintenance Agent: Field Usage Audit...\n")

    datasets = load_datasets()
    pbix_metadata = load_pbix_metadata()

    used_fields = get_used_fields(pbix_metadata)
    unused_fields = get_unused_fields(datasets, used_fields)
    naming_issues = check_naming_consistency(datasets)

    generate_report(used_fields, unused_fields, naming_issues)

    print("Audit complete.")

if __name__ == "__main__":
    run_field_usage_audit()