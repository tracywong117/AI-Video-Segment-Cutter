# AI Video Segment Cutter
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]([https://colab.research.google.com/drive/1ICa2nh3mbflJCrJ4oKNUHWTZ9_vTJw8F?usp=sharing](https://colab.research.google.com/drive/18GD-tQ9hIRG6f_9hLGMqSjx8PNTXPmy3?usp=sharing))

Video Segment Cutter is a program that allows you to cut segments of a video based on specified keywords. With this tool, you can extract specific sections of a video that contain the desired keywords, making it easier to analyze or highlight relevant content.

In this project, we use the Whisper base model to quickly generate subtitles for videos and cut them based on specific words. OpenAI's Whisper model is a state-of-the-art model that can automatically turn speech into text with really high accuracy.

## How to run
1. Prepare the video
2. Install the dependencies
```plaintext
pip3 install -r requirements.txt
```
3. Run 
```plaintext
python3 ai-video-segment-cutter.py -i <path_to_input_video_file> -t <keyword>
```
