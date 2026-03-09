import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scraper.rekrute import scrape_rekrute
from scraper.emploima import scrape_emploima
from database.db_handler import save_offers, load_offers, count_offers
from analysis.skills import extract_skills

DB_PATH = os.path.join(ROOT, "data", "jobs.db")

st.set_page_config(page_title="Data Jobs · Maroc", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

# SVG removed — hero is now full-width with ticker

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#F2EFE9!important;font-family:'Geist',sans-serif!important;color:#1C1C1C!important;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;}
.block-container{max-width:1320px!important;padding:0 3rem 5rem!important;margin:0 auto!important;}
.nav{display:flex;align-items:center;justify-content:space-between;padding:1.8rem 0 1.5rem;border-bottom:1px solid rgba(0,0,0,0.09);margin-bottom:0;}
.nav-logo{font-family:'Instrument Serif',serif;font-size:1.2rem;color:#1C1C1C;letter-spacing:-0.02em;}
.nav-logo .dot{color:#8B6914;}
.nav-status{display:flex;align-items:center;gap:0.5rem;background:#fff;border:1px solid rgba(0,0,0,0.09);border-radius:100px;padding:0.45rem 1rem;font-size:0.72rem;font-weight:500;color:#555;letter-spacing:0.06em;text-transform:uppercase;}
.nav-dot{width:6px;height:6px;border-radius:50%;background:#22C55E;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.4;}}
.hero-eyebrow{display:inline-flex;align-items:center;gap:0.5rem;font-size:0.73rem;font-weight:600;color:#8B6914;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1.3rem;}
.hero-h1{font-family:'Instrument Serif',serif;font-size:clamp(2.8rem,4.5vw,4.2rem);font-weight:400;color:#0D0D0D;line-height:1.08;letter-spacing:-0.03em;margin-bottom:1.3rem;}
.hero-h1 em{font-style:italic;color:#8B6914;}
.hero-desc{font-size:0.97rem;color:#6B6B6B;font-weight:300;line-height:1.75;max-width:460px;}
.stat-row{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid rgba(0,0,0,0.09);border-radius:20px;overflow:hidden;background:rgba(0,0,0,0.06);gap:1px;margin-bottom:3rem;}
.stat-cell{background:#F2EFE9;padding:2rem 2.2rem;transition:background 0.18s;}
.stat-cell:hover{background:#EAE6DE;}
.stat-icon{width:32px;height:32px;background:rgba(139,105,20,0.1);border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:1rem;color:#8B6914;}
.stat-num{font-family:'Instrument Serif',serif;font-size:2.6rem;color:#0D0D0D;line-height:1;letter-spacing:-0.03em;margin-bottom:0.35rem;}
.stat-lbl{font-size:0.72rem;font-weight:600;color:#999;text-transform:uppercase;letter-spacing:0.1em;}
.section-label{display:flex;align-items:center;gap:0.6rem;font-size:0.68rem;font-weight:700;color:#AAA;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:1.4rem;}
.section-label::after{content:'';flex:1;height:1px;background:rgba(0,0,0,0.08);}
.chart-wrap{background:#FFFFFF;border:1px solid rgba(0,0,0,0.08);border-radius:18px;padding:1.8rem 1.8rem 1.2rem;margin-bottom:1rem;}
.chart-title{font-family:'Geist',sans-serif;font-size:0.82rem;font-weight:600;color:#1C1C1C;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1.2rem;display:flex;align-items:center;gap:0.5rem;}
[data-testid="stTextInput"] input{background:#F8F6F2!important;border:1px solid rgba(0,0,0,0.1)!important;border-radius:10px!important;color:#1C1C1C!important;font-family:'Geist',sans-serif!important;font-size:0.875rem!important;box-shadow:none!important;transition:border-color 0.15s!important;}
[data-testid="stTextInput"] input:focus{border-color:#8B6914!important;box-shadow:0 0 0 3px rgba(139,105,20,0.08)!important;outline:none!important;}
[data-testid="stSelectbox"]>div>div{background:#F8F6F2!important;border:1px solid rgba(0,0,0,0.1)!important;border-radius:10px!important;color:#1C1C1C!important;font-family:'Geist',sans-serif!important;font-size:0.875rem!important;box-shadow:none!important;}
[data-testid="stTextInput"] label,[data-testid="stSelectbox"] label{font-size:0.72rem!important;font-weight:600!important;color:#888!important;text-transform:uppercase!important;letter-spacing:0.09em!important;}
[data-testid="stButton"] button{background:#1C1C1C!important;color:#F2EFE9!important;border:none!important;border-radius:10px!important;font-family:'Geist',sans-serif!important;font-weight:500!important;font-size:0.82rem!important;letter-spacing:0.02em!important;padding:0.65rem 1.4rem!important;transition:all 0.15s!important;box-shadow:0 1px 4px rgba(0,0,0,0.18)!important;}
[data-testid="stButton"] button:hover{background:#333!important;transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(0,0,0,0.16)!important;}
.results-bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.2rem;padding-bottom:1rem;border-bottom:1px solid rgba(0,0,0,0.07);}
.results-count{font-size:0.82rem;color:#888;}
.results-count strong{color:#1C1C1C;font-weight:600;}
.job-card{background:#FFFFFF;border:1px solid rgba(0,0,0,0.08);border-radius:16px;padding:1.5rem 1.8rem;margin-bottom:0.7rem;transition:all 0.18s cubic-bezier(0.4,0,0.2,1);}
.job-card:hover{border-color:rgba(139,105,20,0.35);box-shadow:0 6px 28px rgba(0,0,0,0.06);transform:translateY(-2px);}
.job-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.3rem;}
.job-title{font-family:'Instrument Serif',serif;font-size:1.08rem;color:#0D0D0D;line-height:1.3;letter-spacing:-0.01em;}
.job-source{font-size:0.68rem;font-weight:600;color:#AAA;text-transform:uppercase;letter-spacing:0.1em;margin-top:0.15rem;}
.job-company{font-size:0.83rem;font-weight:500;color:#8B6914;margin-bottom:0.75rem;display:flex;align-items:center;gap:0.3rem;}
.chips{display:flex;flex-wrap:wrap;gap:0.4rem;margin-bottom:0.85rem;}
.chip{display:inline-flex;align-items:center;gap:0.28rem;padding:0.25rem 0.7rem;border-radius:7px;font-size:0.72rem;font-weight:500;}
.chip-city{background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;}
.chip-contract{background:#F0FDF4;color:#15803D;border:1px solid #BBF7D0;}
.chip-exp{background:#FFFBEB;color:#B45309;border:1px solid #FDE68A;}
.chip-date{background:#F9FAFB;color:#4B5563;border:1px solid #E5E7EB;}
.job-desc{font-size:0.82rem;color:#6B6B6B;line-height:1.68;margin-bottom:1rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.job-link{display:inline-flex;align-items:center;gap:0.35rem;font-size:0.78rem;font-weight:500;color:#1C1C1C;text-decoration:none;padding:0.4rem 0.9rem;border-radius:8px;border:1px solid rgba(0,0,0,0.12);background:transparent;transition:all 0.15s;}
.job-link:hover{background:#1C1C1C;color:#F2EFE9;border-color:#1C1C1C;}
.divider{height:1px;background:rgba(0,0,0,0.07);margin:2.5rem 0;}
.footer{margin-top:5rem;padding-top:2rem;border-top:1px solid rgba(0,0,0,0.08);display:flex;justify-content:space-between;align-items:center;}
.footer-l{font-family:'Instrument Serif',serif;font-size:0.95rem;color:#AAA;}
.footer-r{font-size:0.73rem;color:#BBB;letter-spacing:0.05em;}
.ticker-wrap{overflow:hidden;border-top:1px solid rgba(0,0,0,0.07);border-bottom:1px solid rgba(0,0,0,0.07);padding:0.9rem 0;margin-bottom:0;background:transparent;}
.ticker-track{white-space:nowrap;}
.ticker-content{display:inline-block;font-size:0.82rem;font-weight:400;color:#888;letter-spacing:0.02em;animation:ticker 40s linear infinite;}
.ticker-content:hover{animation-play-state:paused;}
@keyframes ticker{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}
</style>
""", unsafe_allow_html=True)

# Load data
try:
    df = load_offers(DB_PATH)
except Exception:
    df = pd.DataFrame()

total     = len(df)
companies = df["company"].nunique() if not df.empty else 0
cities_n  = df["location"].nunique() if not df.empty else 0
top_city  = df["location"].value_counts().index[0] if not df.empty and df["location"].notna().any() else "—"
top_city_short = top_city.split(",")[0].strip()

# NAV
st.markdown("""
<div class="nav">
  <div class="nav-logo">DataJobs <span class="dot">·</span> Maroc</div>
  <div class="nav-status"><div class="nav-dot"></div>Live · Rekrute & Emploi.ma</div>
</div>
""", unsafe_allow_html=True)

# HERO — full width with ticker
ticker_items = [
    "Data Scientist", "Data Analyst", "Data Engineer", "Business Intelligence",
    "Machine Learning Engineer", "Power BI Developer", "SQL Developer",
    "AI Engineer", "Data Ops", "NLP Engineer", "MLOps Engineer",
    "Analytics Manager", "Data Architect", "BI Consultant"
]

# If we have real data, use real titles
if not df.empty:
    real_titles = df["title"].dropna().head(20).tolist()
    if len(real_titles) >= 6:
        ticker_items = real_titles + ticker_items

ticker_text = "  ·  ".join(ticker_items)
ticker_doubled = ticker_text + "  ·  " + ticker_text  # duplicate for seamless loop

st.markdown(f"""
<div style="padding:3.5rem 0 2rem;">
  <div class="hero-eyebrow">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <circle cx="7" cy="7" r="6" stroke="#8B6914" stroke-width="1.5"/>
      <circle cx="7" cy="7" r="2.5" fill="#8B6914"/>
    </svg>
    Marché Data · Maroc · 2025
  </div>
  <h1 class="hero-h1">Toutes les offres<br><em>Data, IA &amp; BI</em><br>en un seul endroit.</h1>
  <p class="hero-desc">Agrégateur d'offres en temps réel scrappées depuis Rekrute.com &amp; Emploi.ma.
  Analysez les tendances, filtrez par ville ou contrat, et identifiez les entreprises
  qui recrutent dans la Data au Maroc.</p>
</div>

<div class="ticker-wrap">
  <div class="ticker-track">
    <span class="ticker-content">{ticker_doubled}</span>
  </div>
</div>

<div style="height:1px;background:rgba(0,0,0,0.08);margin:2.5rem 0 3rem;"></div>
""", unsafe_allow_html=True)

# STATS
st.markdown(f"""
<div class="stat-row">
  <div class="stat-cell">
    <div class="stat-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="1" y="8" width="3" height="7" rx="1" fill="#8B6914"/><rect x="6" y="5" width="3" height="10" rx="1" fill="#8B6914" opacity="0.7"/><rect x="11" y="2" width="3" height="13" rx="1" fill="#8B6914" opacity="0.4"/></svg></div>
    <div class="stat-num">{total}</div>
    <div class="stat-lbl">Offres totales</div>
  </div>
  <div class="stat-cell">
    <div class="stat-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="6" width="12" height="9" rx="2" stroke="#8B6914" stroke-width="1.5"/><path d="M5 6V4a3 3 0 016 0v2" stroke="#8B6914" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="stat-num">{companies}</div>
    <div class="stat-lbl">Entreprises</div>
  </div>
  <div class="stat-cell">
    <div class="stat-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1.5C5.5 1.5 3.5 3.5 3.5 6c0 3.5 4.5 8.5 4.5 8.5S12.5 9.5 12.5 6c0-2.5-2-4.5-4.5-4.5z" stroke="#8B6914" stroke-width="1.5"/><circle cx="8" cy="6" r="1.5" fill="#8B6914"/></svg></div>
    <div class="stat-num">{cities_n}</div>
    <div class="stat-lbl">Villes</div>
  </div>
  <div class="stat-cell">
    <div class="stat-icon"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="#8B6914" stroke-width="1.5"/><path d="M8 5v3l2 2" stroke="#8B6914" stroke-width="1.5" stroke-linecap="round"/></svg></div>
    <div class="stat-num" style="font-size:1.7rem">{top_city_short}</div>
    <div class="stat-lbl">Ville #1</div>
  </div>
</div>
""", unsafe_allow_html=True)

# SCRAPE BUTTON
col_btn, col_status = st.columns([1, 4])
with col_btn:
    if st.button("↻  Actualiser les offres"):
        with st.spinner("Scraping en cours…"):
            offers = scrape_rekrute(max_pages=5) + scrape_emploima(max_pages=5)
            new    = save_offers(offers, DB_PATH)
            st.success(f"{new} nouvelles offres ajoutées.")
            st.rerun()

if df.empty:
    st.info("Aucune donnée. Clique sur **Actualiser les offres** pour commencer.")
    st.stop()

with col_status:
    last = pd.to_datetime(df["date_scraped"]).max()
    st.markdown(f'<div style="padding-top:0.65rem;font-size:0.78rem;color:#AAA;">Dernière mise à jour : {last.strftime("%d %b %Y · %H:%M")}</div>', unsafe_allow_html=True)

GOLD  = "#8B6914"
DARK  = "#1C1C1C"
FONT  = "Geist, sans-serif"
LAYOUT = dict(paper_bgcolor="white", plot_bgcolor="white",
              font=dict(family=FONT, color="#444", size=11),
              margin=dict(l=8, r=16, t=16, b=8), height=290)

st.markdown('<div class="section-label">Compétences les plus demandées</div>', unsafe_allow_html=True)

skills_count = extract_skills(df)
skills_df = pd.DataFrame(list(skills_count.items()), columns=["Compétence", "Offres"])
skills_df = skills_df[skills_df["Offres"] > 0].sort_values("Offres", ascending=False)

if not skills_df.empty:
    fig = go.Figure(go.Bar(
        x=skills_df["Offres"],
        y=skills_df["Compétence"],
        orientation="h",
        marker=dict(color="#8B6914"),
        hovertemplate="<b>%{y}</b><br>%{x} offres<extra></extra>"
    ))
    fig.update_layout(**LAYOUT,
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#333"), gridcolor="rgba(0,0,0,0)"),
        xaxis=dict(tickfont=dict(size=10, color="#777"), gridcolor="rgba(0,0,0,0.06)", zeroline=False)
    )
    fig.update_layout(height=500)
    st.markdown('<div class="chart-wrap"><div class="chart-title">Top compétences · toutes offres</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
    
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# CHARTS
st.markdown('<div class="section-label">Analyse du marché</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    d = df["location"].replace("", pd.NA).dropna().value_counts().head(7).reset_index()
    d.columns = ["Ville", "Offres"]
    fig = go.Figure(go.Bar(x=d["Offres"], y=d["Ville"], orientation="h",
                           marker=dict(color=DARK, opacity=0.85),
                           hovertemplate="<b>%{y}</b><br>%{x} offres<extra></extra>"))
    fig.update_layout(**LAYOUT,
                      yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#333"), gridcolor="rgba(0,0,0,0)"),
                      xaxis=dict(tickfont=dict(size=10, color="#777"), gridcolor="rgba(0,0,0,0.06)", zeroline=False))
    st.markdown('<div class="chart-wrap"><div class="chart-title">Villes qui recrutent</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    d = df["company"].replace("", pd.NA).dropna().value_counts().head(7).reset_index()
    d.columns = ["Entreprise", "Offres"]
    fig = go.Figure(go.Bar(x=d["Offres"], y=d["Entreprise"], orientation="h",
                           marker=dict(color=GOLD),
                           hovertemplate="<b>%{y}</b><br>%{x} offres<extra></extra>"))
    fig.update_layout(**LAYOUT,
                      yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#333"), gridcolor="rgba(0,0,0,0)"),
                      xaxis=dict(tickfont=dict(size=10, color="#777"), gridcolor="rgba(0,0,0,0.06)", zeroline=False))
    st.markdown('<div class="chart-wrap"><div class="chart-title">Top entreprises</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)
PALETTE = ["#1C1C1C","#8B6914","#C9A84C","#4B4B4B","#787878","#A0A0A0","#D4C4A0"]

with c3:
    ct = df["contract_type"].replace("", pd.NA).dropna().value_counts().reset_index()
    ct.columns = ["Contrat", "Offres"]
    if not ct.empty:
        fig = go.Figure(go.Pie(labels=ct["Contrat"], values=ct["Offres"], hole=0.58,
                               marker=dict(colors=PALETTE),
                               textfont=dict(family=FONT, size=10, color="#333"),
                               hovertemplate="<b>%{label}</b><br>%{value} offres (%{percent})<extra></extra>"))
        fig.update_layout(**LAYOUT, legend=dict(font=dict(size=10, color="#555")))
        st.markdown('<div class="chart-wrap"><div class="chart-title">Types de contrats</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

with c4:
    exp = df["experience"].replace("", pd.NA).dropna().value_counts().reset_index()
    exp.columns = ["Expérience", "Offres"]
    if not exp.empty:
        colors = [DARK if i == 0 else f"rgba(28,28,28,{max(0.25, 0.75 - i*0.12)})" for i in range(len(exp))]
        fig = go.Figure(go.Bar(x=exp["Expérience"], y=exp["Offres"],
                               marker=dict(color=colors),
                               hovertemplate="<b>%{x}</b><br>%{y} offres<extra></extra>"))
        fig.update_layout(**LAYOUT,
                          xaxis=dict(tickfont=dict(size=9, color="#555"), gridcolor="rgba(0,0,0,0)", tickangle=-20),
                          yaxis=dict(tickfont=dict(size=10, color="#777"), gridcolor="rgba(0,0,0,0.06)", zeroline=False))
        st.markdown('<div class="chart-wrap"><div class="chart-title">Expérience requise</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# FILTERS
st.markdown('<div class="section-label">Offres d\'emploi</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns([3, 2, 2])
with f1:
    search = st.text_input("Recherche", placeholder="Data Analyst, Python, Power BI…")
with f2:
    city_opts = ["Toutes les villes"] + sorted(df["location"].dropna().replace("", pd.NA).dropna().unique().tolist())
    city_filter = st.selectbox("Ville", city_opts)
with f3:
    ct_opts = ["Tous les contrats"] + sorted(df["contract_type"].dropna().replace("", pd.NA).dropna().unique().tolist())
    ct_filter = st.selectbox("Type de contrat", ct_opts)

filtered = df.copy()
if search:
    mask = (filtered["title"].str.contains(search, case=False, na=False) |
            filtered["company"].str.contains(search, case=False, na=False) |
            filtered["description"].str.contains(search, case=False, na=False))
    filtered = filtered[mask]
if city_filter != "Toutes les villes":
    filtered = filtered[filtered["location"].str.contains(city_filter, case=False, na=False)]
if ct_filter != "Tous les contrats":
    filtered = filtered[filtered["contract_type"] == ct_filter]

st.markdown(f'<div class="results-bar"><div class="results-count"><strong>{len(filtered)}</strong> offres trouvées</div></div>', unsafe_allow_html=True)

# JOB CARDS
for _, row in filtered.iterrows():
    city = str(row.get("location","") or "")
    contract = str(row.get("contract_type","") or "")
    exp = str(row.get("experience","") or "")
    date = str(row.get("date_posted","") or "")
    desc = str(row.get("description","") or "")
    company = str(row.get("company","") or "")
    title = str(row.get("title","") or "")
    url = str(row.get("url","#") or "#")
    chips = ""
    if city and city != "nan": chips += f'<span class="chip chip-city">📍 {city}</span>'
    if contract and contract != "nan": chips += f'<span class="chip chip-contract">{contract}</span>'
    if exp and exp != "nan": chips += f'<span class="chip chip-exp">{exp}</span>'
    if date and date != "nan": chips += f'<span class="chip chip-date">{date}</span>'
    desc_block = f'<div class="job-desc">{desc[:220]}{"…" if len(desc)>220 else ""}</div>' if desc and desc != "nan" else ""
    co_block = f'<div class="job-company">{company}</div>' if company and company != "nan" else ""
    st.markdown(f"""
<div class="job-card">
  <div class="job-top"><div class="job-title">{title}</div><div class="job-source">{row.get("source", "")}</div></div>
  {co_block}
  <div class="chips">{chips}</div>
  {desc_block}
  <a class="job-link" href="{url}" target="_blank">Voir l'offre →</a>
</div>
""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
  <div class="footer-l">DataJobs · Maroc</div>
  <div class="footer-r">Adam El Ouarga · Projet Portfolio · 2025</div>
</div>
""", unsafe_allow_html=True)