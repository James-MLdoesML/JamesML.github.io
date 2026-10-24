# Ming Liang Ang: personal site

A static website with no build step. Open `index.html` to preview it locally.

## Folder layout

- Root HTML files: Home, Research, Writing, Teaching, and About.
- `blogs/`: all blog posts, Markdown sources, post images, and downloadable resources. See [the blog guide](blogs/README.md).
- `assets/`: shared site styles, scripts, favicon, and profile image.
- `dist/`: ignored deployment copy, configured in `.openai/hosting.json`.
- `tmp/`: local working files.

Edit the source files above, then refresh `dist/` with the root HTML pages, `assets/`, and `blogs/` before publishing. Keep blog-specific files inside their post folder under `blogs/`.
