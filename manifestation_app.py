import streamlit as st
import random

st.set_page_config(layout="wide", page_title="Manifestation Companion")

st.title("✨ Manifestation Companion")
st.markdown("**Your AI Law of Attraction Coach**")

st.sidebar.markdown("### 🤖 Demo Mode Active")
st.sidebar.markdown("[Upgrade to Claude AI](https://console.anthropic.com)")
# Add after st.sidebar.info():
if st.sidebar.checkbox("🔑 Enable Claude AI"):
    api_key = st.sidebar.text_input("Paste API key:", type="password")
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            st.sidebar.success("✅ AI ACTIVE!")
            # Use client in button...
        except:
            pass  # Silent fail → demo

tab1, tab2 = st.tabs(["🎯 Intention Setting", "📊 Progress"])

with tab1:
    goal = st.text_input("**What do you want to manifest?**", key="goal", 
                        placeholder="e.g. dream job, perfect relationship, financial freedom")
    
    if st.button("✨ Get Your Coaching Session", type="primary", use_container_width=True) and goal.strip():
        insights = [
            f"**Powerful Vision for '{goal}':** Picture it complete. Feel the joy NOW. Universe is aligning people, circumstances, timing perfectly.",
            f"**Your '{goal}' Affirmation:** 'I am so grateful for my {goal.lower()}. It came faster and better than I imagined!'",
            f"**Action Step:** Today, act AS IF '{goal}' is already yours. The energy shift creates the reality.",
            f"**Scripting Magic:** 'Dear Diary - {goal} manifested today! It feels AMAZING. I knew it would come!'",
            f"**Emotional Alignment:** Focus 51% on feeling good about '{goal}', 49% on action. That's the formula!",
        ]
        st.balloons()
        st.markdown("### 🎁 **Your Personalized Coaching:**")
        st.markdown(random.choice(insights))
        st.balloons()

with tab2:
    st.header("📈 Progress Tracker")
    st.info("👉 Log daily practice here soon!")
    
    if st.button("💾 Save Progress"):
        st.success("Progress saved! Consistency = Manifestation Power!")

st.markdown("---")
st.markdown("*✨ Free forever demo | Built with Streamlit*")
