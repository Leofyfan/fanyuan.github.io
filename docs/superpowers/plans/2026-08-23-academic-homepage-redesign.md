# Fan Yuan Academic Homepage Redesign Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Academic Pages demo content with a concise English academic homepage for Fan Yuan, including a supplied profile image and image-backed cards for two real publications.

**Architecture:** Keep the existing Jekyll/Academic Pages build and GitHub Pages deployment. Store publication metadata in the `publications` collection, render it through one reusable Liquid include on the home and publications pages, and isolate the new visual treatment in one Sass partial. A dependency-free Python verifier checks the generated site as the acceptance-test boundary.

**Tech Stack:** Jekyll, Liquid, Markdown, Sass, Python 3 standard library, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-08-23-academic-homepage-redesign-design.md`

---

## File map

- `scripts/verify_site.py`: generated-site acceptance checks only.
- `_config.yml`: site identity, author details, URL/base path, collection output, exclusions, and SEO defaults.
- `_data/navigation.yml`: two-item English navigation.
- `_pages/about.md`: English biography, interests, and selected-publications loop.
- `_pages/publications.html`: dedicated English publication archive using the same card include.
- `_pages/404.md`: concise English error page.
- `_includes/publication-card.html`: one publication-card rendering unit.
- `_includes/footer.html`: minimal English footer.
- `_publications/2026-gsm8k-v.md`: GSM8K-V metadata.
- `_publications/2024-vidbot.md`: VidBot metadata.
- `_sass/layout/_academic-home.scss`: homepage, sidebar, publication-card, focus, and responsive styles.
- `assets/css/main.scss`: imports the new Sass partial.
- `images/profile.jpg`: user-supplied avatar copied into the served tree.
- `images/publications/gsm8k-v.png`: project-owned GSM8K-V introductory figure.
- `images/publications/vidbot.png`: rendered first page of the official VidBot paper.
- `images/publications/SOURCES.md`: asset provenance; excluded from the public Jekyll build.
- Template demo records/pages: deleted so they cannot generate public routes or feed entries.

## Chunk 1: Acceptance boundary and content model

### Task 1: Add a failing generated-site acceptance test

**Files:**
- Create: `scripts/verify_site.py`

- [ ] **Step 1: Implement the verifier before changing site content**

  The script must accept `_site` as an optional argument and fail with one collected report when any check fails. It must:

  - require `/`, `/publications/`, and `/404.html` and reject any other generated HTML route;
  - require both `/` and `/publications/` to contain exactly two publication cards and exactly one copy of each paper title;
  - require `Fan Yuan`, `Zhejiang University`, `EMNLP 2026 Main Conference`, `Best Demo Paper`, `/images/profile.jpg`, and both publication-image paths;
  - require the exact GitHub, email, arXiv, GSM8K-V repository/project/dataset, IEEE Xplore, and DOI links;
  - reject known demo strings including `Your Name`, `Red Brick University`, `Paper Title Number`, `GitHub Journal of Bugs`, `Teaching`, `Portfolio`, `Blog Posts`, and `Guide`;
  - reject CJK characters in generated `.html` and `.xml` files;
  - parse local `href` and `src` values with `html.parser.HTMLParser`, strip the configured `/fanyuan.github.io` base path, and require target files to exist under `_site`;
  - reject empty image alternative text;
  - print `Site verification passed.` and exit zero only when all checks pass.

- [ ] **Step 2: Build the untouched site**

  Run: `bundle exec jekyll build`

  Expected: the command succeeds and produces `_site`, or dependency setup is performed with the repository's existing Gemfile before rerunning.

- [ ] **Step 3: Run the verifier and confirm RED**

  Run: `python3 scripts/verify_site.py _site`

  Expected: FAIL listing missing real content and existing template/demo routes or strings.

- [ ] **Step 4: Commit the test boundary**

  Run:

  ```bash
  git add scripts/verify_site.py
  git commit -m "test: define academic homepage acceptance"
  ```

### Task 2: Replace site identity and public routing

**Files:**
- Modify: `_config.yml`
- Modify: `_data/navigation.yml`
- Modify: `_includes/masthead.html`
- Modify: `_includes/footer.html`
- Modify: `_pages/about.md`
- Modify: `_pages/404.md`
- Delete: `_pages/archive-layout-with-content.md`
- Delete: `_pages/category-archive.html`
- Delete: `_pages/collection-archive.html`
- Delete: `_pages/cv-json.md`
- Delete: `_pages/cv.md`
- Delete: `_pages/markdown.md`
- Delete: `_pages/non-menu-page.md`
- Delete: `_pages/page-archive.html`
- Delete: `_pages/portfolio.html`
- Delete: `_pages/sitemap.md`
- Delete: `_pages/tag-archive.html`
- Delete: `_pages/talkmap.html`
- Delete: `_pages/talks.html`
- Delete: `_pages/teaching.html`
- Delete: `_pages/terms.md`
- Delete: `_pages/year-archive.html`

- [ ] **Step 1: Configure the real site identity**

  Set `title`, `name`, and author name to `Fan Yuan`; use a concise English description; set `url` to `https://leofyfan.github.io`, `baseurl` to `/fanyuan.github.io`, and `repository` to `leofyfan/fanyuan.github.io`. Set the avatar to `profile.jpg`, bio to `AI student at Zhejiang University (2026–2029).`, location to `Hangzhou, China`, employer to `Zhejiang University`, email to `yuanfan7777777@gmail.com`, and GitHub to `leofyfan`. Remove every placeholder academic/social profile.

- [ ] **Step 2: Limit generated collections and build inputs**

  Keep only `publications` as a custom collection with `output: false`. Remove teaching, portfolio, and talks collection defaults. Disable comments, related content, sharing, and feed-follow display for the remaining pages. Add `docs`, `scripts`, `README.md`, `CONTRIBUTING.md`, `markdown_generator`, `_drafts`, and `images/publications/SOURCES.md` to `exclude`.

  Also exclude `_posts`, `_talks`, `_teaching`, and `talkmap` immediately so their remaining files cannot produce or copy public HTML before final source cleanup.

- [ ] **Step 3: Reduce navigation and footer**

  Change the masthead's site-title link label to `Home`, put only `Publications` in `_data/navigation.yml`, and keep both links exactly once. Replace the template attribution block with `© {{ site.time | date: '%Y' }} Fan Yuan.` plus GitHub and email links with English accessible labels.

- [ ] **Step 4: Remove publishable demo pages and redirects, and keep the 404 page English**

  Delete the listed demo pages, remove the `/about/` and `/about.html` redirects from `_pages/about.md`, and keep `_pages/404.md` at `/404.html` with a short English message and a `Back to home` link.

- [ ] **Step 5: Rebuild and observe that the verifier still fails only on content/assets**

  Run: `bundle exec jekyll build && python3 scripts/verify_site.py _site`

  Expected: FAIL because the real biography, publication cards, and publication assets do not exist yet; template-route failures are gone.

- [ ] **Step 6: Commit identity and routing**

  Run:

  ```bash
  git add _config.yml _data/navigation.yml _includes/masthead.html _includes/footer.html _pages/about.md _pages/404.md _pages/archive-layout-with-content.md _pages/category-archive.html _pages/collection-archive.html _pages/cv-json.md _pages/cv.md _pages/markdown.md _pages/non-menu-page.md _pages/page-archive.html _pages/portfolio.html _pages/sitemap.md _pages/tag-archive.html _pages/talkmap.html _pages/talks.html _pages/teaching.html _pages/terms.md _pages/year-archive.html
  git commit -m "feat: establish Fan Yuan site identity"
  ```

### Task 3: Add real publication records and reusable rendering

**Files:**
- Create: `_includes/publication-card.html`
- Create: `_publications/2026-gsm8k-v.md`
- Create: `_publications/2024-vidbot.md`
- Modify: `_pages/about.md`
- Modify: `_pages/publications.html`
- Delete: `_publications/2009-10-01-paper-title-number-1.md`
- Delete: `_publications/2010-10-01-paper-title-number-2.md`
- Delete: `_publications/2015-10-01-paper-title-number-3.md`
- Delete: `_publications/2024-02-17-paper-title-number-4.md`
- Delete: `_publications/2025-06-08-paper-title-number-5.md`

- [ ] **Step 1: Add the two publication records**

  Use front matter fields `title`, `date`, `venue`, `status`, `award`, `authors`, `summary`, `image`, `image_alt`, and a `links` array. GSM8K-V links are arXiv, GitHub, project page, and Hugging Face dataset. VidBot links are IEEE Xplore and DOI. Mark Fan Yuan in the author string using a separate `highlight_author` field rather than embedding HTML in YAML.

- [ ] **Step 2: Create the publication-card include**

  Render a semantic `<article>` with a linked image, English badge/status line, title, authors, venue, summary, and link list. Use `relative_url` for local assets, `target="_blank"` with `rel="noopener noreferrer"` for external links, descriptive alt text, and no link when a field is absent.

- [ ] **Step 3: Rewrite the home page in English**

  Keep permalink `/` and the author profile. Add `About Me`, a two-paragraph biography, `Research Interests` chips for `AI Agents`, `OPD`, `Large Language Models`, and `Reinforcement Learning`, plus `Selected Publications`. The biography may mention multimodal reasoning in connection with the published work. Sort `site.publications` by date in reverse and include the card for each item.

- [ ] **Step 4: Rewrite the publications archive in English**

  Keep permalink `/publications/`, use the same sort/include logic, and avoid duplicate publication markup.

- [ ] **Step 5: Remove demo publication records**

  Delete all five template records so fake titles and dummy URLs cannot appear anywhere.

- [ ] **Step 6: Rebuild and confirm that failures are now asset/style related**

  Run: `bundle exec jekyll build && python3 scripts/verify_site.py _site`

  Expected: FAIL only for missing profile/publication image files until Chunk 2.

- [ ] **Step 7: Commit the content model**

  Run:

  ```bash
  git add _includes/publication-card.html _pages/about.md _pages/publications.html _publications
  git commit -m "feat: add academic profile and publications"
  ```

## Chunk 2: Assets, styling, cleanup, and verification

### Task 4: Add deterministic profile and publication imagery

**Files:**
- Create: `images/profile.jpg`
- Create: `images/publications/gsm8k-v.png`
- Create: `images/publications/vidbot.png`
- Create: `images/publications/SOURCES.md`

- [ ] **Step 1: Copy the supplied profile image**

  Copy `/Users/leofyfan/Desktop/zju/homepage/profile.jpg` to `images/profile.jpg` without recompression.

- [ ] **Step 2: Source the GSM8K-V project visual**

  Download the project-owned introductory figure from `https://raw.githubusercontent.com/ZJU-REAL/GSM8K-V/main/assets/intro.png`, store it as `images/publications/gsm8k-v.png`, and visually verify that its embedded labels are English.

- [ ] **Step 3: Render the VidBot paper's first page**

  Obtain the official VidBot PDF from IEEE Xplore using the paper record `https://ieeexplore.ieee.org/document/10645449` and its publisher PDF path `https://ieeexplore.ieee.org/iel8/10645349/10645352/10645449.pdf`. Render page 1 as `images/publications/vidbot.png`, crop only outer page whitespace when needed, and do not substitute generic video-learning imagery. Visually confirm that the rendered page and all embedded labels are English.

- [ ] **Step 4: Validate files and record provenance**

  Use `file` and image-dimension inspection to confirm both publication assets are genuine, decodable PNG files rather than renamed formats. In `images/publications/SOURCES.md`, record each filename, exact source URL, capture/download date, page/figure selection, and that the profile image was user supplied.

- [ ] **Step 5: Run the verifier**

  Run: `bundle exec jekyll build && python3 scripts/verify_site.py _site`

  Expected: PASS for route, content, language, link, and image-file checks before visual polish.

- [ ] **Step 6: Commit the assets**

  Run:

  ```bash
  git add images/profile.jpg images/publications
  git commit -m "feat: add profile and publication imagery"
  ```

### Task 5: Apply the academic visual system

**Files:**
- Create: `_sass/layout/_academic-home.scss`
- Modify: `assets/css/main.scss`

- [ ] **Step 1: Add scoped academic-page styles**

  Style the page background, measure, typography, section spacing, interest chips, publication cards, badges, image crop, link pills, avatar crop, and minimal footer. Use existing theme variables where possible and a single blue accent. Do not add animation beyond existing theme behavior.

- [ ] **Step 2: Add responsive and accessibility states**

  Use a two-column media/content publication card from the large breakpoint upward and one column below it. Ensure images use `object-fit: cover`, long paper titles/URLs wrap, `:focus-visible` is obvious, and no component forces horizontal overflow at 320px.

- [ ] **Step 3: Import the partial**

  Add `layout/academic-home` after existing layout imports in `assets/css/main.scss` so the focused overrides win without editing unrelated theme files.

- [ ] **Step 4: Rebuild and rerun acceptance tests**

  Run: `JEKYLL_ENV=production bundle exec jekyll build && python3 scripts/verify_site.py _site`

  Expected: `Site verification passed.`

- [ ] **Step 5: Keep the visual changes ready for browser QA**

  Do not commit until Task 6 browser QA and any remediation are complete. Keep changes limited to the new partial and its import.

### Task 6: Remove remaining template records and complete browser QA

**Files:**
- Delete: `_posts/2012-08-14-blog-post-1.md`
- Delete: `_posts/2013-08-14-blog-post-2.md`
- Delete: `_posts/2014-08-14-blog-post-3.md`
- Delete: `_posts/2015-08-14-blog-post-4.md`
- Delete: `_posts/2199-01-01-future-post.md`
- Delete: `_talks/2012-03-01-talk-1.md`
- Delete: `_talks/2013-03-01-tutorial-1.md`
- Delete: `_talks/2014-02-01-talk-2.md`
- Delete: `_talks/2014-03-01-talk-3.md`
- Delete: `_teaching/2014-spring-teaching-1.md`
- Delete: `_teaching/2015-spring-teaching-2.md`
- Delete: `_portfolio/portfolio-1.md`
- Delete: `_portfolio/portfolio-2.html`
- Modify: `README.md`
- Modify if QA requires: `_sass/layout/_academic-home.scss`
- Modify if QA requires: `_includes/publication-card.html`
- Modify if QA requires: `_pages/about.md`
- Modify if QA requires: `_pages/publications.html`

- [ ] **Step 1: Delete remaining sample records**

  Remove all listed blog, talk, teaching, and portfolio examples. Preserve theme implementation files that are not public content.

- [ ] **Step 2: Replace the template README**

  Write a short English README naming the site, its public URL, local `bundle exec jekyll serve` command, production build command, and `python3 scripts/verify_site.py _site` verification command.

- [ ] **Step 3: Run a pre-QA production verification**

  Run:

  ```bash
  JEKYLL_ENV=production bundle exec jekyll build
  python3 scripts/verify_site.py _site
  git status --short
  ```

  Expected: build succeeds, verifier prints `Site verification passed.`, and status lists only intentional visual, cleanup, and README changes.

- [ ] **Step 4: Perform explicit desktop browser QA**

  Serve the built site at its configured base path and test both `/fanyuan.github.io/` and `/fanyuan.github.io/publications/` at 1440px width. Verify the supplied avatar and both publication images render, text is English, every internal and external link targets the intended destination, and no template content remains. Keyboard-tab through every interactive element in order and require a visible focus indicator. Calculate foreground/background contrast for body text, secondary text, badges, links, and focus indicators and require WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text and UI indicators). Record each route/viewport as PASS in the task notes.

- [ ] **Step 5: Perform explicit mobile browser QA**

  Test both routes at 390px and 320px widths. Verify the sidebar stacks cleanly, publication cards are one column, long titles/authors/URLs wrap, tap targets remain usable, and `document.documentElement.scrollWidth <= window.innerWidth`. Keyboard-tab through every interactive element at 390px and require the mobile menu, links, and theme toggle to expose visible focus. Record each route/viewport as PASS.

- [ ] **Step 6: Fix QA failures and reverify**

  Fix any browser issue only in the files listed for QA remediation. Rebuild and repeat the failed route/viewport checks until all desktop/mobile, keyboard, overflow, and contrast checks pass. Then run:

  ```bash
  JEKYLL_ENV=production bundle exec jekyll build
  python3 scripts/verify_site.py _site
  ```

  Expected: production build succeeds, `Site verification passed.`, and every QA matrix entry is PASS after the final code change.

- [ ] **Step 7: Commit visual system, cleanup, and README**

  Run:

  ```bash
  git add README.md _posts _talks _teaching _portfolio _sass/layout/_academic-home.scss assets/css/main.scss _includes/publication-card.html _pages/about.md _pages/publications.html
  git commit -m "style: finish concise academic homepage"
  ```

- [ ] **Step 8: Verify the final commit state**

  Run: `git status --short && git log -7 --oneline`

  Expected: clean status and a focused sequence of spec, test, content, asset, style, and cleanup commits.
