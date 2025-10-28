class Post:
    def __init__(self, fileName=None, mediaUrl=None, caption=None, hashtags=None):
        # Each post should have a picture and some text
        self.fileName = fileName
        self.mediaUrl = mediaUrl
        self.caption = caption
        self.hashtags = hashtags

    def __repr__(self):
        return str({"Text": self.text, "Media URL" : self.mediaUrl})
