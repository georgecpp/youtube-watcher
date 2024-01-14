#!/usr/bin/env python

import json
import logging
import sys
import requests
from config import config

def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems",params={
        "key":google_api_key,
        "playlistId": youtube_playlist_id,
        "part": "contentDetails",
        "pageToken": page_token
    })
    payload = json.loads(response.text)
    logging.debug("GOT %s", payload)
    return payload

def fetch_playlist_items(google_api_key, youtube_playlist_id, page_token=None):
    # fetch one page
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token)
    # serve up items from that page
    yield from payload["items"]
    next_page_token = payload.get("nextPageToken")
    # if there is another page, carry on from there.    
    if next_page_token is not None:
        yield from fetch_playlist_items(google_api_key,youtube_playlist_id,next_page_token)

def main():
    logging.info("START")
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]
    for video_item in fetch_playlist_items(google_api_key,youtube_playlist_id):
        logging.info("GOT %s", video_item)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
