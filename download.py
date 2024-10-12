import os
import re
from pathlib import Path
import yt_dlp

def get_youtube_video_titles(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Only extract metadata, not download
        'force_generic_extractor': True,  # Use generic extractor for lists
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        # Extract titles from the playlist
        titles = [video['title'].lower() for video in info_dict.get('entries', [])]
    return info_dict['entries'], titles

def clean_filename(filename):
    # Remove everything within brackets (e.g., [TkaV4MgNBDw])
    cleaned_name = re.sub(r'\[.*?\]', '', filename)
    # Remove extra spaces and make the name lowercase
    return cleaned_name.strip().lower()

def download_video(url, download_path):
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'format': 'best',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def processing_video(download_folder, youtube_entries):
    # Create the download folder if it doesn't exist
    download_path = Path(download_folder)
    download_path.mkdir(parents=True, exist_ok=True)

    # Find missing titles and download videos
    for entry in youtube_entries:
        title = entry['title'].lower()
        video_id = entry['id']
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading video: {title}")
        download_video(url, download_path)

if __name__ == "__main__":
    download_folder = Path(r"F:\channel2 data")  # Replace with the desired download folder
    
    # Replace with your YouTube channel URL
    channel_url = 'CHANNEL URL'
    
    youtube_entries, _ = get_youtube_video_titles(channel_url)
    processing_video(download_folder, youtube_entries)