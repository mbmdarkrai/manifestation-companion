import streamlit as st
import os
from anthropic import Anthropic

st.set_page_config(page_title="Manifestation Companion", layout="wide", initial_sidebar_state="expanded")

api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
client = Anthropic(api_key=api_key) if api_key else None

if "messages" not in st.session_state:
    st.session_state.messages = []
if "goal" not in st.session_state:
    st.session_state.goal = ""
if "tracking" not in st.session_state:
    st.session_state.tracking = []

st.markdown("""
<h1 style='text-align: center; color: #38bdf8;'>âœ¨ Manifestation Companion âœ¨</h1>
<p style='text-align: center; color: #cbd5e1;'>AI-Powered Law of Attraction Coaching</p>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ðŸ”‘ API Configuration")
    api_input = st.text_input("Anthropic API Key (optional)", type="password", value=api_key)
    if api_input:
        st.session_state.api_key = api_input
        client = Anthropic(api_key=api_input)
    st.markdown("---")
    st.info("7 tools for daily manifestation. Use with Claude AI or free simulated responses.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "ðŸŽ¯ Intention", 
    "ðŸ’¬ Affirmations", 
    "ðŸŽ¨ Visualization",
    "ðŸ“ Scripting",
    "âœ… Actions",
    "ðŸ”„ Sessions",
    "ðŸ“Š Tracking"
])

with tab1:
    st.markdown("## Clarify Your Intention")
    goal = st.text_area("What do you want to manifest?", placeholder="Be specific...", height=100)
    if st.button("Get Coaching Insight", key="intention_btn"):
        if goal:
            st.session_state.goal = goal
            if client and api_key:
                try:
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=500,
                        messages=[{"role": "user", "content": f"Help me clarify this manifestation goal: {goal}. Give me a powerful reframe and identify limiting beliefs."}]
                    )
                    st.success(response.content[0].text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.info("ðŸŽ¯ Your goal is powerful. Believe it's already yours.")

with tab2:
    st.markdown("## Personalized Affirmations")
    goal_affirmations = st.text_input("Your manifestation goal:", value=st.session_state.goal)
    style = st.radio("Choose affirmation style:", ["Present Tense", "Grateful", "Becoming", "Belief"])
    if st.button("Generate Affirmations", key="aff_btn"):
        if goal_affirmations:
            if client and api_key:
                try:
                    prompt = f"Create 5 powerful affirmations in {style} style for: {goal_affirmations}"
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success(response.content[0].text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.success(f"âœ¨ I am now experiencing {goal_affirmations}\nâœ¨ I deserve {goal_affirmations}")

with tab3:
    st.markdown("## Guided Visualization Script")
    duration = st.radio("Choose duration:", ["3 minutes", "5 minutes", "10 minutes"])
    goal_viz = st.text_input("Visualize achieving:", value=st.session_state.goal)
    if st.button("Create Visualization Script", key="viz_btn"):
        if goal_viz:
            if client and api_key:
                try:
                    prompt = f"Create a {duration} sensory-rich visualization script for achieving: {goal_viz}"
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=800,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.info(response.content[0].text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.info(f"Imagine {goal_viz} is already real. Feel it with all your senses.")

with tab4:
    st.markdown("## Future Self Letter")
    timeframe = st.select_slider("From your future self:", ["3 months", "6 months", "1 year", "5 years"])
    goal_letter = st.text_input("What have you achieved?", value=st.session_state.goal)
    if st.button("Write Future Letter", key="script_btn"):
        if goal_letter:
            if client and api_key:
                try:
                    prompt = f"Write a letter from {timeframe} in the future who has achieved: {goal_letter}"
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=800,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.info(response.content[0].text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.info(f"Dear Me, I'm writing from {timeframe} about {goal_letter}. Keep believing.")

with tab5:
    st.markdown("## 7 Aligned Actions for Today")
    goal_actions = st.text_input("Your goal:", value=st.session_state.goal)
    if st.button("Generate Aligned Actions", key="actions_btn"):
        if goal_actions:
            if client and api_key:
                try:
                    prompt = f"Generate 7 small aligned daily actions for manifesting: {goal_actions}"
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=600,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.success(response.content[0].text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.success("âœ… Affirm your goal\nâœ… Visualize\nâœ… Take 1 action\nâœ… Journal\nâœ… Express gratitude")

with tab6:
    st.markdown("## Complete Manifestation Sessions")
    session_type = st.radio("Choose session:", ["Quick 5-min", "Full 20-min"])
    goal_session = st.text_input("Your manifestation goal:", 
                            value=st.session_state.get('goal', ''), 
                            key='goal_input')
    if st.button("Start Session", key="session_btn"):
        if goal_session:
            if client and api_key:
                try:
                    prompt = f"Create a {session_type} complete manifestation session for: {goal_session}"
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.info(response.content[0].text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.info("Session: Ground â†’ Intend â†’ Affirm â†’ Visualize â†’ Act â†’ Gratitude â†’ Done!")

with tab7:
    st.markdown("## Track Your Practice")
    practice_type = st.selectbox("What did you practice?", 
                                  ["Affirmations", "Visualization", "Full Session", "Journaling", "Other"])
    notes = st.text_area("Notes:", placeholder="How did it feel?")
    if st.button("Log Practice", key="track_btn"):
        entry = {"type": practice_type, "notes": notes}
        st.session_state.tracking.append(entry)
        st.success("âœ… Practice logged! Consistency builds momentum!")
        st.write(f"Total practices logged: {len(st.session_state.tracking)}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>âœ¨ Made with Claude AI â€¢ Your Manifestation Companion âœ¨</p>", unsafe_allow_html=True)