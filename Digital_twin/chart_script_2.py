
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Define the timeline data
phases_data = [
    # DQ Phase (Weeks 1-2)
    {"Task": "DQ: Design Review", "Start": 1, "Finish": 1.5, "Type": "Activity", "Status": "on-track"},
    {"Task": "DQ: Requirements Doc", "Start": 1, "Finish": 2, "Type": "Deliverable", "Status": "on-track"},
    {"Task": "DQ Sign-off Gate", "Start": 2, "Finish": 2, "Type": "Gate", "Status": "on-track"},
    
    # Parallel Activities (Weeks 3-4)
    {"Task": "Procurement", "Start": 3, "Finish": 4, "Type": "Parallel", "Status": "caution"},
    {"Task": "Development Setup", "Start": 3, "Finish": 4, "Type": "Parallel", "Status": "caution"},
    
    # IQ Phase (Weeks 5-8)
    {"Task": "IQ: Installation", "Start": 5, "Finish": 6.5, "Type": "Activity", "Status": "on-track"},
    {"Task": "IQ: Config & Testing", "Start": 6.5, "Finish": 8, "Type": "Activity", "Status": "on-track"},
    {"Task": "IQ: Install Report", "Start": 7, "Finish": 8, "Type": "Deliverable", "Status": "on-track"},
    {"Task": "IQ Sign-off Gate", "Start": 8, "Finish": 8, "Type": "Gate", "Status": "on-track"},
    
    # OQ Phase (Weeks 9-12)
    {"Task": "OQ: Operational Tests", "Start": 9, "Finish": 11, "Type": "Activity", "Status": "on-track"},
    {"Task": "OQ: Test Protocol", "Start": 10, "Finish": 12, "Type": "Deliverable", "Status": "on-track"},
    {"Task": "OQ Sign-off Gate", "Start": 12, "Finish": 12, "Type": "Gate", "Status": "caution"},
    
    # PQ Phase (Weeks 13-20)
    {"Task": "PQ: Performance Val", "Start": 13, "Finish": 17, "Type": "Activity", "Status": "caution"},
    {"Task": "PQ: Final Testing", "Start": 17, "Finish": 19, "Type": "Activity", "Status": "at-risk"},
    {"Task": "PQ: Final Report", "Start": 18, "Finish": 20, "Type": "Deliverable", "Status": "at-risk"},
    {"Task": "PQ Sign-off Gate", "Start": 20, "Finish": 20, "Type": "Gate", "Status": "at-risk"},
]

df = pd.DataFrame(phases_data)

# Color mapping based on status and type
color_map = {
    ("Activity", "on-track"): "#2E8B57",      # Sea green
    ("Activity", "caution"): "#D2BA4C",       # Moderate yellow
    ("Activity", "at-risk"): "#DB4545",       # Bright red
    ("Deliverable", "on-track"): "#1FB8CD",   # Strong cyan
    ("Deliverable", "caution"): "#D2BA4C",    # Moderate yellow
    ("Deliverable", "at-risk"): "#DB4545",    # Bright red
    ("Parallel", "caution"): "#5D878F",       # Cyan
    ("Gate", "on-track"): "#2E8B57",          # Sea green
    ("Gate", "caution"): "#D2BA4C",           # Moderate yellow
    ("Gate", "at-risk"): "#DB4545",           # Bright red
}

df['Color'] = df.apply(lambda row: color_map.get((row['Type'], row['Status']), '#1FB8CD'), axis=1)
df['Duration'] = df['Finish'] - df['Start']

# Create figure
fig = go.Figure()

# Add Gantt bars
for idx, row in df.iterrows():
    fig.add_trace(go.Bar(
        y=[row['Task']],
        x=[row['Duration']],
        base=row['Start'],
        orientation='h',
        marker=dict(color=row['Color'], line=dict(width=0)),
        name=row['Type'],
        showlegend=False,
        hovertemplate=f"<b>{row['Task']}</b><br>Weeks {row['Start']}-{row['Finish']}<br>{row['Status']}<extra></extra>",
    ))

# Add risk markers at critical points
risk_points = [
    {"week": 12, "task": "OQ Sign-off Gate", "reason": "Integration risk"},
    {"week": 15, "task": "PQ: Performance Val", "reason": "Performance risk"},
    {"week": 19, "task": "PQ: Final Testing", "reason": "Timeline risk"},
]

for risk in risk_points:
    task_idx = df[df['Task'] == risk['task']].index[0]
    fig.add_trace(go.Scatter(
        x=[risk['week']],
        y=[risk['task']],
        mode='markers',
        marker=dict(symbol='diamond', size=12, color='#DB4545', line=dict(width=2, color='white')),
        name='Risk Item',
        showlegend=False,
        hovertemplate=f"<b>Risk</b><br>{risk['reason']}<extra></extra>",
    ))

# Create cumulative cost curve data (normalized to fit on chart)
weeks = np.linspace(0, 24, 25)
# S-curve for typical project cost accumulation
cost_curve = 100 * (1 / (1 + np.exp(-0.3 * (weeks - 12))))

# Normalize to fit in the task space (scale to number of tasks)
cost_normalized = (cost_curve / 100) * (len(df) - 1)

# Add cumulative cost line
fig.add_trace(go.Scatter(
    x=weeks,
    y=cost_normalized,
    mode='lines',
    line=dict(color='#1FB8CD', width=3, dash='dot'),
    name='Budget Curve',
    showlegend=False,
    yaxis='y2',
    hovertemplate='Week %{x}<br>Cost: %{text}%<extra></extra>',
    text=[f"{int(c)}" for c in cost_curve]
))

# Update layout
fig.update_layout(
    title={
        "text": "Digital Twin POC Project Timeline with Risk Assessment (24 weeks)<br><span style='font-size: 18px; font-weight: normal;'>Green=on-track | Yellow=caution | Red=at-risk | Dotted line=budget</span>"
    },
    xaxis=dict(
        title="Week Number",
        range=[0, 24],
        tickmode='linear',
        tick0=0,
        dtick=2,
    ),
    yaxis=dict(
        title="",
        categoryorder='array',
        categoryarray=df['Task'].tolist()[::-1]
    ),
    yaxis2=dict(
        overlaying='y',
        side='right',
        showticklabels=False,
        showgrid=False,
    ),
    barmode='overlay',
    hovermode='closest',
)

# Add phase separators and labels as annotations
phase_annotations = [
    {"phase": "DQ Phase", "start": 1, "end": 2, "y_pos": 14.5},
    {"phase": "Parallel", "start": 3, "end": 4, "y_pos": 11.5},
    {"phase": "IQ Phase", "start": 5, "end": 8, "y_pos": 9},
    {"phase": "OQ Phase", "start": 9, "end": 12, "y_pos": 5},
    {"phase": "PQ Phase", "start": 13, "end": 20, "y_pos": 1.5},
]

for i, phase in enumerate(phase_annotations):
    fig.add_vrect(
        x0=phase['start'], x1=phase['end'],
        fillcolor=['rgba(31,184,205,0.05)', 'rgba(46,139,87,0.05)', 'rgba(210,186,76,0.05)', 
                   'rgba(219,69,69,0.05)', 'rgba(93,135,143,0.05)'][i],
        layer='below',
        line_width=0,
    )

# Add decision gates as vertical lines
for week in [2, 8, 12, 20]:
    fig.add_vline(x=week, line_dash="dash", line_color="gray", line_width=1, opacity=0.5)

fig.update_traces(cliponaxis=False)

# Save the figure
fig.write_image("gantt_chart.png")
fig.write_image("gantt_chart.svg", format="svg")
