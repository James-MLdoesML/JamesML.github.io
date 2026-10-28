# Site structure and editing

The HTML pages remain directly viewable in a browser. No framework or dependency
installation is needed; the build uses Python's standard library.

```text
index.html, writing.html, research.html, teaching.html, about.html
assets/                         shared styles, scripts and images
data/series.json                 shared series names and descriptions
blogs/
  index.html                    blog listing
  <article>/
    index.html                  article or series landing page
    images/                     illustrations and existing public exports
    animations/                 optional animation sources
    additional-resources/       optional downloads, data and sources
  <legacy-name>.html            compatibility redirects only
scripts/                        build, link checker and regression tests
docs/                           site conventions and open loops
tasks/lessons.md, TODO.md        repository workflow records
sitemap.xml                     generated canonical public page list
dist/                           generated deployment output; ignored by Git
tmp/                            disposable build work; ignored by Git
```

## Edit and build

Edit article prose in `blogs/<article>/index.html`. Edit repeated series titles,
taglines and categories in `data/series.json`, then run:

```sh
python3 scripts/build.py
```

The build refreshes elements marked with `data-series` and `data-field`, generates
`sitemap.xml`, checks links and stages public files in `dist/`. Open source pages
directly to preview locally, or run `python3 -m http.server --directory dist 8000`.
Commit updated HTML, catalog and sitemap together. Secondary page titles,
metadata descriptions and citation labels are derived from each series title.
GitHub Actions runs the same checks on pushes and pull requests. Root HTML continues to work
with GitHub Pages branch deployment; Sites continues to use `dist/`.

Do not hand-edit `dist/`. Check metadata freshness without writing files with
`python3 scripts/build.py --check`.

## Compatibility

Each article uses a folder URL ending in `/`. Add `data-local-index` to links to
article folders for direct `file://` previews. Legacy `.html` redirects retain
query strings and fragments. Existing machine-learning slugs remain unchanged
even though display titles now say Deep Learning.

Math now lives in `blogs/math-of-machine-learning-primer-series/index.html`;
the old `.html` URL redirects there. The old `#series-primers` fragment on the
Science page remains as a compatibility anchor.

Existing animation exports stay under `learning-dynamics/images/` to preserve
published download URLs. These are intentional master, phone and social variants.
For a new article, put new share-only files in its `exports/` folder; the build
includes tracked public media there. CSS image paths resolve relative to the
stylesheet, not the article.

## Public files

The deployment copy includes public HTML, assets, and tracked blog images,
videos, PDFs, notebooks, ZIPs and data files. It excludes Python sources,
documentation, caches, personal notes and ignored files. The unreleased Odysea
tutorial and its notebook/archive remain excluded. GitHub branch deployments
still serve tracked repository files, so unpublished files must stay ignored.

Add an intended public download to Git before building so it can be included.
Keep the personal calendar transcription out of the repository.

## Verification

```sh
python3 scripts/test_site_tools.py
python3 scripts/build.py
python3 scripts/check_links.py dist
```

Checks cover navigation, file paths, fragments, accessibility references,
duplicate IDs, CSS image paths and sitemap entries. External website availability
is not checked. Preview browser interactions after changing their markup or code.
