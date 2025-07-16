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

# Function to extract excerpt from markdown files
def extract_excerpt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---', '', content, flags=re.DOTALL).strip()
    
    # Check for explicit excerpt marker
    excerpt_match = re.search(r'<!-- more -->', content)
    if excerpt_match:
        excerpt = content[:excerpt_match.start()].strip()
    else:
        # Take first paragraph
        paragraph_match = re.search(r'^# .*?\n\n(.*?)(\n\n|$)', content, re.DOTALL)
        if paragraph_match:
            excerpt = paragraph_match.group(1).strip()
        else:
            # Just take the first 200 characters
            excerpt = content[:200].strip() + '...'
    
    return excerpt

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
        
        # Get categories
        categories = frontmatter.get('categories', [])
        
        # Get post title
        with open(post_file, 'r', encoding='utf-8') as file:
            content = file.read()
            title_match = re.search(r'^# (.*?)$', content, flags=re.MULTILINE)
            title = title_match.group(1) if title_match else os.path.basename(post_file).replace('.md', '')
        
        # Get excerpt
        excerpt = extract_excerpt(post_file)
        
        # Get post URL
        post_url = 'blog/posts/' + os.path.basename(post_file).replace('.md', '/')
        
        blog_posts.append({
            'title': title,
            'date': date,
            'date_str': date.strftime('%B %d, %Y'),
            'categories': categories,
            'excerpt': excerpt,
            'url': post_url
        })

# Sort posts by date (newest first)
blog_posts.sort(key=lambda x: x['date'], reverse=True)

# Take the latest 3 posts
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

<div class="blog-posts">
"""

# Add each post to the home page
for post in latest_posts:
    home_page_content += f"""  <div class="blog-post">
    <h2 class="post-title"><a href="{post['url']}">{post['title']}</a></h2>
    <div class="post-meta">
      <span class="post-date">
        <i class="far fa-calendar-alt"></i> {post['date_str']}
      </span>
    </div>
    <div class="post-categories">
"""
    
    for category in post['categories']:
        category_url = f"blog/category/{category.lower().replace(' ', '-')}/"
        home_page_content += f'      <a href="{category_url}" class="post-category">{category}</a>\n'
    
    home_page_content += f"""    </div>
    <div class="post-excerpt">
      <p>{post['excerpt']}</p>
    </div>
    <a href="{post['url']}" class="read-more">
      Read more <i class="fas fa-arrow-right"></i>
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

print("Home page updated with the latest blog posts!")