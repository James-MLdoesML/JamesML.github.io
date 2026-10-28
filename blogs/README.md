# Blog posts and series

- [Science of Deep Learning](science-of-machine-learning-primer-series/) — preamble and taster list.
- [Math of Deep Learning](math-of-machine-learning-primer-series/) — mathematics series.
- [Training Dynamics](learning-dynamics/) — taster, with illustrations and public exports in `images/`, animation sources in `animations/`, and resources in `additional-resources/`.
- [Singular Learning Theory](singular-learning-theory/) — forthcoming taster.
- [The 4th step](the-fourth-step/) — essay and [Markdown source](the-fourth-step/the-fourth-step.md).
- [Towards a frontier-level scientific ecosystem in Singapore — Part I](frontier-scientific-ecosystem-singapore/) — essay.

Every article and series uses a dedicated folder with `index.html`. Keep its
images, sources and downloads together. Shared styles, scripts and favicon are
in `../assets/`. Series labels come from `../data/series.json`; run
`python3 scripts/build.py` from the root after editing them.

Clean URLs end in `/`. Legacy `.html` files preserve old links. See the
[editing guide](../docs/structure.md) for build and verification details.
