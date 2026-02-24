import streamlit as st
import anthropic

st.set_page_config(layout="wide")

st.title("✨ Manifestation Companion")
st.markdown("**AI Law of Attraction Coach**")

api_key = st.sidebar.text_input("🔑 Anthropic API (optional)", type="password")
client = None
if api_key:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        st.sidebar.success("✅ AI ON")
    except:
        st.sidebar.error("Key issue")

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
