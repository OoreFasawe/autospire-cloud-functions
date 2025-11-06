from Classes.post_model import Post, PostTypes
from Utility import last_sentence

class VideoPost(Post):
    def __init__(self, fileName=None, mediaUrl=None, caption=None, hashtags=None):
        super().__init__(fileName, mediaUrl, caption, hashtags)
        self.numberOfPost = 1
        self.postType = PostTypes.VIDEO

    def createPost(self, creationServiceToUse):
        previousPosts = creationServiceToUse.retrieveList("./tmp/previousPosts.txt")
        self.caption = creationServiceToUse.generateCaption(previousPosts)
        self.hashtags = creationServiceToUse.generateHashtags(self.caption)
        self.mediaUrl = creationServiceToUse.generateVideo(self.caption)
        self.caption = last_sentence(self.caption)
        self.fileName = creationServiceToUse.createFileName()
        return self
