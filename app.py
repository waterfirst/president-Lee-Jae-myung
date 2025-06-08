import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="이재명 대통령 정책공약 기반 투자 분석",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f4e79, #2e6da4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .sector-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f4e79;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .highlight-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1f4e79;
    }
    .policy-tag {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #1a1a1a;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.8rem;
        margin: 0.1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 정의
@st.cache_data
def load_investment_data():
    # BIG3 신산업 데이터
    big3_data = {
        '시스템반도체': [
            {'종목명': 'SK하이닉스', '티커': '000660', '구분': '메모리+시스템반도체', '투자포인트': '종합반도체 강국 정책'},
            {'종목명': '삼성전자', '티커': '005930', '구분': '파운드리+메모리', '투자포인트': '대·중소기업 상생협력'},
            {'종목명': '원익IPS', '티커': '240810', '구분': '반도체 제조장비', '투자포인트': '소재·부품·장비 지원'},
            {'종목명': '솔브레인', '티커': '357780', '구분': '반도체 화학소재', '투자포인트': '100대 품목 공급안정성'}
        ],
        '미래차': [
            {'종목명': '현대차', '티커': '005380', '구분': '전기차·수소차', '투자포인트': '전기·수소차 연계산업 육성'},
            {'종목명': '기아', '티커': '000270', '구분': '글로벌 전기차', '투자포인트': '2024년 완전자율주행차'},
            {'종목명': 'LG에너지솔루션', '티커': '373220', '구분': '전기차 배터리', '투자포인트': '차량용 배터리 기술개발'},
            {'종목명': '현대모비스', '티커': '012330', '구분': '자율주행 부품', '투자포인트': '자율주행 인프라 구축'}
        ],
        '바이오헬스': [
            {'종목명': '셀트리온', '티커': '068270', '구분': '바이오의약품', '투자포인트': '글로벌 바이오 생산허브'},
            {'종목명': '삼성바이오로직스', '티커': '207940', '구분': 'CMO 서비스', '투자포인트': '바이오 클러스터 조성'},
            {'종목명': '씨젠', '티커': '096530', '구분': '분자진단', '투자포인트': '메디푸드·대체식품 R&D'},
            {'종목명': '녹십자', '티커': '006280', '구분': '백신·혈액제제', '투자포인트': '2030년 점유율 3배 확대'}
        ]
    }
    
    # 그린뉴딜 데이터
    green_data = {
        '재생에너지': [
            {'종목명': '한화솔루션', '티커': '009830', '구분': '태양광 모듈', '투자포인트': '새만금 2.1GW 태양광'},
            {'종목명': '두산에너빌리티', '티커': '034020', '구분': '해상풍력', '투자포인트': '서남해 2.4GW 해상풍력'},
            {'종목명': '삼성SDI', '티커': '006400', '구분': 'ESS 배터리', '투자포인트': 'ESS 연계 비즈니스'},
            {'종목명': 'LS ELECTRIC', '티커': '010120', '구분': '전력변환장치', '투자포인트': '스마트그리드 구축'}
        ],
        '수소경제': [
            {'종목명': '두산퓨얼셀', '티커': '336260', '구분': '수소연료전지', '투자포인트': '모빌리티·에너지 양대축'},
            {'종목명': '현대차', '티커': '005380', '구분': '수소승용·상용차', '투자포인트': '수소경제 생태계 구축'},
            {'종목명': '효성중공업', '티커': '267270', '구분': '수소충전소', '투자포인트': '수소충전소 660기 확충'}
        ]
    }
    
    # TMT 데이터
    tmt_data = {
        '5G·AI·빅데이터': [
            {'종목명': 'SK텔레콤', '티커': '017670', '구분': '5G 네트워크', '투자포인트': '스마트시티 2025년 전국토'},
            {'종목명': '네이버', '티커': '035420', '구분': '클라우드 서비스', '투자포인트': '중소기업 ICT 솔루션'},
            {'종목명': '카카오', '티커': '035720', '구분': 'AI 플랫폼', '투자포인트': '빅데이터·AI 신산업'},
            {'종목명': '안랩', '티커': '053800', '구분': '사이버보안', '투자포인트': '드론·자율주행 보안'}
        ],
        '콘텐츠': [
            {'종목명': '엔씨소프트', '티커': '036570', '구분': '글로벌 게임', '투자포인트': '콘텐츠 제작비 세액공제'},
            {'종목명': 'HYBE', '티커': '352820', '구분': 'K-콘텐츠', '투자포인트': '브랜드K 제품 확대'},
            {'종목명': 'CJ ENM', '티커': '035760', '구분': '콘텐츠 제작', '투자포인트': '콘텐츠 R&D 예산 1% 확대'}
        ]
    }
    
    # 정책 예산 데이터
    policy_budget = {
        '정책명': ['반도체 R&D', '소재부품장비', '스마트공장', '상생협력기금', '콘텐츠 R&D'],
        '예산규모': [1, 5, 0.5, 1, 0.3],
        '기간': ['10년간', '3년간', '2022년까지', '신규조성', '현재→목표'],
        '단위': ['조원', '조원', '조원', '조원', '% 확대']
    }
    
    return big3_data, green_data, tmt_data, policy_budget

# 메인 앱
def main():
    st.markdown('<h1 class="main-header">🇰🇷 이재명 대통령 정책공약 기반 투자 분석</h1>', unsafe_allow_html=True)
    
    # 사이드바
    st.sidebar.header("📊 분석 메뉴")
    analysis_type = st.sidebar.selectbox(
        "분석 유형 선택",
        ["정책 개요", "BIG3 신산업", "그린뉴딜", "TMT·디지털", "정책 예산 현황", "투자 전략"]
    )
    
    big3_data, green_data, tmt_data, policy_budget = load_investment_data()
    
    if analysis_type == "정책 개요":
        show_policy_overview()
    elif analysis_type == "BIG3 신산업":
        show_big3_analysis(big3_data)
    elif analysis_type == "그린뉴딜":
        show_green_analysis(green_data)
    elif analysis_type == "TMT·디지털":
        show_tmt_analysis(tmt_data)
    elif analysis_type == "정책 예산 현황":
        show_budget_analysis(policy_budget)
    elif analysis_type == "투자 전략":
        show_investment_strategy()

def show_policy_overview():
    st.header("📋 정책 개요")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="highlight-number">10조원</div>
            <div>반도체 R&D 투자</div>
            <div style="font-size: 0.8rem; color: #666;">10년간</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="highlight-number">5조원</div>
            <div>소재부품장비</div>
            <div style="font-size: 0.8rem; color: #666;">3년간</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="highlight-number">660기</div>
            <div>수소충전소</div>
            <div style="font-size: 0.8rem; color: #666;">2030년</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="highlight-number">3만개</div>
            <div>스마트공장</div>
            <div style="font-size: 0.8rem; color: #666;">2022년</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 주요 정책 영역
    st.subheader("🎯 주요 정책 영역")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="sector-card">
            <h4>🚀 BIG3 신산업</h4>
            <p><span class="policy-tag">시스템반도체</span> <span class="policy-tag">미래차</span> <span class="policy-tag">바이오헬스</span></p>
            <p>2030년 차세대 주력산업으로 육성</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sector-card">
            <h4>🌱 그린뉴딜</h4>
            <p><span class="policy-tag">재생에너지</span> <span class="policy-tag">수소경제</span> <span class="policy-tag">탄소중립</span></p>
            <p>2040년 미세먼지 10㎍/㎥ 달성</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="sector-card">
            <h4>📱 TMT·디지털</h4>
            <p><span class="policy-tag">5G·AI</span> <span class="policy-tag">스마트시티</span> <span class="policy-tag">드론·자율주행</span></p>
            <p>2024-2025년 상용화 목표</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sector-card">
            <h4>💰 금융·벤처</h4>
            <p><span class="policy-tag">핀테크</span> <span class="policy-tag">스톡옵션</span> <span class="policy-tag">스타트업</span></p>
            <p>벤처투자 활성화 및 규제완화</p>
        </div>
        """, unsafe_allow_html=True)

def show_big3_analysis(big3_data):
    st.header("🚀 BIG3 신산업 투자 분석")
    
    tab1, tab2, tab3 = st.tabs(["시스템반도체", "미래차", "바이오헬스"])
    
    with tab1:
        st.subheader("🔬 시스템반도체 (2030년 종합 반도체 강국)")
        df = pd.DataFrame(big3_data['시스템반도체'])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df, use_container_width=True)
        with col2:
            st.info("💰 **투자 규모**\n\n차세대 지능형 반도체 R&D\n**10년간 1조원** 투자")
        
        # 구분별 분포 차트
        구분_count = df['구분'].value_counts()
        fig = px.pie(values=구분_count.values, names=구분_count.index, 
                    title="시스템반도체 분야별 종목 분포")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🚗 미래차 (2030년 미래차 경쟁력 1위)")
        df = pd.DataFrame(big3_data['미래차'])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df, use_container_width=True)
        with col2:
            st.info("🎯 **정책 목표**\n\n• 2024년 완전자율주행 상용화\n• 전기·수소차 연계산업 육성\n• 배터리 소재 국산화")
        
        # 미래차 밸류체인 시각화
        categories = ['완성차', '배터리', '부품']
        counts = [df[df['구분'].str.contains(cat)].shape[0] for cat in categories]
        
        fig = go.Figure(data=[go.Bar(x=categories, y=counts, 
                                   marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'])])
        fig.update_layout(title="미래차 밸류체인별 종목 수", yaxis_title="종목 수")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🧬 바이오헬스 (5대 수출 주력산업)")
        df = pd.DataFrame(big3_data['바이오헬스'])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df, use_container_width=True)
        with col2:
            st.info("📈 **성장 목표**\n\n2030년 제약·의료기기\n세계시장 점유율\n**3배 확대**")

def show_green_analysis(green_data):
    st.header("🌱 그린뉴딜 투자 분석")
    
    tab1, tab2 = st.tabs(["재생에너지", "수소경제"])
    
    with tab1:
        st.subheader("☀️ 재생에너지 (재생에너지 3020 목표)")
        df = pd.DataFrame(green_data['재생에너지'])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df, use_container_width=True)
        with col2:
            st.success("🎯 **주요 프로젝트**\n\n• 새만금 2.1GW 태양광\n• 서남해 2.4GW 해상풍력\n• ESS 연계 비즈니스")
        
        # 재생에너지 프로젝트 규모
        projects = ['새만금 태양광', '서남해 해상풍력']
        capacity = [2.1, 2.4]
        
        fig = go.Figure(data=[go.Bar(x=projects, y=capacity, 
                                   marker_color=['#FFA500', '#87CEEB'])])
        fig.update_layout(title="주요 재생에너지 프로젝트 규모 (GW)", yaxis_title="발전용량 (GW)")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("💨 수소경제 (2030년 수소충전소 660기)")
        df = pd.DataFrame(green_data['수소경제'])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df, use_container_width=True)
        with col2:
            st.success("⚡ **인프라 목표**\n\n2030년까지\n수소충전소\n**660기 구축**")

def show_tmt_analysis(tmt_data):
    st.header("📱 TMT·디지털 투자 분석")
    
    tab1, tab2 = st.tabs(["5G·AI·빅데이터", "콘텐츠"])
    
    with tab1:
        st.subheader("🤖 5G·AI·빅데이터")
        df = pd.DataFrame(tmt_data['5G·AI·빅데이터'])
        st.dataframe(df, use_container_width=True)
        
        st.info("🏙️ **스마트시티 확산**\n\n2025년까지 전국토로 스마트시티 확산\nCCTV 연계 국민안전 통합플랫폼 매년 30개씩 보급")
    
    with tab2:
        st.subheader("🎮 게임·콘텐츠")
        df = pd.DataFrame(tmt_data['콘텐츠'])
        st.dataframe(df, use_container_width=True)
        
        # 콘텐츠 지원 정책
        policies = ['제작비 세액공제', 'R&D 예산 확대', '브랜드K 지원']
        benefits = ['중소 15%, 중견 10%, 대기업 5%', '0.3% → 1%', '500개사 육성']
        
        policy_df = pd.DataFrame({'정책': policies, '혜택': benefits})
        st.subheader("📺 콘텐츠 지원 정책")
        st.table(policy_df)

def show_budget_analysis(policy_budget):
    st.header("💰 정책 예산 현황")
    
    df = pd.DataFrame(policy_budget)
    
    # 예산 규모 시각화
    fig = px.bar(df, x='정책명', y='예산규모', 
                title="주요 정책별 예산 규모",
                labels={'예산규모': '예산 (조원)', '정책명': '정책 분야'})
    fig.update_traces(marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    st.plotly_chart(fig, use_container_width=True)
    
    # 예산 테이블
    st.subheader("📊 정책별 상세 예산")
    st.dataframe(df, use_container_width=True)
    
    # 예산 총액 계산
    total_budget = df['예산규모'].sum()
    st.metric("총 정책 예산", f"{total_budget}조원", "주요 정책 합계")

def show_investment_strategy():
    st.header("📈 투자 전략 가이드")
    
    # 투자 시점별 전략
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="sector-card">
            <h4>🎯 단기 (1-2년)</h4>
            <p><strong>핵심 테마</strong></p>
            <ul>
                <li>재생에너지 정책 초기 수혜</li>
                <li>드론·자율주행 상용화</li>
                <li>핀테크 규제완화</li>
                <li>스마트공장 보급 확대</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="sector-card">
            <h4>🎯 중기 (3-5년)</h4>
            <p><strong>핵심 테마</strong></p>
            <ul>
                <li>시스템반도체 R&D 투자</li>
                <li>미래차 글로벌 경쟁력</li>
                <li>수소경제 인프라 구축</li>
                <li>소재부품장비 육성</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="sector-card">
            <h4>🎯 장기 (5-10년)</h4>
            <p><strong>핵심 테마</strong></p>
            <ul>
                <li>바이오헬스 글로벌화</li>
                <li>전 산업 디지털 전환</li>
                <li>탄소중립 정책 가속화</li>
                <li>스타트업 유니콘 육성</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 리스크 요인
    st.subheader("⚠️ 투자 리스크 고려사항")
    
    risk_data = {
        '리스크 유형': ['정책 변경', '글로벌 경쟁', '예산 제약', '기술 변화'],
        '위험도': ['중간', '높음', '중간', '높음'],
        '대응 방안': [
            '정치적 안정성 모니터링',
            '기술 경쟁력 확보 기업 선별',
            '재정 건전성 있는 정책 우선',
            '신기술 트렌드 지속 추적'
        ]
    }
    
    risk_df = pd.DataFrame(risk_data)
    st.dataframe(risk_df, use_container_width=True)
    
    st.warning("⚠️ **면책조항**: 본 분석은 정책공약을 바탕으로 한 투자 아이디어 제공을 목적으로 하며, 투자 결정은 개별 투자자의 판단과 책임하에 이루어져야 합니다.")

if __name__ == "__main__":
    main()
