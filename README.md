# Fan Yuan Academic Homepage

The source for Fan Yuan's academic homepage: [leofyfan.github.io/fanyuan.github.io](https://leofyfan.github.io/fanyuan.github.io/).

## Development

Serve the site locally:

```bash
bundle exec jekyll serve
```

Build the production site:

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

Verify the generated site:

```bash
python3 scripts/verify_site.py _site
```
