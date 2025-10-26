import logging
import os
import requests
import Utility
from firebase_functions import https_fn
from flask import jsonify
from shared.Classes.Post import Post


base_ig_url = "https://graph.instagram.com/"
base_fb_url = "https://graph.facebook.com/"
params = {}
userData = {}

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=os.environ.get("LOG_LEVEL", "INFO"),
)

class PostPublishingService:
    instagram_access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    # Singleton design pattern in python.
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PostPublishingService, cls).__new__(cls)
        return cls.instance 

    def publishPost(self, post:Post):
        logging.info("Starting Post Publishing Service")
        userData = self.getUserDetails()
        if not userData:
            logging.error("Error retrieving user details.")
            return None
        userId = userData["user_id"]
        containerId = self.createMediaContainer(userId, post)
        mediaId = self.publishMediaContainer(userId, containerId)
        return mediaId
    
    def getUserDetails(self):
        logging.info("Getting Instagram user details...")
        access_token = Utility.get_token()
        if not access_token:
            logging.error("Instagram access token not found.")
            return None
        params = {
            "access_token": access_token,
            "fields": "user_id,username,account_type,name"
        }
        logging.debug(f"Instagram Access Token, last 5 chars: {access_token[-5:]}")
        try:
            response = requests.get(base_ig_url + "me", params=params)
            response.raise_for_status()  # Raises HTTPError if status is 4xx/5xx
            userData = response.json()
            logging.info(f"Username: {userData.get('username')}. User id: {userData.get('user_id')}\n")
            return userData
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error: {e} - Response: {response.text}")
        except ValueError:
            logging.error(f"Failed to parse JSON from response: {response.text}")
        except Exception as e:
            logging.error(f"Unexpected error fetching user details: {e}")
            
        return dict()
    
    def createMediaContainer(self, userId, post:Post):
        logging.info(f"Creating media container...")
        logging.debug(f"Post media url: {post.mediaUrl}")
        logging.debug(f"Post caption:{post.caption}")
        logging.debug(f"Post hashtags:{post.hashtags}")
        access_token = Utility.get_token()
        if not access_token:
            logging.error("Instagram access token not found.")
            return None
        params["access_token"] = access_token
        params["image_url"] = post.mediaUrl
        params["caption"] = post.caption + "\n\n" + post.hashtags
        response = requests.post(base_ig_url + f"{userId}/media", params)
        logging.debug(f"Creating media container response details: {response.json()}")
        containerId = response.json()["id"]
        params["image_url"] = None
        params["caption"] = None
        logging.info(f"Media container created, container id: {containerId}\n")
        return containerId

    def publishMediaContainer(self, userId, containerId):
        logging.info(f"Publishing post...")
        params["access_token"] = Utility.get_token()
        params["creation_id"] = containerId
        response = requests.post(base_ig_url + f"{userId}/media_publish", params)
        logging.debug(f"Publishing media container response details: {response.json()}")
        mediaId = response.json()["id"]
        params["creation_id"] = None
        logging.info(f"Post published, media id: {mediaId}\n")
        return mediaId

    
@https_fn.on_request()
def main(request):
    logging.info("Starting Post Publishing Service...")
    logging.info("Checking if token needs refresh...")
    Utility.maybe_refresh_token()
    
    # Parse JSON body
    try:
        request_json = request.get_json(force=True)
        post_caption = request_json.get("caption")
        post_fileName = request_json.get("fileName")
        post_hashtags = request_json.get("hashtags")
        post_mediaUrl = request_json.get("mediaUrl")
        if not (post_caption and post_fileName and post_hashtags and post_mediaUrl):
            return https_fn.Response(
                response=jsonify({"error": "Incomplete Post information, exiting"}).get_data(as_text=True),
                status=400,
                content_type="application/json"
            )
        new_post = Post(caption=post_caption, fileName=post_fileName, hashtags=post_hashtags, mediaUrl=post_mediaUrl)

    except Exception as e:
        logging.error(f"Error parsing JSON: {e}")
        return https_fn.Response(
            response=jsonify({"error": "Invalid JSON body"}).get_data(as_text=True),
            status=400,
            content_type="application/json"
        )

    # Use the post publishing service
    p = PostPublishingService()
    media_id = p.publishPost(new_post)
    
    logging.info("Shutting down Post Publishing Service")
    
    return https_fn.Response(
        response=jsonify({"mediaId": media_id}).get_data(as_text=True),
        content_type="application/json"
    )
