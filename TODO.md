# Blog folder cleanup

# Training Dynamics Manim animation

- [ ] Create a phone portrait layout with larger math, thicker trajectories, simultaneous network flow and staged derivation; export a high-quality MP4 and preview it at phone size.

- [x] Move reference superscript 2 onto “conservation law” and update the animation exports.

- [x] Add superscript reference markers for Neural Mechanics and Saxe et al., add compact citations, and verify the exports.

- [x] End the animation at displayed t=5 and loop immediately; verify the GIF and video exports.

- [x] Remove the green invariance equation, start fanning immediately, and run network forward passes concurrently; verify the revised exports.

- [x] Remove the saddle label and final expression emphasis, and verify the updated animation exports.

- [x] Revise the titles and identity-map setup; show the continuous-symmetry differentiation and its conservation derivation, then verify exports.

- [x] Remove trajectory highlighting and its readout, render legend text in LaTeX, and verify the updated exports.

- [x] Remove the subtitle, assumption footnotes and bottom narration; match network-caption fonts to LaTeX and re-export. Checked the poster and verified GIF dimensions, timing and infinite loop.

- [x] Revise the network to match the website, use a LaTeX implication heading, and render a darker mathematical-animation style. Checked network spacing, equation layout and exported GIF; revised loop is 21.96 seconds.

- [x] Build the three-panel Manim scene with trajectories on both sides of a=-b, the linear network, and symmetry/conservation equations.
- [x] Render a looping GIF and verify the layout and numerical conservation. Checked start, middle, endpoint and exported GIF frames; conservation drift below 8e-12.
- [x] Deliver the GIF, poster, MP4 and reproducible Manim source for the blog (1440×900, 19.71-second loop).

- [x] Consolidate blog posts, sources, and images under `blogs/`.
- [x] Update links and folder documentation.
- [x] Refresh the local deployment copy and check local links.

# Research calendar prototype

- [x] Inspect personal-site design and verified LSE/UCL listings.
- [x] Build a separate calendar prototype with filters, saved events, and export.
- [x] Verify the interface in the browser and present a local preview.

# Primer series navigation

- [x] Turn the primer series file into a styled page with its preamble and a link to Training Dynamics.
- [x] Link Writing and the blog index to the series, and add return navigation from Training Dynamics.
- [x] Refresh the deployment copy and verify navigation.

# Learning and physics comparison

- [x] Add matched equations and symbol explanations side by side.
- [x] Check notation and update the deployment copy.

# Objective-function notation

- [x] Define the dataset loss and its normalisation at the learning-problem introduction.
- [x] Use consistent loss notation throughout the notes and derivations.
- [x] Check the formulas and refresh the deployment page.

# Finite-step fact check

- [x] Re-derive exact recurrences, divergence, and curvature criteria.
- [x] Check the research attribution and correct overstatements.
- [x] Verify the revised section and refresh the deployment copy.

# Training Dynamics grammar pass

- [x] Review the full article and correct grammar while preserving its voice.
- [x] Check that equations, links, and structure are preserved.
- [x] Refresh the local deployment copy.

# Oxford Physics events

- [x] Add the published Oxford Physics seminars to the dashboard and source links to Markdown.
- [x] Verify event counts, dates, access notes and JavaScript syntax.

# Manual calendar events

- [x] Replace export button with an accessible event form and local persistence.
- [x] Verify date, duration, personal-calendar display and reload behavior. Verified form creation in browser and reload/edit/delete/overnight/DST behavior with automated checks.

# Recurring dashboard events

- [x] Add repeat options and an end-date picker while preserving the chosen time zone.
- [x] Verify repeat dates, month ends, persistence and individual occurrence editing.

# Quiet thoughts editor

- [x] Replace toolbar and split preview with a single formatted editor.
- [x] Preserve Markdown storage, nested bullets, image pasting and saved thoughts.
- [x] Verify typing, indentation, formatting and reload in the browser. Checked nested Tab/Shift-Tab, headings, highlights, saved notes, screenshot paste and image persistence.

# Google Analytics

- [x] Add measurement ID G-65WXKTLNBW to all 12 published content pages.
- [x] Refresh the corresponding deployment files and verify tag coverage, single initialization, and JavaScript syntax.

# Higher-resolution landscape animation

- [x] Preserve all equations and render at 2880 × 1800.
- [x] Export and visually verify the MP4, looping GIF and poster; confirm resolution, frame count and infinite looping.

# Ultra-high-resolution animation

- [x] Render the unchanged landscape animation at 5760 × 3600.
- [x] Export and verify the video, GIF and poster; 145 frames, 6.04 seconds, infinite GIF loop, and visually checked layout.

# Calendar database

- [x] Connect dashboard event creation, editing, saving and deletion to SQLite.
- [x] Import the eight screenshot events and migrate existing browser events on first connection.
- [x] Verify persistence, frontend rendering, concurrent changes and failure handling. Six database tests pass; browser creation, reload and failed-save form retention verified.
- [x] Install the local service and document startup and database backup. Login service installed; database-backed frontend displays all eight events.

# Cambridge event sources

- [x] Inspect Cambridge Computer Science and Engineering listings and feeds. Included the maintained replacement linked from Engineering list 6199.
- [x] Add Cambridge events and institution filtering with original source links. Imported 97 distinct listings into SQLite: 63 Computer Science and 34 Engineering.
- [x] Verify frontend rendering, saving and source coverage. Nine database tests pass; live Cambridge filter and official detail links verified. All 11 existing saved event records unchanged.

# Science of Deep Learning sources

- [x] Add linked footnotes for Rahimi’s talk and LeCun’s response.
- [x] Verify footnote anchors, backlinks and timestamp URLs; refresh the deployment copy.

# Deep Learning series names

- [x] Rename the Science and Math series across site titles, descriptions and citations.
- [x] Verify naming consistency and preserve existing URLs.

# Consistent site structure

- [x] Standardize article folders while retaining legacy redirects and public media paths.
- [x] Centralize series metadata and add an automatic static-site build.
- [x] Add navigation, fragment, image and download checks plus a generated sitemap.
- [x] Build, verify all pages and document the editing workflow.
