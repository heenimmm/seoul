import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GELATICO",
    page_icon="🍦",
    layout="wide"
)

# ─────────────────────────────────────────────
# CSS (원본 유지 + 오류 수정)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;800&family=Playfair+Display:wght@700&display=swap');

body {
    font-family: 'Noto Sans KR', sans-serif;
}

.hero-banner {
    background: linear-gradient(135deg, #1B3A6B, #4A90D9);
    border-radius: 20px;
    padding: 60px;
    text-align: center;
    color: white;
}

.hero-title {
    font-size: 64px;
    font-weight: 800;
    font-family: 'Playfair Display', serif;
}

.hero-sub {
    font-size: 20px;
    opacity: 0.9;
    margin-top: 10px;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: white;
    border-radius: 25px;
    padding: 6px 18px;
    font-size: 13px;
    margin-bottom: 20px;
    letter-spacing: 1.2px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 데이터 로드 (안정성 추가)
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        base_df = pd.read_csv("data/매장_기본_데이터.csv", encoding="utf-8-sig")
        monthly_df = pd.read_csv("data/월별_매출_데이터.csv", encoding="utf-8-sig")
        return base_df, monthly_df
    except Exception as e:
        st.error(f"데이터 로딩 오류: {e}")
        st.stop()

base_df, monthly_df = load_data()

# ─────────────────────────────────────────────
# 데이터 전처리
# ─────────────────────────────────────────────
def parse_monthly(df):
    df = df.copy()
    for col in df.columns:
        if col != "년도-월":
            df[col] = (
                df[col].astype(str)
                .str.replace("만원","")
                .str.replace(",","")
                .astype(float)
            )
    return df

monthly_clean = parse_monthly(monthly_df)
store_cols = [c for c in monthly_clean.columns if c != "년도-월"]

# ─────────────────────────────────────────────
# 헤더 (원본 UI 유지)
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-tag">PREMIUM GELATO BUSINESS</div>
    <div class="hero-title">GELATICO</div>
    <div class="hero-sub">프리미엄 젤라또 창업 플랫폼</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI 카드 (원본 디자인 유지)
# ─────────────────────────────────────────────
avg_sales = int(base_df["월매출(만원)"].mean())
avg_revisit = round(base_df["재방문율(%)"].mean(),1)

c1, c2, c3 = st.columns(3)

cards = [
    (c1, "매장 수", len(base_df), "운영 매장"),
    (c2, "평균 월매출", f"{avg_sales:,}만원", "전체 평균"),
    (c3, "재방문율", f"{avg_revisit}%", "고객 충성도"),
]

for col, label, value, sub in cards:
    with col:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:20px;text-align:center;
                    border:1px solid #E5E9F2;box-shadow:0 2px 10px rgba(27,58,107,0.06);">
            <div style="font-size:13px;color:#7A8BA6;margin-bottom:6px;">{label}</div>
            <div style="font-size:20px;font-weight:800;color:#1B3A6B;">{value}</div>
            <div style="font-size:11px;color:#A0AFBF;margin-top:6px;">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# 월별 매출 차트
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
# 창업 시뮬레이션 (오류 수정)
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

sim_items = [
    (r1, "예상 매출", f"{sales:,}만원"),
    (r2, "고정비", f"{cost:,}만원"),
    (r3, "순이익", f"{profit:,}만원"),
]

for col, label, value in sim_items:
    with col:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:20px;text-align:center;
                    border:1px solid #E5E9F2;box-shadow:0 2px 10px rgba(27,58,107,0.06);">
            <div style="font-size:13px;color:#7A8BA6;">{label}</div>
            <div style="font-size:20px;font-weight:800;color:#1B3A6B;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 푸터
# ─────────────────────────────────────────────
st.markdown("""
---
<center>© GELATICO 2026</center>
""", unsafe_allow_html=True)
