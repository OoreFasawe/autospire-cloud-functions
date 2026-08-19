# AutoInspire (Phase One)
Instagram Account: [butterman_411](https://www.instagram.com/butterman_411/)  
<img src="https://firebasestorage.googleapis.com/v0/b/instagram-autobot-df35b.appspot.com/o/Post%23295.jpg?alt=media&token=14015e10-5e95-47a4-97d7-f346a1eab18f" alt="Screenshot of instagram page" width="370" height="700">

###

<img src="https://firebasestorage.googleapis.com/v0/b/instagram-autobot-df35b.appspot.com/o/Post%23301.jpg?alt=media&token=f42f2cd2-855d-4b0d-b829-56a6f0c62354" alt="Screenshot of sample ig post" width="370" height="600">

## Purpose  
AutoInspire is a project built to generate and publish motivational posts on Instagram. While designed for motivational content, the framework is flexible enough to support any theme for creating an Instagram account via using differrent prompts.

This is a serverless backend for AutoSpire, an automated system that creates and posts motivational content. Built with Google Cloud Functions, it uses ChatGPT, DALL-E, sora-2, the Instagram Graph API and Firebase to generate, store, and publish posts with image and video content. Each function deploys independently, shares data through firebase and connects through http requests.

## Overview  
The project is divided into two primary services: the post creation service, which uses OpenAI's ChatGPT and DALL-E models to generate captions, hashtags, images and videos, and the post publishing service, which handles interactions with the Instagram account via the Facebook and Instagram Graph APIs. All post data is stored in Google Firebase database and storage. Additional services may be introduced as the project evolves and more features are added.

## Setup  
Coming soon...

## Development notes 
This project is still in development, and while the design isn't final, I’ve prioritized delivering a functional version first. Some aspects, such as file path management, absence of a dedicated logger for different logging priorities, and processes that could be run asynchronously, are still rough and will be refined over time. Since this is a personal project, it’s currently tailored to my own needs, but adjustments could be made later if it’s extended for broader use. My focus for now is tackling the most challenging and urgent requirements before refining other aspects.

## 2026 Strategy
[Strategy doc](https://docs.google.com/document/d/1Xn2k-1OTZy8S2uZ8SaTVE-ouuVoO6oo5jWcPxq58ATg/edit?tab=t.0a) (For my eyes only). 
