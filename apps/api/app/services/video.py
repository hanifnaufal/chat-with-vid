import re
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    VideoUnavailable,
    TranscriptsDisabled,
    CouldNotRetrieveTranscript,
)
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
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
    """Retrieve and format YouTube video transcript."""
    logger.debug("Retrieving YouTube transcript", extra={"video_id": video_id})
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)

        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript_list)

        logger.debug(
            "YouTube transcript retrieved successfully",
            extra={
                "video_id": video_id,
                "transcript_length": len(formatted_transcript),
            },
        )
        return formatted_transcript
    except (
        NoTranscriptFound,
        VideoUnavailable,
        TranscriptsDisabled,
        CouldNotRetrieveTranscript,
    ) as e:
        logger.error(
            "Failed to retrieve transcript",
            extra={"video_id": video_id, "error": str(e)},
            exc_info=True,
        )
        raise VideoProcessingError(
            f"Failed to retrieve transcript for video {video_id}: {str(e)}"
        )
    except Exception as e:
        logger.error(
            "Unexpected error while retrieving transcript",
            extra={"video_id": video_id, "error": str(e)},
            exc_info=True,
        )
        raise VideoProcessingError(
            f"Unexpected error while retrieving transcript for video {video_id}: {str(e)}"
        )


def get_youtube_metadata(video_id: str) -> dict:
    """Retrieve YouTube video metadata using yt-dlp."""
    logger.debug(
        "Retrieving YouTube metadata with yt-dlp", extra={"video_id": video_id}
    )
    try:
        # Configure yt-dlp options for metadata extraction
        ydl_opts = {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": "in_playlist",
        }

        # Extract metadata using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            info = ydl.extract_info(video_url, download=False)

            metadata = {
                "title": info.get("title", "Unknown Title"),
                "channel_name": info.get("uploader", "Unknown Channel"),
                "publication_date": None,
                "view_count": info.get("view_count", 0),
                "thumbnail_url": info.get("thumbnail", ""),
            }

            timestamp = info.get("timestamp")
            if timestamp:
                try:
                    metadata["publication_date"] = datetime.fromtimestamp(timestamp)
                except (ValueError, OSError, OverflowError):
                    metadata["publication_date"] = None

        logger.debug(
            "YouTube metadata retrieved successfully with yt-dlp",
            extra={"video_id": video_id, "metadata_keys": list(metadata.keys())},
        )
        return metadata

    except (DownloadError, ExtractorError) as e:
        logger.error(
            "Failed to retrieve metadata with yt-dlp",
            extra={"video_id": video_id, "error": str(e)},
            exc_info=True,
        )
        raise VideoProcessingError(
            f"Failed to retrieve metadata for video {video_id}: {str(e)}"
        )
    except Exception as e:
        logger.error(
            "Unexpected error while retrieving metadata with yt-dlp",
            extra={"video_id": video_id, "error": str(e)},
            exc_info=True,
        )
        raise VideoProcessingError(
            f"Unexpected error while retrieving metadata for video {video_id}: {str(e)}"
        )
