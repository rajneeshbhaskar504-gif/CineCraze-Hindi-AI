import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Script Generator", page_icon="🎬", layout="wide")

# --- INITIALIZATION ---
if "script" not in st.session_state:
    st.session_state.script = None

st.title("🎬 CineCraze Hindi AI")

# --- GEMINI CONFIG (FIXED) ---
# Yahan secret name wahi rakhein jo aapne Streamlit Cloud Secrets mein dala hai
try:
    # Aapne screenshot mein dekha hoga, key 'GEMINI_API_KEY' hi honi chahiye
    api_key = st.secrets.get("GEMINI_API_KEY") 
    if not api_key:
        st.error("❌ Secrets mein GEMINI_API_KEY nahi mili.")
        st.stop()
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"❌ Gemini Config Error: {e}")
    st.stop()

# --- INPUT FIELDS ---
movie_name = st.text_input("🎥 Movie Name")
language = st.selectbox("Language", ["Hindi", "English"])
style = st.selectbox("Script Style", ["Movie Explained", "Emotional", "Funny", "Suspense"])
duration = st.slider("Video Length (Minutes)", 5, 20, 10)

# --- GENERATE SCRIPT ---
if st.button("🚀 Generate Script"):
    if not movie_name:
        st.warning("Movie Name लिखें")
    else:
        prompt = f"Write an ORIGINAL YouTube movie explanation script. Movie: {movie_name}, Language: {language}, Style: {style}, Duration: {duration} minutes."
        with st.spinner("🤖 AI Script बना रहा है..."):
            try:
                response = model.generate_content(prompt)
                st.session_state.script = response.text
                st.success("✅ Script Ready")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# --- SCRIPT ACTIONS ---
if st.session_state.script:
    st.subheader("📜 Generated Script")
    st.text_area("Script", value=st.session_state.script, height=300)
    
    # Import yahan rakhein taaki error na aaye agar utils missing ho
    from utils.image_prompt import generate_scene_prompts
    from utils.voice import generate_voice
    from utils.video import create_video
    from utils.image_generator import generate_image

    if st.button("🎤 Generate Voice"):
        audio_file = generate_voice(st.session_state.script)
        st.audio(audio_file)

    if st.button("🎬 Create Final Video"):
        # HF_TOKEN check
        hf_token = st.secrets.get("HF_API_TOKEN")
        if not hf_token:
            st.error("❌ HF_API_TOKEN missing in secrets!")
            st.stop()

        # [BAAKI KA LOGIC WAHI RAKHEIN JO AAPKA THA]
        # Bas dhyan rakhein ki images folder ka access sahi ho

