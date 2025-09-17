import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    VideoUnavailable,
    TranscriptsDisabled,
    CouldNotRetrieveTranscript,
)
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
        # Try to get the transcript with a preference for English, but fall back to any available language
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        
        formatter = TextFormatter()
        transcript = formatter.format_transcript(transcript_data)
        
        logger.debug(
            "YouTube transcript retrieved successfully",
            extra={"video_id": video_id, "transcript_length": len(transcript)},
        )
        return transcript
    except NoTranscriptFound:
        logger.warning(
            "No transcript found for video in preferred language, trying any available language",
            extra={"video_id": video_id},
        )
        try:
            # Try to get transcript in any available language
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            
            formatter = TextFormatter()
            transcript = formatter.format_transcript(transcript_data)
            
            logger.debug(
                "YouTube transcript retrieved successfully (using non-English language)",
                extra={"video_id": video_id, "transcript_length": len(transcript)},
            )
            return transcript
        except NoTranscriptFound:
            logger.error(
                "No transcript found for video in any language",
                extra={"video_id": video_id},
            )
            raise VideoProcessingError(f"No transcript available for video {video_id}")
        except (VideoUnavailable, TranscriptsDisabled):
            logger.error(
                "Video is unavailable or transcripts are disabled",
                extra={"video_id": video_id},
            )
            raise VideoProcessingError(f"Video {video_id} is unavailable or transcripts are disabled")
        except CouldNotRetrieveTranscript as e:
            logger.error(
                "Could not retrieve transcript for video",
                extra={"video_id": video_id, "error": str(e)},
            )
            raise VideoProcessingError(f"Failed to retrieve transcript for video {video_id}: {str(e)}")
        except Exception as e:
            logger.error(
                "Unexpected error retrieving transcript",
                extra={"video_id": video_id, "error": str(e)},
                exc_info=True,
            )
            raise VideoProcessingError(f"Failed to retrieve transcript for video {video_id}: {str(e)}")
    except (VideoUnavailable, TranscriptsDisabled):
        logger.error(
            "Video is unavailable or transcripts are disabled",
            extra={"video_id": video_id},
        )
        raise VideoProcessingError(f"Video {video_id} is unavailable or transcripts are disabled")
    except CouldNotRetrieveTranscript as e:
        logger.error(
            "Could not retrieve transcript for video",
            extra={"video_id": video_id, "error": str(e)},
        )
        raise VideoProcessingError(f"Failed to retrieve transcript for video {video_id}: {str(e)}")
    except Exception as e:
        logger.error(
            "Unexpected error retrieving transcript",
            extra={"video_id": video_id, "error": str(e)},
            exc_info=True,
        )
        raise VideoProcessingError(f"Failed to retrieve transcript for video {video_id}: {str(e)}")


def get_youtube_metadata(video_id: str) -> dict:
    """Retrieve YouTube video metadata."""
    logger.debug("Retrieving YouTube metadata", extra={"video_id": video_id})
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        metadata = {
            "title": yt.title if hasattr(yt, 'title') else "Unknown Title",
            "channel_name": yt.author if hasattr(yt, 'author') else "Unknown Channel",
            "publication_date": yt.publish_date if hasattr(yt, 'publish_date') else None,
            "view_count": yt.views if hasattr(yt, 'views') else 0,
            "thumbnail_url": yt.thumbnail_url if hasattr(yt, 'thumbnail_url') else "",
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
        # Return default metadata instead of failing completely
        metadata = {
            "title": "Unknown Title",
            "channel_name": "Unknown Channel",
            "publication_date": None,
            "view_count": 0,
            "thumbnail_url": "",
        }
        return metadata
