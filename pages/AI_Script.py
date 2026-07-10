import streamlit as st
import google.generativeai as genai
import os
from utils.image_prompt import generate_scene_prompts
from utils.image_generator import generate_image
from utils.voice import generate_voice
from utils.video import create_video

    if st.button("🎬 Create Final Video"):
        with st.spinner("🎬 Final Video बना रहे हैं..."):
            hf_token = st.secrets["HF_API_TOKEN"]

            # 1. Voice Generate
            audio_file = generate_voice(st.session_state.script)

            # 2. Scene List
            scenes = generate_scene_prompts(movie_name, st.session_state.script)
            
            # 1. Zero Division check (Sudhaar)
            if len(scenes) == 0:
                st.error("❌ कोई Scene Generate नहीं हुआ।")
                st.stop()

            # 3. Images Generate
            images = []
            progress = st.progress(0)
            
            if not os.path.exists("images"):
                os.makedirs("images")

            for i, scene in enumerate(scenes):
                image_path = f"images/scene_{i}.png"
                
                # 2. Image generation Error Handling
                try:
                    generate_image(prompt=scene, output_file=image_path, hf_token=hf_token)
                    images.append(image_path)
                except Exception as e:
                    st.error(f"❌ Image {i+1} Error: {e}")
                    st.stop()
                
                progress.progress((i + 1) / len(scenes))

            if not images:
                st.error("❌ कोई Image Generate नहीं हुई।")
                st.stop()

            st.success("✅ सभी Images तैयार")

            # 4. Final Video Assemble with Error Handling (Sudhaar)
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

