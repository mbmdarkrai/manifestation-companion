import streamlit as st
import streamlit as st
import random  # ← ADD THIS

st.set_page_config(layout="wide")

st.title("✨ Manifestation Companion")

st.sidebar.info("🤖 **Demo Mode** - Enter goal → get coaching!")
st.sidebar.markdown("[Get Claude API](https://console.anthropic.com) for full AI")

tab1, tab2 = st.tabs(["🎯 Intention", "📊 Progress"])

with tab1:
    goal = st.text_input("**Your goal:**", key="goal")
    if st.button("✨ Get Coaching", type="primary") and goal:
        insights = [
            f"**Visualize '{goal}' daily!** Feel it real now. Universe aligns perfectly.",
            f"**'{goal}' is yours!** Speak it, feel it, receive it.",
            f"**Perfect script:** 'I am so grateful for my {goal.lower()}. It feels AMAZING!'"
        ]
        st.balloons()
        st.markdown("### 🎁 **Your Coach:**")
        st.markdown(random.choice(insights))


st.title("✨ Manifestation Companion")
st.markdown("**AI Law of Attraction Coach**")

# Lines 8-16 (around here ↓)
api_key = st.sidebar.text_input("🔑 Anthropic API Key", type="password")

client = None
if api_key and api_key.strip():           # ← Line 12
    try:                                 # ← Line 13
        client = anthropic.Anthropic(api_key=api_key)  # Line 14
        st.sidebar.success("✅ AI Ready!")              # Line 15  
    except:                              # Line 16
        st.sidebar.info("⚠️ Demo mode active")  # ← CHANGE THIS LINE


tab1, tab2 = st.tabs(["🎯 Intention", "📊 Progress"])

with tab1:
    goal = st.text_input("**Goal:**", key="goal")
    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("✨ Get AI Coach", type="primary") and goal:
            if client:
                msg = client.messages.create(model="claude-3-5-sonnet-20240620", max_tokens=300, 
                    messages=[{"role": "user", "content": f"Law of Attraction coaching: {goal}"}])
                st.markdown("### 🎁 **AI Coach:**")
                st.markdown(msg.content[0].text)
            else:
                st.balloons()
                st.success(f"**Feel '{goal}' NOW!** Universe delivers. 💫")
    with col2:
        st.info("Demo OK!")

with tab2:
    st.info("Daily tracking → soon!")

st.markdown("*Claude AI + Streamlit*")

