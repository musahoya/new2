"""
프롬프트 엔지니어링 자동화 - Streamlit 프론트엔드
"""
import streamlit as st
import requests
import json
from typing import Dict, Any

# 페이지 설정
st.set_page_config(
    page_title="프롬프트 엔지니어링 자동화",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API 엔드포인트
API_BASE_URL = "http://localhost:8000"

# 커스텀 CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .strategy-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .prompt-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    .trend-item {
        padding: 0.5rem;
        margin: 0.3rem 0;
        background-color: #e3f2fd;
        border-radius: 5px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def init_session_state():
    """세션 스테이트 초기화"""
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "prompts_result" not in st.session_state:
        st.session_state.prompts_result = None
    if "selected_strategy" not in st.session_state:
        st.session_state.selected_strategy = None


def call_api(endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """API 호출 헬퍼 함수"""
    try:
        if data:
            response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        else:
            response = requests.get(f"{API_BASE_URL}{endpoint}")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("⚠️ 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
        st.info("터미널에서 다음 명령어로 서버를 실행하세요:\n\n`cd backend && python -m uvicorn app.main:app --reload`")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API 호출 실패: {str(e)}")
        return None


def display_header():
    """헤더 표시"""
    st.markdown('<h1 class="main-header">✨ 프롬프트 엔지니어링 자동화</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # 설명
    st.markdown(
        """
    ### 🎯 무엇을 할 수 있나요?

    1. **자동 트렌드 조사**: AI가 최신 정보를 자동으로 수집합니다
    2. **의도 파악**: 당신이 원하는 것을 정확히 이해합니다
    3. **5가지 전략**: CoT, Few-Shot, Meta, Self-Refine, Structured 프롬프트를 생성합니다
    4. **즉시 사용**: 생성된 프롬프트를 복사하여 바로 사용하세요
    """
    )
    st.markdown("---")


def step1_input():
    """1단계: 사용자 입력"""
    st.header("📝 1단계: 무엇을 도와드릴까요?")

    user_query = st.text_area(
        "원하는 내용을 입력하세요",
        placeholder="예: 제주도 3박4일 여행 계획 짜줘\n예: 2025년 반도체 산업 투자 전망 분석\n예: 겨울 서울 데이트 코스 블로그 글",
        height=150,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 분석 시작", use_container_width=True, type="primary"):
            if user_query.strip():
                with st.spinner("🔍 AI가 분석하고 최신 트렌드를 수집하고 있습니다..."):
                    # API 호출
                    result = call_api("/api/analyze", {"query": user_query})

                    if result:
                        st.session_state.analysis_result = result
                        st.session_state.step = 2
                        st.rerun()
            else:
                st.warning("⚠️ 내용을 입력해주세요!")


def step2_confirmation():
    """2단계: 분석 결과 확인"""
    st.header("📊 2단계: 분석 결과 확인")

    if not st.session_state.analysis_result:
        st.error("분석 결과가 없습니다.")
        return

    result = st.session_state.analysis_result
    intent = result["intent"]
    trends = result["trends"]

    # 분석 결과 표시
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 의도 분석")
        st.info(f"""
        **입력:** {result['query']}

        **목적:** {intent['primary_intent']}

        **형식:** {intent['output_type']}

        **대상:** {intent['target_audience']}

        **분야:** {intent['domain']}

        **신뢰도:** {intent['confidence']:.1%}
        """)

    with col2:
        st.subheader("🔥 수집된 트렌드 TOP 10")
        for i, trend in enumerate(trends["trends"], 1):
            st.markdown(f'<div class="trend-item">{i}. {trend}</div>', unsafe_allow_html=True)

    # 요약
    st.subheader("💬 트렌드 요약")
    st.write(trends["summary"])

    # 확인 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("⬅️ 다시 입력", use_container_width=True):
            st.session_state.step = 1
            st.session_state.analysis_result = None
            st.rerun()

    with col3:
        if st.button("✅ 맞아요! 계속하기", use_container_width=True, type="primary"):
            with st.spinner("🎨 5가지 프롬프팅 전략을 생성하고 있습니다..."):
                # 프롬프트 생성
                prompts_result = call_api("/api/generate-prompts", st.session_state.analysis_result)

                if prompts_result:
                    st.session_state.prompts_result = prompts_result
                    st.session_state.step = 3
                    st.rerun()


def step3_prompts():
    """3단계: 프롬프트 선택"""
    st.header("✨ 3단계: 프롬프팅 전략 선택")

    if not st.session_state.prompts_result:
        st.error("프롬프트 결과가 없습니다.")
        return

    prompts = st.session_state.prompts_result["prompts"]["prompts"]

    # 전략 카드 표시
    st.markdown("### 🎯 5가지 전략을 확인하고 선택하세요")

    for prompt_strategy in prompts:
        with st.expander(
            f"{prompt_strategy['icon']} {prompt_strategy['name']} - {prompt_strategy['best_for']}",
            expanded=False,
        ):
            st.markdown(f"**설명:** {prompt_strategy['description']}")
            st.markdown(f"**최적 용도:** {prompt_strategy['best_for']}")

            st.markdown("**생성된 프롬프트:**")
            st.code(prompt_strategy["prompt"], language="text")

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(
                    "📋 이 전략 선택",
                    key=f"select_{prompt_strategy['type']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_strategy = prompt_strategy
                    st.session_state.step = 4
                    st.rerun()

    # 뒤로 가기
    st.markdown("---")
    if st.button("⬅️ 분석 결과로 돌아가기"):
        st.session_state.step = 2
        st.rerun()


def step4_final():
    """4단계: 최종 프롬프트"""
    st.header("🎉 완성된 프롬프트")

    if not st.session_state.selected_strategy:
        st.error("선택된 전략이 없습니다.")
        return

    strategy = st.session_state.selected_strategy

    # 축하 메시지
    st.success(f"✅ **{strategy['name']}** 전략을 선택하셨습니다!")

    # 최종 프롬프트 표시
    st.markdown("### 📄 완성된 프롬프트")
    st.markdown(
        f'<div class="prompt-box">{strategy["prompt"]}</div>',
        unsafe_allow_html=True,
    )

    # 복사 기능
    st.code(strategy["prompt"], language="text")

    st.info("💡 위 프롬프트를 복사하여 ChatGPT, Claude 등 AI 서비스에 붙여넣으세요!")

    # 버튼들
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🔄 다른 전략 보기", use_container_width=True):
            st.session_state.step = 3
            st.session_state.selected_strategy = None
            st.rerun()

    with col3:
        if st.button("🆕 새로 시작하기", use_container_width=True, type="primary"):
            st.session_state.step = 1
            st.session_state.analysis_result = None
            st.session_state.prompts_result = None
            st.session_state.selected_strategy = None
            st.rerun()


def main():
    """메인 함수"""
    init_session_state()
    display_header()

    # 사이드바
    with st.sidebar:
        st.header("📌 진행 단계")
        steps = [
            "1️⃣ 입력",
            "2️⃣ 분석 확인",
            "3️⃣ 전략 선택",
            "4️⃣ 완성",
        ]

        for i, step in enumerate(steps, 1):
            if i == st.session_state.step:
                st.markdown(f"**➡️ {step}**")
            elif i < st.session_state.step:
                st.markdown(f"✅ {step}")
            else:
                st.markdown(f"⚪ {step}")

        st.markdown("---")
        st.markdown(
            """
        ### 💡 팁

        - 구체적으로 입력할수록 좋아요
        - 원하는 형식을 명시하세요
        - 대상 독자를 언급하세요

        ### 📚 프롬프팅 전략

        - **CoT**: 복잡한 분석
        - **Few-Shot**: 블로그 글
        - **Meta**: 전문 리뷰
        - **Self-Refine**: 고품질
        - **Structured**: 보고서
        """
        )

    # 단계별 화면 표시
    if st.session_state.step == 1:
        step1_input()
    elif st.session_state.step == 2:
        step2_confirmation()
    elif st.session_state.step == 3:
        step3_prompts()
    elif st.session_state.step == 4:
        step4_final()


if __name__ == "__main__":
    main()
