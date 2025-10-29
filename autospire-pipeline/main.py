import logging
import os
import requests
from firebase_functions import https_fn
from flask import jsonify

logging.basicConfig(level=logging.INFO)
POST_CREATION_SERVICE_URL = os.environ.get("POST_CREATION_SERVICE_URL")
POST_PUBLISHING_SERVICE_URL = os.environ.get("POST_PUBLISHING_SERVICE_URL")

@https_fn.on_request()
def main(request):
    logging.info("Starting AutoSpire")
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # post creation
        logging.info("Creating post with post creation service")
        response = requests.get(POST_CREATION_SERVICE_URL, headers = headers).json()

        # attempt parsing
        post_fileName = response.get('fileName')
        post_caption = response.get("caption")
        post_mediaUrl = response.get("mediaUrl")
        post_hashtags = response.get("hashtags")
        post_type = response.get("postType")

        if not (post_caption and post_fileName and post_hashtags and post_mediaUrl):
            return https_fn.Response(
                response=jsonify({"error": "Incomplete Post information, exiting"}).get_data(as_text=True),
                status=400,
                content_type="application/json"
            )
        logging.info(f"Post Created:\nFile name: {post_fileName}.\nCaption: {post_caption}.\nMedia URL: {post_mediaUrl}.\nHashtags: {post_hashtags}\n")

        # post publishing
        logging.info("Publshing post with post publishing service")
        payload = {
            "caption": post_caption,
            "fileName": post_fileName,
            "hashtags": post_hashtags,
            "mediaUrl": post_mediaUrl,
            "postType": post_type
            }
        response = requests.post(POST_PUBLISHING_SERVICE_URL, headers = headers,json=payload).json()
        if response:
            logging.info(f"Post published. Media id: {response.get('mediaId')}")

    except Exception as e:
        logging.error(f"Unexpected error running AutoSpire: {e}")
    
    logging.info("Shutting down AutoSpire")
    
    return https_fn.Response(
        response=jsonify({"Success": "OK 200"}).get_data(as_text=True),
        content_type="application/json"
    )