"""
Premium glassmorphism + animated aurora theme for Health Hub PRO.
Inject once per page via `inject_theme()`.
"""
import streamlit as st

_AURORA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root{
  --glass-bg: rgba(255,255,255,0.06);
  --glass-brd: rgba(255,255,255,0.14);
  --glass-shadow: 0 8px 32px rgba(8,6,30,0.45);
  --primary:#7c5cff;
  --secondary:#ff6ec7;
  --accent:#34e7c8;
  --text:#eef0ff;
  --muted:#a9adc9;
}

/* Base canvas ---------------------------------------------------------- */
html, body, [data-testid="stAppViewContainer"]{
  background: #060617;
  color: var(--text);
  font-family: 'Inter', system-ui, sans-serif;
}
h1,h2,h3,h4,.stMarkdown h1,.stMarkdown h2,.stMarkdown h3{
  font-family: 'Sora', sans-serif !important;
  color: var(--text) !important;
  letter-spacing:-0.02em;
}

/* Animated aurora blobs behind everything ------------------------------ */
[data-testid="stAppViewContainer"]::before{
  content:"";
  position:fixed; inset:-20% -10% -10% -10%;
  z-index:0;
  background:
    radial-gradient(38% 42% at 18% 22%, rgba(124,92,255,0.55) 0%, transparent 60%),
    radial-gradient(34% 38% at 82% 26%, rgba(255,110,199,0.45) 0%, transparent 60%),
    radial-gradient(40% 45% at 50% 88%, rgba(52,231,200,0.40) 0%, transparent 60%),
    radial-gradient(30% 30% at 78% 78%, rgba(255,179,71,0.30) 0%, transparent 60%);
  filter: blur(70px) saturate(140%);
  animation: auroraMove 22s ease-in-out infinite alternate;
  pointer-events:none;
}
[data-testid="stAppViewContainer"]::after{
  content:"";
  position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(1200px 600px at 50% -10%, rgba(255,255,255,0.05), transparent 70%);
}
@keyframes auroraMove{
  0%   { transform: translate3d(0,0,0) rotate(0deg) scale(1); }
  50%  { transform: translate3d(2%, -2%,0) rotate(8deg) scale(1.08); }
  100% { transform: translate3d(-2%, 2%,0) rotate(-6deg) scale(1.04); }
}

/* Lift real content above the aurora ---------------------------------- */
.main .block-container{
  position:relative; z-index:1;
  padding-top:2.2rem; max-width:1180px;
}
[data-testid="stHeader"]{ background:transparent; }

/* Sidebar as frosted glass -------------------------------------------- */
[data-testid="stSidebar"]{
  background: rgba(12,10,32,0.55);
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
  border-right:1px solid var(--glass-brd);
}
[data-testid="stSidebar"] *{ color: var(--text); }

/* Reusable glass surface ---------------------------------------------- */
.glass{
  background: var(--glass-bg);
  border:1px solid var(--glass-brd);
  border-radius:22px;
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(18px) saturate(160%);
  -webkit-backdrop-filter: blur(18px) saturate(160%);
  padding:26px 28px;
  position:relative; overflow:hidden;
  transition: transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s;
}
.glass::before{
  content:""; position:absolute; inset:0; border-radius:inherit;
  padding:1px; background:linear-gradient(135deg, rgba(255,255,255,.4), transparent 40%);
  -webkit-mask:linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite:xor; mask-composite:exclude; opacity:.5; pointer-events:none;
}
.glass:hover{ transform: translateY(-6px); box-shadow:0 18px 50px rgba(124,92,255,0.35); }

/* Hero header ---------------------------------------------------------- */
.hero{
  background: linear-gradient(135deg, rgba(124,92,255,0.30), rgba(255,110,199,0.20));
  border:1px solid var(--glass-brd);
  border-radius:28px; padding:38px 40px; margin-bottom:26px;
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  box-shadow: var(--glass-shadow); position:relative; overflow:hidden;
}
.hero h1{ font-size:2.5rem; margin:0 0 .35rem 0;
  background:linear-gradient(90deg,#fff,#c9b8ff 40%,#ffb3e6);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;}
.hero p{ color:var(--muted); font-size:1.05rem; margin:0; }
.hero .pill{ display:inline-block; margin-top:14px; padding:6px 16px; border-radius:999px;
  font-size:.8rem; font-weight:600; color:#fff;
  background:rgba(255,255,255,0.12); border:1px solid var(--glass-brd); }

/* Feature / stat cards ------------------------------------------------- */
.feature-grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:18px; }
.fcard{ background:var(--glass-bg); border:1px solid var(--glass-brd); border-radius:20px;
  padding:22px; backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
  transition:transform .3s, box-shadow .3s; }
.fcard:hover{ transform:translateY(-5px); box-shadow:0 14px 40px rgba(255,110,199,0.28); }
.fcard .ico{ font-size:1.9rem; }
.fcard h3{ margin:.5rem 0 .25rem; font-size:1.15rem; }
.fcard p{ color:var(--muted); margin:0; font-size:.92rem; }

/* Streamlit widgets ---------------------------------------------------- */
.stButton>button, .stFormSubmitButton>button{
  background:linear-gradient(135deg,var(--primary),var(--secondary));
  color:#fff; border:none; border-radius:14px; padding:.6rem 1.2rem;
  font-weight:600; transition:transform .2s, box-shadow .2s;
  box-shadow:0 6px 18px rgba(124,92,255,0.35);
}
.stButton>button:hover, .stFormSubmitButton>button:hover{
  transform:translateY(-2px); box-shadow:0 10px 26px rgba(255,110,199,0.45); color:#fff;
}
[data-testid="stMetric"]{
  background:var(--glass-bg); border:1px solid var(--glass-brd);
  border-radius:18px; padding:16px 18px; backdrop-filter:blur(14px);
}
[data-testid="stMetricValue"]{ color:var(--text)!important; }
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"]>div, .stChatInput textarea{
  background:rgba(255,255,255,0.06)!important; color:var(--text)!important;
  border:1px solid var(--glass-brd)!important; border-radius:12px!important;
}
.stTabs [data-baseweb="tab-list"]{ gap:8px; }
.stTabs [data-baseweb="tab"]{
  background:var(--glass-bg); border:1px solid var(--glass-brd);
  border-radius:12px; padding:8px 18px; color:var(--muted);
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,var(--primary),var(--secondary))!important; color:#fff!important;
}
.streamlit-expanderHeader, [data-testid="stExpander"]{
  background:var(--glass-bg); border:1px solid var(--glass-brd); border-radius:16px;
}
.stAlert{ border-radius:14px; backdrop-filter:blur(10px); }

/* Chat bubbles --------------------------------------------------------- */
.msg-user{ background:linear-gradient(135deg,var(--primary),var(--secondary)); color:#fff;
  padding:14px 18px; border-radius:18px 18px 4px 18px; margin:10px 0 10px 18%;
  box-shadow:0 6px 20px rgba(124,92,255,0.35); animation:fadeUp .4s ease; }
.msg-ai{ background:var(--glass-bg); border:1px solid var(--glass-brd); color:var(--text);
  padding:14px 18px; border-radius:18px 18px 18px 4px; margin:10px 18% 10px 0;
  border-left:3px solid var(--accent); backdrop-filter:blur(14px); animation:fadeUp .4s ease; }
.msg-user b, .msg-ai b{ opacity:.8; font-size:.8rem; }
@keyframes fadeUp{ from{opacity:0; transform:translateY(10px);} to{opacity:1; transform:translateY(0);} }
.pulse{ animation:pulse 1.4s infinite; display:inline-block; }
@keyframes pulse{ 0%,100%{transform:scale(1);} 50%{transform:scale(1.18);} }

/* AI Coach — conversation history ------------------------------------- */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{ gap:.55rem; }

.hist-card{
  background:var(--glass-bg); border:1px solid var(--glass-brd);
  border-radius:16px; padding:12px 14px 10px;
  backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px);
  transition:transform .25s, box-shadow .25s, border-color .25s;
}
.hist-card:hover{ transform:translateY(-2px); border-color:rgba(124,92,255,.55);
  box-shadow:0 8px 22px rgba(124,92,255,.28); }
.hist-card.active{ border-color:transparent;
  background:linear-gradient(135deg,rgba(124,92,255,.32),rgba(255,110,199,.22));
  box-shadow:0 8px 24px rgba(124,92,255,.30); }
.hist-row{ display:flex; align-items:center; gap:9px; }
.hist-ico{ width:26px;height:26px;border-radius:9px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:.85rem;
  background:linear-gradient(135deg,var(--primary),var(--secondary)); }
.hist-title{ font-weight:600; font-size:.9rem; color:var(--text);
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.hist-preview{ color:var(--muted); font-size:.78rem; margin:7px 0 6px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;
  overflow:hidden; line-height:1.35; }
.hist-meta{ color:var(--muted); font-size:.7rem; opacity:.85;
  display:flex; gap:7px; align-items:center; }
.hist-meta .dot{ width:3px;height:3px;border-radius:50%;background:currentColor; }

/* Subtle ghost buttons inside the sidebar (history actions) ------------ */
[data-testid="stSidebar"] .stButton>button{
  background:rgba(255,255,255,0.05); border:1px solid var(--glass-brd);
  box-shadow:none; color:var(--text); font-weight:500;
}
[data-testid="stSidebar"] .stButton>button:hover{
  background:rgba(124,92,255,0.22); border-color:rgba(124,92,255,.55);
  transform:translateY(-1px); box-shadow:0 6px 16px rgba(124,92,255,.3); color:#fff;
}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{
  background:linear-gradient(135deg,var(--primary),var(--secondary));
  border:none; color:#fff; box-shadow:0 6px 18px rgba(124,92,255,.35);
}

#MainMenu, footer{ visibility:hidden; }
</style>
"""


def inject_theme() -> None:
    """Inject the aurora glass theme. Call at the top of every page."""
    st.markdown(_AURORA_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "", pill: str = "") -> None:
    """Render a glass hero header."""
    pill_html = f'<span class="pill">{pill}</span>' if pill else ""
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p>{pill_html}</div>',
        unsafe_allow_html=True,
    )
