import firebase_admin
import functions_framework
import logging
import os
import random
import replicate
import requests
import sys
from firebase_admin import firestore, credentials, storage
from firebase_functions import https_fn
from flask import jsonify
from shared.Post import Post
from openai import OpenAI 

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=os.environ.get("LOG_LEVEL", "INFO"),
)

class PostCreationService(object):
    # Initialize openai, firebase database and firebase data storage clients.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", 0))
    cred = credentials.Certificate("./firebaseServiceAccount.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "instagram-autobot-df35b.appspot.com"})
    db = firestore.client()
    bucket = storage.bucket()
    
    def __new__(cls):
        # Singleton design pattern in python.
        if not hasattr(cls, 'instance'):
            cls.instance = super(PostCreationService, cls).__new__(cls)
        return cls.instance

    def createPost(self):
        previousPosts = self.retrieveList("./tmp/previousPosts.txt")
        newPost = Post()
        newPost.caption = self.generateCaption(previousPosts)
        newPost.hashtags = self.generateHashtags(newPost.caption)
        newPost.mediaUrl = self.generateImage(newPost.caption)
        newPost.fileName = self.createFileName()
        return newPost

    def savePost(self, post: Post):
        # save to firebase storage
        logging.info(f"Saving {post.fileName} to database...")
        blob = PostCreationService.bucket.blob(f"{post.fileName}.jpg")
        imageData = requests.get(post.mediaUrl).content
        blob.upload_from_string(
            imageData,
            content_type='image/jpg'
        )
        # change temporary url to firebase permanent url and store in database
        post.mediaUrl = blob.public_url
        blob.make_public()
        PostCreationService.db.collection("posts").add(document_id=post.fileName, document_data={"document" "text": post.caption, "hashtags": post.hashtags, "mediaUrl": post.mediaUrl})
        # update previous post cache 
        self.updateMostPreviousPosts(post.caption)
        logging.info(f"Saved {post.fileName} to database. Public url: {post.mediaUrl}\n")
        return
    
    def updateMostPreviousPosts(self, text):
        blob = self.bucket.blob("tmp/previousPosts.txt")
        local_path = "./tmp/previousPosts.txt"  

        if not blob.exists():
            try:
                # Create new file
                with open(local_path, "w") as f:
                    for _ in range(20):
                        f.write("xx\n")
                blob.upload_from_filename(local_path)
                blob.make_public()
            except Exception as error:
                logging.error("File exists but was not found by system: " + str(error))
        
        # Download file from GCS to /tmp/
        blob.download_to_filename(local_path)

        # Read and update the file
        with open(local_path, "r+") as f:
            _ = f.readline()  # Read first line (to remove it)
            data = f.read()   # Read the rest of the file
            f.seek(0)         # Move cursor to start
            f.write(data)     # Overwrite file without first line
            f.truncate()      # Ensure no leftover content
            f.write(f"{text}\n")  # Append new text

        # Upload the modified file back to GCS
        blob.upload_from_filename(local_path)

    def retrieveList(self, path):
        if not os.path.isfile(path):
            try:
                # Create new file
                open(path, "x")
                with open(path, "a") as f:
                    for _ in range(20):
                        f.write("xx\n")
            except Exception as error:
                logging.error("File exists but was not found by system: " + str(error))

        # Read file content
        textList = []
        with open(path, "r") as f:
            for _ in range(20):
                line = f.readline().rstrip("xx\n")
                if line:
                    textList.append(line)

        return textList
        
    def generateCaption(self, noRepeatList):
        logging.info("Generating caption...")
        motivationThemes = ["reward", "socialRecognition", "obligation", "fear", "socialStatus", "competition"]
        storyTypes = ["Linear Narrative", "Nonlinear Narrative", "Circular Narrative", "Framed Narrative", "Episodic Narrative", "Multi-Perspective Narrative", "Stream of Consciousness", "Epistolary Narrative", "Anthology Narrative", "Interactive Narrative", "Allegorical Narrative", "Metafiction", "Oral Tradition", "Found Footage Narrative", "Flashback Narrative"]
        randomTheme = random.choice(motivationThemes)
        logging.debug("Theme: ", randomTheme)
        prompts = self.retrieveList(f"./tmp/{randomTheme}.txt")

        if not prompts:
            raise ValueError(f"Prompt list for theme '{randomTheme}' is empty. Check if the file exists and contains data.")
        
        randomPrompt = random.choice(prompts)
        logging.debug(randomPrompt)
        noRepeatListOnALine = " ".join(noRepeatList)
    
        textCompletion = PostCreationService.client.chat.completions.create(
            messages=[{"role": "user", "content": f"{randomPrompt}; no hashtags, just a text. If it is a story, follow the {random.choice(storyTypes)} storytelling type with specific scenarios ad interactions leading to speicifc results, shorter than 100 words.\
                       Also I just don't want it starting with a ' in a <someplace> where <some context>', be creative such that the variance of your results is high and creativity high\
                       This quote should follow a different pattern structure, probability of weirdness than from these quotes from previous posts:{noRepeatListOnALine}"}],
            model="gpt-4o-mini",
            temperature=0.8 
        ).to_dict()
        caption = textCompletion["choices"][0]["message"]["content"]
        logging.info(f"Caption: {caption}\n")
        return caption
    
    def generateHashtags(self, text):
        logging.info("Generating hashtags")
        hashtagCompletion = PostCreationService.client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": f"Make ten space-seperated relevant hashtags to this text on a single line):{text}."}],
        ).to_dict()
        hashtags = hashtagCompletion["choices"][0]["message"]["content"]
        logging.info(f"Hashtags: {hashtags}\n")
        return f"#Motivation {hashtags}"
    
    def generateImage(self, text):
        logging.info("Generating image...")
        # Define categories with possible values
        art_styles = ["photorealistic", "cinematic", "digital painting", "anime-inspired", "surrealist"]
        lighting_moods = ["warm golden hour", "moody and dramatic", "soft glow", "neon cyberpunk", "high contrast"]
        composition_styles = ["close-up portrait", "wide-angle shot", "dynamic perspective", "bird’s eye view", "symmetrical composition"]
        color_palettes = ["vibrant neon", "soft pastel", "earthy tones", "monochrome", "colorful gradients"]
        art_mediums = ["oil painting", "watercolor", "cyberpunk digital art", "sketch drawing", "charcoal illustration"]
        detail_levels = ["hyper-detailed", "minimalist", "abstract", "realistic with fine textures"]
        poses_emotions = ["powerful stance", "calm and serene", "determined expression", "energetic movement", "mysterious gaze"]

        imgGenerationPrePrompt = (
            f"Please generate an image generation prompt for the motivational caption '{text}'. Try not to be abstract with the description and the prompt should be structured in two parts: "
            "first, a 'Main Theme' that clearly describes the main idea, emotion, and message of the caption, making it the primary focus of the image; do not put any text at all on the image "
            "second, a 'Style Options' section that lists customizable artistic categories. "
            f"For the style options, feel free appeal to any combination of the following: lighting mood = {random.choice(lighting_moods)}, "
            f"composition = {random.choice(composition_styles)}, color palette = {random.choice(color_palettes)}, "
            f"art medium = {random.choice(art_mediums)}, detail level = {random.choice(detail_levels)}, "
            f"and pose/emotion = {random.choice(poses_emotions)}."
        )

        # Making prompt for image generation

        imageGenerationPrompt = PostCreationService.client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": imgGenerationPrePrompt}],
        ).to_dict()
        imgPrompt = imageGenerationPrompt["choices"][0]["message"]["content"]
        logging.debug(f"\n{imgPrompt}\n")

        # Image generation
        input = {
            "prompt": imgPrompt,
            "prompt_upsampling": True
        }

        output = replicate.run(
            "black-forest-labs/flux-1.1-pro",
            input=input
        )
        image_url = output[0] if isinstance(output, list) else output
        mediaUrl = image_url #imageCompletion["data"][0]["url"]
        logging.info(f"Image url: {mediaUrl}\n")
        return mediaUrl
    
    def createFileName(self):
        logging.info("Creating post file name...")
        postCollection = PostCreationService.db.collection("posts")
        # TODO(oore): Add count variable to database for faster lookup
        countQuery = postCollection.count()
        numberOfPosts = countQuery.get()[0][0].value
        fileName = f"Post#{int(numberOfPosts + 1)}"
        logging.info(f"File name: {fileName}\n")
        return fileName

@https_fn.on_request()
def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    logging.info("Starting Post Creation Service...")
    p = PostCreationService()
    newPost = p.createPost()
    p.savePost(newPost)
    logging.info("Shutting down Post Creation Service")

    return https_fn.Response(
    response=jsonify({"fileName": newPost.fileName, "mediaUrl": newPost.mediaUrl, "caption": newPost.caption, "hashtags": newPost.hashtags}).get_data(as_text=True), 
    content_type="application/json"
    )
