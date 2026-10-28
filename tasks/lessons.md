
- When moving site images, update and verify CSS `url(...)` references as well as HTML links and social image metadata. CSS paths resolve relative to the stylesheet.

- For mathematical analogies in these essays, prefer side-by-side LaTeX equations with matching colors and a compact key over large explanatory tables.

- For the training-dynamics toy model, introduce the input mean square as a fixed multiplicative factor, then absorb it into time or the learning rate below the calculation instead of imposing input normalisation in the setup.

- Check section nesting when fixing article alignment: a missing closing section can nest a .row inside another .row and apply desktop indentation twice.

- In the dashboard personal calendar, clicking an event opens editing; deletion belongs only to the eraser button, whose click must not bubble to the event card.

- Calendar persistence must be connected to the frontend's read and write paths. A standalone Markdown transcription does not update the dashboard; use the shared SQLite service for saved events.

- The dashboard thoughts editor should have one formatted writing surface with nested bullet guides, without a toolbar or split preview. Preserve Markdown and local images when simplifying the UI.

- For the Training Dynamics animation, match the website's three-node neural network with small arrowheads and proportional spacing. Prefer a dark mathematical-animation style and the LaTeX heading “Symmetries ⇒ conservation law”.

- Keep the Training Dynamics animation minimal: no subtitle, model-assumption footnotes, gradient-flow footnote or bottom narration. Use LaTeX fonts for network captions and text below the network.

- Use LaTeX for the phase-portrait legend too, and do not single out a highlighted trajectory or show its imbalance readout.

- Introduce the animation as a simple neural network learning the identity map, label it a two-layer, two-neuron linear network, and explicitly differentiate the continuous rescaling symmetry at lambda=1 before deriving conservation, following the blog.

- Omit the “saddle” text label and end-of-animation expression highlighting from the Training Dynamics GIF; keep the equations still while the endpoint is displayed.

- Start phase-portrait fanning immediately and animate repeated network forward passes concurrently, without an introductory pause. Omit the standalone green loss-invariance expression.

- Loop the Training Dynamics animation as soon as displayed training time reaches t=5, with no final hold or fade-out.

- Place reference superscript 1 on “Symmetries” and reference superscript 2 on “conservation law”, not on the neural-network heading.

- For the landscape Training Dynamics animation, preserve all equations and layout; the latest request is only to increase export resolution.

- On the Writing page, use a small “Preface” label above each of the two introductory pieces rather than a standalone section heading.

- Writing-page prefaces use a black “Preface” section heading, gray “Preface Part I” and “Preface Part II” labels, and tight label-to-title spacing.

- Keep preface labels close to titles, but use the Primer Series article spacing (1.9rem above subsequent entries) between preface articles.

- When renaming the deep-learning series, update repeated category labels and taglines on Writing, the blog index and each series page; these static HTML pages do not share content automatically.
