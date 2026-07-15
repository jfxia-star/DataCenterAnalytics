# ============================================================
# Maintenance Agent: Slicer Coverage Audit
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
# 2. Identify slicers and their coverage
# ------------------------------------------------------------
def get_slicer_coverage(pbix_metadata):
    visuals = pbix_metadata.get("visuals", [])
    slicer_map = {}

    # Build slicer → visuals mapping
    for v in visuals:
        slicers = v.get("slicers", [])
        for s in slicers:
            if s not in slicer_map:
                slicer_map[s] = []
            slicer_map[s].append(v["name"])

    return slicer_map

# ------------------------------------------------------------
# 3. Identify slicers that affect no visuals
# ------------------------------------------------------------
def get_unused_slicers(slicer_map):
    unused = []
    for slicer, visuals in slicer_map.items():
        if len(visuals) == 0:
            unused.append(slicer)
    return unused

# ------------------------------------------------------------
# 4. Identify visuals not affected by any slicer
# ------------------------------------------------------------
def get_unfiltered_visuals(pbix_metadata):
    visuals = pbix_metadata.get("visuals", [])
    unfiltered = []

    for v in visuals:
        if len(v.get("slicers", [])) == 0:
            unfiltered.append(v["name"])

    return unfiltered

# ------------------------------------------------------------
# 5. Identify slicer redundancy
# ------------------------------------------------------------
def get_slicer_redundancy(pbix_metadata):
    visuals = pbix_metadata.get("visuals", [])
    redundancy = {}

    for v in visuals:
        slicers = v.get("slicers", [])
        if len(slicers) > 1:
            redundancy[v["name"]] = slicers

    return redundancy

# ------------------------------------------------------------
# 6. Identify slicer overload
# ------------------------------------------------------------
def get_slicer_overload(pbix_metadata, threshold=3):
    visuals = pbix_metadata.get("visuals", [])
    overload = {}

    for v in visuals:
        slicers = v.get("slicers", [])
        if len(slicers) > threshold:
            overload[v["name"]] = slicers

    return overload

# ------------------------------------------------------------
# 7. Generate audit report
# ------------------------------------------------------------
def generate_report(slicer_map, unused_slicers, unfiltered_visuals, redundancy, overload):
    report_path = os.path.join("docs", "slicer-coverage-report.md")

    with open(report_path, "w") as f:
        f.write("# Maintenance Agent: Slicer Coverage Audit\n\n")

        f.write("## Slicer Coverage Map\n")
        f.write("```\n")
        for slicer, visuals in slicer_map.items():
            f.write(f"{slicer}: {', '.join(visuals)}\n")
        f.write("```\n\n")

        f.write("## Unused Slicers\n")
        f.write("```\n")
        for s in unused_slicers:
            f.write(f"{s}\n")
        f.write("```\n\n")

        f.write("## Visuals Not Affected by Any Slicer\n")
        f.write("```\n")
        for v in unfiltered_visuals:
            f.write(f"{v}\n")
        f.write("```\n\n")

        f.write("## Slicer Redundancy (Multiple slicers affecting same visual)\n")
        f.write("```\n")
        for visual, slicers in redundancy.items():
            f.write(f"{visual}: {', '.join(slicers)}\n")
        f.write("```\n\n")

        f.write("## Slicer Overload (More than 3 slicers affecting a visual)\n")
        f.write("```\n")
        for visual, slicers in overload.items():
            f.write(f"{visual}: {', '.join(slicers)}\n")
        f.write("```\n\n")

    print(f"Slicer coverage report generated at {report_path}")

# ------------------------------------------------------------
# 8. Main execution
# ------------------------------------------------------------
def run_slicer_coverage_audit():
    print("Running Maintenance Agent: Slicer Coverage Audit...\n")

    pbix_metadata = load_pbix_metadata()

    slicer_map = get_slicer_coverage(pbix_metadata)
    unused_slicers = get_unused_slicers(slicer_map)
    unfiltered_visuals = get_unfiltered_visuals(pbix_metadata)
    redundancy = get_slicer_redundancy(pbix_metadata)
    overload = get_slicer_overload(pbix_metadata)

    generate_report(slicer_map, unused_slicers, unfiltered_visuals, redundancy, overload)

    print("Audit complete.")

if __name__ == "__main__":
    run_slicer_coverage_audit()