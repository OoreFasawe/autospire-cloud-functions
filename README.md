# AutoInspire  
Instagram Account: [butterman_411](https://www.instagram.com/butterman_411/)  
<img src="https://firebasestorage.googleapis.com/v0/b/instagram-autobot-df35b.appspot.com/o/IMG_B108D631FF82-1.jpeg?alt=media&token=6ea618ae-b89a-4020-9636-8c74c14eed4b" alt="Screenshot of instagram page" width="370" height="700">

###

<img src="https://firebasestorage.googleapis.com/v0/b/instagram-autobot-df35b.appspot.com/o/IMG_F633978156DD-1.jpeg?alt=media&token=d97fc1ef-3562-4236-811b-c84156739314" alt="Screenshot of sample ig post" width="370" height="600">

## Purpose  
AutoInspire is a project built to generate and publish motivational posts on Instagram. While designed for motivational content, the framework is flexible enough to support any theme for creating an Instagram account via using differrent prompts.

This is a serverless backend for AutoSpire, an automated system that creates and posts motivational content. Built with Google Cloud Functions, it uses ChatGPT, DALL-E, and the Instagram Graph API to generate, design, and publish posts. Each function deploys independently and connects through Firebase.

## Overview  
The project is divided into two primary services: the post creation service, which uses OpenAI's ChatGPT and DALL-E models to generate captions, hashtags and images, and the post publishing service, which handles interactions with the Instagram account via the Facebook and Instagram Graph APIs. All post data is stored in Google Firebase database and storage. Additional services may be introduced as the project evolves and more features are added.

## Setup  
Coming soon...

## Development notes 
This project is still in development, and while the design isn't final, I’ve prioritized delivering a functional version first. Some aspects, such as file path management, absence of a dedicated logger for different logging priorities, and processes that could be run asynchronously, are still rough and will be refined over time. Since this is a personal project, it’s currently tailored to my own needs, but adjustments could be made later if it’s extended for broader use. My focus for now is tackling the most challenging and urgent requirements before refining other aspects.
