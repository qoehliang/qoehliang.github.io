#!/usr/bin/env python3
import os
import re
import glob
from datetime import datetime
import yaml

print("Home page uses a custom template - no updates needed!")
print("Blog posts are automatically pulled from docs/blog/posts/ by the template.")

# List current blog posts
blog_posts = []
for post_file in glob.glob('docs/blog/posts/*.md'):
    with open(post_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
            if 'date' in frontmatter:
                title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else os.path.basename(post_file).replace('.md', '')
                blog_posts.append({
                    'title': title,
                    'date': frontmatter['date'],
                    'file': post_file
                })
        except yaml.YAMLError:
            pass

# Sort by date
blog_posts.sort(key=lambda x: x['date'], reverse=True)

print(f"\nFound {len(blog_posts)} blog posts:")
for post in blog_posts:
    print(f"  - {post['title']} ({post['date']})")

print("\nThe latest 3 posts will be displayed on the home page automatically.")