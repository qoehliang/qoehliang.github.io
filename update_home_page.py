#!/usr/bin/env python3
import os
import re
import glob
from datetime import datetime
import yaml

# Function to extract frontmatter from markdown files
def extract_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter_text = frontmatter_match.group(1)
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter
        except yaml.YAMLError:
            return {}
    return {}

# Get all blog posts
blog_posts = []
for post_file in glob.glob('docs/blog/posts/*.md'):
    frontmatter = extract_frontmatter(post_file)
    
    if 'date' in frontmatter:
        date_str = frontmatter['date']
        if isinstance(date_str, str):
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                continue
        else:
            date = date_str
        
        # Get post title
        with open(post_file, 'r', encoding='utf-8') as file:
            content = file.read()
            title_match = re.search(r'^# (.*?)$', content, flags=re.MULTILINE)
            title = title_match.group(1) if title_match else os.path.basename(post_file).replace('.md', '')
        
        # Get post URL
        post_url = f"blog/{date.strftime('%Y/%m/%d')}/{os.path.basename(post_file).replace('.md', '')}"
        
        # Get image path
        image_path = frontmatter.get('image', f"assets/images/blog/{os.path.basename(post_file).replace('.md', '')}.svg")
        
        # Get description
        description = frontmatter.get('description', '')
        
        # Format date for display
        display_date = date.strftime('%b %d, %y')
        
        blog_posts.append({
            'title': title,
            'date': date,
            'display_date': display_date,
            'image': image_path,
            'description': description,
            'url': post_url
        })

# Sort posts by date (newest first)
blog_posts.sort(key=lambda x: x['date'], reverse=True)

# Take the latest 3 posts (or all if less than 3)
latest_posts = blog_posts[:3]

# Generate the home page content
home_page_content = """---
hide:
  - navigation
  - toc
---

<div class="profile-section">
  <img src="assets/images/profile-photo.svg" alt="Alan Liang" class="profile-image">
  <h1 class="profile-name">Alan Liang</h1>
  <p class="profile-title">Staff Platform Engineer</p>
  
  <div class="social-links">
    <a href="mailto:alan.liang@example.com" class="social-link">
      <i class="fas fa-envelope"></i>
    </a>
    <a href="https://www.linkedin.com/in/alanliangdev/" class="social-link">
      <i class="fab fa-linkedin"></i>
    </a>
    <a href="https://github.com/alanliangdev" class="social-link">
      <i class="fab fa-github"></i>
    </a>
  </div>
</div>

<div class="blog-grid">
"""

# Add each post to the home page in a card format
for post in latest_posts:
    home_page_content += f"""  <div class="blog-card">
    <a href="{post['url']}" class="blog-card-link">
      <div class="blog-card-image" style="background-image: url('{post['image']}')">
        <div class="blog-card-date">{post['display_date']}</div>
      </div>
      <div class="blog-card-content">
        <h2 class="blog-card-title">{post['title']}</h2>
        <p class="blog-card-description">{post['description']}</p>
      </div>
    </a>
  </div>
  
"""

home_page_content += """</div>

<div class="site-footer">
  &copy; 2024 Alan Liang. All rights reserved.
</div>"""

# Write the home page content to index.md
with open('docs/index.md', 'w', encoding='utf-8') as file:
    file.write(home_page_content)

print("Home page updated with the latest blog posts in card format!")