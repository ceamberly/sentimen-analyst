
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# =====================================
# ENVIRONMENT CONFIGURATION
# =====================================

load_dotenv()


# =====================================
# YOUTUBE API CLIENT
# =====================================

def get_youtube_client():
    """
    Membuat koneksi ke YouTube Data API.
    """

    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise ValueError(
            "YouTube API Key belum ditemukan. "
            "Tambahkan YOUTUBE_API_KEY ke file .env."
        )

    return build(
        "youtube",
        "v3",
        developerKey=api_key,
        cache_discovery=False
    )


# =====================================
# YOUTUBE SEARCH & COMMENT SCRAPER
# =====================================

def search_youtube(
    keyword,
    max_contents=50,
    max_comments=100,
    language="Indonesian"
):
    """
    Mencari beberapa video YouTube berdasarkan keyword,
    kemudian mengambil komentar dari setiap video.

    Returns:
        {
            "contents": list,
            "comments": list,
            "errors": list
        }
    """

    youtube = get_youtube_client()

    contents = []
    comments = []
    errors = []

    # =====================================
    # 1. SEARCH VIDEOS
    # =====================================

    page_token = None

    try:

        while len(contents) < max_contents:

            remaining = max_contents - len(contents)

            request_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "maxResults": min(50, remaining),
                "order": "relevance"
            }

            if page_token:
                request_params["pageToken"] = page_token

            # LANGUAGE FILTER

            if language == "Indonesian":
                request_params["relevanceLanguage"] = "id"

            elif language == "English":
                request_params["relevanceLanguage"] = "en"

            # EXECUTE SEARCH

            response = youtube.search().list(
                **request_params
            ).execute()

            items = response.get("items", [])

            if not items:
                break

            for item in items:

                video_id = item["id"]["videoId"]
                snippet = item["snippet"]

                contents.append({
                    "platform": "YouTube",
                    "content_id": video_id,
                    "title": snippet.get("title", ""),
                    "content_url": (
                        f"https://www.youtube.com/watch?v={video_id}"
                    ),
                    "author": snippet.get("channelTitle", ""),
                    "channel_id": snippet.get("channelId", ""),
                    "description": snippet.get("description", ""),
                    "published_at": snippet.get("publishedAt", "")
                })

            page_token = response.get("nextPageToken")

            if not page_token:
                break

    except HttpError as error:

        raise RuntimeError(
            f"Gagal mencari video YouTube: {error}"
        )

    # =====================================
    # 2. COLLECT COMMENTS
    # =====================================

    for video in contents:

        video_id = video["content_id"]
        collected_for_video = 0
        comment_page_token = None

        try:

            while collected_for_video < max_comments:

                remaining = max_comments - collected_for_video

                request_params = {
                    "part": "snippet",
                    "videoId": video_id,
                    "maxResults": min(100, remaining),
                    "textFormat": "plainText",
                    "order": "relevance"
                }

                if comment_page_token:
                    request_params["pageToken"] = comment_page_token

                response = youtube.commentThreads().list(
                    **request_params
                ).execute()

                items = response.get("items", [])

                if not items:
                    break

                for item in items:

                    comment = item["snippet"]["topLevelComment"]
                    snippet = comment["snippet"]

                    comments.append({
                        "platform": "YouTube",
                        "content_id": video_id,
                        "content_title": video["title"],
                        "content_url": video["content_url"],
                        "author": snippet.get("authorDisplayName", ""),
                        "text": snippet.get("textDisplay", ""),
                        "published_at": snippet.get("publishedAt", ""),
                        "like_count": snippet.get("likeCount", 0),
                        "reply_count": item["snippet"].get(
                            "totalReplyCount", 0
                        )
                    })

                    collected_for_video += 1

                    if collected_for_video >= max_comments:
                        break

                comment_page_token = response.get("nextPageToken")

                if not comment_page_token:
                    break

        except HttpError as error:

            errors.append({
                "platform": "YouTube",
                "content_id": video_id,
                "content_title": video["title"],
                "error": str(error)
            })

            # Lanjut mengambil komentar dari video berikutnya.
            continue

    # =====================================
    # 3. RETURN DATA
    # =====================================

    return {
        "contents": contents,
        "comments": comments,
        "errors": errors
    }