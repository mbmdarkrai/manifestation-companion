
# =====================================================
# Manifestation Companion — AI Law of Attraction Coach
# =====================================================
# Works free with template-based responses. If ANTHROPIC_API_KEY
# is set (env var or entered in the sidebar), responses are
# personalized live via the Claude API.

import json
import os
import random
from datetime import date, datetime, timedelta

import streamlit as st

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC_LIB = True
except ImportError:
    HAS_ANTHROPIC_LIB = False

st.set_page_config(page_title="Manifestation Companion", page_icon="✨", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }
    .stButton > button:hover {
        filter: brightness(1.05);
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > textarea {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_FILE = "manifestation_log.json"

if "outputs" not in st.session_state:
    st.session_state.outputs = {}

if "copied" not in st.session_state:
    st.session_state.copied = ""


def copy_to_clipboard(text):
    if not text:
        return
    try:
        st.session_state.copied = text
        st.code(text[:80] + ("..." if len(text) > 80 else ""))
        st.toast("Copied to clipboard")
    except Exception:
        st.toast("Copy action is unavailable in this environment")


def render_result_box(key, title, placeholder):
    result = st.session_state.outputs.get(key, "")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_area(title, value=result or placeholder, height=220, key=f"{key}_output")
    with col2:
        if st.button("Copy", key=f"copy_{key}"):
            copy_to_clipboard(result)
        if result and st.session_state.copied == result:
            st.caption("Copied")

# =====================================================
# SIDEBAR — optional API key
# =====================================================
st.sidebar.markdown("### ✨ Manifestation Companion")
st.sidebar.caption("Free templates work out of the box. Add a Claude API key for personalized coaching.")

env_key = os.getenv("ANTHROPIC_API_KEY", "")
api_key = st.sidebar.text_input("Claude API key (optional)", value=env_key, type="password")

client = None
if api_key and HAS_ANTHROPIC_LIB:
    try:
        client = Anthropic(api_key=api_key)
    except Exception:
        client = None

if client:
    st.sidebar.success("Personalized AI coaching enabled.")
elif api_key and not HAS_ANTHROPIC_LIB:
    st.sidebar.warning("Install the `anthropic` package to enable live coaching.")
else:
    st.sidebar.caption("Using free simulated responses.")

# =====================================================
# STORAGE
# =====================================================
def load_log():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_log(log):
    with open(DATA_FILE, "w") as f:
        json.dump(log, f, indent=2)

def add_log_entry(tool_name):
    log = load_log()
    log.append({"date": str(date.today()), "tool": tool_name, "ts": datetime.now().isoformat()})
    save_log(log)

def compute_streak(log):
    dates = sorted({e["date"] for e in log}, reverse=True)
    if not dates:
        return 0
    streak = 0
    cursor = date.today()
    for i, d in enumerate(dates):
        cursor_str = str(cursor)
        if d == cursor_str:
            streak += 1
            cursor -= timedelta(days=1)
        elif i == 0:
            break
        else:
            break
    return streak

# =====================================================
# CLAUDE CALL
# =====================================================
def ask_claude(prompt):
    if not client:
        return None
    try:
        with st.spinner("Generating a thoughtful response..."):
            msg = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=700,
                messages=[{"role": "user", "content": prompt}],
            )
        return msg.content[0].text
    except Exception as e:
        st.warning(f"Live API call failed, showing free template instead: {e}")
        return None

# =====================================================
# TEMPLATE GENERATORS
# =====================================================
def intention_template(goal):
    beliefs = [
        "that you're not ready yet",
        "that people like you don't get this",
        "that it's selfish to want more",
        "that you'll have to sacrifice everything else to get it",
        "that timing is never right",
    ]
    return f"""INTENTION CLARITY

Your stated goal: "{goal}"

Deeper why: you're not just after the outcome — you're after how it will make you feel: capable, secure, proud, free. Naming that feeling is often more motivating than the goal itself.

Likely limiting belief in the way: the quiet story {random.choice(beliefs)}. Notice if that thought shows up when you think about this goal — it's worth questioning, not obeying.

Reframed intention: "I am worthy of {goal.lower()}, and I'm taking steps toward it starting today."

Try this: write your intention in one sentence, present tense, as if it's already unfolding — then read it aloud each morning this week."""

def affirm_template(goal, style):
    starters = {
        "present": [f"I am {goal.lower()}.", f"I attract everything I need to {goal.lower()}.", f"I move through today fully capable of {goal.lower()}."],
        "grateful": [f"I'm grateful that {goal.lower()} is unfolding for me.", "Thank you for the people and opportunities helping me get there.", "I'm grateful for every small sign that I'm on the right path."],
        "becoming": [f"I am becoming the person who {goal.lower()}.", f"Every day I am becoming more aligned with {goal.lower()}.", "I am becoming someone who takes consistent action toward this."],
        "belief": [f"I believe I am capable of {goal.lower()}.", "I believe the right opportunities are already on their way.", "I believe consistent effort compounds into real change."],
    }
    lines = "\n".join(f"{i+1}. {s}" for i, s in enumerate(starters[style]))
    return f"AFFIRMATIONS ({style} style)\n\n{lines}\n\nUse these: pick one, repeat it slowly for 60 seconds each morning, and notice any resistance that comes up — that resistance is exactly what you're working through."

def visual_template(goal, length):
    beats = {
        "3": ["Settle in, breathe, picture the moment your goal becomes real.", "Notice the sounds, colors, and feelings around you.", "Let yourself smile — this is already yours."],
        "5": ["Settle into a comfortable position and take three slow breaths.", "Picture the exact moment you realize your goal has happened — where are you, who's there.", "Zoom in on the details: what you're wearing, what you can hear, the temperature of the air.", "Feel the emotion fully — pride, relief, joy — let it fill your chest.", "Open your eyes and carry that feeling with you into the rest of your day."],
        "10": ["Settle in, close your eyes, and take five slow breaths to arrive fully in the present.", "Picture the day your goal is realized — start with the moment you wake up.", "Walk through the day in detail: the people around you, the environment, your own posture and confidence.", "Notice a specific conversation where someone acknowledges your success.", "Feel the full emotional payoff — let it move through your whole body.", "Ask your future self one question about how they got here, and listen for the answer.", "Thank yourself for doing the work, then gently open your eyes."],
    }
    lines = "\n".join(f"{i+1}. {b}" for i, b in enumerate(beats[length]))
    return f"VISUALIZATION SCRIPT — {length} minutes\nGoal: {goal}\n\n{lines}"

def letter_template(goal, time_ahead):
    return f"""A LETTER FROM YOUR FUTURE SELF, {time_ahead.upper()} FROM NOW

Dear present-day me,

I'm writing from {time_ahead} ahead, and I want you to know: {goal} happened. Not all at once, and not without doubt along the way — but it happened because you kept showing up on the ordinary days, not just the inspired ones.

The turning point wasn't a single big moment. It was the accumulation of small, unglamorous choices you made even when you weren't sure they were working. Trust that process more than you currently do.

One thing I wish you knew sooner: the version of you asking "am I ready" was already ready. Readiness was never the blocker — starting was.

Keep going. I'm proof it's worth it.

With love,
Your future self"""

def actions_template(goal):
    actions = [
        f'Write down exactly what "{goal}" looks like when achieved — specific and measurable.',
        "Identify one person who has done something similar and send them a message this week.",
        "Block 25 minutes tomorrow morning for focused work on this, before checking your phone.",
        "Remove one small obstacle in your environment that's been quietly slowing you down.",
        "Say your intention out loud to one person you trust — accountability compounds momentum.",
        "Do the smallest possible version of the next step today, even imperfectly.",
        "End today by writing one sentence about progress made, however small.",
    ]
    lines = "\n".join(f"{i+1}. {a}" for i, a in enumerate(actions))
    return f"7 ALIGNED ACTIONS\nGoal: {goal}\n\n{lines}\n\nPick one to do today. Small, consistent action is what turns intention into reality."

# =====================================================
# PROMPT BUILDERS (for live API mode)
# =====================================================
def intention_prompt(goal):
    return f'Act as a warm, grounded manifestation/law-of-attraction coach. The user\'s goal is: "{goal}". Help them clarify their true intention: identify the underlying emotional "why", name a likely limiting belief that could be blocking them, and offer one reframed, present-tense intention statement. Keep it under 200 words, encouraging and specific, no generic filler.'

def affirm_prompt(goal, style):
    return f'Write 3 personalized manifestation affirmations in the "{style}" style for someone whose goal is: "{goal}". Make them specific to the goal, not generic. Return them as a numbered list, then one short line of practice guidance.'

def visual_prompt(goal, length):
    return f'Write a {length}-minute guided visualization script (as numbered steps, sensory and specific) for someone manifesting: "{goal}". Keep it grounded and vivid, not cheesy.'

def letter_prompt(goal, time_ahead):
    return f'Write a warm, specific letter from the user\'s future self, {time_ahead} ahead, to their present self. Their goal is: "{goal}". The letter should describe the goal as achieved, reflect on what made the difference, and end with encouragement. Keep it under 220 words, emotionally resonant, not generic.'

def actions_prompt(goal):
    return f'Give 7 specific, doable, non-generic actions someone can take this week to move toward this goal: "{goal}". Number them 1-7, each one sentence, concrete and immediately actionable — not vague advice.'

def run_tool(goal, template_fn, prompt_fn, *args):
    live = ask_claude(prompt_fn(goal, *args)) if client else None
    return live if live else template_fn(goal, *args)

# =====================================================
# MAIN APP
# =====================================================
st.markdown(
    """
    <div style="background: linear-gradient(135deg, rgba(56,189,248,0.18), rgba(2,132,199,0.14));
    border: 1px solid rgba(56,189,248,0.28); border-radius: 18px; padding: 24px 24px 20px; margin-bottom: 18px;">
        <h1 style="margin:0 0 8px; color:#38bdf8;">✨ Manifestation Companion</h1>
        <p style="margin:0 0 14px; color:#e2e8f0; font-size: 1.02rem;">A grounded, practical toolkit for intention, affirmations, visualization, and aligned action.</p>
        <div style="display:flex; flex-wrap:wrap; gap:10px;">
            <span style="background: rgba(15,23,42,0.7); border: 1px solid rgba(56,189,248,0.28); border-radius: 999px; padding: 6px 12px; color:#cbd5e1; font-size: 0.92rem;">🧭 Clear your intention</span>
            <span style="background: rgba(15,23,42,0.7); border: 1px solid rgba(56,189,248,0.28); border-radius: 999px; padding: 6px 12px; color:#cbd5e1; font-size: 0.92rem;">💬 Shape your affirmations</span>
            <span style="background: rgba(15,23,42,0.7); border: 1px solid rgba(56,189,248,0.28); border-radius: 999px; padding: 6px 12px; color:#cbd5e1; font-size: 0.92rem;">✅ Turn reflection into action</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("Start with a clear goal, then move through the tools below to reflect, reframe, and take grounded action.")

with st.expander("Quick start", expanded=False):
    st.markdown(
        "1. Write one clear goal.\n"
        "2. Pick a tool that matches your current need.\n"
        "3. Use the result as a reflection prompt, then take one small action."
    )

goal = st.text_input("Your goal", placeholder="e.g. Land a leadership role I love, doubling my income within a year")
goal = goal.strip() or "living a life fully aligned with what I want"

tabs = st.tabs([
    "🎯 Intention", "💬 Affirmations", "🎨 Visualization",
    "📝 Future Self Letter", "✅ Aligned Actions", "🔄 Complete Session", "📊 Progress"
])

with tabs[0]:
    st.subheader("Intention Setting")
    if st.button("Clarify my intention"):
        result = ask_claude(intention_prompt(goal)) or intention_template(goal)
        st.session_state.outputs["intention"] = result
        add_log_entry("Intention Setting")
    render_result_box("intention", "Your reflection", "Your reflection will appear here.")

with tabs[1]:
    st.subheader("Personalized Affirmations")
    style = st.selectbox("Style", ["present", "grateful", "becoming", "belief"], format_func=lambda s: s.title())
    if st.button("Generate affirmations"):
        result = ask_claude(affirm_prompt(goal, style)) or affirm_template(goal, style)
        st.session_state.outputs["affirmations"] = result
        add_log_entry("Affirmations")
    render_result_box("affirmations", "Your affirmations", "Your affirmations will appear here.")

with tabs[2]:
    st.subheader("Guided Visualization")
    length = st.selectbox("Length", ["3", "5", "10"], index=1, format_func=lambda x: f"{x} minutes")
    if st.button("Generate visualization script"):
        result = ask_claude(visual_prompt(goal, length)) or visual_template(goal, length)
        st.session_state.outputs["visualization"] = result
        add_log_entry("Visualization")
    render_result_box("visualization", "Your visualization", "Your visualization script will appear here.")

with tabs[3]:
    st.subheader("Future Self Letter")
    time_ahead = st.selectbox("Time ahead", ["3 months", "6 months", "1 year", "5 years"], index=2)
    if st.button("Write my letter"):
        result = ask_claude(letter_prompt(goal, time_ahead)) or letter_template(goal, time_ahead)
        st.session_state.outputs["letter"] = result
        add_log_entry("Future Self Letter")
    render_result_box("letter", "Your letter", "Your future self letter will appear here.")

with tabs[4]:
    st.subheader("Aligned Actions")
    if st.button("Get my 7 actions"):
        result = ask_claude(actions_prompt(goal)) or actions_template(goal)
        st.session_state.outputs["actions"] = result
        add_log_entry("Aligned Actions")
    render_result_box("actions", "Your actions", "Your aligned actions will appear here.")

with tabs[5]:
    st.subheader("Complete Session")
    session_len = st.radio("Session length", ["Quick (5 min)", "Full (20 min)"], index=1)
    if st.button("Run session"):
        parts = [intention_template(goal), affirm_template(goal, "present")]
        if session_len.startswith("Full"):
            parts += [visual_template(goal, "5"), letter_template(goal, "1 year"), actions_template(goal)]
        result = ("\n\n" + "—" * 30 + "\n\n").join(parts)
        st.session_state.outputs["session"] = result
        add_log_entry("Quick session" if session_len.startswith("Quick") else "Full session")
    render_result_box("session", "Your session", "Your full session will appear here.")

with tabs[6]:
    st.subheader("Progress Tracking")
    log = load_log()
    streak = compute_streak(log)
    c1, c2, c3 = st.columns(3)
    c1.metric("Day streak", streak)
    c2.metric("Total sessions", len(log))
    c3.metric("Tools used", len({e["tool"] for e in log}))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log today's practice"):
            add_log_entry("Manual log entry")
            st.rerun()
    with col2:
        if st.button("Clear log"):
            save_log([])
            st.rerun()

    if log:
        st.markdown("**Recent activity**")
        for entry in reversed(log[-30:]):
            st.caption(f"{entry['date']} — {entry['tool']}")
    else:
        st.info("No practice logged yet.")

if st.button("Clear generated text", use_container_width=True):
    st.session_state.outputs = {}
    st.rerun()

st.markdown("---")
st.caption("Free to use • Optional API integration • No ads • Manifestation results vary by individual — this is a reflection and motivation tool, not a guarantee.")
