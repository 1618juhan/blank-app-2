import streamlit as st

# -------------------------------
# 앱 제목
# -------------------------------
st.title("MBTI 학습 유형 진단")

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if 'answers' not in st.session_state:
    st.session_state['answers'] = {}

# -------------------------------
# MBTI 질문과 선택지
# -------------------------------
questions = {
    "Q1. 학습할 때 새로운 것을 시도하는 것을 좋아한다.": ["그렇다", "보통", "그렇지 않다"],
    "Q2. 계획을 세우고 체계적으로 학습하는 편이다.": ["그렇다", "보통", "그렇지 않다"],
    "Q3. 시각적 자료를 활용하면 이해가 쉽다.": ["그렇다", "보통", "그렇지 않다"],
    "Q4. 학습 중 토론이나 대화를 통해 이해가 깊어진다.": ["그렇다", "보통", "그렇지 않다"],
    "Q5. 학습 중 직관을 믿고 결정을 내리는 편이다.": ["그렇다", "보통", "그렇지 않다"],
    "Q6. 실습이나 경험을 통해 학습하는 것이 효과적이다.": ["그렇다", "보통", "그렇지 않다"]
}

# -------------------------------
# 질문 표시
# -------------------------------
for q, options in questions.items():
    st.session_state['answers'][q] = st.radio(q, options, key=q)

# -------------------------------
# 제출 버튼
# -------------------------------
if st.button("제출"):
    # 간단 MBTI 계산 로직 예시 (실제 MBTI 심화 로직 아님)
    # '그렇다' 선택 개수로 간단 유형 결정
    score = sum(1 for ans in st.session_state['answers'].values() if ans == "그렇다")

    if score >= 5:
        mbti_type = "ENTJ"
        learning_type = "계획적이며 도전적인 학습자"
    elif score >= 3:
        mbti_type = "INFP"
        learning_type = "자기 주도적이며 감성적인 학습자"
    else:
        mbti_type = "ISFJ"
        learning_type = "신중하고 체계적인 학습자"

    st.subheader("결과")
    st.write(f"**MBTI 유형:** {mbti_type}")
    st.write(f"**학습 유형 설명:** {learning_type}")
    

