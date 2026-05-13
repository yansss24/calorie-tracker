import streamlit as st
from datetime import datetime

# --- APP CONFIG & STYLING ---
st.set_page_config(page_title="Cal In, Cal Out", layout="centered")

# Custom CSS for the specific "Card" look and colors
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0B101B;
    }

    /* Header Styling */
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #808495;
        margin-bottom: 30px;
    }

    /* Metric Styling */
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
    }

    /* Goal Status Box */
    .goal-box {
        background-color: rgba(46, 204, 113, 0.1);
        border: 1px solid #2ECC71;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: #2ECC71;
        font-weight: bold;
        margin: 20px 0px;
    }

    /* Section Headers */
    .section-header {
        border-left: 4px solid #4A90E2;
        padding-left: 10px;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'food_log' not in st.session_state:
    st.session_state.food_log = []
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []
if 'goal' not in st.session_state:
    st.session_state.goal = 2000

# Presets from your screenshots
FOOD_PRESETS = {
    "Apple (medium)": 95,
    "Banana": 105,
    "Chicken Breast (100g)": 165,
    "White Rice (1 cup)": 200,
    "Pasta (1 cup)": 220,
    "Egg (large)": 72
}

ACTIVITY_PRESETS = {
    "Walking (30 min, moderate)": 150,
    "Running (30 min)": 300,
    "Swimming (30 min)": 250,
    "Yoga (60 min)": 120
}

# --- HEADER ---
st.markdown('<p class="main-title">🔥 Cal In, Cal Out</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Calorie Intake & Activity Tracker</p>', unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["Today", "History", "Goal"])

with tab1:
    # Date display
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"<p style='text-align: center; color: #808495;'>{current_date}</p>", unsafe_allow_html=True)

    # Logic Calculations
    total_eaten = sum(item['cals'] for item in st.session_state.food_log)
    total_burned = sum(item['cals'] for item in st.session_state.activity_log)
    net_kcal = total_eaten - total_burned
    remaining = st.session_state.goal - net_kcal

    # Metrics Row
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("🍽️ Eaten", f"{total_eaten} kcal")
    m_col2.metric("🏃 Burned", f"{total_burned} kcal")
    m_col3.metric("⚖️ Net", f"{net_kcal} kcal")

    st.caption(f"{remaining} kcal remaining of {st.session_state.goal} kcal goal")

    # Status Box
    status_text = "under goal" if net_kcal <= st.session_state.goal else "over goal"
    st.markdown(f'<div class="goal-box">✅ {abs(remaining)} kcal {status_text}</div>', unsafe_allow_html=True)

    st.divider()

    # LOG FOOD SECTION
    st.markdown('<div class="section-header">🍎 Log Food</div>', unsafe_allow_html=True)
    with st.container(border=True):
        selected_food = st.selectbox("Select food", options=list(FOOD_PRESETS.keys()))

        f_col1, f_col2 = st.columns([2, 1])
        food_name = f_col1.text_input("Food name", value=selected_food)
        food_cals = f_col2.number_input("Calories (kcal)", value=FOOD_PRESETS[selected_food], step=1)

        if st.button("➕ Add Food", type="primary", use_container_width=True):
            st.session_state.food_log.append({"name": food_name, "cals": food_cals})
            st.rerun()

    # LOG ACTIVITY SECTION
    st.markdown('<div class="section-header">🏃 Log Activity</div>', unsafe_allow_html=True)
    with st.container(border=True):
        selected_act = st.selectbox("Select activity", options=list(ACTIVITY_PRESETS.keys()))

        a_col1, a_col2 = st.columns([2, 1])
        act_name = a_col1.text_input("Activity name", value=selected_act)
        act_cals = a_col2.number_input("Calories burned", value=ACTIVITY_PRESETS[selected_act], step=1)

        if st.button("➕ Add Activity", use_container_width=True):
            st.session_state.activity_log.append({"name": act_name, "cals": act_cals})
            st.rerun()

    # Simple Daily List (To show it's working)
    if not st.session_state.food_log and not st.session_state.activity_log:
        st.markdown("<p style='text-align: center; color: gray;'>No logs yet today.</p>", unsafe_allow_html=True)

with tab2:
    st.subheader("Daily History")
    if st.session_state.food_log:
        st.write("**Food Logged:**")
        for item in st.session_state.food_log:
            st.text(f"- {item['name']}: {item['cals']} kcal")

    if st.session_state.activity_log:
        st.write("**Activity Logged:**")
        for item in st.session_state.activity_log:
            st.text(f"- {item['name']}: {item['cals']} kcal")

with tab3:
    st.subheader("Settings")
    new_goal = st.number_input("Adjust Daily Calorie Goal", value=st.session_state.goal, step=50)
    if st.button("Update Goal"):
        st.session_state.goal = new_goal
        st.success("Goal updated!")