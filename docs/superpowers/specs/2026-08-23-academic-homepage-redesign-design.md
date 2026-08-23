# Fan Yuan Academic Homepage Redesign

## Goal

Turn the untouched Academic Pages template into a concise, professional academic homepage for Fan Yuan, an Artificial Intelligence student at Zhejiang University from 2026 to 2029. The site should foreground research interests and two real publications, remove visible template content, and remain compatible with GitHub Pages.

## Audience and tone

The primary audience is researchers, prospective collaborators, and recruiters. Copy is in professional English, uses first person sparingly, and avoids unsupported claims beyond the user-provided education, interests, acceptance, and award information.

## Information architecture

The public site has two primary destinations:

1. `/` is the main academic profile. It contains a compact biography, research interests, and a selected-publications section.
2. `/publications/` lists the same two publications in a dedicated archive for direct linking.

The header exposes only `Home` and `Publications`. Template destinations for talks, teaching, portfolio, blog, CV, and guide are removed from navigation. Placeholder publication, talk, teaching, and blog records are removed so they cannot appear in generated archives or feeds.

## Profile content

The sidebar uses the supplied `profile.jpg` as the avatar and identifies the person as Fan Yuan. It states:

- Artificial Intelligence student at Zhejiang University, 2026–2029.
- Research interests: AI agents, OPD, large language models, and reinforcement learning.
- Location and employer are reduced to `Hangzhou, China` and `Zhejiang University`.
- GitHub links to `https://github.com/leofyfan`.
- Email links to `yuanfan7777777@gmail.com`, based on the public contact associated with the GSM8K-V project.

The main biography expands the abbreviations once and stays brief. It emphasizes intelligent agents, reasoning, multimodal language models, and reinforcement learning rather than adding unprovided biography details.

## Publications

Each publication is a responsive card with a locally stored, descriptive image, title, authors, venue/status, award or acceptance badge, a short one-sentence summary, and primary links.

### GSM8K-V

- Title: `GSM8K-V: Can Vision Language Models Solve Grade School Math Word Problems in Visual Contexts`
- Authors: Fan Yuan, Yuchen Yan, Yifan Jiang, Haoran Zhao, Tao Feng, Jinyan Chen, Yanwei Lou, Wenqi Zhang, Yongliang Shen, Weiming Lu, Jun Xiao, Yueting Zhuang
- Venue: `EMNLP 2026 Main Conference`
- Status: `Accepted`
- Links: arXiv, project repository, and dataset when available.
- Summary: presents a purely visual, multi-image benchmark for grade-school mathematical reasoning.
- Image: a real GSM8K-V project visual or paper figure copied into the repository, not a generic stock image.

### VidBot

- Title: `VidBot: Intelligent Video Learning Tool for Content Mining and Playback Traffic Statistics`
- Authors: Qinhua Xie, Weicong Liu, Fan Yuan, Jifan Shi, Ziyu Liu, Yanbing Zhang
- Venue: `2024 IEEE International Conference on Multimedia and Expo Workshops (ICMEW)`
- Award: `Best Demo Paper`
- Links: IEEE Xplore and DOI.
- Summary: describes an LLM-based video-learning system with content mining, knowledge organization, intelligent tutoring, and playback analytics.
- Image: a real image from the paper or its first page, stored locally.

## Visual design

The design keeps the familiar Academic Pages structure but removes template density. A warm off-white background, charcoal text, Zhejiang-inspired blue accents, generous whitespace, and restrained borders establish an academic rather than product-marketing tone. The avatar is square-cropped into a circle without modifying the source image. Publication cards use a fixed media column on desktop and stack on mobile.

No decorative animations, carousels, generated illustrations, or unrelated stock photography are added. Publication imagery has meaningful alternative text. Links and badges meet keyboard and contrast requirements.

## Implementation boundaries

- Jekyll configuration owns site identity, author details, URLs, and enabled collections.
- Markdown pages own biography and publication-card markup.
- Publication collection records own the dedicated archive data.
- A focused Sass partial owns the homepage and publication-card styling.
- Image files under `images/publications/` are static assets with stable paths.

No new JavaScript or runtime dependencies are introduced.

## Cleanup

Visible template copy, fake publications, sample talks, teaching records, portfolio content, demo blog posts, template-only navigation, placeholder social profiles, and dummy paper/PDF links are removed. Theme infrastructure remains because it is required for GitHub Pages generation.

## Verification

Verification consists of:

1. A content test that asserts the generated site contains Fan Yuan, Zhejiang University, both publication titles, EMNLP 2026, Best Demo Paper, the profile image, and no known template placeholders.
2. A Jekyll production build using the repository's existing dependencies.
3. Inspection of generated URLs and image references for missing files.
4. A responsive browser check at desktop and mobile widths after the build.

## Assumptions

- `OPD` is preserved exactly as provided because its intended expansion was not supplied.
- The user-provided EMNLP 2026 acceptance and Best Demo Paper statements are authoritative even when older public metadata has not yet caught up.
- The public GSM8K-V contact email and the GitHub username inferred from the supplied site URL are appropriate to display.
- Deployment remains through the repository's existing GitHub Pages workflow; no separate hosting provider is introduced.
