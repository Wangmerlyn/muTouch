# muTouch Project Page

Project page source for:

- Paper: `μTouch: Enabling Accurate, Lightweight Self-Touch Sensing with Passive Magnets`
- arXiv: https://arxiv.org/abs/2601.22864
- Code: https://github.com/Wangmerlyn/muTouch

## Deployment Target

This site is configured to be hosted at:

- `https://wangmerlyn.github.io/muTouch/`

Because this is a static site, deployment to GitHub Pages only requires publishing the repository contents (including `index.html` and `static/`) to the branch/folder configured for Pages.

## Project Structure

- `index.html`: main project page
- `static/css/index.css`: page styling
- `static/js/index.js`: page interactions (BibTeX copy, carousel, scroll-to-top)
- `static/images/mutouch_*`: paper figures used by the page
- `static/pdfs/mutouch.pdf`: local PDF mirror

## Local Preview

Any static server works, for example:

```bash
python3 -m http.server 8000
```

Or use the helper script (with port auto-check):

```bash
./scripts/preview.sh 18080
```

Then open `http://localhost:<port>`.

## Credits

This page is adapted from the Academic Project Page Template:
https://github.com/eliahuhorwitz/Academic-project-page-template
