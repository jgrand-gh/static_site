# Static Site Generator

This project is a simple static site generator written in Python. It converts Markdown files into HTML using custom parsing logic and templates, supporting basic Markdown features and inline formatting. The generated site can be served locally using Python's HTTP server.

## Features

- Converts Markdown files to HTML using a template
- Supports headings, paragraphs, code blocks, blockquotes, ordered and unordered lists
- Inline formatting: bold, italic, code, links, images
- Recursively processes content directories
- Copies static assets to the output directory

## Requirements

- Python 3.12 or newer

## Getting Started

1. **Clone the repository**
2. **Prepare your content:**
   - Place Markdown files in the `content/` directory.
   - Place static assets (CSS, images, etc.) in the `static/` directory.
   - Edit `template.html` to customize your site's layout.
3. **Build and Deploy:**
   - For **GitHub Pages deployment** (outputs to `docs/`):
     ```sh
     ./build.sh
     ```
     This will build the site for GitHub Pages, using `/static_site/` as the base path.
   - For **local deployment** (outputs to `public/`):
     ```sh
     ./main.sh
     ```
     This will build the site for local use and start a local server at [http://localhost:8888](http://localhost:8888).
   - Both scripts use `src/main.py` with arguments:
     - `build.sh` runs: `python3 src/main.py github "/static_site/"`
     - `main.sh` runs: `python3 src/main.py local`
   - You can also run `src/main.py` directly:
     ```sh
     python3 src/main.py [local|github] [basepath]
     ```
     - `local` outputs to `public/` (default basepath `/`)
     - `github` outputs to `docs/` (default basepath `/static_site/`)

   > **Note:** The `docs/` directory is used for GitHub Pages and the `public/` directory is for local deployment.

## Running Tests

Unit tests are provided in the `tests/` directory. Run all tests with:
```sh
./test.sh
```
Or manually:
```sh
python3 -m unittest discover -s tests
```

## Project Structure

- `src/main.py` — Main script for building the site
- `src/block_markdown.py` — Markdown block parsing and HTML conversion
- `src/inline_markdown.py` — Inline Markdown parsing (bold, italic, links, images, etc.)
- `src/htmlnode.py` — HTML node classes for building HTML trees
- `src/textnode.py` — Text node classes for inline formatting
- `content/` — Markdown source files
- `static/` — Static assets (CSS, images, etc.)
- `docs/` — Output directory for generated site (for GitHub Pages, must be included in repo for Github Pages)
- `public/` — Output directory for local deployment (excluded from git)
- `template.html` — HTML template for all pages
- `tests/` — Unit tests

## License

This project is for educational purposes as part of a Boot.dev learning module.