import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random

# -------------------- CONFIG --------------------

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(
    page_title="CrowdSense AI",
    page_icon="",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

.main-title {
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0;
}

.sub-title {
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.glass-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.metric-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 15px;
}

.stButton button {
    width: 100%;
    border-radius: 14px;
    border: none;
    background: linear-gradient(to right, #2563eb, #7c3aed);
    color: white;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
    transition: 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.02);
    opacity: 0.92;
}

.stTextArea textarea {
    background-color: #0f172a;
    color: white;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

.stTextInput input {
    background-color: #0f172a;
    color: white;
    border-radius: 12px;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------

if "fan_xp" not in st.session_state:
    st.session_state.fan_xp = 120

if "fan_comments" not in st.session_state:
    st.session_state.fan_comments = []

# -------------------- HEADER --------------------

st.markdown("""
<div class="main-title"> CrowdSense AI</div>
<div class="sub-title">
AI-powered emotional second-screen experience for live sports fans
</div>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------

st.sidebar.title("⚙️ Match Controls")

language = st.sidebar.selectbox(
    " Fan Language",
    ["English", "Hindi", "Kannada"]
)

mode = st.sidebar.selectbox(
    " Experience Mode",
    [
        "Neutral Broadcast",
        "Hyped Stadium",
        "Funny Twitter Mode",
        "Ultra Dramatic"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    " Tip: Use dramatic IPL moments for the best AI crowd reactions."
)

# -------------------- LAYOUT --------------------

left, right = st.columns([2,1])

# -------------------- LEFT PANEL --------------------

with left:

    st.markdown("##  Live Match Situation")

    commentary = st.text_area(
        "",
        height=240,
        value="""
RCB 198/4 in 19 overs.
Virat Kohli batting on 94 off 52 balls.
Dinesh Karthik smashing sixes.
Chinnaswamy crowd roaring loudly.
CSK bowlers under massive pressure.
"""
    )

    if st.button(" Generate Crowd Experience"):

        with st.spinner("Analyzing live crowd emotions with Gemini AI..."):

            prompt = f"""
            You are an AI sports atmosphere engine.

            Analyze this live cricket match situation:

            {commentary}

            Generate output in {language}.

            Experience mode:
            {mode}

            Generate:

            1.  Crowd Emotion Meter
            2.  Fan Chant
            3.  Stadium Pressure Analysis
            4.  Viral Social Reaction
            5.  Rivalry Intensity
            6.  Fan Challenge
            7.  Cinematic Commentary

            Keep output:
            - immersive
            - emotional
            - dramatic
            - concise
            """

            try:

                response = model.generate_content(prompt)

                st.markdown("""
                <div class="glass-card">
                """, unsafe_allow_html=True)

                st.markdown("## Live Crowd Intelligence")

                st.write(response.text)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:

                st.error(f"Gemini Error: {e}")

# -------------------- RIGHT PANEL --------------------

with right:

    st.markdown("## 🌡 Live Fan Energy")

    energy = random.randint(75, 99)

    st.markdown(f"""
    <div class="metric-card">
        <h2>{energy}%</h2>
        <p>Crowd Energy</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <h2> {st.session_state.fan_xp}</h2>
        <p>Fan XP</p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------- FAN ACTIONS --------------------

    st.markdown("## Fan Actions")

    if st.button(" Trigger Crowd Chant"):
        st.session_state.fan_xp += 15
        st.success("+15 XP")

    if st.button("Predict Stadium Explosion"):
        st.session_state.fan_xp += 10
        st.success("+10 XP")

    if st.button("⚔ Raise Rivalry Intensity"):
        st.session_state.fan_xp += 20
        st.success("+20 XP")

    # -------------------- LIVE COMMENTS --------------------

    st.markdown("##  Live Fan Reactions")

    user_comment = st.text_input(
        "",
        placeholder="Type your live crowd reaction..."
    )

    if st.button(" Post Reaction"):

        if user_comment.strip() != "":

            st.session_state.fan_comments.insert(
                0,
                f" {user_comment}"
            )

            st.session_state.fan_xp += 5

            st.success("Reaction added!")

    st.markdown("### Stadium Feed")

    if st.session_state.fan_comments:

        for comment in st.session_state.fan_comments[:5]:

            st.markdown(f"""
            <div class="glass-card">
            {comment}
            </div>
            """, unsafe_allow_html=True)

    else:

        st.info("No fan reactions yet.")

    # -------------------- DRAMA METER --------------------

    st.markdown("## Match Drama Meter")

    drama = random.randint(70, 100)

    st.progress(drama / 100)

    st.caption(f"Drama Level: {drama}%")

    # -------------------- FAN FEED --------------------

    st.markdown("## Viral Fan Feed")

    fan_feed = [
        "Twitter servers preparing for Kohli edits ",
        "RCB fans already calculating playoff scenarios ",
        "Commentators trying to stay calm challenge: impossible 🎙",
        "Chinnaswamy louder than Bangalore traffic tonight 🚦",
        "CSK bowlers updating LinkedIn profiles "
    ]

    st.info(random.choice(fan_feed))

# -------------------- FOOTER --------------------

st.markdown("---")
