
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

# =====================================
# YOUTUBE API CLIENT
# =====================================

def get_youtube_client():
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
# YOUTUBE SCRAPER
# =====================================

def search_youtube(
    keyword,
    max_contents=50,
    max_comments=100,
    language="Indonesian"
):
    youtube = get_youtube_client()

    contents = []
    comments = []
    errors = []

    # SEARCH VIDEOS
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

            if language == "Indonesian":
                request_params["relevanceLanguage"] = "id"
            elif language == "English":
                request_params["relevanceLanguage"] = "en"

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

    # COLLECT COMMENTS
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

    return {
        "contents": contents,
        "comments": comments,
        "errors": errors
    }

# =====================================
# PLATFORM REGISTRY
# =====================================

SCRAPERS = {
    "YouTube": search_youtube
}

# =====================================
# MULTI-PLATFORM SCRAPER
# =====================================

def search_all_platforms(
    platforms,
    keyword,
    max_contents=50,
    max_comments=100,
    language="Indonesian"
):
    """
    Menjalankan scraper berdasarkan platform yang dipilih.
    Hasil dari seluruh platform digabungkan dalam satu dataset.
    """

    all_contents = []
    all_comments = []
    all_errors = []
    successful_platforms = []

    for platform in platforms:

        scraper_function = SCRAPERS.get(platform)

        # Platform belum memiliki scraper.
        if scraper_function is None:
            all_errors.append({
                "platform": platform,
                "content_title": "",
                "error": (
                    f"Scraper {platform} belum diintegrasikan."
                )
            })
            continue

        try:
            result = scraper_function(
                keyword=keyword,
                max_contents=max_contents,
                max_comments=max_comments,
                language=language
            )

            if not isinstance(result, dict):
                raise ValueError(
                    "Format hasil scraper tidak valid."
                )

            contents = result.get("contents", [])
            comments = result.get("comments", [])
            errors = result.get("errors", [])

            # Pastikan semua baris memiliki identitas platform.
            for item in contents:
                item["platform"] = platform

            for item in comments:
                item["platform"] = platform

            for item in errors:
                if isinstance(item, dict):
                    item["platform"] = platform

            all_contents.extend(contents)
            all_comments.extend(comments)
            all_errors.extend(errors)

            successful_platforms.append(platform)

        except Exception as error:
            all_errors.append({
                "platform": platform,
                "content_title": "",
                "error": str(error)
            })

    return {
        "contents": all_contents,
        "comments": all_comments,
        "errors": all_errors,
        "platforms_requested": list(platforms),
        "platforms_succeeded": successful_platforms
    }