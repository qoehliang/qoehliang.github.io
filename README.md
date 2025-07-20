# Alan Liang's Personal Website

This is my personal website built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and hosted on GitHub Pages.

## Features

- Responsive design that works on all devices
- Dark/light mode toggle
- Blog with categories and tags
- Custom styling with CSS
- Optimized for performance

## Local Development

To run the site locally:

1. Install MkDocs and required plugins:
   ```bash
   pip install mkdocs-material mkdocs-blog-plugin
   ```

2. Start the development server:
   ```bash
   mkdocs serve
   ```

3. Open your browser to http://localhost:8000

## Project Structure

```
.
├── docs/                     # Documentation source files
│   ├── assets/               # Static assets (images, JS, etc.)
│   │   ├── images/           # Image files
│   │   │   ├── blog/         # Blog post images
│   │   │   └── ...
│   │   ├── js/               # JavaScript files
│   │   └── ...
│   ├── blog/                 # Blog posts
│   │   ├── posts/            # Individual blog posts
│   │   ├── .authors.yml      # Blog author information
│   │   └── index.md          # Blog landing page
│   ├── overrides/            # Theme overrides
│   │   └── main.html         # Main template override
│   ├── stylesheets/          # CSS stylesheets
│   │   └── custom.css        # Custom styles
│   ├── about.md              # About page
│   ├── index.md              # Home page
│   └── 404.md                # 404 page
├── .github/                  # GitHub configuration
│   └── workflows/            # GitHub Actions workflows
│       └── deploy-mkdocs.yml # Deployment workflow
├── mkdocs.yml                # MkDocs configuration
└── README.md                 # This file
```

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch using GitHub Actions.

## Customization

- Edit `mkdocs.yml` to change site configuration
- Modify `docs/stylesheets/custom.css` for custom styling
- Update content in the `docs/` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.