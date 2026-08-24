import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Persistent CSV path ──────────────────────────────────────────────────────
# Edits made in the app are saved here; on first run the hardcoded defaults are
# written to this file so subsequent sessions load user-saved data.
CSV_PATH = "data/properties.csv"

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rumah SelangorKu Comparison",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Header */
.main-header {
    background: linear-gradient(90deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    text-align: center;
}
.main-header h1 {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.main-header p {
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 0.5rem;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(30,27,75,0.8), rgba(49,46,129,0.6));
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(99,102,241,0.25);
}
.metric-label {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-value {
    color: #e2e8f0;
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 0.2rem;
}
.metric-sub {
    color: #6366f1;
    font-size: 0.8rem;
    font-weight: 500;
    margin-top: 0.1rem;
}

/* Section headers */
.section-header {
    color: #a78bfa;
    font-size: 1.2rem;
    font-weight: 700;
    border-left: 4px solid #6366f1;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem 0;
}

/* Property card */
.property-card {
    background: linear-gradient(135deg, rgba(15,12,41,0.9), rgba(48,43,99,0.7));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.property-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #a78bfa, #60a5fa);
}
.property-card:hover {
    border-color: rgba(99,102,241,0.6);
    box-shadow: 0 10px 40px rgba(99,102,241,0.2);
    transform: translateY(-2px);
}
.property-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
}
.property-price {
    font-size: 1.5rem;
    font-weight: 800;
    color: #34d399;
}
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-right: 0.3rem;
    margin-top: 0.3rem;
}
.badge-freehold { background: rgba(52,211,153,0.2); color: #34d399; border: 1px solid rgba(52,211,153,0.4); }
.badge-leasehold { background: rgba(251,191,36,0.2); color: #fbbf24; border: 1px solid rgba(251,191,36,0.4); }
.badge-developer { background: rgba(96,165,250,0.2); color: #60a5fa; border: 1px solid rgba(96,165,250,0.4); }
.badge-location { background: rgba(167,139,250,0.2); color: #a78bfa; border: 1px solid rgba(167,139,250,0.4); }
.badge-completion { background: rgba(249,115,22,0.2); color: #fb923c; border: 1px solid rgba(249,115,22,0.4); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,12,41,0.95), rgba(30,27,75,0.95)) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(30,27,75,0.5);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
    border-radius: 8px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #6366f1, #a78bfa) !important;
    color: white !important;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent);
    margin: 1.5rem 0;
}

/* Best pick banner */
.best-pick {
    background: linear-gradient(135deg, rgba(52,211,153,0.15), rgba(16,185,129,0.1));
    border: 1px solid rgba(52,211,153,0.4);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
}
.best-pick-title { color: #34d399; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; }
.best-pick-name { color: #e2e8f0; font-weight: 700; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# ─── Data helpers ─────────────────────────────────────────────────────────────
DEFAULT_DATA = {
    "Project Name": [
        "Aurum @ Bandar Sunway", "The Atera 2", "M Terra",
        "Residensi Rimba Flora", "The Avantro", "Residensi Ria", "Quayside Plaza",
    ],
    "Price (RM)": [265000, 270000, 250000, 270000, 250000, 250000, 250000],
    "Developer": [
        "Shayher Group", "Paramount Property", "Mah Sing",
        "Trinity Group", "Chin Hin", "Sime Darby", "Gamuda",
    ],
    "Title": ["Leasehold", "Leasehold", "Leasehold", "Freehold", "Freehold", "Freehold", "Leasehold"],
    "Size (sqft)": [550, 555, 550, 550, 550, 550, 549],
    "Price/sqft (RM)": [482, 486, 455, 491, 455, 455, 455],
    "Rooms": ["2", "2", "1+1", "2", "2", "2", "2"],
    "Bathroom": [
        "Separate bath & WC", "Attached bath & WC", "1 bath",
        "2 bath", "1 bath", "1 bath", "1 bath",
    ],
    "Completion": [
        "Q2 2030", "End 2027/Early 2028", "2028",
        "2028", "Jan 2028", "End 2027/Early 2028", "Oct 2026",
    ],
    "Location": [
        "Sunway", "Petaling Jaya", "Puchong",
        "Bandar Kinrara (near Pavilion Bkt Jalil)",
        "Bandar Kinrara (near Pavilion Bkt Jalil)",
        "Subang", "Kota Kemuning",
    ],
    "FOC": [
        "2 aircon + 1 heater",
        "Kitchen cabinet, countertop, hood & hob, shower screen, water heater",
        "None", "—", "—", "—", "—",
    ],
    "Units (RSK)": [734, None, None, 80, 208, 961, None],
    "Website": [
        "https://aurumbandarsunway.com/",
        "https://paramountproperty.my/developments/the-atera/the-atera-phase-2/",
        "https://mterra.com.my/",
        "https://rainfora.com.my/",
        "https://www.residensiwilayahpersekutuan.com/avantro-bandar-kinrara-puchong-rumah-selangor",
        "https://www.simedarbyproperty.com/sj7/",
        "https://www.gamudaland.com.my/developments/township/township/quayside-plazas-serviced-apartments",
    ],
}

def _derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add/refresh computed helper columns from editable fields."""
    df = df.copy()
    df["Rooms"] = df["Rooms"].astype(str).str.strip()
    df["Rooms_num"] = df["Rooms"].apply(lambda x: 2 if "1+1" in x else int(x) if x.isdigit() else 2)
    df["Bathrooms_num"] = df["Bathroom"].apply(lambda x: 2 if "2 bath" in str(x) else 1)
    completion_map = {
        "Q2 2030": 2030.25, "End 2027/Early 2028": 2027.75,
        "2028": 2028.0, "Jan 2028": 2028.0, "Oct 2026": 2026.75,
    }
    df["Completion_Year"] = df["Completion"].map(completion_map).fillna(2028.0)
    return df

def load_data() -> pd.DataFrame:
    """Load from saved CSV; fall back to hardcoded defaults on first run."""
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        os.makedirs("data", exist_ok=True)
        df = pd.DataFrame(DEFAULT_DATA)
        df.to_csv(CSV_PATH, index=False)
    return _derive_columns(df)

def save_data(df: pd.DataFrame):
    """Persist the editable columns back to CSV."""
    os.makedirs("data", exist_ok=True)
    editable_cols = [
        "Project Name", "Price (RM)", "Developer", "Title", "Size (sqft)",
        "Price/sqft (RM)", "Rooms", "Bathroom", "Completion", "Location",
        "FOC", "Units (RSK)", "Website",
    ]
    cols_to_save = [c for c in editable_cols if c in df.columns]
    df[cols_to_save].to_csv(CSV_PATH, index=False)

# ─── Session-state bootstrap ───────────────────────────────────────────────────
# Use session_state so in-memory edits survive Streamlit reruns within a session.
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# ─── Sidebar Filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:2rem'>🏠</div>
        <div style='color:#a78bfa; font-weight:700; font-size:1.1rem;'>Rumah SelangorKu</div>
        <div style='color:#64748b; font-size:0.8rem;'>Property Comparison Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("### 🔍 Filters")

    max_price = st.slider(
        "Max Price (RM)",
        min_value=200000, max_value=300000,
        value=300000, step=5000,
        format="RM %d",
    )

    title_filter = st.multiselect(
        "Land Title",
        options=["Freehold", "Leasehold"],
        default=["Freehold", "Leasehold"],
    )

    location_filter = st.multiselect(
        "Location",
        options=sorted(st.session_state.df["Location"].unique()),
        default=list(st.session_state.df["Location"].unique()),
    )

    st.divider()
    st.markdown("### ⚖️ Scoring Weights")
    st.caption("Adjust importance for your top pick recommendation")

    w_price = st.slider("Price (lower = better)", 0, 10, 8)
    w_psf = st.slider("Price/sqft (lower = better)", 0, 10, 7)
    w_title = st.slider("Freehold Bonus", 0, 10, 6)
    w_completion = st.slider("Earlier Completion", 0, 10, 5)
    w_foc = st.slider("FOC Items Bonus", 0, 10, 4)

# ─── Filter data ──────────────────────────────────────────────────────────────
_df = st.session_state.df
filtered = _df[
    (_df["Price (RM)"] <= max_price) &
    (_df["Title"].isin(title_filter)) &
    (_df["Location"].isin(location_filter))
].copy()

# ─── Scoring ──────────────────────────────────────────────────────────────────
if not filtered.empty:
    max_p = filtered["Price (RM)"].max()
    min_p = filtered["Price (RM)"].min()
    max_psf = filtered["Price/sqft (RM)"].max()
    min_psf = filtered["Price/sqft (RM)"].min()

    def score_row(row):
        price_range = max_p - min_p if max_p != min_p else 1
        psf_range = max_psf - min_psf if max_psf != min_psf else 1
        s_price = w_price * (1 - (row["Price (RM)"] - min_p) / price_range)
        s_psf = w_psf * (1 - (row["Price/sqft (RM)"] - min_psf) / psf_range)
        s_title = w_title if row["Title"] == "Freehold" else 0
        # Earlier completion = better score
        s_comp = w_completion * (1 - (row["Completion_Year"] - 2026) / 4)
        s_foc = w_foc if row["FOC"] not in ["None", "—", ""] else 0
        return round(s_price + s_psf + s_title + s_comp + s_foc, 2)

    filtered["Score"] = filtered.apply(score_row, axis=1)
    filtered = filtered.sort_values("Score", ascending=False).reset_index(drop=True)
    best = filtered.iloc[0]

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏠 Rumah SelangorKu Comparison</h1>
    <p>Affordable Housing Scheme · July 2026 Market Data · Selangor, Malaysia</p>
</div>
""", unsafe_allow_html=True)

if filtered.empty:
    st.warning("⚠️ No properties match your current filters. Please adjust the sidebar.")
    st.stop()

# ─── Top KPIs ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Projects Listed</div>
        <div class="metric-value">{len(filtered)}</div>
        <div class="metric-sub">of {len(st.session_state.df)} total</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Lowest Price</div>
        <div class="metric-value">RM {filtered["Price (RM)"].min():,.0f}</div>
        <div class="metric-sub">{filtered.loc[filtered["Price (RM)"].idxmin(),"Project Name"]}</div>
    </div>""", unsafe_allow_html=True)
with col3:
    avg_psf = filtered["Price/sqft (RM)"].mean()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Avg Price/sqft</div>
        <div class="metric-value">RM {avg_psf:.0f}</div>
        <div class="metric-sub">Range: {filtered["Price/sqft (RM)"].min()}–{filtered["Price/sqft (RM)"].max()}</div>
    </div>""", unsafe_allow_html=True)
with col4:
    fh = (filtered["Title"] == "Freehold").sum()
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Freehold Projects</div>
        <div class="metric-value">{fh}</div>
        <div class="metric-sub">{len(filtered)-fh} Leasehold</div>
    </div>""", unsafe_allow_html=True)
with col5:
    earliest = filtered.loc[filtered["Completion_Year"].idxmin(), "Project Name"]
    earliest_date = filtered["Completion"].iloc[filtered["Completion_Year"].values.argmin()]
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Earliest Completion</div>
        <div class="metric-value">{earliest_date}</div>
        <div class="metric-sub">{earliest[:20]}...</div>
    </div>""", unsafe_allow_html=True)

# ─── Best Pick ────────────────────────────────────────────────────────────────
st.markdown(f"""<div class="best-pick">
    <div class="best-pick-title">🏆 Top Pick (Based on Your Weights)</div>
    <div class="best-pick-name">{best["Project Name"]}</div>
    <div style='color:#94a3b8; font-size:0.85rem; margin-top:0.3rem;'>
        RM {best["Price (RM)"]:,} · {best["Title"]} · {best["Location"]} · Score: {best["Score"]:.1f} pts
    </div>
</div>""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Property Cards", "📊 Charts", "📈 Comparison Table", "🗺️ Location Map", "✏️ Edit Data"])

# ── Tab 1: Property Cards ──
with tab1:
    st.markdown('<div class="section-header">All Properties</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (_, row) in enumerate(filtered.iterrows()):
        title_cls = "freehold" if row["Title"] == "Freehold" else "leasehold"
        rank_emoji = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
        foc_html = f'<div style="color:#fbbf24;font-size:0.8rem;margin-top:0.5rem;">🎁 FOC: {row["FOC"]}</div>' if row["FOC"] not in ["None","—",""] else ""

        # Use components.html so <a href> tags are NOT stripped — renders in a real iframe
        card_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
          * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
          body {{ background: transparent; padding: 4px 2px 8px 2px; }}
          .card {{
            background: linear-gradient(135deg, rgba(15,12,41,0.95), rgba(48,43,99,0.85));
            border: 1px solid rgba(99,102,241,0.3);
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            position: relative;
            overflow: hidden;
            transition: box-shadow 0.3s ease;
          }}
          .card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #a78bfa, #60a5fa);
          }}
          .top-row {{ display:flex; justify-content:space-between; align-items:flex-start; }}
          .rank {{ color:#6366f1; font-size:0.75rem; font-weight:700; }}
          .name {{ color:#e2e8f0; font-size:1rem; font-weight:700; margin-top:2px; }}
          .price {{ color:#34d399; font-size:1.3rem; font-weight:800; text-align:right; }}
          .psf  {{ color:#94a3b8; font-size:0.72rem; text-align:right; }}
          .badges {{ margin-top:0.7rem; }}
          .badge {{
            display:inline-block; padding:0.18rem 0.55rem;
            border-radius:999px; font-size:0.68rem; font-weight:600;
            margin-right:0.3rem; margin-top:0.3rem;
          }}
          .freehold  {{ background:rgba(52,211,153,0.2);  color:#34d399; border:1px solid rgba(52,211,153,0.4); }}
          .leasehold {{ background:rgba(251,191,36,0.2);  color:#fbbf24; border:1px solid rgba(251,191,36,0.4); }}
          .dev       {{ background:rgba(96,165,250,0.2);  color:#60a5fa; border:1px solid rgba(96,165,250,0.4); }}
          .loc       {{ background:rgba(167,139,250,0.2); color:#a78bfa; border:1px solid rgba(167,139,250,0.4); }}
          .comp      {{ background:rgba(249,115,22,0.2);  color:#fb923c; border:1px solid rgba(249,115,22,0.4); }}
          .details {{ color:#94a3b8; font-size:0.78rem; margin-top:0.55rem; }}
          .footer {{
            margin-top:0.75rem; padding-top:0.55rem;
            border-top:1px solid rgba(99,102,241,0.18);
            display:flex; justify-content:space-between; align-items:center;
          }}
          .score {{ color:#a78bfa; font-size:0.78rem; font-weight:600; }}
          .website-link {{
            color:#60a5fa; font-size:0.75rem; text-decoration:none;
            font-weight:500; transition: color 0.2s;
          }}
          .website-link:hover {{ color:#93c5fd; }}
        </style>
        </head>
        <body>
          <div class="card">
            <div class="top-row">
              <div>
                <div class="rank">{rank_emoji} RANK #{i+1}</div>
                <div class="name">{row["Project Name"]}</div>
              </div>
              <div>
                <div class="price">RM {row["Price (RM)"]:,}</div>
                <div class="psf">RM {row["Price/sqft (RM)"]}/sqft</div>
              </div>
            </div>
            <div class="badges">
              <span class="badge {title_cls}">{row["Title"]}</span>
              <span class="badge dev">{row["Developer"]}</span>
              <span class="badge loc">📍 {row["Location"].split("(")[0].strip()}</span>
              <span class="badge comp">🗓 {row["Completion"]}</span>
            </div>
            <div class="details">
              🛏 {row["Rooms"]} Rooms &nbsp;|&nbsp; 🚿 {row["Bathroom"]} &nbsp;|&nbsp; 📐 {row["Size (sqft)"]} sqft
            </div>
            {foc_html}
            <div class="footer">
              <div class="score">⭐ Score: {row["Score"]:.1f} pts</div>
              <a class="website-link" href="{row["Website"]}" target="_blank">🔗 Website →</a>
            </div>
          </div>
        </body>
        </html>
        """
        with cols[i % 2]:
            # height auto-sizes to card content; scrolling=False removes iframe scrollbar
            components.html(card_html, height=270, scrolling=False)

# ── Tab 2: Charts ──
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">Price per sqft Comparison</div>', unsafe_allow_html=True)
        colors = ["#6366f1" if row["Title"] == "Leasehold" else "#34d399" for _, row in filtered.iterrows()]
        fig1 = px.bar(
            filtered, x="Project Name", y="Price/sqft (RM)",
            color="Title",
            color_discrete_map={"Freehold": "#34d399", "Leasehold": "#6366f1"},
            text="Price/sqft (RM)",
            template="plotly_dark",
        )
        fig1.update_traces(texttemplate='RM %{text}', textposition='outside')
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#e2e8f0"),
            xaxis=dict(tickangle=-30, gridcolor="rgba(99,102,241,0.1)"),
            yaxis=dict(gridcolor="rgba(99,102,241,0.1)"),
            margin=dict(t=20, b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Score Ranking</div>', unsafe_allow_html=True)
        fig2 = px.bar(
            filtered.sort_values("Score"),
            x="Score", y="Project Name",
            orientation="h",
            color="Score",
            color_continuous_scale=["#312e81", "#6366f1", "#a78bfa", "#34d399"],
            text="Score",
            template="plotly_dark",
        )
        fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#e2e8f0"),
            xaxis=dict(gridcolor="rgba(99,102,241,0.1)"),
            yaxis=dict(gridcolor="rgba(99,102,241,0.1)"),
            margin=dict(t=20, b=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="section-header">Price vs Completion Year</div>', unsafe_allow_html=True)
        fig3 = px.scatter(
            filtered,
            x="Completion_Year", y="Price (RM)",
            size="Price/sqft (RM)", color="Title",
            hover_name="Project Name",
            hover_data={"Completion_Year": False, "Completion": True, "Developer": True},
            color_discrete_map={"Freehold": "#34d399", "Leasehold": "#6366f1"},
            template="plotly_dark",
            size_max=40,
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#e2e8f0"),
            xaxis=dict(gridcolor="rgba(99,102,241,0.1)", title="Est. Completion Year"),
            yaxis=dict(gridcolor="rgba(99,102,241,0.1)", tickprefix="RM "),
            margin=dict(t=20, b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Freehold vs Leasehold Split</div>', unsafe_allow_html=True)
        title_counts = filtered["Title"].value_counts()
        fig4 = px.pie(
            names=title_counts.index,
            values=title_counts.values,
            color=title_counts.index,
            color_discrete_map={"Freehold": "#34d399", "Leasehold": "#6366f1"},
            hole=0.55,
            template="plotly_dark",
        )
        fig4.update_traces(
            textposition='outside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#0f0c29', width=3)),
        )
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#e2e8f0"),
            margin=dict(t=20, b=10),
            showlegend=False,
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Radar chart for top 3
    st.markdown('<div class="section-header">Radar: Top 3 Picks</div>', unsafe_allow_html=True)
    top3 = filtered.head(3)
    categories = ["Value for $", "PSF Score", "Freehold", "Early Completion", "FOC"]

    fig5 = go.Figure()
    colors_radar = ["#6366f1", "#34d399", "#f59e0b"]
    fills_radar  = ["rgba(99,102,241,0.15)", "rgba(52,211,153,0.15)", "rgba(245,158,11,0.15)"]

    for idx, (_, row) in enumerate(top3.iterrows()):
        max_p = filtered["Price (RM)"].max(); min_p = filtered["Price (RM)"].min()
        max_psf = filtered["Price/sqft (RM)"].max(); min_psf = filtered["Price/sqft (RM)"].min()
        p_range = max_p - min_p if max_p != min_p else 1
        psf_range = max_psf - min_psf if max_psf != min_psf else 1
        values = [
            round(10 * (1 - (row["Price (RM)"] - min_p) / p_range), 1),
            round(10 * (1 - (row["Price/sqft (RM)"] - min_psf) / psf_range), 1),
            10 if row["Title"] == "Freehold" else 4,
            round(10 * (1 - (row["Completion_Year"] - 2026) / 4), 1),
            10 if row["FOC"] not in ["None", "—", ""] else 2,
        ]
        fig5.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=row["Project Name"][:22],
            line=dict(color=colors_radar[idx], width=2),
            fillcolor=fills_radar[idx],
        ))

    fig5.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(99,102,241,0.2)", tickfont=dict(color="#64748b")),
            angularaxis=dict(gridcolor="rgba(99,102,241,0.2)", linecolor="rgba(99,102,241,0.3)"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#e2e8f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h"),
        margin=dict(t=30, b=10),
        height=400,
    )
    st.plotly_chart(fig5, use_container_width=True)

# ── Tab 3: Comparison Table ──
with tab3:
    st.markdown('<div class="section-header">Full Comparison Table</div>', unsafe_allow_html=True)
    display_cols = ["Project Name", "Price (RM)", "Developer", "Title", "Size (sqft)",
                    "Price/sqft (RM)", "Rooms", "Bathroom", "Completion", "Location", "FOC", "Score"]
    tbl = filtered[display_cols].copy()
    tbl["Price (RM)"] = tbl["Price (RM)"].apply(lambda x: f"RM {x:,}")
    tbl["Price/sqft (RM)"] = tbl["Price/sqft (RM)"].apply(lambda x: f"RM {x}")
    tbl["Score"] = tbl["Score"].apply(lambda x: f"{x:.1f} ⭐")
    st.dataframe(
        tbl.style.set_properties(**{
            "background-color": "rgba(15,12,41,0.5)",
            "color": "#e2e8f0",
        }).highlight_max(subset=[], color="transparent"),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown('<div class="section-header">Feature-by-Feature Matrix</div>', unsafe_allow_html=True)
    matrix_data = {
        "Feature": ["Price", "Land Title", "Rooms", "Bathrooms", "Completion", "FOC Items", "Score"],
    }
    for _, row in filtered.iterrows():
        name = row["Project Name"].split("@")[0].strip()[:18]
        foc_val = "✅ Yes" if row["FOC"] not in ["None", "—", ""] else "❌ No"
        bath_val = "🟢 2" if row["Bathrooms_num"] == 2 else "🔵 1"
        matrix_data[name] = [
            f"RM {row['Price (RM)']:,}",
            "🟢 Freehold" if row["Title"] == "Freehold" else "🟡 Leasehold",
            f"🛏 {row['Rooms']}",
            bath_val,
            row["Completion"],
            foc_val,
            f"⭐ {row['Score']:.1f}",
        ]
    matrix_df = pd.DataFrame(matrix_data)
    st.dataframe(matrix_df, use_container_width=True, hide_index=True)

# ── Tab 4: Location ──
with tab4:
    st.markdown('<div class="section-header">Project Locations</div>', unsafe_allow_html=True)

    # Rough coordinates for locations
    location_coords = {
        "Sunway": (3.0723, 101.6040),
        "Petaling Jaya": (3.1073, 101.6067),
        "Puchong": (3.0276, 101.6185),
        "Bandar Kinrara (near Pavilion Bkt Jalil)": (3.0598, 101.6851),
        "Subang": (3.1085, 101.5770),
        "Kota Kemuning": (2.9951, 101.5524),
    }

    map_data = []
    for _, row in filtered.iterrows():
        loc = row["Location"]
        coord_key = next((k for k in location_coords if k.startswith(loc.split("(")[0].strip())), None)
        if coord_key:
            lat, lon = location_coords[coord_key]
            map_data.append({
                "Project": row["Project Name"],
                "lat": lat + (hash(row["Project Name"]) % 100) * 0.001,
                "lon": lon + (hash(row["Developer"]) % 100) * 0.001,
                "Price": f"RM {row['Price (RM)']:,}",
                "Score": row["Score"],
                "Title": row["Title"],
            })

    map_df = pd.DataFrame(map_data)
    if not map_df.empty:
        fig_map = px.scatter_mapbox(
            map_df,
            lat="lat", lon="lon",
            hover_name="Project",
            hover_data={"Price": True, "Score": True, "Title": True, "lat": False, "lon": False},
            color="Score",
            size=[20] * len(map_df),
            color_continuous_scale=["#312e81", "#6366f1", "#34d399"],
            zoom=11,
            center={"lat": 3.05, "lon": 101.62},
            mapbox_style="carto-darkmatter",
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#e2e8f0"),
            margin=dict(t=0, b=0, l=0, r=0),
            height=500,
        )
        st.plotly_chart(fig_map, use_container_width=True)

    st.markdown('<div class="section-header">Distance to Key Areas</div>', unsafe_allow_html=True)
    dist_data = {
        "Project": [r["Project Name"] for _, r in filtered.iterrows()],
        "Location": [r["Location"].split("(")[0].strip() for _, r in filtered.iterrows()],
        "Near Pavilion BJ": ["✅ Yes" if "Kinrara" in r["Location"] else "⬜" for _, r in filtered.iterrows()],
        "Near LRT/MRT": ["🟢 Close" if r["Location"] in ["Sunway","Petaling Jaya","Puchong"] else "🟡 Moderate" for _, r in filtered.iterrows()],
        "Within Private Dev": [
            "✅ Same block" if "same block" in r.get("FOC","").lower() or "same" in str(r.get("Units (RSK)","")).lower() else "ℹ️ Separate"
            for _, r in filtered.iterrows()
        ],
    }
    st.dataframe(pd.DataFrame(dist_data), use_container_width=True, hide_index=True)

# ── Tab 5: Edit Data ──
with tab5:
    st.markdown('<div class="section-header">✏️ Edit Property Dataset</div>', unsafe_allow_html=True)
    st.caption(
        "Add, edit, or remove rows below. Click **💾 Save Changes** to persist to CSV and refresh all charts. "
        "Use **🔄 Reset to Defaults** to restore the original 7 properties."
    )

    EDITABLE_COLS = [
        "Project Name", "Price (RM)", "Developer", "Title",
        "Size (sqft)", "Price/sqft (RM)", "Rooms", "Bathroom",
        "Completion", "Location", "FOC", "Units (RSK)", "Website",
    ]
    edit_df = st.session_state.df[[c for c in EDITABLE_COLS if c in st.session_state.df.columns]].copy()

    edited = st.data_editor(
        edit_df,
        num_rows="dynamic",          # allows adding & deleting rows
        use_container_width=True,
        hide_index=True,
        column_config={
            "Project Name":    st.column_config.TextColumn("Project Name",    required=True, width="large"),
            "Price (RM)":      st.column_config.NumberColumn("Price (RM)",     min_value=0,   format="RM %d"),
            "Developer":       st.column_config.TextColumn("Developer",        width="medium"),
            "Title":           st.column_config.SelectboxColumn("Title",       options=["Freehold", "Leasehold"], required=True),
            "Size (sqft)":     st.column_config.NumberColumn("Size (sqft)",    min_value=0,   format="%d sqft"),
            "Price/sqft (RM)": st.column_config.NumberColumn("Price/sqft (RM)",min_value=0,   format="RM %d"),
            "Rooms":           st.column_config.TextColumn("Rooms",            help="e.g. 2 or 1+1"),
            "Bathroom":        st.column_config.TextColumn("Bathroom"),
            "Completion":      st.column_config.TextColumn("Completion",       help="e.g. Q2 2030, Oct 2026"),
            "Location":        st.column_config.TextColumn("Location"),
            "FOC":             st.column_config.TextColumn("FOC",              help="Free items; use — if none"),
            "Units (RSK)":     st.column_config.NumberColumn("Units (RSK)",    min_value=0,   format="%d units"),
            "Website":         st.column_config.LinkColumn("Website",          display_text="🔗 Open"),
        },
        key="data_editor",
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 3])

    with btn_col1:
        if st.button("💾 Save Changes", type="primary", use_container_width=True):
            if edited.empty or edited["Project Name"].isnull().all():
                st.error("Dataset cannot be empty — please keep at least one row.")
            else:
                new_df = _derive_columns(edited.dropna(subset=["Project Name"]))
                st.session_state.df = new_df
                save_data(new_df)
                st.success("✅ Changes saved! All charts have been updated.")
                st.rerun()

    with btn_col2:
        csv_bytes = edit_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_bytes,
            file_name="Rumah_SelangorKu_properties.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with btn_col3:
        with st.expander("🔄 Reset to original defaults", expanded=False):
            st.warning("This will discard **all edits** and restore the original 7 properties.")
            if st.button("⚠️ Yes, reset now", type="secondary"):
                if os.path.exists(CSV_PATH):
                    os.remove(CSV_PATH)
                st.session_state.df = load_data()
                st.success("✅ Reset to defaults.")
                st.rerun()

    st.divider()
    st.markdown('<div class="section-header">📋 Current Dataset Preview</div>', unsafe_allow_html=True)
    st.caption(f"{len(st.session_state.df)} properties in dataset · Click any cell above to edit · \u2795 Add rows with the ＋ button at the bottom of the table")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="divider"></div>
<div style='text-align:center; color:#475569; font-size:0.78rem; padding: 1rem 0 2rem;'>
    📊 Data sourced from Rumah SelangorKu Comparison · July 2026 &nbsp;|&nbsp;
    🎓 UC Berkeley ML/AI Certification Program &nbsp;|&nbsp;
    Built with Streamlit &amp; Plotly
</div>
""", unsafe_allow_html=True)
