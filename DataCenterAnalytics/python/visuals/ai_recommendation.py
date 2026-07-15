import pandas as pd
import matplotlib.pyplot as plt
import textwrap

plt.close('all')

fig, ax = plt.subplots(figsize=(4.5, 2.5))
ax.axis('off')

fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

df = dataset

def clean_val(val, is_num=False):
    text = str(val).replace('[','').replace(']','').replace("'", "").strip()
    if text.lower() in ['nan','none','null','blank','']:
        return None
    if is_num:
        try:
            return float(text)
        except:
            return None
    return text

selected_state = clean_val(df['state'].values)
high_risk = clean_val(df['High_Risk_Facility_Count'].values, is_num=True)
max_temp = clean_val(df['Max_Summer_Heat'].values, is_num=True)
peak_load = clean_val(df['Peak_Load_MWh'].values, is_num=True)

# --- AI Recommendation Logic ---
if selected_state and high_risk is not None:
    if high_risk >= 10:
        rec = (
            f"{selected_state} shows elevated reliability exposure with "
            f"{high_risk:.0f} high‑risk facilities. Prioritizing targeted "
            f"reinforcement and operator coordination may reduce strain during "
            f"peak periods."
        )
    elif high_risk >= 4:
        rec = (
            f"{selected_state} maintains moderate facility exposure. Monitoring "
            f"seasonal load patterns and preparing for heat‑driven demand spikes "
            f"will support continued resilience."
        )
    else:
        rec = (
            f"{selected_state} exhibits low facility exposure. Current indicators "
            f"suggest stable reliability, though periodic review of cooling demand "
            f"and transmission congestion remains advisable."
        )
else:
    rec = (
        "AI recommendation unavailable. Select a state to generate targeted "
        "operational guidance."
    )

# wrapped = "\n".join(textwrap.wrap(rec, width=50))

ax.text(
    0.00, 0.99,
    "AI Recommendation",
    fontsize=18,
    weight='bold',
    color='#1F4E79',
    va='top'
)

# ax.text(
#    0.00, 0.78,
#    wrapped,
#    fontsize=14,
#    color='#333333',
#    va='top',
#    linespacing=1.3
#)

ax.text(
    0.00, 0.78,
    rec,
    fontsize=14,
    color='#333333',
    va='top',
    linespacing=1.3,
    wrap=True,
    transform=ax.transAxes
)

plt.subplots_adjust(left=0.00, right=1.00, top=1.00, bottom=0.00)
plt.show()