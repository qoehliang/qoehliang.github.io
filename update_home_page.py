#!/usr/bin/env python3
"""
Simple script to list blog posts.
The home page is now a static markdown file.
"""

import os
import glob
from datetime import datetime
import yaml
import re

def main():
    print("Blog posts found:")
    
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

    for i, post in enumerate(blog_posts, 1):
        print(f"  {i}. {post['title']} ({post['date']})")
    
    print(f"\nTotal: {len(blog_posts)} posts")
    print("The home page shows the latest 3 posts manually.")

if __name__ == "__main__":
    main()