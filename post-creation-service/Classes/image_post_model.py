from Classes.post_model import Post, PostTypes

class ImagePost(Post):
    def __init__(self, fileName=None, mediaUrl=None, caption=None, hashtags=None):
        super().__init__(fileName, mediaUrl, caption, hashtags)
        self.numberOfPost = 1
        self.postType = PostTypes.IMAGE

    def createPost(self, creationServiceToUse):
        previousPosts = creationServiceToUse.retrieveList("./tmp/previousPosts.txt")
        self.caption = creationServiceToUse.generateCaption(previousPosts)
        self.hashtags = creationServiceToUse.generateHashtags(self.caption)
        self.mediaUrl = creationServiceToUse.generateImage(self.caption)
        self.fileName = creationServiceToUse.createFileName()
        return self