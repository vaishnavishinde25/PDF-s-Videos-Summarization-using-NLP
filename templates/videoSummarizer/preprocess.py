from youtube_transcript_api import YouTubeTranscriptApi

def get_text_from_video(link):
    a=link.split("=")
    video_id=a[-1]
    raw_text = YouTubeTranscriptApi.get_transcript(video_id)
    text = '. '.join([line['text'] for line in raw_text])
    return text