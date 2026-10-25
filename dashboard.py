import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(page_title="COP โฮมสุขพลัส สาขาเซกา", page_icon="🏦",
                   layout="wide", initial_sidebar_state="collapsed")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================================================
# HELPERS
# =====================================================
def safe_load_image(filename):
    stem, ext = os.path.splitext(filename)
    for e in [ext, ".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]:
        path = os.path.join(BASE_DIR, stem + e)
        if os.path.exists(path):
            try:
                return Image.open(path)
            except Exception:
                return None
    return None

def html(s):
    st.markdown(s, unsafe_allow_html=True)

def show_img(filename, caption=None):
    img = safe_load_image(filename)
    if img is None:
        html(f'<div class="img-ph">🖼️ ยังไม่พบไฟล์ <code>{filename}</code></div>')
        return
    try:
        st.image(img, caption=caption, use_container_width=True)
    except TypeError:
        st.image(img, caption=caption, use_column_width=True)

def section_head(eyebrow, title, sub=""):
    html(f'<div class="sec"><span class="eyebrow">{eyebrow}</span>'
         f'<div class="sec-title">{title}</div><div class="sec-sub">{sub}</div></div>')

def kpi_grid(items):
    cards = "".join(
        f'<div class="kpi"><div class="kpi-ic">{ic}</div><div class="kpi-lb">{lb}</div>'
        f'<div class="kpi-val">{v}</div><div class="kpi-dl">{d}</div></div>'
        for ic, lb, v, d in items)
    html(f'<div class="kpi-grid">{cards}</div>')

def info_card(tag, title, items, extra=""):
    lis = "".join(f"<li>{i}</li>" for i in items)
    html(f'<div class="card"><span class="chip">{tag}</span>'
         f'<div class="card-title">{title}</div><ul class="card-list">{lis}</ul>{extra}</div>')

def feature_row(img_file, tag, title, items, caption=None, reverse=False):
    if reverse:
        txt_col, img_col = st.columns([1.85, 1.15])
    else:
        img_col, txt_col = st.columns([1.15, 1.85])
    with img_col:
        show_img(img_file, caption)
    with txt_col:
        info_card(tag, title, items)
    html('<div class="spacer"></div>')

def chat_preview(label, filename, caption):
    with st.expander(label, expanded=False):
        _, mid, _ = st.columns([1, 1.3, 1])
        with mid:
            show_img(filename, caption)

def page_hero(badge, title_html, sub):
    html(f'<div class="hero hero-sm"><div class="hero-inner">'
         f'<span class="hero-badge">{badge}</span>'
         f'<div class="hero-title hero-title-sm">{title_html}</div>'
         f'<div class="hero-sub">{sub}</div></div></div>')

def style_fig(fig, h=380):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Prompt", color="#cbd5e1"), height=h,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", y=1.15, x=1, xanchor="right"))
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.1)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.1)", zeroline=False)
    return fig

NEON_SEQ = ["#38bdf8", "#818cf8", "#ec4899", "#34d399", "#f59e0b", "#a78bfa"]
PLOT_CFG = {"displayModeBar": False}

# =====================================================
# CSS
# =====================================================
html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
.stApp {
  background:
    radial-gradient(1100px 600px at 10% -10%, rgba(56,189,248,0.13), transparent 60%),
    radial-gradient(900px 500px at 95% 5%, rgba(236,72,153,0.10), transparent 60%),
    #070b19;
  color:#f3f4f6; font-family:'Prompt', sans-serif;
}
.stApp p, .stApp li, .stApp label, .stApp button, .stApp input, .stApp h1, .stApp h2, .stApp h3 { font-family:'Prompt', sans-serif; }
#MainMenu, footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none; }
.block-container { padding-top:1.2rem; padding-bottom:3rem; max-width:1280px; }

.brand { display:flex; align-items:center; gap:10px; margin-top:4px; }
.logo { width:38px; height:38px; border-radius:50%; background:linear-gradient(90deg,#38bdf8 50%,#ec4899 50%); box-shadow:0 0 18px rgba(56,189,248,0.45); }
.brand-txt b { display:block; color:#f8fafc; font-size:16px; line-height:1.2; }
.brand-txt span { color:#94a3b8; font-size:12px; }

div[role="radiogroup"] {
  display:flex; flex-wrap:wrap; justify-content:center; gap:6px; width:fit-content; margin:0 auto;
  background:rgba(15,23,42,0.7); border:1px solid rgba(56,189,248,0.18);
  border-radius:999px; padding:6px; backdrop-filter:blur(12px); box-shadow:0 8px 30px rgba(0,0,0,0.35);
}
div[role="radiogroup"] label { padding:8px 18px !important; border-radius:999px; margin:0 !important; cursor:pointer; transition:all .25s ease; }
div[role="radiogroup"] label > div:first-child { display:none; }
div[role="radiogroup"] label:hover { background:rgba(56,189,248,0.10); }
div[role="radiogroup"] label:has(input:checked) { background:linear-gradient(135deg,#0284c7,#2563eb); box-shadow:0 0 18px rgba(37,99,235,0.5); }
div[role="radiogroup"] label p { color:#cbd5e1; font-size:14px; margin:0; }
div[role="radiogroup"] label:has(input:checked) p { color:#fff; font-weight:500; }

.cta-wrap { text-align:right; margin-top:4px; }
.cta { display:inline-block; padding:10px 22px; border-radius:999px; background:#f8fafc; color:#070b19 !important; font-weight:600; font-size:14px; text-decoration:none !important; transition:.25s; }
.cta:hover { box-shadow:0 0 24px rgba(56,189,248,0.6); transform:translateY(-2px); }

.hero { position:relative; min-height:600px; padding:90px 20px 60px; text-align:center; border-radius:32px; overflow:hidden; margin-top:18px; border:1px solid rgba(56,189,248,0.10); background:rgba(10,16,36,0.55); }
.hero-inner { position:relative; z-index:2; }
.hero-sm { min-height:auto; padding:50px 20px 40px; }
.hero-badge { display:inline-block; padding:6px 16px; border-radius:999px; background:rgba(56,189,248,0.10); border:1px solid rgba(56,189,248,0.3); color:#7dd3fc; font-size:13px; }
.hero-title { font-size:clamp(2.3rem,5vw,4.4rem); font-weight:700; line-height:1.3; color:#f8fafc; margin:20px 0 14px; }
.hero-title-sm { font-size:clamp(1.8rem,3.6vw,3rem); }
.grad { background:linear-gradient(90deg,#38bdf8,#818cf8,#ec4899); -webkit-background-clip:text; background-clip:text; color:transparent; }
.muted { color:rgba(148,163,184,0.45); }
.hero-sub { color:#94a3b8; font-size:17px; max-width:640px; margin:0 auto 30px; line-height:1.7; }

.sec { text-align:center; margin:46px 0 22px; }
.eyebrow { display:inline-block; padding:4px 14px; border-radius:999px; font-size:12px; color:#f9a8d4; background:rgba(236,72,153,0.10); border:1px solid rgba(236,72,153,0.3); }
.sec-title { font-size:clamp(1.6rem,3vw,2.3rem); font-weight:700; color:#f8fafc; margin-top:10px; }
.sec-sub { color:#94a3b8; font-size:15px; margin-top:4px; }

.kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:16px; margin:6px 0 26px; }
.kpi { background:linear-gradient(160deg,rgba(30,41,59,0.75),rgba(15,23,42,0.75)); border:1px solid rgba(56,189,248,0.18); border-radius:22px; padding:20px 22px; transition:.3s; }
.kpi:hover { transform:translateY(-5px); border-color:rgba(56,189,248,0.55); box-shadow:0 0 32px rgba(56,189,248,0.18); }
.kpi-ic { width:42px; height:42px; border-radius:13px; display:grid; place-items:center; background:rgba(56,189,248,0.12); font-size:20px; margin-bottom:12px; }
.kpi-lb { color:#94a3b8; font-size:14px; }
.kpi-val { color:#f8fafc; font-size:28px; font-weight:700; margin:2px 0; text-shadow:0 0 14px rgba(56,189,248,0.35); }
.kpi-dl { color:#34d399; font-size:13px; }

.card { background:rgba(15,23,42,0.65); border:1px solid rgba(56,189,248,0.15); border-radius:24px; padding:26px 28px; backdrop-filter:blur(10px); }
.chip { display:inline-block; padding:4px 12px; border-radius:999px; font-size:12px; background:rgba(56,189,248,0.10); color:#7dd3fc; border:1px solid rgba(56,189,248,0.3); margin-bottom:10px; }
.card-title { font-size:21px; font-weight:600; color:#e0f2fe; margin-bottom:10px; }
.card-list { margin:0; padding-left:0; list-style:none; }
.card-list li { padding:9px 0 9px 26px; border-bottom:1px dashed rgba(148,163,184,0.15); color:#cbd5e1; position:relative; line-height:1.6; }
.card-list li:last-child { border-bottom:none; }
.card-list li::before { content:""; position:absolute; left:4px; top:18px; width:8px; height:8px; border-radius:50%; background:#38bdf8; box-shadow:0 0 8px #38bdf8; }
.card-list b { color:#38bdf8; }
.spacer { height:30px; }

.tl { display:grid; gap:10px; }
.tl-item { display:flex; gap:16px; align-items:center; background:rgba(15,23,42,0.6); border:1px solid rgba(56,189,248,0.14); border-radius:16px; padding:12px 16px; transition:.25s; }
.tl-date { min-width:64px; text-align:center; border-radius:12px; padding:6px 0; color:#fff; background:linear-gradient(135deg,#0284c7,#7c3aed); }
.tl-date b { display:block; font-size:22px; line-height:1.1; }
.tl-date span { font-size:11px; opacity:.85; }
.tl-place { color:#f1f5f9; font-weight:500; }
.tl-sub { color:#94a3b8; font-size:13px; }

[data-testid="stPlotlyChart"], .stPlotlyChart { background:rgba(15,23,42,0.55); border:1px solid rgba(56,189,248,0.15); border-radius:22px; padding:10px; }
[data-testid="stDataFrame"] { border:1px solid rgba(56,189,248,0.2); border-radius:16px; overflow:hidden; }
[data-baseweb="select"] > div { background:rgba(15,23,42,0.85) !important; border-radius:14px !important; border-color:rgba(56,189,248,0.3) !important; }
.stSelectbox label p { color:#7dd3fc !important; }

.footer { margin-top:56px; padding:24px; border-radius:22px; background:rgba(15,23,42,0.6); border:1px solid rgba(56,189,248,0.12); display:flex; flex-wrap:wrap; gap:14px 36px; justify-content:center; color:#94a3b8; font-size:14px; }
</style>
""")

# =====================================================
# TOP NAVIGATION
# =====================================================
nav_l, nav_c, nav_r = st.columns([1.3, 3.4, 1.3])
with nav_l:
    html('<div class="brand"><div class="logo"></div><div class="brand-txt">'
         '<b>ธ.ก.ส. สาขาเซกา</b><span>COP ชุมชนโฮมสุขพลัส</span></div></div>')
with nav_c:
    page = st.radio("เมนู", ["🏠 ภาพรวม", "📈 ดอกเบี้ย 15 เดือน", "💰 รายได้ FBI", "💳 Digital", "📱 Line OA"],
                    horizontal=True, label_visibility="collapsed")
with nav_r:
    html('<div class="cta-wrap"><a class="cta" href="tel:042489050">ติดต่อสาขา ↗</a></div>')

# =====================================================
# DATA
# =====================================================
records = [
    [2569, "ก.ย.", "โสกก่าม", "บ้านยางเรียน", 52, 64, 1018],
    [2569, "ก.ย.", "ป่งไฮ", "บ้านโชคชัย", 30, 36, 917],
    [2569, "ก.ย.", "น้ำจั้น", "บ้านเหล่าคาม", 30, 22, 894],
    [2569, "ก.ย.", "เซกา", "บ้านสายปัญญา", 40, 33, 896],
    [2569, "ก.ย.", "เซกา", "บ้านท่าสำราญ", 20, 12, 1795],
    [2569, "ก.ย.", "ท่าสะอาด", "บ้านปากท่อ", 50, 45, 1635],
    [2569, "ก.ย.", "หนองทุ่ม", "บ้านหนองทุ่ม", 15, 12, 0],
    [2569, "ก.ย.", "บ้านต้อง", "-", 0, 0, 0],
    [2569, "ก.ย.", "ท่ากกแดง", "-", 0, 0, 0],
    [2569, "ก.ย.", "ซาง", "-", 0, 0, 0],
]
df = pd.DataFrame(records, columns=["ปี", "เดือน", "ตำบล", "จุดบริการ", "ลูกค้า", "รายการ", "FBI"])
active = df[df["จุดบริการ"] != "-"]

fbi_cols = ["เดือน", "หมวด 1", "หมวด 2", "หมวด 3", "หมวด 4", "หมวด 5", "รวมรายได้ (บาท)"]
fbi_data = pd.DataFrame([
    ["มิ.ย. 69", 530443.30, 171220.00, 120085.33, 80657.73,  6000.00,  908406.36],
    ["ก.ค. 69", 797497.43, 220310.00, 161184.70, 136966.96, 8000.00,  1323959.09],
    ["ส.ค. 69", 1063963.33, 266710.00, 208727.37, 182600.77, 10000.00, 1732001.47],
    ["ก.ย. 69", 1293946.82, 344040.00, 256581.91, 222629.03, 12000.00, 2129197.76],
], columns=fbi_cols)

schedule = [
    ("14", "บ้านยางเรียน ม.3", "ต.โสกก่าม"),
    ("15", "บ้านโชคชัย ม.10", "ต.ป่งไฮ"),
    ("16", "บ้านเหล่าคาม ม.4", "ต.น้ำจั้น"),
    ("17", "บ้านสายปัญญา ม.8", "ต.เซกา"),
    ("18", "บ้านท่าสำราญ ม.2", "ต.ซาง"),
    ("25", "บ้านป่าก่อ ม.10", "ต.ท่าสะอาด"),
    ("28", "บ้านหนองหิ้ง ม.2", "ต.ท่ากกแดง"),
    ("29", "บ้านหนองทุ่มใต้ ม.12", "ต.หนองทุ่ม"),
]

# =====================================================
# PAGE 1 : ภาพรวม (มีเรดาร์แผนที่และตัวเลือกตำบล)
# =====================================================
if page == "🏠 ภาพรวม":
    section_head("OVERVIEW", "สรุปผลการดำเนินงานภาพรวม สาขาเซกา", "ข้อมูลอัปเดตเป็นปัจจุบัน (ปีบัญชี 2569)")
    kpi_grid([
        ("📱", "ธุรกรรม Digital (Mobile)", "630,143 รายการ", "ยอดสะสมถึง 15 ต.ค. 69"),
        ("💰", "รายได้ FBI สะสมรวม", "2,129,197.76 ฿", "ยอดสะสมถึง ก.ย. 69"),
        ("👥", "เพื่อน Line OA สาขา", "168 คน", "ทะลุเป้าหมาย 166 คน 🟢"),
        ("📍", "จุดบริการชุมชนโฮมสุข", f"{len(active)} จุด", "ครอบคลุมพื้นที่ 9 ตำบล"),
    ])

    # กราฟแนวตั้งยอดรวมรายได้ FBI รายเดือน
    section_head("FBI TREND", "ภาพรวมยอดรวมรายได้ FBI (รายเดือน)", "เปรียบเทียบการเติบโตสะสมในแต่ละเดือนอย่างชัดเจน")
    f_total_overview = go.Figure(go.Bar(
        x=fbi_data["เดือน"], y=fbi_data["รวมรายได้ (บาท)"],
        marker=dict(color=fbi_data["รวมรายได้ (บาท)"], colorscale="Teal", showscale=False, line=dict(color="#38bdf8", width=2)),
        text=[f"{v:,.2f} ฿" for v in fbi_data["รวมรายได้ (บาท)"]], textposition="outside"
    ))
    f_total_overview.update_layout(title="ยอดรวมรายได้ FBI สะสม (บาท)", showlegend=False)
    style_fig(f_total_overview, 400).update_yaxes(range=[0, fbi_data["รวมรายได้ (บาท)"].max() * 1.18])
    st.plotly_chart(f_total_overview, use_container_width=True, config=PLOT_CFG)

    # -----------------------------------------------------
    # ส่วนแผนที่เรดาร์และตัวเลือกตำบล
    # -----------------------------------------------------
    section_head("AREA INSIGHT", "เรดาร์แผนที่ 3D และข้อมูลรายตำบล", "เลือกตำบลเพื่อดูสถานะจุดบริการและรายละเอียดในพื้นที่")
    
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        tambon_list = ["ทั้งหมด", "เซกา", "โสกก่าม", "ซาง", "ท่ากกแดง", "ท่าสะอาด", "น้ำจั้น", "บ้านต้อง", "ป่งไฮ", "หนองทุ่ม"]
        sel = st.selectbox("📍 เลือกตำบลเป้าหมาย", tambon_list)

    filtered = df if sel == "ทั้งหมด" else df[df["ตำบล"] == sel]
    
    col_map, col_info = st.columns([1.3, 1.7])
    with col_map:
        st.subheader("🗺️ แผนที่โซนพื้นที่ 3D")
        img_map = safe_load_image("map_seka.png")
        w, h = img_map.size if img_map else (1000, 1000)
        pts = {
            "ต.บ้านต้อง": (685, 255), "ต.โสกก่าม": (910, 305), "ต.น้ำจั้น": (530, 335),
            "ต.เซกา": (775, 475), "ต.ท่าสะอาด": (290, 520), "ต.ป่งไฮ": (485, 520),
            "ต.หนองทุ่ม": (560, 615), "ต.ซาง": (860, 690), "ต.ท่ากกแดง": (430, 620),
        }
        target = f"ต.{sel}" if sel != "ทั้งหมด" else None
        names = list(pts.keys())
        fig = go.Figure()
        if img_map:
            fig.add_layout_image(dict(source=img_map, xref="x", yref="y", x=0, y=h,
                                      sizex=w, sizey=h, sizing="stretch", layer="below"))
        fig.add_trace(go.Scatter(
            x=[p[0] for p in pts.values()], y=[h - p[1] for p in pts.values()],
            mode="markers+text", text=names, textposition="top center",
            textfont=dict(color="#e2e8f0", size=11),
            marker=dict(size=[22 if n == target else 13 for n in names],
                        color=["#ec4899" if n == target else "#38bdf8" for n in names],
                        line=dict(width=2, color="#ffffff"))))
        fig.update_xaxes(visible=False, range=[0, w])
        fig.update_yaxes(visible=False, range=[0, h], scaleanchor="x")
        style_fig(fig, 460).update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True, config=PLOT_CFG)
        st.markdown("🔹 *จุดเรืองแสงสีชมพูคือตำแหน่งที่เลือก*")

    with col_info:
        st.subheader(f"📊 รายงานสถานะ: ตำบล{sel}")
        m1, m2, m3 = st.columns(3)
        m1.metric("ลูกค้ารวม", f"{int(filtered['ลูกค้า'].sum()):,} ราย")
        m2.metric("จำนวนรายการ", f"{int(filtered['รายการ'].sum()):,}")
        m3.metric("รายได้ FBI", f"{int(filtered['FBI'].sum()):,} ฿")

        st.markdown("### 📋 ฐานข้อมูลจุดบริการย่อย")
        show = filtered[filtered["จุดบริการ"] != "-"][["จุดบริการ", "ลูกค้า", "รายการ", "FBI"]]
        if show.empty:
            info_card("แจ้งเตือน", f"ยังไม่มีจุดบริการย่อยในตำบล{sel}", ["รอข้อมูลการออกหน่วยรอบถัดไป"])
        else:
            st.dataframe(show, use_container_width=True, hide_index=True)

    section_head("PERFORMANCE", "สัดส่วนและเปรียบเทียบรายได้ FBI รายตำบล", "ข้อมูลเชิงวิเคราะห์จากจุดบริการย่อยในพื้นที่")
    c1, c2 = st.columns(2)
    with c1:
        summ = df.groupby("ตำบล", as_index=False)["FBI"].sum().sort_values("FBI", ascending=False)
        fb = px.bar(summ, x="ตำบล", y="FBI", text_auto=",")
        fb.update_traces(marker_color="#38bdf8", marker_line_color="#7dd3fc", marker_line_width=1)
        st.plotly_chart(style_fig(fb), use_container_width=True, config=PLOT_CFG)
    with c2:
        fp = px.pie(active[active["FBI"] > 0], names="จุดบริการ", values="FBI", hole=0.62,
                    color_discrete_sequence=NEON_SEQ)
        st.plotly_chart(style_fig(fp), use_container_width=True, config=PLOT_CFG)

# =====================================================
# PAGE 2 : ดอกเบี้ย 15 เดือน
# =====================================================
elif page == "📈 ดอกเบี้ย 15 เดือน":
    page_hero("📈 KPI เจาะลึก", 'ดอกเบี้ย <span class="grad">15 เดือน</span>',
              "วิเคราะห์สถิติอัตราดอกเบี้ยและผลสัมฤทธิ์รายเดือน")

    months_i = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค.",
                "ม.ค. (ปีถัดไป)", "ก.พ. (ปีถัดไป)", "มี.ค. (ปีถัดไป)"]
    rates = [3.2, 3.4, 3.5, 3.8, 4.0, 4.2, 4.1, 4.3, 4.5, 4.6, 4.8, 5.0, 5.1, 5.3, 5.5]
    di = pd.DataFrame({"เดือน": months_i, "อัตราดอกเบี้ย (%)": rates})

    kpi_grid([
        ("📊", "อัตราเฉลี่ยรวม", f"{sum(rates)/len(rates):.2f}%", "▲ +0.4% จากงวดก่อน"),
        ("🚀", "สูงสุด (Peak)", f"{max(rates):.2f}%", "มี.ค. (ปีถัดไป)"),
        ("🎯", "สถานะเป้าหมาย", "ผ่านเกณฑ์", "🟢 เติบโตต่อเนื่อง"),
    ])

    section_head("TREND", "แนวโน้มอัตราดอกเบี้ย")
    fm = go.Figure()
    fm.add_trace(go.Bar(x=di["เดือน"], y=di["อัตราดอกเบี้ย (%)"], name="อัตรา (%)",
                        marker_color="rgba(56,189,248,0.55)", marker_line_color="#38bdf8", marker_line_width=1))
    fm.add_trace(go.Scatter(x=di["เดือน"], y=di["อัตราดอกเบี้ย (%)"], name="แนวโน้ม",
                            mode="lines+markers", line=dict(color="#ec4899", width=3, shape="spline"),
                            marker=dict(size=8, color="#fff")))
    st.plotly_chart(style_fig(fm, 420), use_container_width=True, config=PLOT_CFG)

# =====================================================
# PAGE 3 : รายได้ FBI
# =====================================================
elif page == "💰 รายได้ FBI":
    page_hero("💰 KPI เจาะลึก · รายงาน FBI",
              'รายได้ค่าบริการและค่าธรรมเนียม (<span class="grad">FBI</span>)',
              "เปรียบเทียบผลงานรายได้สะสมรายหมวด สาขาเซกา (มิถุนายน – กันยายน 2569)")

    latest_fbi = fbi_data.iloc[-1]
    prev_fbi = fbi_data.iloc[-2]
    diff_fbi = latest_fbi["รวมรายได้ (บาท)"] - prev_fbi["รวมรายได้ (บาท)"]

    kpi_grid([
        ("💰", "รายได้รวมล่าสุด (ก.ย. 69)", f"{latest_fbi['รวมรายได้ (บาท)']:,.2f} ฿", f"▲ +{diff_fbi:,.2f} ฿ จากสิงหาคม"),
        ("📈", "หมวด 1 สูงสุด", f"{latest_fbi['หมวด 1']:,.2f} ฿", "สัดส่วนหลักของสาขา"),
        ("⚡", "อัตราเติบโต (ก.ค.-ก.ย.)", "ทะลุ 2.1 ล้านบาท", "🟢 บรรลุเป้าหมายสะสม"),
    ])

    section_head("TOTAL TREND", "ภาพรวมยอดรวมรายได้ FBI (รายเดือน)", "เปรียบเทียบการเติบโตสะสมในแต่ละเดือนอย่างชัดเจน")
    f_total = go.Figure(go.Bar(
        x=fbi_data["เดือน"], y=fbi_data["รวมรายได้ (บาท)"],
        marker=dict(color=fbi_data["รวมรายได้ (บาท)"], colorscale="Teal", showscale=False, line=dict(color="#38bdf8", width=2)),
        text=[f"{v:,.2f} ฿" for v in fbi_data["รวมรายได้ (บาท)"]], textposition="outside"
    ))
    f_total.update_layout(title="ยอดรวมรายได้ FBI สะสม (บาท)", showlegend=False)
    style_fig(f_total, 400).update_yaxes(range=[0, fbi_data["รวมรายได้ (บาท)"].max() * 1.18])
    st.plotly_chart(f_total, use_container_width=True, config=PLOT_CFG)

    section_head("CATEGORY BREAKDOWN", "เปรียบเทียบรายได้ FBI แยกตามรายหมวด (หมวด 1 - 5)", "เข้าใจง่ายว่าแต่ละหมวดทำรายได้เท่าไหร่ในแต่ละเดือน")
    cat_cols = ["หมวด 1", "หมวด 2", "หมวด 3", "หมวด 4", "หมวด 5"]
    cat_colors = ["#38bdf8", "#818cf8", "#ec4899", "#34d399", "#f59e0b"]
    
    f_cat = go.Figure()
    for idx, cat in enumerate(cat_cols):
        f_cat.add_trace(go.Bar(
            x=fbi_data["เดือน"], y=fbi_data[cat], name=cat,
            marker_color=cat_colors[idx], text=[f"{v:,.0f}" for v in fbi_data[cat]], textposition="auto"
        ))
    f_cat.update_layout(barmode="group", title="เปรียบเทียบรายได้แยกตามหมวดรายเดือน (บาท)")
    style_fig(f_cat, 450)
    st.plotly_chart(f_cat, use_container_width=True, config=PLOT_CFG)

    section_head("DETAIL", "ตารางสรุปรายงาน FBI สาขาเซกา รายเดือน")
    st.dataframe(fbi_data, use_container_width=True, hide_index=True)

# =====================================================
# PAGE 4 : Digital Transactions
# =====================================================
elif page == "💳 Digital":
    page_hero("💳 KPI เจาะลึก · สารสนเทศ SO4",
              '<span class="grad">Digital</span> Transactions',
              "ผลงานสะสมปีบัญชี 2569 ย้อนหลัง 5 เดือน (มิ.ย. – 15 ต.ค. 2569) · ธ.ก.ส. สาขาเซกา จ.บึงกาฬ")

    TARGET_TXN, TARGET_REG = 1139713, 9127
    TARGET_RATIO, TARGET_ACTIVE, TARGET_MONTH = 75.0, 50.0, 90000

    cols = ["เดือน", "ข้อมูล ณ วันที่", "BAAC Mobile", "สาขา/Banking Agent", "ATM/CDM",
            "สัดส่วน Digital (%)", "Mobile Active (%)", "ผลงานธุรกรรม (%)", "ห่างเป้าธุรกรรม",
            "ลูกค้าลงทะเบียน", "ผลงานลงทะเบียน (%)", "ห่างเป้าลงทะเบียน"]
    dm = pd.DataFrame([
        ["มิ.ย. 69",   "30 มิ.ย. 2569", 281711, 15316,  81379, 74.45, 51.74, 24.72, -858713, 8624, 94.49, -503],
        ["ก.ค. 69",    "31 ก.ค. 2569", 380749, 20536, 109727, 74.51, 50.85, 33.41, -759837, 8727, 95.62, -400],
        ["ส.ค. 69",    "31 ส.ค. 2569", 480439, 25606, 136130, 74.81, 51.35, 42.15, -660359, 8820, 96.64, -307],
        ["ก.ย. 69",    "30 ก.ย. 2569", 578649, 31363, 161357, 75.02, 51.32, 50.77, -562396, 8921, 97.74, -206],
        ["15 ต.ค. 69", "15 ต.ค. 2569", 630143, 34316, 176613, 74.92, 43.94, 55.29, -510902, 8982, 98.41, -145],
    ], columns=cols)
    dm["ธุรกรรมเพิ่มในเดือน"] = dm["BAAC Mobile"].diff()

    months = dm["เดือน"].tolist()
    CH = {"BAAC Mobile": "#38bdf8", "สาขา/Banking Agent": "#f59e0b", "ATM/CDM": "#ec4899"}

    section_head("SELECT MONTH", "เลือกเดือนที่ต้องการดู", "ค่าเริ่มต้นคือข้อมูลล่าสุด 15 ต.ค. 2569")
    sel_m = st.radio("เลือกเดือน", months, index=len(months) - 1,
                     horizontal=True, label_visibility="collapsed")
    i = months.index(sel_m)
    cur = dm.iloc[i]
    prev = dm.iloc[i - 1] if i > 0 else None

    def chg(col, fmt="{:,.0f}", unit=""):
        if prev is None:
            return "เดือนแรก"
        d = cur[col] - prev[col]
        return f"{'▲' if d >= 0 else '▼'} {fmt.format(abs(d))}{unit} จากเดือนก่อน"

    def hl(base):
        return ["#ec4899" if m == sel_m else base for m in months]

    html('<div class="spacer"></div>')
    kpi_grid([
        ("📊", "สัดส่วน Digital Transaction", f"{cur['สัดส่วน Digital (%)']:.2f}%", f"เป้า 75% · {chg('สัดส่วน Digital (%)', '{:.2f}', '%')}"),
        ("📱", "ลูกค้า BAAC Mobile Active", f"{cur['Mobile Active (%)']:.2f}%", f"เป้า 50% · {chg('Mobile Active (%)', '{:.2f}', '%')}"),
        ("⚡", "ธุรกรรมดิจิทัลสะสม", f"{int(cur['BAAC Mobile']):,}", f"{cur['ผลงานธุรกรรม (%)']:.2f}% ของเป้า"),
        ("👥", "ลูกค้าลงทะเบียน Mobile", f"{int(cur['ลูกค้าลงทะเบียน']):,} ราย", f"{cur['ผลงานลงทะเบียน (%)']:.2f}% ของเป้า"),
    ])

    total_ch = sum(int(cur[c]) for c in CH)
    kpi_grid([
        ("📲", "BAAC Mobile", f"{int(cur['BAAC Mobile']):,}", f"{int(cur['BAAC Mobile'])/total_ch*100:.2f}%"),
        ("🏦", "สาขา / Banking Agent", f"{int(cur['สาขา/Banking Agent']):,}", f"{int(cur['สาขา/Banking Agent'])/total_ch*100:.2f}%"),
        ("🏧", "ATM / CDM", f"{int(cur['ATM/CDM']):,}", f"{int(cur['ATM/CDM'])/total_ch*100:.2f}%"),
    ])

    section_head("COMPARE 5 MONTHS", "ปริมาณธุรกรรมแยกตามช่องทาง", "ยอดสะสมตั้งแต่ต้นปีบัญชี 2569")
    f1 = go.Figure()
    for ch, color in CH.items():
        f1.add_trace(go.Bar(x=months, y=dm[ch], name=ch, marker_color=color,
                            text=dm[ch], texttemplate="%{text:,}", textposition="outside"))
    f1.update_layout(barmode="group")
    st.plotly_chart(style_fig(f1, 420), use_container_width=True, config=PLOT_CFG)

    section_head("RATIO", "เทียบเป้าหมายรายเดือน", "เส้นประสีชมพูคือเป้าหมาย")
    c1, c2 = st.columns(2)
    with c1:
        f2 = go.Figure(go.Scatter(
            x=months, y=dm["สัดส่วน Digital (%)"], mode="lines+markers+text", name="ผลงาน",
            text=[f"{v:.2f}%" for v in dm["สัดส่วน Digital (%)"]], textposition="top center",
            line=dict(color="#38bdf8", width=3), marker=dict(size=10, color=hl("#38bdf8"))))
        f2.add_hline(y=TARGET_RATIO, line_dash="dash", line_color="#ec4899", annotation_text="เป้า 75%")
        f2.update_layout(title="สัดส่วน Digital Transaction (%)", showlegend=False)
        st.plotly_chart(style_fig(f2, 350), use_container_width=True, config=PLOT_CFG)
    with c2:
        f3 = go.Figure(go.Scatter(
            x=months, y=dm["Mobile Active (%)"], mode="lines+markers+text", name="ผลงาน",
            text=[f"{v:.2f}%" for v in dm["Mobile Active (%)"]], textposition="top center",
            line=dict(color="#818cf8", width=3), marker=dict(size=10, color=hl("#818cf8"))))
        f3.add_hline(y=TARGET_ACTIVE, line_dash="dash", line_color="#ec4899", annotation_text="เป้า 50%")
        f3.update_layout(title="ลูกค้า BAAC Mobile Active (%)", showlegend=False)
        st.plotly_chart(style_fig(f3, 350), use_container_width=True, config=PLOT_CFG)

    section_head("PROGRESS", "ความคืบหน้าเทียบเป้าหมายทั้งปี")
    c3, c4 = st.columns(2)
    with c3:
        f4 = go.Figure(go.Bar(
            x=months, y=dm["BAAC Mobile"], marker_color=hl("#34d399"),
            text=[f"{v:,}" for v in dm["BAAC Mobile"]], textposition="outside"))
        f4.add_hline(y=TARGET_TXN, line_dash="dash", line_color="#ec4899", annotation_text="เป้าทั้งปี")
        f4.update_layout(title="ปริมาณธุรกรรมดิจิทัลสะสม", showlegend=False)
        st.plotly_chart(style_fig(f4, 380), use_container_width=True, config=PLOT_CFG)
    with c4:
        f5 = go.Figure(go.Bar(
            x=months, y=dm["ลูกค้าลงทะเบียน"], marker_color=hl("#38bdf8"),
            text=[f"{v:,}" for v in dm["ลูกค้าลงทะเบียน"]], textposition="outside"))
        f5.add_hline(y=TARGET_REG, line_dash="dash", line_color="#ec4899", annotation_text="เป้าลงทะเบียน")
        f5.update_layout(title="จำนวนลูกค้า BAAC Mobile (สะสม)", showlegend=False)
        st.plotly_chart(style_fig(f5, 380), use_container_width=True, config=PLOT_CFG)

    section_head("MONTHLY", "ธุรกรรมที่เพิ่มขึ้นในแต่ละเดือน")
    c5, c6 = st.columns([1.3, 1])
    with c5:
        inc = dm.iloc[1:]
        f6 = go.Figure(go.Bar(
            x=inc["เดือน"], y=inc["ธุรกรรมเพิ่มในเดือน"],
            marker_color=["#ec4899" if m == sel_m else "#34d399" for m in inc["เดือน"]],
            text=[f"{int(v):,}" for v in inc["ธุรกรรมเพิ่มในเดือน"]], textposition="outside"))
        f6.add_hline(y=TARGET_MONTH, line_dash="dash", line_color="#f59e0b", annotation_text="เป้าเดือน ~0.09M")
        f6.update_layout(title="ธุรกรรมดิจิทัลเพิ่มขึ้นรายเดือน", showlegend=False)
        st.plotly_chart(style_fig(f6, 350), use_container_width=True, config=PLOT_CFG)
    with c6:
        mix = pd.DataFrame({"ช่องทาง": list(CH.keys()), "จำนวน": [int(cur[c]) for c in CH]})
        f7 = px.pie(mix, names="ช่องทาง", values="จำนวน", hole=0.6, color="ช่องทาง", color_discrete_map=CH)
        f7.update_traces(textinfo="percent")
        f7.update_layout(title=f"สัดส่วน · {sel_m}")
        st.plotly_chart(style_fig(f7, 350), use_container_width=True, config=PLOT_CFG)

    section_head("DETAIL", "ตารางสรุปข้อมูล 5 เดือน")
    st.dataframe(dm.drop(columns=["ธุรกรรมเพิ่มในเดือน"]), use_container_width=True, hide_index=True)

# =====================================================
# PAGE 5 : Line OA
# =====================================================
elif page == "📱 Line OA":
    page_hero("📱 Line OA · ธ.ก.ส. สาขาเซกา", 'ศูนย์ข้อมูลและบริการ <span class="grad">Line OA</span>',
              "รวมโบรชัวร์สินเชื่อ โปรโมชั่น กำหนดการออกหน่วย และผังองค์กรสาขา")

    kpi_grid([
        ("👥", "เพื่อนทั้งหมด (Friends)", "168 คน", "▲ +66 จากงวดก่อน"),
        ("🎯", "เป้าหมาย (Target)", "166 คน", "🟢 ทะลุเป้า"),
        ("🤖", "ระบบตอบกลับอัตโนมัติ", "Active 24 ชม.", "พร้อมให้บริการ"),
    ])

    chat_preview("📱 ดูตัวอย่างหน้าจอ Line OA & Rich Menu ของจริง", "line_preview.jpg",
                 "หน้าจอแชทและ Rich Menu Line OA สาขาเซกา")
    html('<div class="spacer"></div>')

    tab1, tab2, tab3, tab4 = st.tabs(["🌿 สินเชื่อ & โบรชัวร์", "🎁 โปรโมชั่นพิเศษ",
                                      "📅 กำหนดการออกหน่วย", "👥 ผังโครงสร้างองค์กร"])

    with tab1:
        section_head("LOAN", "โครงการสินเชื่อเด่น", "ธ.ก.ส. สาขาเซกา")
        feature_row("loan_1.jpg", "🌟 ลดต้นทุนการผลิต", "โครงการสินเชื่อ “ดอกเบี้ยคนละครึ่ง”", [
            "อัตราดอกเบี้ยโครงการ <b>6% ต่อปี</b> (เกษตรกรจ่าย 3% / รัฐบาลช่วยจ่าย 3%)",
            "ผ่านการอบรม Smart Farmer และจัดซื้อปัจจัยการผลิตผ่านสถาบันเกษตรกร",
            "ยื่นกู้ได้ถึง <b>30 เมษายน 2571</b>"])
        feature_row("loan_2.jpg", "♻️ เศรษฐกิจยั่งยืน", "สินเชื่อภายใต้ BCG Model", [
            "<b>Bio Economy</b> เศรษฐกิจชีวภาพ ต่อยอดมูลค่าพืชผล",
            "<b>Circular Economy</b> เศรษฐกิจหมุนเวียน บริหารวัสดุเหลือใช้ (Zero Waste)",
            "<b>Green Credit</b> สินเชื่อสีเขียว เป็นมิตรต่อสิ่งแวดล้อม"], reverse=True)
        feature_row("loan_3.jpg", "🚁 Smart Tech", "สินเชื่อเพื่อเทคโนโลยีและเครื่องจักรกล", [
            "จัดซื้อเครื่องจักรกล เครื่องยนต์ และโดรนเกษตรอัจฉริยะ",
            "อัตราดอกเบี้ย <b>MRR - 1</b> ต่อปี (ต้นลดดอกลด)",
            "ชำระคืนสูงสุดไม่เกิน <b>10 ปี</b>"])

    with tab2:
        section_head("PROMOTION", "โปรโมชั่นและของสมนาคุณ", "ประจำ ธ.ก.ส. สาขาเซกา")
        chat_preview("💬 ดูตัวอย่างแชท Line OA เมื่อพิมพ์คำว่า “โปรโมชั่น”", "chat_promo.jpg",
                     "แชทตอบกลับอัตโนมัติเมื่อพิมพ์ “โปรโมชั่น”")
        html('<div class="spacer"></div>')
        feature_row("promo_1.jpg", "💚 เงินฝากคุ้มครองชีวิต", "ธ.ก.ส. เพิ่มรัก 12/10", [
            "เกษตรกรและครอบครัว อายุ <b>20-60 ปี</b> ส่งชำระล่วงหน้า 1 ปี",
            "เดือนละ <b>300 บาท</b> ➔ ข้าวสาร 2 KG 🌾",
            "เดือนละ <b>500 บาท</b> ➔ ข้าวสาร 5 KG 🌾",
            "เดือนละ <b>1,000 บาท</b> ➔ ข้าวสาร 5 KG หรือ ร่มพับ ☂️",
            "เดือนละ <b>2,000 บาท</b> ➔ ชุดจานเมลามีน 🍽️"])
        feature_row("promo_2.jpg", "💎 ประกันชีวิตสะสมทรัพย์", "ธ.ก.ส. HUG (ฮัก) 10/5", [
            "<b>10,000 บาทขึ้นไป</b> ➔ ข้าวสาร 5 KG หรือ ร่มพับ",
            "<b>30,000 บาทขึ้นไป</b> ➔ ข้าวสาร 5 KG + ร่มพับ",
            "<b>50,000 บาทขึ้นไป</b> ➔ ข้าวสาร 5 KG + กระเป๋า Canvas 👜",
            "<b>70,000 บาทขึ้นไป</b> ➔ ข้าวสาร 5 KG + ชุดจานเมลามีน",
            "<b>100,000 บาทขึ้นไป</b> ➔ ข้าวสาร 5 KG + กระเป๋าเดินทาง 24 นิ้ว 🧳"], reverse=True)

    with tab3:
        section_head("OUTREACH", "ชุมชนโฮมสุข · ออกหน่วยบริการ", "ธนาคารใกล้บ้าน บริการใกล้ชิด — กันยายน 2569")
        chat_preview("💬 ดูตัวอย่างแชท Line OA เมื่อพิมพ์คำว่า “จุดนัดพบ”", "chat_schedule.jpg",
                     "แชทตอบกลับอัตโนมัติเมื่อพิมพ์ “จุดนัดพบ”")
        html('<div class="spacer"></div>')

        st.markdown("### 📸 บรรยากาศการปฏิบัติงานออกหน่วยเคลื่อนที่จริง")
        img_c1, img_c2, img_c3 = st.columns(3)
        with img_c1:
            show_img("outreach_1.jpg", "จุดบริการชุมชนโฮมสุข (ภาพที่ 1)")
        with img_c2:
            show_img("outreach_2.jpg", "การให้บริการธุรกรรม (ภาพที่ 2)")
        with img_c3:
            show_img("outreach_3.jpg", "ให้คำปรึกษาและแนะนำ (ภาพที่ 3)")

        html('<div class="spacer"></div>')

        b1, b2 = st.columns([1.15, 1.85])
        with b1:
            show_img("schedule_banner.jpg", "ประกาศกำหนดการออกจุดบริการนอกสถานที่")
        with b2:
            items = "".join(
                f'<div class="tl-item"><div class="tl-date"><b>{d}</b><span>ก.ย. 69</span></div>'
                f'<div><div class="tl-place">{p}</div><div class="tl-sub">📍 {t}</div></div></div>'
                for d, p, t in schedule)
            html(f'<div class="tl">{items}</div>')

        html('<div class="spacer"></div>')
        s1, s2 = st.columns(2)
        with s1:
            info_card("💳 การเงิน", "บริการด้านการเงิน", [
                "ฝาก - ถอน", "ทำบัตร ATM", "เปิดบัญชีใหม่", "สมัครแอปพลิเคชัน BAAC Mobile",
                "สมัคร SMS Alert", "ฝากสลากออมทรัพย์", "ลงทะเบียนพร้อมเพย์",
                "รับชำระค่าสาธารณูปโภคต่างๆ"])
        with s2:
            info_card("🌾 สินเชื่อ", "บริการด้านสินเชื่อ", [
                "จัดทำสัญญาเงินกู้", "รับชำระหนี้", "ปรับปรุงโครงสร้างหนี้", "เลื่อนงวดชำระ",
                "ลงทะเบียนพักชำระหนี้", "ปรึกษาปัญหาหนี้นอกระบบ", "บริการอื่นๆ"])

    with tab4:
        section_head("OUR TEAM", "ผังโครงสร้างองค์กร", "ทีมงาน ธ.ก.ส. สาขาเซกา")
        chat_preview("💬 ดูตัวอย่างแชท Line OA ข้อมูลผู้บริหารและพนักงาน", "chat_org.jpg",
                     "แชทแสดงข้อมูลโครงสร้างองค์กรใน Line OA")
        html('<div class="spacer"></div>')
        feature_row("manager.jpg", "01 · ผู้บริหาร", "ผู้จัดการสาขา", [
            "บริหารงานภาพรวมของสาขา",
            "กำหนดกลยุทธ์และขับเคลื่อนเป้าหมายตามยุทธศาสตร์องค์กร"])
        feature_row("team_credit.jpg", "02 · สินเชื่อ", "หน่วยสินเชื่อ", [
            "ให้คำปรึกษา แนะนำ และวิเคราะห์อนุมัติสินเชื่อทุกประเภท",
            "สินเชื่อพัฒนาเกษตรกร, BCG Model, Smart Tech และโครงการภาครัฐ",
            "ขับเคลื่อนเศรษฐกิจฐานรากในพื้นที่"], reverse=True)

# =====================================================
# FOOTER
# =====================================================
html('<div class="footer"><span>📍 112 หมู่ 14 ต.เซกา อ.เซกา จ.บึงกาฬ</span>'
     '<span>📞 042-489050</span><span>✉️ baac.seka@gmail.com</span>'
     '<span>📘 ธกส.สาขาเซกา จังหวัดบึงกาฬ</span></div>')