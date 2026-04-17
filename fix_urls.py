import re
import os

# Get the full path
html_path = os.path.join(os.getcwd(), 'index.html')
print(f"Working with: {html_path}")

# Read the HTML file
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Read {len(content)} characters")

# Pattern to find YouTube URLs in the vid property
def extract_video_id(url):
    # Handle youtu.be URLs
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Handle youtube.com URLs with v= parameter
    match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return url

# Replace all vid values that contain URLs
def replace_vid_urls(content):
    # Pattern to match vid:'URL' or vid:"URL"
    pattern = r"vid:'(https?://[^']+)'"
    replacements = 0
    
    def replacer(match):
        nonlocal replacements
        url = match.group(1)
        vid_id = extract_video_id(url)
        replacements += 1
        print(f"  {url[:50]}... → {vid_id}")
        return f"vid:'{vid_id}'"
    
    content = re.sub(pattern, replacer, content)
    print(f"Replaced {replacements} video IDs")
    
    return content

# Replace URLs with video IDs
print("Fixing YouTube URLs...")
content = replace_vid_urls(content)

# Write back
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Done! All YouTube URLs converted to video IDs")
