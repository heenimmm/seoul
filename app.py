import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GELATICO 젤라티코 | 창업 안내",
    page_icon="🍦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# 글로벌 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Playfair+Display:wght@700&display=swap');

/* 전체 배경 */
.stApp { background-color: #F8F9FC; }
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

/* 탭 스타일 */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    background: #1B3A6B;
    border-radius: 12px 12px 0 0;
    padding: 6px 6px 0 6px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: rgba(255,255,255,0.65);
    font-weight: 600;
    font-size: 15px;
    padding: 12px 28px;
    border-radius: 8px 8px 0 0;
    border: none;
    letter-spacing: 0.3px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #1B3A6B !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #FFFFFF;
    border-radius: 0 0 12px 12px;
    border: 1px solid #E5E9F2;
    padding: 32px 36px;
}

/* 헤더 배너 */
.hero-banner {
    background: linear-gradient(135deg, #1B3A6B 0%, #2D5BA3 50%, #4A90D9 100%);
    border-radius: 16px;
    padding: 52px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 40%;
    width: 400px; height: 400px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 700;
    color: white;
    margin: 0;
    letter-spacing: 2px;
}
.hero-sub {
    font-size: 18px;
    color: rgba(255,255,255,0.82);
    margin: 10px 0 0 0;
    font-weight: 300;
    letter-spacing: 0.5px;
}
.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: white;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    margin-bottom: 16px;
    letter-spacing: 1px;
    font-weight: 500;
}

/* KPI 카드 */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 24px 20px;
    text-align: center;
    border: 1px solid #E5E9F2;
    box-shadow: 0 2px 12px rgba(27,58,107,0.07);
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(27,58,107,0.13);
}
.kpi-label { font-size: 13px; color: #7A8BA6; font-weight: 500; margin-bottom: 8px; letter-spacing: 0.3px; }
.kpi-value { font-size: 30px; font-weight: 800; color: #1B3A6B; margin-bottom: 4px; }
.kpi-sub   { font-size: 12px; color: #A0AFBF; }

/* 섹션 제목 */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #1B3A6B;
    margin: 32px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #4A90D9;
    display: inline-block;
}

/* 브랜드 특징 카드 */
.feature-card {
    background: white;
    border-radius: 12px;
    padding: 28px 24px;
    border-left: 4px solid #4A90D9;
    box-shadow: 0 2px 10px rgba(27,58,107,0.06);
    height: 100%;
}
.feature-icon { font-size: 32px; margin-bottom: 12px; }
.feature-title { font-size: 16px; font-weight: 700; color: #1B3A6B; margin-bottom: 8px; }
.feature-desc  { font-size: 14px; color: #5A6A7E; line-height: 1.7; }

/* 메뉴 카드 */
.menu-card {
    background: white;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    border: 1px solid #E5E9F2;
    box-shadow: 0 2px 10px rgba(27,58,107,0.06);
    transition: transform 0.2s;
}
.menu-card:hover { transform: translateY(-4px); }
.menu-emoji { font-size: 44px; margin-bottom: 12px; }
.menu-name  { font-size: 15px; font-weight: 700; color: #1B3A6B; margin-bottom: 6px; }
.menu-desc  { font-size: 13px; color: #6A7A8E; margin-bottom: 10px; line-height: 1.5; }
.menu-badge {
    display: inline-block;
    background: #FFF0E6;
    color: #E8742A;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
}
.menu-badge-new {
    display: inline-block;
    background: #E6F4FF;
    color: #2D7DD2;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 600;
}

/* 창업 절차 스텝 */
.step-card {
    background: white;
    border-radius: 12px;
    padding: 20px 18px;
    border: 1px solid #E5E9F2;
    box-shadow: 0 2px 8px rgba(27,58,107,0.05);
    position: relative;
    text-align: center;
}
.step-num {
    width: 36px; height: 36px;
    background: #1B3A6B;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 15px;
    margin: 0 auto 12px auto;
}
.step-title { font-size: 14px; font-weight: 700; color: #1B3A6B; margin-bottom: 6px; }
.step-desc  { font-size: 12px; color: #7A8BA6; line-height: 1.5; }
.step-period {
    margin-top: 8px;
    display: inline-block;
    background: #EEF4FF;
    color: #2D5BA3;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}

/* 문의 박스 */
.contact-box {
    background: linear-gradient(135deg, #1B3A6B, #2D5BA3);
    border-radius: 16px;
    padding: 36px 32px;
    color: white;
    text-align: center;
}
.contact-name { font-size: 28px; font-weight: 800; margin-bottom: 8px; }
.contact-phone { font-size: 38px; font-weight: 900; letter-spacing: 2px; margin-bottom: 8px; }
.contact-note  { font-size: 14px; color: rgba(255,255,255,0.75); }

/* 시뮬레이션 결과 */
.sim-result {
    background: linear-gradient(135deg, #1B3A6B, #2D5BA3);
    border-radius: 14px;
    padding: 28px;
    color: white;
    text-align: center;
    margin-top: 8px;
}
.sim-label { font-size: 13px; color: rgba(255,255,255,0.75); margin-bottom: 4px; }
.sim-value { font-size: 26px; font-weight: 800; }

/* 상권 카드 */
.district-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    border-top: 4px solid #4A90D9;
    box-shadow: 0 2px 10px rgba(27,58,107,0.06);
}

/* 비용 하이라이트 */
.cost-highlight {
    background: #EEF4FF;
    border-radius: 10px;
    padding: 16px 20px;
    border-left: 4px solid #1B3A6B;
}

/* 구분선 */
.divider {
    border: none;
    border-top: 1px solid #E5E9F2;
    margin: 28px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 데이터 로딩
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base_df      = pd.read_csv("data/매장_기본_데이터.csv",      encoding="utf-8-sig")
    monthly_df   = pd.read_csv("data/월별_매출_데이터.csv",      encoding="utf-8-sig")
    top_df       = pd.read_csv("data/매출_상위권_매장.csv",       encoding="utf-8-sig")
    cost_df      = pd.read_csv("data/점포_규모별_초기비용.csv",   encoding="utf-8-sig")
    marketing_df = pd.read_csv("data/마케팅_전략별_효과.csv",    encoding="utf-8-sig")
    district_df  = pd.read_csv("data/상권_분석_데이터.csv",      encoding="utf-8-sig")
    return base_df, monthly_df, top_df, cost_df, marketing_df, district_df

base_df, monthly_df, top_df, cost_df, marketing_df, district_df = load_data()

# 월별 매출 전처리 (만원 단위 숫자 변환)
def parse_monthly(df):
    df = df.copy()
    for col in df.columns:
        if col != "년도-월":
            df[col] = df[col].astype(str).str.replace("만원","").str.replace(",","").astype(float)
    return df

monthly_clean = parse_monthly(monthly_df)
store_cols = [c for c in monthly_clean.columns if c != "년도-월"]

# 상위 5 매장
top5_names = top_df["매장명"].tolist()[:5]

# ─────────────────────────────────────────────
# 공통 헤더
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-tag">🍦 PREMIUM GELATO FRANCHISE</div>
  <p class="hero-title">GELATICO</p>
  <p class="hero-sub">젤라티코 — 이탈리아의 맛, 당신의 매장에서</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 탭 구성
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🍦 젤라티코란?",
    "📣 마케팅",
    "📊 매출현황",
    "📋 창업안내"
])

# ═══════════════════════════════════════════════
# TAB 1 — 젤라티코란?
# ═══════════════════════════════════════════════
with tab1:

    # KPI 카드
    avg_monthly = int(base_df["월매출(만원)"].mean())
    max_monthly = int(monthly_clean[store_cols].values.max())
    avg_unit    = int(base_df["객단가(원)"].mean())
    avg_revisit = round(base_df["재방문율(%)"].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "전국 운영 매장", f"{len(base_df)}개", "실제 가상 데이터 기준"),
        (c2, "전체 평균 월매출", f"{avg_monthly:,}만원", "18개 매장 평균"),
        (c3, "최고 월매출 기록", f"{max_monthly:,}만원", "제주점 2025-08"),
        (c4, "평균 재방문율",    f"{avg_revisit}%",       "고객 만족도 반영"),
    ]
    for col, label, value, sub in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{value}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 브랜드 소개
    st.markdown('<p class="section-title">✦ 브랜드 소개</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:16px; color:#3A4A5E; line-height:2; margin-bottom:24px;">
    젤라티코(Gelatico)는 최상급 이탈리아 원재료와 전통 제조 방식을 바탕으로,
    매일 신선한 감동을 전달하는 프리미엄 젤라또 브랜드입니다.<br>
    단순한 디저트를 넘어 <b>감성적인 경험</b>을 제공하며, 검증된 운영 시스템과 체계적인 창업 지원으로
    전국 18개 매장을 성공적으로 운영 중입니다.
    </p>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🌿", "프리미엄 원재료", "이탈리아 직수입 원재료만 사용.<br>매일 신선하게 제조하는<br>정통 젤라또의 맛을 보장합니다."),
        ("📱", "SNS 확산력", "감성적인 비주얼로 인스타그램·틱톡<br>바이럴이 자연스럽게 발생.<br>자체 마케팅 효과 극대화."),
        ("🔄", "시즌별 메뉴 운영", "봄·여름·가을·겨울 시즌 한정 메뉴로<br>고객의 재방문을 유도하는<br>전략적 메뉴 운영 시스템."),
        ("🤝", "체계적 창업 지원", "계약부터 오픈까지 전담 팀이<br>동행. 6개월 밀착 사후관리로<br>안정적인 매장 정착을 지원."),
    ]
    for col, (icon, title, desc) in zip([f1,f2,f3,f4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
              <div class="feature-icon">{icon}</div>
              <div class="feature-title">{title}</div>
              <div class="feature-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 메뉴 소개
    st.markdown('<p class="section-title">🍨 시그니처 메뉴</p>', unsafe_allow_html=True)

    menus = [
        ("🍵", "말차 라떼 젤라또",    "우지 말차와 부드러운 크림의 조화",  "베스트셀러", "badge"),
        ("🔴", "스트라치아텔라",        "바닐라 베이스에 초콜릿 칩 가득",    "베스트셀러", "badge"),
        ("🟢", "피스타치오 젤라또",    "시칠리아산 피스타치오 100%",         "프리미엄",   "badge"),
        ("🟡", "망고 소르베",           "열대 망고의 상큼한 non-dairy",       "비건 옵션",  "badge-new"),
        ("☕", "티라미수 젤라또",       "에스프레소와 마스카포네의 정수",     "시즌 한정",  "badge-new"),
        ("🍓", "딸기 바질 소르베",      "국내산 딸기 + 신선 바질의 만남",    "NEW",        "badge-new"),
    ]
    m_cols = st.columns(6)
    for col, (emoji, name, desc, tag, badge_cls) in zip(m_cols, menus):
        with col:
            st.markdown(f"""
            <div class="menu-card">
              <div class="menu-emoji">{emoji}</div>
              <div class="menu-name">{name}</div>
              <div class="menu-desc">{desc}</div>
              <span class="menu-{badge_cls}">{tag}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 시즌별 매출 패턴 차트
    st.markdown('<p class="section-title">📈 연간 매출 시즌 패턴</p>', unsafe_allow_html=True)
    st.caption("전 매장 평균 기준 — 여름 시즌(7~8월) 피크, 겨울(1~2월) 저점 패턴")

    monthly_avg = monthly_clean.copy()
    monthly_avg["평균매출"] = monthly_avg[store_cols].mean(axis=1)
    monthly_avg["월"] = monthly_avg["년도-월"].str.split("-").str[1].astype(int)
    season_avg = monthly_avg.groupby("월")["평균매출"].mean().reset_index()
    month_labels = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]
    season_avg["월명"] = season_avg["월"].apply(lambda x: month_labels[x-1])

    fig_season = go.Figure()
    fig_season.add_trace(go.Bar(
        x=season_avg["월명"],
        y=season_avg["평균매출"],
        marker=dict(
            color=season_avg["평균매출"],
            colorscale=[[0,"#BDD7F5"],[0.5,"#4A90D9"],[1,"#1B3A6B"]],
            showscale=False,
        ),
        text=season_avg["평균매출"].apply(lambda v: f"{v:,.0f}만"),
        textposition="outside",
        textfont=dict(size=11, color="#1B3A6B"),
    ))
    fig_season.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=20,b=20,l=10,r=10),
        yaxis=dict(title="평균 월매출 (만원)", gridcolor="#F0F3F8", showgrid=True),
        xaxis=dict(showgrid=False),
        height=320,
        font=dict(family="Noto Sans KR"),
    )
    st.plotly_chart(fig_season, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 2 — 마케팅
# ═══════════════════════════════════════════════
with tab2:

    st.markdown('<p class="section-title">📣 마케팅 전략 개요</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:15px;color:#3A4A5E;line-height:1.9;">
    젤라티코는 <b>감성 브랜딩 + 데이터 기반 타겟 마케팅</b>을 결합한 전략으로 운영됩니다.
    상권 유형에 따라 최적의 전략을 선택하면 매출 상승 효과를 극대화할 수 있습니다.
    </p>
    """, unsafe_allow_html=True)

    # 마케팅 전략 카드
    strategies = {
        "인스타그램 광고":     {"예산":"80만원", "유입":"+18%", "매출":"+12%", "상권":"대학가, 관광", "icon":"📸", "color":"#E8F4FD"},
        "지역 체험단 운영":    {"예산":"50만원", "유입":"+22%", "매출":"+15%", "상권":"주거, 오피스",  "icon":"👥", "color":"#F0FBF0"},
        "오픈 프로모션":       {"예산":"120만원","유입":"+35%", "매출":"+28%", "상권":"전 상권(초반)", "icon":"🎉", "color":"#FFF7E8"},
        "배달앱 할인 이벤트":  {"예산":"60만원", "유입":"+25%", "매출":"+18%", "상권":"주거, 오피스",  "icon":"🛵", "color":"#FFF0F0"},
        "시즌 한정 메뉴 출시": {"예산":"40만원", "유입":"+30%", "매출":"+22%", "상권":"전 상권",       "icon":"🌸", "color":"#F5F0FF"},
    }

    cols = st.columns(5)
    for col, (name, info) in zip(cols, strategies.items()):
        with col:
            st.markdown(f"""
            <div style="background:{info['color']};border-radius:14px;padding:20px 16px;text-align:center;border:1px solid #E5E9F2;height:100%;">
              <div style="font-size:32px;margin-bottom:10px;">{info['icon']}</div>
              <div style="font-size:13px;font-weight:700;color:#1B3A6B;margin-bottom:12px;">{name}</div>
              <div style="font-size:11px;color:#7A8BA6;margin-bottom:4px;">월 예산</div>
              <div style="font-size:16px;font-weight:800;color:#1B3A6B;margin-bottom:10px;">{info['예산']}</div>
              <div style="display:flex;justify-content:space-around;margin-bottom:10px;">
                <div><div style="font-size:10px;color:#7A8BA6;">유입</div><div style="font-size:14px;font-weight:700;color:#2E9E6B;">{info['유입']}</div></div>
                <div><div style="font-size:10px;color:#7A8BA6;">매출</div><div style="font-size:14px;font-weight:700;color:#2D7DD2;">{info['매출']}</div></div>
              </div>
              <div style="background:white;border-radius:8px;padding:4px 8px;font-size:11px;color:#4A6A8A;">{info['상권']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 마케팅 효과 비교 차트
    st.markdown('<p class="section-title">📊 전략별 효과 비교</p>', unsafe_allow_html=True)

    mkt_names  = ["인스타그램 광고","지역 체험단","오픈 프로모션","배달앱 할인","시즌 한정 메뉴"]
    mkt_inflow = [18, 22, 35, 25, 30]
    mkt_sales  = [12, 15, 28, 18, 22]
    mkt_budget = [80, 50, 120, 60, 40]

    fig_mkt = go.Figure()
    fig_mkt.add_trace(go.Bar(name="유입 증가율 (%)", x=mkt_names, y=mkt_inflow,
        marker_color="#4A90D9", text=[f"+{v}%" for v in mkt_inflow],
        textposition="outside", textfont=dict(size=11)))
    fig_mkt.add_trace(go.Bar(name="매출 상승률 (%)", x=mkt_names, y=mkt_sales,
        marker_color="#1B3A6B", text=[f"+{v}%" for v in mkt_sales],
        textposition="outside", textfont=dict(size=11)))
    fig_mkt.update_layout(
        barmode="group",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=20,b=20,l=10,r=10),
        legend=dict(orientation="h", y=1.08),
        yaxis=dict(title="효과 (%)", gridcolor="#F0F3F8"),
        xaxis=dict(showgrid=False),
        height=340,
        font=dict(family="Noto Sans KR"),
    )
    st.plotly_chart(fig_mkt, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── 운영 시뮬레이션 ──
    st.markdown('<p class="section-title">🧮 운영 시뮬레이션</p>', unsafe_allow_html=True)
    st.caption("상권 유형과 점포 규모를 선택하면 예상 수익을 자동으로 계산합니다.")

    col_sel1, col_sel2, col_sel3 = st.columns(3)

    district_base = {
        "오피스 상권":  {"min":2800, "max":4500, "rent":350},
        "대학가 상권":  {"min":2200, "max":3500, "rent":250},
        "주거 상권":    {"min":1500, "max":2500, "rent":180},
        "관광 상권":    {"min":3000, "max":5200, "rent":420},
    }
    size_base = {
        "소형 (10평)": {"invest":5500, "expected":1800, "staff":1},
        "중형 (15평)": {"invest":7300, "expected":2600, "staff":2},
        "대형 (20평)": {"invest":9700, "expected":3800, "staff":3},
    }

    with col_sel1:
        selected_district = st.selectbox("📍 상권 유형", list(district_base.keys()))
    with col_sel2:
        selected_size     = st.selectbox("🏪 점포 규모", list(size_base.keys()))
    with col_sel3:
        selected_mkt = st.multiselect("📢 마케팅 전략 (복수 선택)", mkt_names,
                                       default=["인스타그램 광고"])

    # 계산
    d = district_base[selected_district]
    s = size_base[selected_size]

    base_sales = (d["min"] + d["max"]) / 2
    mkt_boost  = sum([mkt_sales[mkt_names.index(m)] for m in selected_mkt if m in mkt_names])
    est_sales  = round(base_sales * (1 + mkt_boost / 100))

    rent       = d["rent"]
    labor      = s["staff"] * 250
    material   = round(est_sales * 0.28)
    fixed_cost = rent + labor + material + 80
    net_profit = est_sales - fixed_cost
    recovery   = round(s["invest"] / max(net_profit, 1), 1)

    st.markdown("<br>", unsafe_allow_html=True)
    r1, r2, r3, r4, r5 = st.columns(5)
    sim_items = [
    ("예상 월매출",     f"{est_sales:,}만원"),
    ("예상 고정비",     f"{fixed_cost:,}만원"),
    ("예상 순이익",     f"{net_profit:,}만원"),
    ("초기 투자비",     f"{s['invest']:,}만원"),
    ("예상 회수 기간",  f"{recovery}개월"),
    ]
    for col, (label, value) in zip([r1,r2,r3,r4,r5], sim_items):
        with col:
            st.markdown(f"""
            <div class="sim-result">
              <div class="sim-label">{label}</div>
              <div class="sim-value">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 비용 구성 파이차트
    st.markdown('<p class="section-title">💰 예상 비용 구성</p>', unsafe_allow_html=True)
    left_pie, right_pie = st.columns(2)

    with left_pie:
        st.caption("월 고정비 구성")
        fig_pie1 = go.Figure(go.Pie(
            labels=["임대료","인건비","재료비","기타(공과금 등)"],
            values=[rent, labor, material, 80],
            hole=0.45,
            marker=dict(colors=["#1B3A6B","#4A90D9","#7EB8F7","#BDD7F5"]),
            textinfo="label+percent",
            textfont=dict(size=12),
        ))
        fig_pie1.update_layout(
            showlegend=False, height=280,
            margin=dict(t=10,b=10,l=10,r=10),
            paper_bgcolor="white",
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig_pie1, use_container_width=True)

    with right_pie:
        st.caption("초기 투자비 구성")
        invest_data = cost_df[cost_df["비교 항목"].isin(["인테리어","주방·냉동설비","간판·집기류","초도 물품비","가맹비"])]
        size_map = {"소형 (10평)":"소형(10평)(만원)", "중형 (15평)":"중형(15평)(만원)", "대형 (20평)":"대형(20평)(만원)"}
        cost_col = size_map[selected_size]
        fig_pie2 = go.Figure(go.Pie(
            labels=invest_data["비교 항목"].tolist(),
            values=invest_data[cost_col].tolist(),
            hole=0.45,
            marker=dict(colors=["#1B3A6B","#2D5BA3","#4A90D9","#7EB8F7","#BDD7F5"]),
            textinfo="label+percent",
            textfont=dict(size=12),
        ))
        fig_pie2.update_layout(
            showlegend=False, height=280,
            margin=dict(t=10,b=10,l=10,r=10),
            paper_bgcolor="white",
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig_pie2, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 3 — 매출현황
# ═══════════════════════════════════════════════
with tab3:

    st.markdown('<p class="section-title">🏆 매출 상위 5개 매장</p>', unsafe_allow_html=True)
    st.caption("2023-01 ~ 2025-12 (36개월) 총매출 기준")

    # 상위 5 매장 KPI
    top5_df = top_df.head(5).copy()
    top5_df["총매출(만원)"] = pd.to_numeric(top5_df["총매출(만원)"], errors="coerce")
    top5_df["월평균매출(만원)"] = pd.to_numeric(top5_df["월평균매출(만원)"], errors="coerce")

    t_cols = st.columns(5)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    medal_colors = ["#FFD700","#C0C0C0","#CD7F32","#4A90D9","#7EB8F7"]
    for col, (_, row), medal, mc in zip(t_cols, top5_df.iterrows(), medals, medal_colors):
        with col:
            name = row["매장명"].replace("젤라또 ","")
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:20px 14px;text-align:center;
                        border-top:4px solid {mc};border:1px solid #E5E9F2;
                        box-shadow:0 2px 10px rgba(27,58,107,0.07);">
              <div style="font-size:28px;margin-bottom:6px;">{medal}</div>
              <div style="font-size:13px;font-weight:700;color:#1B3A6B;margin-bottom:10px;">{row['매장명']}</div>
              <div style="font-size:11px;color:#7A8BA6;">총매출</div>
              <div style="font-size:17px;font-weight:800;color:#1B3A6B;">{int(row['총매출(만원)']):,}만</div>
              <div style="font-size:11px;color:#7A8BA6;margin-top:6px;">월평균</div>
              <div style="font-size:15px;font-weight:700;color:#4A90D9;">{row['월평균매출(만원)']:,.2f}만</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 월별 매출 추이 — 상위 5개
    st.markdown('<p class="section-title">📈 상위 5개 매장 월별 매출 추이 (2023~2025)</p>', unsafe_allow_html=True)
    st.caption("36개월 전체 데이터 — 시즌 패턴과 연도별 성장을 확인하세요")

    # 연도 필터
    year_filter = st.multiselect("📅 연도 선택", ["2023","2024","2025"], default=["2023","2024","2025"],
                                  key="year_top5")
    monthly_filtered = monthly_clean[monthly_clean["년도-월"].str[:4].isin(year_filter)]

    colors_top5 = ["#1B3A6B","#4A90D9","#2E9E6B","#E8742A","#9B59B6"]
    fig_line = go.Figure()
    for name, color in zip(top5_names, colors_top5):
        if name in monthly_filtered.columns:
            short = name.replace("젤라또 ","")
            fig_line.add_trace(go.Scatter(
                x=monthly_filtered["년도-월"],
                y=monthly_filtered[name],
                name=short,
                line=dict(color=color, width=2.5),
                mode="lines+markers",
                marker=dict(size=5),
                hovertemplate=f"<b>{short}</b><br>%{{x}}<br>%{{y:,.0f}}만원<extra></extra>",
            ))

    fig_line.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=10)),
        yaxis=dict(title="매출 (만원)", gridcolor="#F0F3F8"),
        legend=dict(orientation="h", y=1.08, font=dict(size=12)),
        margin=dict(t=20,b=60,l=10,r=10),
        height=420,
        font=dict(family="Noto Sans KR"),
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 전체 매장 현황
    st.markdown('<p class="section-title">📋 전체 매장 현황 (18개)</p>', unsafe_allow_html=True)

    col_view, col_filter = st.columns([3,1])
    with col_filter:
        sangkwon_filter = st.selectbox("상권 필터", ["전체"] + list(base_df["상권 유형"].unique()))

    filtered_base = base_df if sangkwon_filter == "전체" else base_df[base_df["상권 유형"] == sangkwon_filter]

    # 매장별 평균 월매출 바 차트
    fig_bar = go.Figure(go.Bar(
        x=filtered_base["매장명"],
        y=filtered_base["월매출(만원)"],
        marker=dict(
            color=filtered_base["월매출(만원)"],
            colorscale=[[0,"#BDD7F5"],[0.5,"#4A90D9"],[1,"#1B3A6B"]],
            showscale=False,
        ),
        text=filtered_base["월매출(만원)"].apply(lambda v: f"{int(v):,}만"),
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="<b>%{x}</b><br>월매출: %{y:,.0f}만원<extra></extra>",
    ))
    fig_bar.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(tickangle=-40, tickfont=dict(size=10), showgrid=False),
        yaxis=dict(title="월매출 (만원)", gridcolor="#F0F3F8"),
        margin=dict(t=20,b=80,l=10,r=10),
        height=380,
        font=dict(family="Noto Sans KR"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 상권별 평균 매출 비교
    st.markdown('<p class="section-title">🗺️ 상권별 평균 매출 비교</p>', unsafe_allow_html=True)

    sangkwon_avg = base_df.groupby("상권 유형")["월매출(만원)"].mean().reset_index()
    sangkwon_avg = sangkwon_avg.sort_values("월매출(만원)", ascending=False)

    sk_colors = {"관광":"#1B3A6B","오피스":"#4A90D9","주거":"#7EB8F7","대학가":"#BDD7F5"}
    fig_sk = go.Figure(go.Bar(
        x=sangkwon_avg["상권 유형"],
        y=sangkwon_avg["월매출(만원)"],
        marker_color=[sk_colors.get(t,"#4A90D9") for t in sangkwon_avg["상권 유형"]],
        text=sangkwon_avg["월매출(만원)"].apply(lambda v: f"{v:,.0f}만원"),
        textposition="outside",
        textfont=dict(size=13, color="#1B3A6B", family="Noto Sans KR"),
        width=0.5,
    ))
    fig_sk.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False, tickfont=dict(size=14)),
        yaxis=dict(title="평균 월매출 (만원)", gridcolor="#F0F3F8"),
        margin=dict(t=20,b=20,l=10,r=10),
        height=340,
        font=dict(family="Noto Sans KR"),
    )
    st.plotly_chart(fig_sk, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 전체 매장 연도별 총매출 성장
    st.markdown('<p class="section-title">📆 연도별 전체 매출 성장 추이</p>', unsafe_allow_html=True)
    st.caption("전 매장 합산 기준 — 창업 후 매출 성장 패턴을 보여드립니다")

    monthly_clean["년도"] = monthly_clean["년도-월"].str[:4]
    yearly = monthly_clean.groupby("년도")[store_cols].sum().sum(axis=1).reset_index()
    yearly.columns = ["년도","총매출(만원)"]
    growth = []
    for i, row in yearly.iterrows():
        if i == 0:
            growth.append(None)
        else:
            prev = yearly.loc[i-1,"총매출(만원)"]
            growth.append(round((row["총매출(만원)"]-prev)/prev*100,1))
    yearly["성장률"] = growth

    fig_year = make_subplots(specs=[[{"secondary_y": True}]])
    fig_year.add_trace(go.Bar(
        x=yearly["년도"], y=yearly["총매출(만원)"],
        name="연간 총매출",
        marker_color=["#BDD7F5","#4A90D9","#1B3A6B"],
        text=yearly["총매출(만원)"].apply(lambda v: f"{v:,.0f}만"),
        textposition="outside",
        textfont=dict(size=12),
    ), secondary_y=False)
    fig_year.add_trace(go.Scatter(
        x=yearly["년도"][1:], y=yearly["성장률"][1:],
        name="전년 대비 성장률",
        line=dict(color="#E8742A", width=2.5),
        mode="lines+markers+text",
        marker=dict(size=10),
        text=[f"+{v}%" for v in yearly["성장률"][1:]],
        textposition="top center",
        textfont=dict(size=12, color="#E8742A"),
    ), secondary_y=True)
    fig_year.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", y=1.08),
        margin=dict(t=20,b=20,l=10,r=10),
        height=340,
        font=dict(family="Noto Sans KR"),
        barmode="group",
    )
    fig_year.update_yaxes(title_text="총매출 (만원)", gridcolor="#F0F3F8", secondary_y=False)
    fig_year.update_yaxes(title_text="성장률 (%)", showgrid=False, secondary_y=True)
    st.plotly_chart(fig_year, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 4 — 창업안내
# ═══════════════════════════════════════════════
with tab4:

    st.markdown('<p class="section-title">🚀 창업 절차 안내</p>', unsafe_allow_html=True)
    st.caption("문의부터 오픈까지 젤라티코 전담팀이 함께합니다")

    steps = [
        ("창업 문의",      "온라인 폼 / 전화\n초기 관심 접수",     "1일"),
        ("브랜드 상담",    "1:1 전담 상담\n방향성·예산 협의",       "1주"),
        ("상권 분석",      "유동인구·입지·\n경쟁 점포 분석",        "2주"),
        ("점포 규모 산정", "10/15/20평 기준\n비용·수익 비교",       "1주"),
        ("가맹 계약",      "계약 조건 검토\n계약서 서명",            "1주"),
        ("인테리어/설비",  "브랜드 가이드\n시공 진행",               "4~6주"),
        ("교육/운영 준비", "제조·POS·CS\n교육 (본사 진행)",         "2주"),
        ("오픈 & 사후관리","그랜드 오픈\n6개월 밀착 지원",          "지속"),
    ]

    step_cols = st.columns(8)
    for col, (title, desc, period) in zip(step_cols, steps):
        with col:
            num = steps.index((title, desc, period)) + 1
            st.markdown(f"""
            <div class="step-card">
              <div style="width:32px;height:32px;background:#1B3A6B;color:white;border-radius:50%;
                          display:flex;align-items:center;justify-content:center;
                          font-weight:700;font-size:14px;margin:0 auto 10px auto;">{num}</div>
              <div class="step-title">{title}</div>
              <div class="step-desc">{desc}</div>
              <div class="step-period">{period}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 초기 비용 섹션
    st.markdown('<p class="section-title">💰 창업 초기 비용 안내</p>', unsafe_allow_html=True)

    cost_col1, cost_col2 = st.columns([3,2])

    with cost_col1:
        # 점포 규모별 비용 테이블
        display_cost = cost_df.copy()
        display_cost.columns = ["항목","소형(10평)","중형(15평)","대형(20평)","비고"]

        def highlight_total(row):
            if row["항목"] in ["총 초기 투자비"]:
                return ["background-color:#EEF4FF;font-weight:700;color:#1B3A6B"]*len(row)
            elif row["항목"] in ["예상 월매출","예상 투자 회수"]:
                return ["background-color:#F0FBF0;font-weight:600;color:#2E7D32"]*len(row)
            return [""]*len(row)

        styled = display_cost.style.apply(highlight_total, axis=1)\
            .set_properties(**{"font-size":"13px","text-align":"center"})\
            .set_table_styles([
                {"selector":"thead th","props":[("background","#1B3A6B"),("color","white"),
                                                 ("font-size","13px"),("text-align","center"),
                                                 ("padding","10px")]},
                {"selector":"tbody td","props":[("padding","8px 12px"),("border","1px solid #E5E9F2")]},
            ])
        st.dataframe(styled, use_container_width=True, hide_index=True)

    with cost_col2:
        # 초기 투자비 비교 막대
        fig_cost = go.Figure(go.Bar(
            x=["소형(10평)","중형(15평)","대형(20평)"],
            y=[5500, 7300, 9700],
            marker_color=["#BDD7F5","#4A90D9","#1B3A6B"],
            text=["5,500만원","7,300만원","9,700만원"],
            textposition="outside",
            textfont=dict(size=12, color="#1B3A6B"),
            width=0.5,
        ))
        fig_cost.update_layout(
            title=dict(text="점포 규모별 총 초기 투자비", font=dict(size=14,color="#1B3A6B")),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(title="투자비 (만원)", gridcolor="#F0F3F8", range=[0,12000]),
            margin=dict(t=40,b=20,l=10,r=10),
            height=320,
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 상권 분석 카드
    st.markdown('<p class="section-title">🗺️ 상권별 창업 가이드</p>', unsafe_allow_html=True)

    sk_icons = {"오피스 상권":"🏢","대학가 상권":"🎓","주거 상권":"🏘️","관광 상권":"🗼"}
    sk_colors_card = {"오피스 상권":"#E8F4FD","대학가 상권":"#F0FBF0","주거 상권":"#FFF7E8","관광 상권":"#F5F0FF"}
    sk_border = {"오피스 상권":"#4A90D9","대학가 상권":"#2E9E6B","주거 상권":"#E8742A","관광 상권":"#9B59B6"}

    sk_cols = st.columns(4)
    for col, (_, row) in zip(sk_cols, district_df.iterrows()):
        sk_type = row["상권 유형"]
        icon = sk_icons.get(sk_type, "📍")
        bg   = sk_colors_card.get(sk_type, "#F8F9FC")
        br   = sk_border.get(sk_type, "#4A90D9")
        with col:
            st.markdown(f"""
            <div style="background:{bg};border-radius:14px;padding:20px 16px;
                        border-top:4px solid {br};border:1px solid #E5E9F2;">
              <div style="font-size:28px;margin-bottom:8px;">{icon}</div>
              <div style="font-size:14px;font-weight:700;color:#1B3A6B;margin-bottom:12px;">{sk_type}</div>
              <div style="font-size:12px;color:#5A6A7E;line-height:1.9;">
                👥 {row['주 고객층']}<br>
                🚶 일평균 {int(row['일평균 유동인구(명)']):,}명<br>
                🏪 추천 규모: {row['추천 규모']}<br>
                💰 평균 임대료: {int(row['평균 임대료(만원)']):,}만원<br>
                📈 예상 월매출: {row['예상 월매출(만원)']}만원
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # 문의 섹션
    st.markdown('<p class="section-title">📞 창업 문의</p>', unsafe_allow_html=True)

    contact_l, contact_r = st.columns([1,1])

    with contact_l:
        st.markdown("""
        <div class="contact-box">
          <div style="font-size:14px;color:rgba(255,255,255,0.75);margin-bottom:6px;letter-spacing:1px;">FRANCHISE CONTACT</div>
          <div class="contact-name">홍 길 동 대표</div>
          <div class="contact-phone">010-XXXX-XXXX</div>
          <div class="contact-note">📅 평일 09:00 ~ 18:00 (주말·공휴일 휴무)<br>
          📧 franchise@gelatico.co.kr</div>
          <div style="margin-top:20px;background:rgba(255,255,255,0.15);border-radius:10px;padding:12px;">
            <div style="font-size:13px;color:rgba(255,255,255,0.9);">
              ✅ 창업 상담은 무료입니다<br>
              ✅ 상권 분석 리포트 무상 제공<br>
              ✅ 계약 전 취소 수수료 없음
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with contact_r:
        st.markdown("""
        <div style="background:white;border-radius:16px;padding:32px;border:1px solid #E5E9F2;
                    box-shadow:0 2px 12px rgba(27,58,107,0.07);">
          <div style="font-size:16px;font-weight:700;color:#1B3A6B;margin-bottom:20px;">📝 간편 온라인 문의</div>
        """, unsafe_allow_html=True)

        name_input    = st.text_input("성함", placeholder="홍길동")
        phone_input   = st.text_input("연락처", placeholder="010-0000-0000")
        region_input  = st.text_input("희망 지역 (예: 서울 강남, 부산 해운대)")
        message_input = st.text_area("문의 내용", placeholder="창업 관련 궁금한 점을 자유롭게 적어주세요.", height=100)

        if st.button("📨 문의하기", use_container_width=True, type="primary"):
            if name_input and phone_input:
                st.success(f"✅ {name_input}님의 문의가 접수되었습니다! 1~2 영업일 내 연락드리겠습니다.")
            else:
                st.warning("성함과 연락처를 입력해주세요.")

        st.markdown("</div>", unsafe_allow_html=True)

    # 하단 푸터
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:24px;color:#A0AFBF;font-size:13px;
                border-top:1px solid #E5E9F2;margin-top:20px;">
      <b style="color:#1B3A6B;font-size:16px;">GELATICO 젤라티코</b><br>
      이탈리아의 맛, 당신의 매장에서 — Taste of Italy, In Your Hands<br><br>
      © 2025 Gelatico Franchise. All rights reserved. | 가상 프로젝트 (바이브 코딩 실습)
    </div>
    """, unsafe_allow_html=True)
