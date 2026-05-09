#!/usr/bin/env python3
"""
Scrape YouTube for dental lab owner pain-point content.
Outputs transcripts.json with title, url, channel, transcript text.
"""
import json
import warnings
from pathlib import Path
from typing import Dict, List, Optional

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

SEARCH_QUERIES = [
    "running a dental lab",
    "dental lab owner interview",
    "dental lab management problems",
    "dental laboratory workflow",
    "dental lab prescription problems",
    "independent dental lab business",
    "dental lab technician shortage",
    "dental lab remake rate",
    "NADL dental lab",
    "LMT dental lab management",
]

VIDEOS_PER_QUERY = 8
OUTPUT_FILE = "transcripts.json"

YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": True,
    "skip_download": True,
}


def search_videos(query: str, n: int) -> List[Dict]:
    """Use yt_dlp to search YouTube and return video metadata."""
    opts = {**YDL_OPTS, "playlistend": n}
    videos = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch{n}:{query}", download=False)
            except Exception as e:
                print(f"  ! search failed for {query!r}: {e}")
                return []
    for entry in (info or {}).get("entries") or []:
        if not entry or not entry.get("id"):
            continue
        videos.append({
            "id": entry.get("id"),
            "title": entry.get("title"),
            "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
            "channel": entry.get("channel") or entry.get("uploader"),
            "duration": entry.get("duration"),
            "view_count": entry.get("view_count"),
            "search_query": query,
        })
    return videos


def fetch_transcript(video_id: str) -> Optional[str]:
    """Fetch English transcript text for a video, or None if unavailable."""
    try:
        api = YouTubeTranscriptApi()
        chunks = api.fetch(video_id, languages=["en", "en-US"])
        return " ".join(c.text for c in chunks)
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"  ! transcript failed for {video_id}: {e}")
        return None


def main():
    all_videos: Dict[str, Dict] = {}

    for query in SEARCH_QUERIES:
        print(f"Searching: {query!r}")
        for vid in search_videos(query, VIDEOS_PER_QUERY):
            if vid["id"] and vid["id"] not in all_videos:
                all_videos[vid["id"]] = vid

    print(f"\nFound {len(all_videos)} unique videos. Fetching transcripts...\n")

    results = []
    for i, (vid_id, vid) in enumerate(all_videos.items(), 1):
        title = (vid.get("title") or "")[:80]
        print(f"[{i}/{len(all_videos)}] {title}")
        transcript = fetch_transcript(vid_id)
        if not transcript:
            print("  - no transcript, skipping")
            continue
        vid["transcript"] = transcript
        vid["transcript_word_count"] = len(transcript.split())
        results.append(vid)

    results.sort(key=lambda v: v.get("view_count") or 0, reverse=True)

    Path(OUTPUT_FILE).write_text(json.dumps(results, indent=2))
    print(f"\nSaved {len(results)} videos with transcripts to {OUTPUT_FILE}")
    print(f"Total words: {sum(v['transcript_word_count'] for v in results):,}")


if __name__ == "__main__":
    main()
