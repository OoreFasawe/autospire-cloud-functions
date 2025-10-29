import logging
from Classes.post_model import Post, PostTypes

class VideoPost(Post):
    def __init__(self, fileName=None, mediaUrl=None, caption=None, hashtags=None):
        super().__init__(fileName, mediaUrl, caption, hashtags)
        self.numberOfPost = 1
        self.postType = PostTypes.VIDEO

    def publishPost(self, publishingServiceToUse):
        userData = publishingServiceToUse.getUserDetails()
        if not userData:
            logging.error("Error retrieving user details.")
            return None
        userId = userData["user_id"]
        containerId = publishingServiceToUse.createVideoContainer(userId, self)
        mediaId = publishingServiceToUse.publishMediaContainer(userId, containerId)
        return mediaId