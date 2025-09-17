import re
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from ..core.exceptions import VideoProcessingError
from ..core.logging import setup_logging

logger = setup_logging()


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    logger.debug("Extracting video ID from URL", extra={"url": url})
    # Regular expression to match YouTube video IDs
    video_id_pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(video_id_pattern, url)
    if match:
        video_id = match.group(1)
        logger.debug("Video ID extracted successfully", extra={"video_id": video_id})
        return video_id
    else:
        logger.error("Invalid YouTube URL provided", extra={"url": url})
        raise VideoProcessingError("Invalid YouTube URL")


def get_youtube_transcript(video_id: str) -> str:
    """Retrieve YouTube video transcript."""
    logger.debug("Retrieving YouTube transcript", extra={"video_id": video_id})
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all transcript segments into a single string
        transcript = " ".join([entry["text"] for entry in transcript_list])
        logger.debug(
            "YouTube transcript retrieved successfully",
            extra={"video_id": video_id, "transcript_length": len(transcript)},
        )
        return transcript
    except Exception as e:
        logger.error(
            "Failed to retrieve transcript",
            extra={"video_id": video_id, "error": str(e)},
            exc_info=True,
        )
        raise VideoProcessingError(f"Failed to retrieve transcript: {str(e)}")


def get_youtube_metadata(video_id: str) -> dict:
    """Retrieve YouTube video metadata."""
    logger.debug("Retrieving YouTube metadata", extra={"video_id": video_id})
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        metadata = {
            "title": yt.title,
            "channel_name": yt.author,
            "publication_date": yt.publish_date,
            "view_count": yt.views,
            "thumbnail_url": yt.thumbnail_url,
        }
        logger.debug(
            "YouTube metadata retrieved successfully",
            extra={"video_id": video_id, "metadata_keys": list(metadata.keys())},
        )
        return metadata
    except Exception as e:
        logger.error(
            "Failed to retrieve metadata",
            extra={"video_id": video_id, "error": str(e)},
            exc_info=True,
        )
        raise VideoProcessingError(f"Failed to retrieve metadata: {str(e)}")
