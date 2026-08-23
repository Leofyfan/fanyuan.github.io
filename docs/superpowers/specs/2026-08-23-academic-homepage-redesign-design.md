# Fan Yuan Academic Homepage Redesign

## Goal

Turn the untouched Academic Pages template into a concise, professional academic homepage for Fan Yuan, an Artificial Intelligence student at Zhejiang University from 2026 to 2029. The site should foreground research interests and two real publications, remove visible template content, and remain compatible with GitHub Pages.

## Audience and tone

The primary audience is researchers, prospective collaborators, and recruiters. Copy is in professional English, uses first person sparingly, and avoids unsupported claims beyond the user-provided education, interests, acceptance, and award information.

## Information architecture

The public site has exactly two primary HTML destinations:

1. `/` is the main academic profile. It contains a compact biography, research interests, and a selected-publications section.
2. `/publications/` lists the same two publications in a dedicated archive for direct linking.

The header exposes only `Home` and `Publications`. Template destinations for talks, teaching, portfolio, blog, CV, guide, terms, category/tag/year/page archives, talk maps, collection archives, and Markdown examples are deleted or unpublished so they do not remain reachable directly or appear in the sitemap. The site retains only the home page, publications page, English 404 page, sitemap, and feed files. Unused teaching, portfolio, and talks collections are disabled. The publications collection remains available as structured input for the archive but does not emit individual paper pages.

## Profile content

The sidebar uses the supplied `profile.jpg` as the avatar and identifies the person as Fan Yuan. It states:

- Artificial Intelligence student at Zhejiang University, 2026–2029.
- Research interests: AI agents, OPD, large language models, and reinforcement learning.
- Location and employer are reduced to `Hangzhou, China` and `Zhejiang University`.
- GitHub links to `https://github.com/leofyfan`.
- Email links to `yuanfan7777777@gmail.com`, based on the public contact associated with the GSM8K-V project.

The main biography expands known abbreviations once and stays brief; `OPD` remains unchanged until an expansion is supplied. It emphasizes intelligent agents, reasoning, multimodal language models, and reinforcement learning rather than adding unprovided biography details.

## Publications

Each publication is a responsive card with a locally stored, descriptive image, title, authors, venue/status, award or acceptance badge, a short one-sentence summary, and primary links.

### GSM8K-V

- Title: `GSM8K-V: Can Vision Language Models Solve Grade School Math Word Problems in Visual Contexts`
- Authors: Fan Yuan, Yuchen Yan, Yifan Jiang, Haoran Zhao, Tao Feng, Jinyan Chen, Yanwei Lou, Wenqi Zhang, Yongliang Shen, Weiming Lu, Jun Xiao, Yueting Zhuang
- Venue: `EMNLP 2026 Main Conference`
- Status: `Accepted`
- Links: arXiv at `https://arxiv.org/abs/2509.25160`, repository at `https://github.com/ZJU-REAL/GSM8K-V`, and dataset links discovered from that repository.
- Summary: presents a purely visual, multi-image benchmark for grade-school mathematical reasoning.
- Image: a real GSM8K-V project visual or paper figure copied into the repository, not a generic stock image.

### VidBot

- Title: `VidBot: Intelligent Video Learning Tool for Content Mining and Playback Traffic Statistics`
- Authors: Qinhua Xie, Weicong Liu, Fan Yuan, Jifan Shi, Ziyu Liu, Yanbing Zhang
- Venue: `2024 IEEE International Conference on Multimedia and Expo Workshops (ICMEW)`
- Award: `Best Demo Paper`
- Links: IEEE Xplore and DOI at `https://doi.org/10.1109/ICMEW63481.2024.10645449`.
- Summary: describes an LLM-based video-learning system with content mining, knowledge organization, intelligent tutoring, and playback analytics.
- Image: a real image from the paper or its first page, stored locally.

## Visual design

The design keeps the familiar Academic Pages structure but removes template density. A warm off-white background, charcoal text, Zhejiang-inspired blue accents, generous whitespace, and restrained borders establish an academic rather than product-marketing tone. The avatar is square-cropped into a circle without modifying the source image. Publication cards use a fixed media column on desktop and stack on mobile.

No decorative animations, carousels, generated illustrations, or unrelated stock photography are added. Publication imagery has meaningful English alternative text. Links, focus states, and badges meet keyboard and contrast requirements.

## Implementation boundaries

- Jekyll configuration owns site identity, author details, URLs, and enabled collections.
- Markdown pages own biography and publication-card markup.
- Publication collection records own the dedicated archive data.
- A focused Sass partial owns the homepage and publication-card styling.
- The supplied `../profile.jpg` is copied to `images/profile.jpg` so GitHub Pages can serve it deterministically.
- Image files under `images/publications/` are static assets with stable paths. Each records its source URL and provenance in the implementation plan and uses a project- or paper-owned visual. A link or image that cannot be sourced is omitted instead of replaced with a placeholder.

No new JavaScript or runtime dependencies are introduced.

## Cleanup

Visible template copy, fake publications, sample talks, teaching records, portfolio content, demo blog posts, template-only navigation, placeholder social profiles, dummy paper/PDF links, and publishable demo routes are removed. Theme infrastructure and untranslated source-only strings that are never rendered may remain because they are required for GitHub Pages generation.

All rendered public-facing content is English: biography copy, navigation, headings, badges, buttons, link labels, image alternative text, ARIA labels, 404 page, footer, SEO/Open Graph metadata, and feed/sitemap labels. The site keeps `locale: en-US`.

## Verification

Verification consists of:

1. A content test that asserts the generated site contains Fan Yuan, Zhejiang University, both publication titles, EMNLP 2026, Best Demo Paper, the profile image, and no known template placeholders.
2. A Jekyll production build using the repository's existing dependencies.
3. Inspection of generated HTML and XML verifies that every rendered public-facing string is English and that only the allowed HTML routes are generated.
4. Automated checks verify that all internal links and image references resolve to generated or source files.
5. A responsive browser check verifies keyboard focus, readable contrast, and no horizontal overflow at desktop and mobile widths.

## Assumptions

- `OPD` is preserved exactly as provided because its intended expansion was not supplied.
- The user-provided EMNLP 2026 acceptance and Best Demo Paper statements are authoritative even when older public metadata has not yet caught up.
- The public GSM8K-V contact email and the GitHub username inferred from the supplied site URL are appropriate to display.
- Deployment remains through the repository's existing GitHub Pages workflow; no separate hosting provider is introduced.
