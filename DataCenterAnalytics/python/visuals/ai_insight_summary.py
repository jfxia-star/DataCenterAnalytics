import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# Clear out any stuck memory containers
plt.close('all')

# Create a clean canvas with absolute minimal padding
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.axis('off')

# Keep backgrounds transparent so Power BI container color fills the edges
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

df = dataset

# Helper function to strip brackets [] and quotes cleanly
def clean_val(val, is_num=False):
    text = str(val).replace('[', '').replace(']', '').replace("'", "").strip()
    if text.lower() in ['nan', 'none', 'blank', 'null', '']:
        return None
    if is_num:
        try:
            return float(text)
        except:
            return None
    return text

# Extract single clean values
peak_load = clean_val(df['Peak_Load_MWh'].values, is_num=True)
max_temp = clean_val(df['Max_Summer_Heat'].values, is_num=True)
high_risk = clean_val(df['High_Risk_Facility_Count'].values, is_num=True)
grid_op = clean_val(df['Lowest_Margin_Operator'].values)
risk_state = clean_val(df['Highest_Risk_State'].values)
selected_state = clean_val(df['state'].values)

# --- CONTEXT GUARD NARRATIVE LOGIC ---
# Paragraph 1 Logic
if peak_load and grid_op:
    p1 = f"The current operational snapshot shows a peak system load of {peak_load:,.0f} MWh under grid operator {grid_op}. This level of demand reflects both seasonal consumption patterns and underlying structural growth in the region’s energy footprint."
else:
    p1 = "The current operational snapshot reflects core seasonal consumption patterns and underlying structural growth across the regional electrical energy footprint."

# Paragraph 2 Logic 
# Modified to handle Virginia safely if it doesn't match a filtered state data profile
if selected_state and high_risk and risk_state != "Multiple States":
    p2 = f"Risk concentration remains uneven across the network. The state of {selected_state} continues to exhibit the highest exposure, with {high_risk:,.0f} active facilities operating under elevated reliability constraints. This distribution highlights the need for targeted resilience planning rather than uniform system‑wide measures."
elif high_risk and high_risk > 0:
    p2 = f"Risk concentration remains uneven across the network, tracking {high_risk:,.0f} active facilities operating under elevated reliability constraints. This distribution highlights the need for targeted resilience planning rather than uniform system‑wide measures."
else:
    p2 = "Risk concentration remains stable across the network. Current tracking indicates baseline facility exposures are operating within normal regional reliability bounds."

# Paragraph 3 Logic
if max_temp:
    p3 = f"Climate conditions also play a measurable role. The average maximum temperature during the selected period reached {max_temp:.1f}°F, contributing to increased cooling demand and amplifying stress on transmission assets. This reinforces the importance of integrating climate‑sensitive forecasting into operational decision‑making."
else:
    p3 = "Climate conditions also play a measurable role. Variations in maximum regional temperatures contribute to shifting cooling demands and drive the importance of integrating climate‑sensitive forecasting into operational decision‑making."

# Paragraph 4
p4 = "Together, these indicators provide a forward‑looking perspective on system reliability. By combining operational metrics with climate signals and geographic risk distribution, this AI‑generated summary supports more proactive planning and helps analysts quickly identify where deeper investigation may be warranted."

# --- HEADERS ---
notice = "⚡ INTERACTIVE PANEL — Please click a state to recalculate insights automatically"
title = "AI Insight Summary"

# --- AUTOMATIC LINE WRAPPING ---
wrap_width = 80  
p1_wrapped = "\n".join(textwrap.wrap(p1, width=wrap_width))
p2_wrapped = "\n".join(textwrap.wrap(p2, width=wrap_width))
p3_wrapped = "\n".join(textwrap.wrap(p3, width=wrap_width))
p4_wrapped = "\n".join(textwrap.wrap(p4, width=wrap_width))

# --- DYNAMIC PLACEMENT (RESTORED EXACT SPACING MARGINS) ---
ax.text(0.02, 0.96, notice, fontsize=11, color='#1F4E79', weight='bold', va='top')
ax.text(0.02, 0.90, title, fontsize=20, weight='bold', color='#111111', va='top')

ax.text(0.02, 0.81, p1_wrapped, fontsize=13, color='#333333', va='top', linespacing=1.3)
ax.text(0.02, 0.65, p2_wrapped, fontsize=13, color='#333333', va='top', linespacing=1.3)
ax.text(0.02, 0.45, p3_wrapped, fontsize=13, color='#333333', va='top', linespacing=1.3)
ax.text(0.02, 0.21, p4_wrapped, fontsize=13, color='#333333', va='top', linespacing=1.3)

# Expand plot limits to touch the absolute outer pixel grid border
plt.subplots_adjust(left=0.00, right=1.00, top=1.00, bottom=0.00)
plt.show()