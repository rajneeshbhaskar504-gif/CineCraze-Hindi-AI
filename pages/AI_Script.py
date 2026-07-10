import streamlit as st
import google.generativeai as genai
import os
from utils.image_prompt import generate_scene_prompts
from utils.image_generator import generate_image
from utils.voice import generate_voice
from utils.video import create_video

# Page Configuration
st.set_page_config(page_title="AI Script Generator", page_icon="🎬", layout="wide")

if "script" not in st.session_state:
    st.session_state.script = None

st.title("🎬 CineCraze Hindi AI")

# Gemini API Configuration
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    st.error("❌ Gemini API Key सेट नहीं है।")
    st.stop()

# Input Fields
movie_name = st.text_input("🎥 Movie Name")
language = st.selectbox("Language", ["Hindi", "English"])
style = st.selectbox("Script Style", ["Movie Explained", "Emotional", "Funny", "Suspense"])
duration = st.slider("Video Length (Minutes)", 5, 20, 10)

# Generate Script Button
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

# If Script exists, show other options
if st.session_state.script:
    st.subheader("📜 Generated Script")
    st.text_area("Script", value=st.session_state.script, height=300)
    st.download_button("📥 Download Script", st.session_state.script, file_name=f"{movie_name}_script.txt")

    # Generate Scenes
    if st.button("🎬 Generate Animation Scenes"):
        with st.spinner("Animation Scenes बना रहे हैं..."):
            scenes = generate_scene_prompts(movie_name, st.session_state.script)
            st.write(scenes)
            st.download_button(
                "📥 Download Scene Prompts",
                "\n\n".join(scenes),
                file_name="scene_prompts.txt"
            )

    # Generate Voice
    if st.button("🎤 Generate Voice"):
        with st.spinner("🎤 Voice Generate हो रही है..."):
            audio_file = generate_voice(st.session_state.script)
            st.audio(audio_file)
            with open(audio_file, "rb") as f:
                st.download_button("⬇️ Download Voice", f, file_name="voice.mp3")

    st.divider()

    # Final Video Creation
    if st.button("🎬 Create Final Video"):
        with st.spinner("🎬 Final Video बना रहे हैं..."):
            hf_token = st.secrets["HF_API_TOKEN"]

            # Voice Generate
            audio_file = generate_voice(st.session_state.script)

            # Scene List
            scenes = generate_scene_prompts(movie_name, st.session_state.script)
            
            # Check for Empty scenes
            if len(scenes) == 0:
                st.error("❌ कोई Scene Generate नहीं हुआ।")
                st.stop()

            # Images Generate
            images = []
            progress = st.progress(0)
            
            if not os.path.exists("images"):
                os.makedirs("images")

            for i, scene in enumerate(scenes):
                temp_output = f"images/scene_{i}.png"
                
                # Image generation with Return Path Handling
                try:
                    returned_path = generate_image(
                        prompt=scene, 
                        output_file=temp_output, 
                        hf_token=hf_token
                    )
                    images.append(returned_path)
                except Exception as e:
                    st.error(f"❌ Image {i+1} Error: {e}")
                    st.stop()
                
                progress.progress((i + 1) / len(scenes))

            if not images:
                st.error("❌ कोई Image Generate नहीं हुई।")
                st.stop()

            st.success("✅ सभी Images तैयार")

            # Check all images exist (Aapka latest sudhaar)
            for img in images:
                if not os.path.exists(img):
                    st.error(f"❌ Image नहीं मिली: {img}")
                    st.stop()

            # Final Video Assemble with Error Handling
            try:
                video = create_video(images, audio_file, "final_video.mp4")
                st.video(video)

                with open(video, "rb") as f:
                    st.download_button(
                        "⬇️ Download Final Video",
                        f,
                        file_name="final_video.mp4"
                    )
            except Exception as e:
                st.error(f"❌ Video Creation Error: {e}")

