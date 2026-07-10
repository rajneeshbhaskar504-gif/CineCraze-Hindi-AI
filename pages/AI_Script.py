import streamlit as st
import google.generativeai as genai
from utils.image_prompt import generate_scene_prompts
from utils.voice import generate_voice
# create_video को बाद में जोड़ेंगे

st.set_page_config(page_title="AI Script Generator", page_icon="🎬", layout="wide")

if "script" not in st.session_state:
    st.session_state.script = None

st.title("🎬 CineCraze Hindi AI")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    st.error("❌ Gemini API Key सेट नहीं है।")
    st.stop()

movie_name = st.text_input("🎥 Movie Name")
language = st.selectbox("Language", ["Hindi", "English"])
style = st.selectbox("Script Style", ["Movie Explained", "Emotional", "Funny", "Suspense"])
duration = st.slider("Video Length (Minutes)", 5, 20, 10)

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

if st.session_state.script:
    # 10/10 सुधार: st.write की जगह st.text_area
    st.subheader("📜 Generated Script")
    st.text_area("Script", value=st.session_state.script, height=300)
    st.download_button("📥 Download Script", st.session_state.script, file_name=f"{movie_name}_script.txt")

    if st.button("🎬 Generate Animation Scenes"):
        with st.spinner("Animation Scenes बना रहे हैं..."):
            scenes = generate_scene_prompts(movie_name, st.session_state.script)
            st.write(scenes)
            st.download_button("📥 Download Scene Prompts", scenes, file_name="scene_prompts.txt")

    if st.button("🎤 Generate Voice"):
        with st.spinner("🎤 Voice Generate हो रही है..."):
            audio_file = generate_voice(st.session_state.script)
        st.audio(audio_file)
        with open(audio_file, "rb") as f:
            st.download_button("⬇️ Download Voice", f, file_name="voice.mp3")

    st.divider()
    if st.button("🎬 Create Final Video"):
        st.info("🚧 Final Video Generator अगले स्टेप में जोड़ा जाएगा।")

