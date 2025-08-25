import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(page_title="Click Tycoon", page_icon="💰")

# -------------------------------
# 1초마다 자동 새로고침
# -------------------------------
st_autorefresh(interval=1000, key="auto_refresh")  # 1000ms = 1초

# -------------------------------
# 세션 상태 초기화
# -------------------------------
if 'gold' not in st.session_state:
    st.session_state.gold = 0
if 'click_value' not in st.session_state:
    st.session_state.click_value = 1
if 'shop' not in st.session_state:
    st.session_state.shop = {"auto1": False, "auto2": False, "party": False, "auto3": False, "auto4": False}
if 'last_auto1' not in st.session_state:
    st.session_state.last_auto1 = time.time()
if 'last_auto2' not in st.session_state:
    st.session_state.last_auto2 = time.time()
if 'last_auto3' not in st.session_state:
    st.session_state.last_auto3 = time.time()
if 'last_auto4' not in st.session_state:
    st.session_state.last_auto4 = time.time()
if 'party_last_used' not in st.session_state:
    st.session_state.party_last_used = -20
if 'party_active_until' not in st.session_state:
    st.session_state.party_active_until = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

GOAL = 99999

# -------------------------------
# 자동 골드 계산
# -------------------------------
def auto_gold():
    current_time = time.time()
    # 게임오버 상태가 아닐 때만 자동 골드 획득
    if not st.session_state.game_over:
        if st.session_state.shop["auto1"] and current_time - st.session_state.last_auto1 >= 5:
            st.session_state.gold += 1
            st.session_state.last_auto1 = current_time
        if st.session_state.shop["auto2"] and current_time - st.session_state.last_auto2 >= 8:
            st.session_state.gold += 4
            st.session_state.last_auto2 = current_time
        if st.session_state.shop["auto3"] and current_time - st.session_state.last_auto3 >= 5:
            st.session_state.gold += 30
            st.session_state.last_auto3 = current_time
        if st.session_state.shop["auto4"] and current_time - st.session_state.last_auto4 >= 4:
            st.session_state.gold += 50
            st.session_state.last_auto4 = current_time

    # 파티 아이템 쿨타임 로직 (자동 골드 획득과 별개로 관리)
    if st.session_state.shop["party"] and current_time - st.session_state.party_last_used >= 20:
        # 이 부분은 파티 '사용' 로직이므로, 버튼 클릭 시에만 처리하는 것이 더 명확할 수 있습니다.
        # 자동 갱신 로직에 두면 쿨타임마다 자동으로 파티가 활성화될 수 있습니다.
        # 현재 코드에서는 파티 구매 시 바로 활성화되고, 클릭 시 효과가 적용되므로 이 로직은 그대로 두어도 큰 문제는 없습니다.
        pass

    if st.session_state.gold >= GOAL:
        st.session_state.gold = GOAL
        st.session_state.game_over = True

# 스크립트가 실행될 때마다 (1초마다 또는 인터랙션 시) 자동 골드 계산
auto_gold()

# -------------------------------
# 게임 화면
# -------------------------------
st.title("Click Tycoon 💰")
st.write(f"Gold: {st.session_state.gold}")

# 클릭 버튼
if st.session_state.game_over:
    st.button("게임 종료!", disabled=True, key="game_over_btn")
else:
    if st.button("Click!", key="click_btn"):
        current_time = time.time()
        if st.session_state.shop["party"] and current_time <= st.session_state.party_active_until:
            st.session_state.gold += st.session_state.click_value * 3
        else:
            st.session_state.gold += st.session_state.click_value

        if st.session_state.gold >= GOAL:
            st.session_state.gold = GOAL
            st.session_state.game_over = True
        # st.experimental_rerun() 제거

# -------------------------------
# 상점 버튼
# -------------------------------
st.subheader("상점")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("100골드 Auto1", key="auto1_btn", disabled=st.session_state.shop["auto1"]):
        if st.session_state.gold >= 100:
            st.session_state.gold -= 100
            st.session_state.shop["auto1"] = True
            # st.experimental_rerun() 제거
with col2:
    if st.button("300골드 Auto2", key="auto2_btn", disabled=st.session_state.shop["auto2"]):
        if st.session_state.gold >= 300:
            st.session_state.gold -= 300
            st.session_state.shop["auto2"] = True
            # st.experimental_rerun() 제거
with col3:
    if st.button("500골드 Party", key="party_btn", disabled=st.session_state.shop["party"]):
        if st.session_state.gold >= 500:
            st.session_state.gold -= 500
            st.session_state.shop["party"] = True
            now = time.time()
            st.session_state.party_last_used = now
            st.session_state.party_active_until = now + 7
            # st.experimental_rerun() 제거
with col4:
    if st.button("1000골드 Auto3", key="auto3_btn", disabled=st.session_state.shop["auto3"]):
        if st.session_state.gold >= 1000:
            st.session_state.gold -= 1000
            st.session_state.shop["auto3"] = True
            # st.experimental_rerun() 제거
with col5:
    if st.button("5000골드 Auto4", key="auto4_btn", disabled=st.session_state.shop["auto4"]):
        if st.session_state.gold >= 5000:
            st.session_state.gold -= 5000
            st.session_state.shop["auto4"] = True
            # st.experimental_rerun() 제거

# -------------------------------
# 목표 달성 메시지
# -------------------------------
if st.session_state.game_over:
    st.success("축하합니다! 목표 99999 골드 달성!")
    st.balloons()