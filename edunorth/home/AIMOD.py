import os
import google.generativeai as genai
import googleapiclient.discovery
import requests
from concurrent.futures import ThreadPoolExecutor

# Set up API keys
GEMINI_API_KEY = "AIzaSyBqjPE0TbxzqYfeyafdcYV2NDMcPH7o1nQ"  # Replace with your actual Gemini API key
YOUTUBE_API_KEY = "AIzaSyBjJd35uZABWMDqb6P0eX0s7V48y04L5Lo"  # Replace with your actual YouTube API key
GOOGLE_SEARCH_API_KEY = "AIzaSyBjJd35uZABWMDqb6P0eX0s7V48y04L5Lo"  # Replace with your Google Custom Search API Key
SEARCH_ENGINE_ID = "75a78cddbd2294533"  # Replace with your Custom Search Engine ID

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


# Function to fetch subtopics from Gemini
def get_subtopics(topic):
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    prompt = f"Provide only the subtopics of '{topic}'. No extra words, just a list of subtopics."
    
    response = model.generate_content(prompt)
    
    # Extract response text and limit to 10 subtopics
    subtopics = response.text.strip().split("\n")[:10]
    
    # Store in dictionary format
    subtopics_dict = {"topic": topic, "subtopics": subtopics}
    
    return subtopics_dict

# Function to fetch the most viewed YouTube video (at least 30 mins long)
def get_top_youtube_video(subtopic, topic):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Construct a dynamic search query using the main topic
    search_query = f"{subtopic} {topic}"
    
    # Search for videos sorted by view count
    request = youtube.search().list(
        q=search_query,
        part="snippet",
        maxResults=5,  # Fetch more results to filter better
        type="video",
        order="viewCount"
    )
    response = request.execute()

    valid_videos = []

    # Fetch video details with duration filter
    for video in response.get("items", []):
        video_id = video["id"]["videoId"]
        
        # Get video details including duration
        video_details = youtube.videos().list(
            part="contentDetails,snippet,statistics",
            id=video_id
        ).execute()
        
        if video_details["items"]:
            details = video_details["items"][0]
            duration = details["contentDetails"]["duration"]
            video_title = details["snippet"]["title"]
            view_count = int(details["statistics"]["viewCount"])  # Get view count

            # Convert duration to minutes (ISO 8601 format: PT#H#M#S)
            hours = minutes = seconds = 0
            if "H" in duration:
                hours = int(duration.split("H")[0].replace("PT", ""))
            if "M" in duration:
                minutes = int(duration.split("M")[0].split("H")[-1].replace("PT", ""))
            if "S" in duration:
                seconds = int(duration.split("S")[0].split("M")[-1].split("H")[-1].replace("PT", ""))
            
            total_minutes = (hours * 60) + minutes + (seconds / 60)
            
            # Only consider videos that are at least 30 minutes long
            if total_minutes >= 30:
                valid_videos.append({
                    "subtopic": subtopic,  # Include the subtopic name
                    "title": video_title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "views": view_count
                })

    # Select the video with the highest view count
    if valid_videos:
        best_video = max(valid_videos, key=lambda v: v["views"])
        return best_video  # Already contains subtopic key

    return None  # No suitable video found

# Function to fetch one blog per subtopic
def get_blog_link(subtopic, topic):
    search_query = f"{subtopic} {topic} blog"
    url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}"

    response = requests.get(url)
    results = response.json()

    if "items" in results and len(results["items"]) > 0:
        blog = results["items"][0]  # Select the first (most relevant) blog
        return {"title": blog["title"], "url": blog["link"]}

    return None  # No blog found




# 🔴 REMOVE input() function!
def get_ai_response(topic):
    subtopics_dict = get_subtopics(topic)
    subtopic_data = {}
    topic_name = subtopics_dict["topic"]

  
    def fetch_video_and_blog(subtopic, topic):
        video_info = get_top_youtube_video(subtopic, topic)
        blog_info = get_blog_link(subtopic, topic)
        return subtopic, {"subtopic": subtopic, "video": video_info, "blog": blog_info}

# Run API calls in parallel for all subtopics
    subtopic_data = {}
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda s: fetch_video_and_blog(s, topic_name), subtopics_dict["subtopics"])

# Store results in dictionary
    for subtopic, data in results:
        subtopic_data[subtopic] = data
    return {"topic": topic, "subtopics": subtopic_data }