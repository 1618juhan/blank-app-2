import streamlit as st
import time

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(page_title="Click Tycoon", page_icon="💰")

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
    if st.session_state.shop["party"] and current_time - st.session_state.party_last_used >= 20:
        st.session_state.party_last_used = current_time
        st.session_state.party_active_until = current_time + 7
    if st.session_state.gold >= GOAL:
        st.session_state.gold = GOAL
        st.session_state.game_over = True

auto_gold()  # 클릭 전에도 오토 골드 갱신

# -------------------------------
# 1초마다 자동 새로고침
# -------------------------------
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1000, key="auto_refresh")  # 1000ms = 1초

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
        auto_gold()
        if st.session_state.shop["party"] and current_time <= st.session_state.party_active_until:
            st.session_state.gold += st.session_state.click_value*3
        else:
            st.session_state.gold += st.session_state.click_value
        if st.session_state.gold >= GOAL:
            st.session_state.gold = GOAL
            st.session_state.game_over = True
        st.experimental_rerun()

# -------------------------------
# 상점 버튼
# -------------------------------
st.subheader("상점")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("100골드 Auto1", key="auto1_btn"):
        if st.session_state.gold >= 100:
            st.session_state.gold -= 100
            st.session_state.shop["auto1"] = True
            st.experimental_rerun()
with col2:
    if st.button("300골드 Auto2", key="auto2_btn"):
        if st.session_state.gold >= 300:
            st.session_state.gold -= 300
            st.session_state.shop["auto2"] = True
            st.experimental_rerun()
with col3:
    if st.button("500골드 Party", key="party_btn"):
        if st.session_state.gold >= 500:
            st.session_state.gold -= 500
            st.session_state.shop["party"] = True
            st.session_state.party_last_used = time.time()
            st.session_state.party_active_until = time.time() + 7
            st.experimental_rerun()
with col4:
    if st.button("1000골드 Auto3", key="auto3_btn"):
        if st.session_state.gold >= 1000:
            st.session_state.gold -= 1000
            st.session_state.shop["auto3"] = True
            st.experimental_rerun()
with col5:
    if st.button("5000골드 Auto4", key="auto4_btn"):
        if st.session_state.gold >= 5000:
            st.session_state.gold -= 5000
            st.session_state.shop["auto4"] = True
            st.experimental_rerun()

# -------------------------------
# 목표 달성 메시지
# -------------------------------
if st.session_state.game_over:
    st.success("축하합니다! 목표 99999 골드 달성!")