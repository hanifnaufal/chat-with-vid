import re
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from ..core.exceptions import VideoProcessingError


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    # Regular expression to match YouTube video IDs
    video_id_pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(video_id_pattern, url)
    if match:
        return match.group(1)
    else:
        raise VideoProcessingError("Invalid YouTube URL")


def get_youtube_transcript(video_id: str) -> str:
    """Retrieve YouTube video transcript."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all transcript segments into a single string
        transcript = " ".join([entry["text"] for entry in transcript_list])
        return transcript
    except Exception as e:
        raise VideoProcessingError(f"Failed to retrieve transcript: {str(e)}")


def get_youtube_metadata(video_id: str) -> dict:
    """Retrieve YouTube video metadata."""
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        return {
            "title": yt.title,
            "channel_name": yt.author,
            "publication_date": yt.publish_date,
            "view_count": yt.views,
            "thumbnail_url": yt.thumbnail_url,
        }
    except Exception as e:
        raise VideoProcessingError(f"Failed to retrieve metadata: {str(e)}")
