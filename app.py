import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GELATICO 젤라티코 | 창업 안내",
    page_icon="🍦",
    layout="wide"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;800&family=Playfair+Display:wght@700&display=swap');

.hero-banner {
    background: linear-gradient(135deg, #1B3A6B, #4A90D9);
    border-radius: 16px;
    padding: 60px;
    text-align: center;
    color: white;
}
.hero-title {
    font-size: 60px;
    font-weight: 800;
}
.hero-sub {
    font-size: 20px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 데이터 로드
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base_df = pd.read_csv("data/매장_기본_데이터.csv", encoding="utf-8-sig")
    monthly_df = pd.read_csv("data/월별_매출_데이터.csv", encoding="utf-8-sig")
    return base_df, monthly_df

try:
    base_df, monthly_df = load_data()
except:
    st.error("데이터 파일이 없습니다.")
    st.stop()

# 전처리
def parse_monthly(df):
    df = df.copy()
    for col in df.columns:
        if col != "년도-월":
            df[col] = df[col].astype(str).str.replace("만원","").str.replace(",","").astype(float)
    return df

monthly_clean = parse_monthly(monthly_df)
store_cols = [c for c in monthly_clean.columns if c != "년도-월"]

# ─────────────────────────────────────────────
# 헤더
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">GELATICO</div>
    <div class="hero-sub">프리미엄 젤라또 창업 플랫폼</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI
# ─────────────────────────────────────────────
avg_sales = int(base_df["월매출(만원)"].mean())
avg_revisit = round(base_df["재방문율(%)"].mean(),1)

c1, c2, c3 = st.columns(3)

kpis = [
    (c1, "매장 수", len(base_df)),
    (c2, "평균 월매출", f"{avg_sales:,}만원"),
    (c3, "재방문율", f"{avg_revisit}%")
]

for col, label, value in kpis:
    with col:
        st.markdown(f"""
        <div class="card">
            <div>{label}</div>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# 시즌 매출 차트
# ─────────────────────────────────────────────
monthly_clean["평균매출"] = monthly_clean[store_cols].mean(axis=1)
monthly_clean["월"] = monthly_clean["년도-월"].str.split("-").str[1].astype(int)

season = monthly_clean.groupby("월")["평균매출"].mean().reset_index()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=season["월"],
    y=season["평균매출"],
    text=season["평균매출"].apply(lambda x: f"{x:.0f}"),
    textposition="outside"
))

fig.update_layout(
    title="월별 평균 매출",
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# 시뮬레이션
# ─────────────────────────────────────────────
st.subheader("🧮 창업 시뮬레이션")

district = st.selectbox("상권", ["오피스", "대학가", "주거"])
size = st.selectbox("규모", ["소형", "중형", "대형"])

base_sales_map = {
    "오피스": 4000,
    "대학가": 3000,
    "주거": 2000
}

cost_map = {
    "소형": 2000,
    "중형": 3000,
    "대형": 4500
}

sales = base_sales_map[district]
cost = cost_map[size]
profit = sales - cost

r1, r2, r3 = st.columns(3)

results = [
    (r1, "예상 매출", f"{sales:,}만원"),
    (r2, "고정비", f"{cost:,}만원"),
    (r3, "순이익", f"{profit:,}만원")
]

for col, label, value in results:
    with col:
        st.markdown(f"""
        <div class="card">
            <div>{label}</div>
            <h3>{value}</h3>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────
st.markdown("""
---
<center>© GELATICO 2026</center>
""", unsafe_allow_html=True)
