import re

# Read
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all YouTube URLs with just the video ID
content = re.sub(r"vid:'https://youtu\.be/([a-zA-Z0-9_-]+)[^']*'", r"vid:'\1'", content)

# Write
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All YouTube URLs converted to video IDs!")

