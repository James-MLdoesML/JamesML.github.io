# Ming Liang Ang: personal site

A static website with directly previewable HTML and a small Python build tool.

- Root HTML files: Home, Writing, Research, Teaching and About.
- `blogs/<name>/index.html`: each article or series, alongside its media and resources.
- `assets/`: shared styles, scripts and images.
- `data/series.json`: repeated series names, taglines and categories.
- `scripts/`: build and link checks; `docs/`: conventions and project notes.
- `dist/`: generated deployment output; `tmp/`: temporary work. Both are ignored.

After editing content or shared series metadata, run:

```sh
python3 scripts/build.py
```

This updates shared labels, generates the sitemap and builds a verified public
copy in `dist/`. Source HTML still works with GitHub Pages and direct local
previews. Existing public URLs and legacy redirects are retained.

See [the structure and editing guide](docs/structure.md) and [blog guide](blogs/README.md).
