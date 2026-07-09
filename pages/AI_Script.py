import streamlit as st
import google.generativeai as genai
from utils.image_prompt import generate_scene_prompts
st.set_page_config(
    page_title="AI Script Generator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CineCraze Hindi AI")

# API Key
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    st.error("❌ Gemini API Key नहीं मिली। Settings → Secrets में GEMINI_API_KEY जोड़ें।")
    st.stop()

movie_name = st.text_input("🎥 Movie Name")

language = st.selectbox(
    "Language",
    ["Hindi", "English"]
)

style = st.selectbox(
    "Script Style",
    [
        "Movie Explained",
        "Emotional",
        "Funny",
        "Suspense"
    ]
)

duration = st.slider(
    "Video Length (Minutes)",
    5,
    20,
    10
)

if st.button("🚀 Generate Script"):

    if movie_name == "":
        st.warning("Movie Name लिखें")
        st.stop()

    prompt = f"""
Write an ORIGINAL YouTube movie explanation script.

Movie: {movie_name}
Language: {language}
Style: {style}
Duration: {duration} minutes

Requirements:
- Write an original script in your own words.
- Do not copy dialogue from the movie.
- Make it engaging for YouTube.
- Add a strong intro and ending.
"""
    with st.spinner("🤖 AI Script बना रहा है..."):

        try:
            response = model.generate_content(prompt)

            script = response.text

            st.success("✅ Script Ready")

            st.subheader("📜 Generated Script")
            st.write(script)

            st.download_button(
                label="📥 Download Script",
                data=script,
                file_name=f"{movie_name}_script.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
            
if st.button("🎬 Generate Animation Scenes"):
    with st.spinner("Animation Scenes बना रहे हैं..."):
        scenes = generate_scene_prompts(movie_name, script)

        st.subheader("🎨 Animation Scene Prompts")
        st.write(scenes)

        st.download_button(
            "📥 Download Scene Prompts",
            scenes,
            file_name="scene_prompts.txt"
        )
