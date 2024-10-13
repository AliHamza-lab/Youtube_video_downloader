import os
import re
from pathlib import Path
import yt_dlp
#To run this script you must  have to install yt-dlp pakage by just typing the pip install yt-dlp command in your terminal
def get_youtube_video_titles(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        titles = [video['title'].lower() for video in info_dict.get('entries', [])]
    
    return info_dict['entries'], titles

def clean_filename(filename):
    cleaned_name = re.sub(r'\[.*?\]', '', filename)
    return cleaned_name.strip().lower()

def download_video(url, download_path):
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'noplaylist': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"Failed to download {url}: {str(e)}")
        print("Attempting fallback format...")
        ydl_opts['format'] = 'best'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def process_videos(download_folder, youtube_entries):
    download_path = Path(download_folder)
    download_path.mkdir(parents=True, exist_ok=True)
    
    for entry in youtube_entries:
        title = entry['title'].lower()
        video_id = entry['id']
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading video: {title}")
        download_video(url, download_path)

if __name__ == "__main__":
    #Define the path where you want your video to store
    download_folder = r"The path where video is going to downlod"
    #Enter the Url of channel from where you want to download all videos 
    channel_url = 'https://www.youtube.com/@YourChannelName'
    youtube_entries, _ = get_youtube_video_titles(channel_url)
    process_videos(download_folder, youtube_entries)
