+=========================================================================+
|                         Data Center Analytics                           |
|                 AI‑Augmented Power BI Dashboard (PBIX)                  |
+=========================================================================+

                                +----------------------+
                                |      Power BI        |
                                |     Data Model       |
                                +----------------------+
                                          |
                                          |
                                          v
                     +-----------------------------------------------+
                     |               Dashboard Pages                 |
                     |-----------------------------------------------|
                     |  Page 1: Datacenter Overview                  |
                     |  Page 2: Energy & Weather                     |
                     |  Page 3: AI Insights & Governance             |
                     +-----------------------------------------------+
                                          |
                                          |
                                          v
+---------------------------------------------------------------------------+
|                           Embedded Python Agents                          |
+---------------------------------------------------------------------------+
|                                                                           |
|   +------------------------------+     +--------------------------------+ |
|   |        Insight Agent         |     |     Recommendation Agent       | |
|   |     (Narrative Engine)       |     |   (Actionable Suggestions)     | |
|   |------------------------------|     |--------------------------------| |
|   | • Reads PBIX model           |     | • Interprets dashboard state   | |
|   | • Generates narrative text   |     | • Produces recommendations     | |
|   | • Uses matplotlib text       |     | • Rule-based logic + heuristics| |
|   +------------------------------+     +--------------------------------+ |
|                                                                           |
|   +---------------------------------------------------------------------+ |
|   |                         Maintenance Agent                           | |
|   |                     (Automated Governance Audits)                   | |
|   |---------------------------------------------------------------------| |
|   | • Field Usage Audit                                                 | |
|   | • Measure Hygiene Audit                                             | |
|   | • Visual Complexity Audit                                           | |
|   | • Slicer Coverage Audit                                             | |
|   | • Python Script Audit                                               | |
|   |                                                                     | |
|   | → Produces component scores                                         | |
|   | → Generates unified Health Score (0–100)                            | |
|   | → Outputs CSV + Markdown reports                                    | |
|   +---------------------------------------------------------------------+ |
|                                                                           |
+---------------------------------------------------------------------------+

                                          |
                                          v

+---------------------------------------------------------------------------+
|                         Governance Panel (Page 3)                         |
+---------------------------------------------------------------------------+
|                                                                           |
|   • AI Narrative (Python visual)                                          |
|   • AI Recommendation (Python visual)                                     |
|   • Maintenance Agent Assessment                                          |
|   • Health Score KPI                                                      |
|   • Component Score Bar Chart                                             |
|   • Slicer + Page Navigation                                              |
|                                                                           |
+---------------------------------------------------------------------------+

                                          |
                                          v

+---------------------------------------------------------------------------+
|                           Repository Structure                            |
+---------------------------------------------------------------------------+
|                                                                           |
|   /data_raw/                                                              |
|       eia_raw_*.json                                                      |
|       noaa_raw_*.json                                                     |
|       noaa_raw_combined_*.json                                            |
|                                                                           |
|   /data_processed/                                                        |
|       eia_daily_*.csv                                                     |
|       im3_datacenters_*.csv                                               |
|       noaa_daily_*.csv                                                    |
|       states_to_grids.csv                                                 |
|       usdm_*.geojson                                                      |
|                                                                           |
|   /python/                                                                |
|       ingestion/ (API scripts)                                            |
|       maintenance/ (audit agents)                                         |
|       narrative/ (placeholder)                                            |
|       recommendation/ (placeholder)                                       |
|       visuals/ (Python visuals for PBIX)                                  |
|                                                                           |
|   /docs/                                                                  |
|       audit reports, metadata, design logic                               |
|                                                                           |
|   /assets/                                                                |
|       icons, screenshots                                                  |
|                                                                           |
+---------------------------------------------------------------------------+
