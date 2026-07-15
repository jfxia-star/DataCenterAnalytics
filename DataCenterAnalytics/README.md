Data Center Analytics — AI‑Augmented Power BI Dashboard



This project showcases an AI‑augmented analytics dashboard built in Power BI, enhanced with Python‑based agents for narrative generation, recommendations, and automated maintenance audits. It demonstrates how AI can elevate data interpretation, strengthen governance, and improve dashboard maintainability.



The dashboard integrates multi‑source U.S. datacenter, energy, weather, and drought data into a unified analytics product.



⭐ Key Features



End‑to‑End Analytics Engineering



1.Multi‑source API ingestion

\- EIA (energy)

\- NOAA (weather)

\- USDM (drought)

\- IM3 (datacenters)



2\. Automated data processing pipelines

\- Raw → processed → PBIX model



3\. AI‑generated narrative \& recommendations

\- Natural‑language summary of dashboard insights

\- Actionable recommendations based on current data



4\. Python‑driven maintenance audits

\- Measure Hygiene Audit

\- Visual Complexity Audit

\- Slicer Coverage Audit

\- Python Script Audit

\- Field Usage Audit



5\. Power BI modeling \& visualization

\- Relationships

\- Measures

\- GeoJSON mapping

\- KPI cards

\- AI visuals



⭐ Folder Structure



DataCenterAnalytics/

│

├── DataCenterAnalytics.pbix        # Main Power BI dashboard

│

├── data\_raw/                       # Raw API outputs

│   ├── eia\_raw\_20260622\_1418.json

│   ├── noaa\_raw\_20260611\_1009.json

│   └── noaa\_raw\_combined\_20260622\_1230.json

│

├── data\_processed/                 # Cleaned \& transformed data for PBIX

│   ├── eia\_daily\_20260622\_1434.csv

│   ├── im3\_datacenters\_20260611\_1634.csv

│   ├── noaa\_daily\_20260622\_1230.csv

│   ├── states\_to\_grids.csv

│   └── usdm\_20260611\_1036.geojson

│

├── python/

│   ├── ingestion/                  # API ingestion scripts

│   │   ├── eia\_ingest.py

│   │   ├── im3\_ingest.py

│   │   ├── noaa\_ingest.py

│   │   └── usdm\_ingest.py

│   │

│   ├── maintenance/                # Automated audit agents

│   │   ├── field\_usage\_audit.py

│   │   ├── health\_score.py

│   │   ├── measure\_hygiene\_audit.py

│   │   ├── python\_script\_audit.py

│   │   ├── slicer\_coverage\_audit.py

│   │   └── visual\_complexity\_audit.py

│   │

│   ├── narrative/                  # AI narrative generator (placeholder)

│   ├── recommendation/             # AI recommendation generator (placeholder)

│   └── visuals/                    # Python scripts used inside PBIX visuals

│       ├── ai\_insight\_summary.py

│       └── ai\_recommendation.py

│

├── assets/

│   ├── icons/

│   │   └── DataCenter\_1.jpg

│   └── screenshots/

│       └── Page 3.png

│

├── docs/                           # Documentation \& metadata

│   ├── architecture-diagram.md

│   ├── dashboard-health-score.md

│   ├── dashboard-health\_score.csv

│   ├── design-logic.md

│   ├── maintenance-report.md

│   ├── measure-hygiene-report.md

│   ├── measures-metadata.json

│   ├── pbix-metadata.json

│   ├── python-script-audit-report.md

│   ├── slicer-coverage-report.md

│   └── visual-complexity-report.md

│

└── teaching/                       # Teaching materials (placeholders)

&#x20;   ├── notes/

&#x20;   └── slides/



⭐ Dashboard Overview



Page 1 — Datacenter Overview

\- State‑level datacenter distribution

\- Map visualization

\- Clustered column chart

\- KPI banner cards



Page 2 — Energy \& Weather

\- EIA daily energy metrics

\- NOAA weather indicators

\- USDM drought severity (GeoJSON)



Page 3 — AI Insights

\- AI narrative summary

\- AI recommendation engine

\- KPI health card

\- Health score bar chart



⭐ How to Use the Report



1\. Install Power BI Desktop (if needed)



2\. Configure Python scripting

Power BI → File → Options → Python scripting → Select your Python installation.



3\. Install Python (if needed)

Python visuals require:

\- Python 3.10+

\- pandas

\- numpy

\- matplotlib



4\. Clone the repository

git clone https://github.com/jfxia/DataCenterAnalytics.git



5\. Open the PBIX

Open DataCenterAnalytics.pbix.



6\. Refresh the data

All data sources are local CSV/JSON files inside data\_raw and data\_processed.



Python visuals will render automatically.



⭐ Maintenance Agent Health Score



The Maintenance Agent evaluates dashboard maintainability using five audits.

Scores are combined into a single 0–100 health score, displayed on Page 3 as:

\- a KPI card

\- a bar chart



This provides a quick, AI‑augmented assessment of dashboard quality.



⭐ Screenshots



A screenshot of Page 3 is available in: /assets/screenshots/Page 3.png



⭐ License



MIT License

