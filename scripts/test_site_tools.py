"""Regression checks for shared metadata and broken-link detection."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build
import check_links


class SiteToolsTest(unittest.TestCase):
    def test_catalog_updates_text_metadata_and_citation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            (root / "data/series.json").write_text(json.dumps({"science": {
                "title": "Science & learning", "description": 'A "quoted" description',
                "citation_label": "Updated series"}}))
            path = root / "index.html"
            path.write_text('<meta content="old" data-series="science" data-field="description">'
                            '<article aria-label="old" data-series="science" data-field="aria_label">'
                            '<h1 data-series="science" data-field="title">old</h1>'
                            '<code>note = {<span data-series="science" data-field="citation_label">old</span>}</code></article>')
            with patch.object(build, "ROOT", root):
                with self.assertRaises(SystemExit):
                    build.synchronize(check=True)
                build.synchronize()
                build.synchronize(check=True)
            self.assertIn('content="A &quot;quoted&quot; description"', path.read_text())
            self.assertIn('aria-label="Science &amp; learning"', path.read_text())
            self.assertIn('>Science &amp; learning</h1>', path.read_text())
            self.assertIn('>Updated series</span>', path.read_text())

    def test_links_directories_fragments_css_and_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "post").mkdir()
            (root / "post/index.html").write_text('<h1 id="intro">Post</h1>')
            page = root / "index.html"
            page.write_text('<a href="post/#intro">Post</a>')
            (root / "image.svg").write_text('<svg/>')
            (root / "site.css").write_text('body { background: url("image.svg"); }')
            with contextlib.redirect_stdout(io.StringIO()):
                check_links.check(root)
            page.write_text('<a href="post/#missing">Broken</a><img src="gone.png"><p id="x"></p><p id="x"></p>')
            with self.assertRaises(SystemExit) as failure:
                check_links.check(root)
            for message in ("missing fragment", "gone.png", "duplicate ID"):
                self.assertIn(message, str(failure.exception))


if __name__ == "__main__":
    unittest.main()
