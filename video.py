from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

def create_video(images, audio_file, output="final_video.mp4"):
    audio = AudioFileClip(audio_file)

    duration = audio.duration / len(images)

    clips = []
    for img in images:
        clip = ImageClip(img).with_duration(duration)
        clips.append(clip)

    video = concatenate_videoclips(clips)
    video = video.with_audio(audio)

    video.write_videofile(output, fps=24)

    return output
