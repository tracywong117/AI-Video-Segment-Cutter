"""
Video Segment Cutter - A program to cut segments of a video based on specified keywords.

"""

import argparse
import whisper
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

# python counting-any-words-in-video.py -i OpenAI-testing-video.mp4 -t GPT
parser = argparse.ArgumentParser(
    description="Example script with command-line arguments"
)
parser.add_argument("--input", "-i", help="Path to the input file")
parser.add_argument("--keyword", "-t", help="Keyword to count")
args = parser.parse_args()

input_video_file = args.input
# input_video_file = "OpenAI-testing-video.mp4"
keyword = args.keyword
# keyword = "GPT-4"

# parameter
max_words_in_line_subtitle = 10
output_audio_file = f"audio_{input_video_file}.mp3"

# load model
model = whisper.load_model("base.en")


# convert video to mp3
def convert_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)


print("Converting video to mp3...")
convert_to_mp3(input_video_file, output_audio_file)
print("Done!")

# transcribe mp3 using whisper
print("Transcribing...")
transcribe_result = model.transcribe(
    audio=output_audio_file, word_timestamps=True, task="transcribe"
)
print("Done!")
# print(transcribe_result["text"])

# adjust number of words in each line of subtitle
subtitle_list = []

for subtitle in transcribe_result["segments"]:
    temp = []
    word_list = subtitle["text"].split()
    if len(word_list) > max_words_in_line_subtitle:
        for index, each_word in enumerate(word_list):
            if each_word.endswith(",") and (index != 0 or index < len(word_list)):
                temp.append(index)
    if temp == []:
        subtitle_list.append(
            [
                (
                    round(subtitle["words"][0]["start"], 2),
                    round(subtitle["words"][-1]["end"], 2),
                ),
                subtitle["text"],
            ]
        )
    else:
        current_index = 0
        for index in temp:
            subtitle_list.append(
                [
                    (
                        round(subtitle["words"][current_index]["start"], 2),
                        round(subtitle["words"][index]["end"], 2),
                    ),
                    " ".join(word_list[current_index : index + 1]).lstrip(),
                ]
            )
            current_index = index + 1
        if current_index >= len(word_list):
            continue
        subtitle_list.append(
            [
                (
                    round(subtitle["words"][current_index]["start"], 2),
                    round(subtitle["words"][-1]["end"], 2),
                ),
                " ".join(word_list[current_index:]).lstrip(),
            ]
        )

for sub in subtitle_list:
    sub[1] = sub[1].strip()

# print(subtitle_list)

# find segment with keyword
segment_with_keyword = []

for subtitle in transcribe_result["segments"]:
    for word in subtitle["words"]:
        if keyword.lower() in word["word"].lower():
            temp = {"start": word["start"], "end": word["end"], "text": word["word"]}
            segment_with_keyword.append(temp)

# print(segment_with_keyword)

# generate subtitle on the original video
generator = lambda txt: TextClip(txt, font="Arial", fontsize=32, color="white")

subtitles = SubtitlesClip(subtitle_list, generator)

video = VideoFileClip(input_video_file)

result_video = CompositeVideoClip(
    [video, subtitles.set_position(("center", video.size[1] - 100))]
)

# generate video with segment with keyword
clips = []

for counting, segment in enumerate(segment_with_keyword):
    start_time = segment["start"]
    end_time = segment["end"]

    # adjust start and end time to make sure each clip is not too short
    if end_time - start_time < 1:
        diff = 1 - (end_time - start_time)
        start_time -= diff / 2
        end_time += diff / 2

    clip = result_video.subclip(start_time, end_time)

    # add counter to the video (right top corner)
    txt_clip = TextClip(str(counting + 1), font="Arial", fontsize=32, color="white")
    txt_clip = txt_clip.set_position((video.size[0] - 100, 50)).set_duration(
        clip.duration
    )
    clip = CompositeVideoClip([clip, txt_clip])

    clips.append(clip)

final_video = concatenate_videoclips(clips)

final_video.write_videofile(
    f"{input_video_file}_segments.mp4",
    fps=result_video.fps,
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
    codec="libx264",
    audio_codec="aac",
)
