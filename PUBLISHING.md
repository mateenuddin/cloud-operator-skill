# Publishing this repo to GitHub

Step-by-step to take this folder, push it to GitHub as a public repo, and have the docs site auto-build at `https://YOUR-USERNAME.github.io/cloud-operator-skill/`.

You'll do these steps yourself — for safety, I cannot create accounts or push to your GitHub on your behalf.

---

## Prerequisites

- A GitHub account (free is fine; public repos are unlimited).
- `git` installed locally.
- Either the `gh` CLI ([install guide](https://cli.github.com)) **or** the GitHub web UI for repo creation. The `gh` CLI path is faster.

## Step 1 — Customize the placeholders

Two files reference `YOUR-USERNAME`. Replace it everywhere with your actual GitHub username:

```bash
# From the repo root
USERNAME="your-github-username"
grep -rl "YOUR-USERNAME" . --include="*.md" --include="*.yml" \
  | xargs sed -i.bak "s/YOUR-USERNAME/$USERNAME/g"
find . -name "*.bak" -delete
```

Files affected: `README.md`, `mkdocs.yml`, `docs/index.md`, `CONTRIBUTING.md`, and a few links inside the docs.

(On macOS replace `sed -i.bak` with `sed -i ''` if you don't want backup files.)

## Step 2 — Initialize git and commit

```bash
git init
git add .
git commit -m "Initial commit: cloud-operator skill v2 + docs"
git branch -M main
```

## Step 3 — Create the GitHub repo and push

### Option A — `gh` CLI (one command)

```bash
gh repo create cloud-operator-skill \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Multi-cloud operator agent skill for AWS, GCP, and Azure"
```

That's it — repo created, code pushed.

### Option B — GitHub web UI

1. Go to https://github.com/new
2. Name: `cloud-operator-skill`
3. Visibility: Public
4. **Do not** initialize with a README, .gitignore, or license — you already have those.
5. Click **Create repository**.
6. Back in your terminal:

```bash
git remote add origin https://github.com/YOUR-USERNAME/cloud-operator-skill.git
git push -u origin main
```

## Step 4 — Enable GitHub Pages

GitHub Pages serves the docs site. The included workflow at `.github/workflows/docs.yml` builds and deploys automatically on every push to `main`.

1. In the repo on GitHub, go to **Settings → Pages**.
2. Under **Source**, select **GitHub Actions**.
3. Save.

The first deploy will start automatically (because you just pushed). Watch progress at the **Actions** tab. After ~1 minute, your docs site will be live at:

```
https://YOUR-USERNAME.github.io/cloud-operator-skill/
```

## Step 5 — Verify

Open the site URL and check:

- [ ] Home page loads with the dark/light theme toggle
- [ ] Navigation tabs at the top work (Getting Started, The Skill, Reference Catalog, Guides, Eval Results)
- [ ] Search box at the top right (or press `/`) returns hits for "spot interrupt", "n2-standard", "savings plan"
- [ ] Mindmap page renders the diagram
- [ ] Code blocks have a copy button on hover

If something's off, the most common cause is a placeholder that didn't get replaced. `grep -r "YOUR-USERNAME"` to find any leftovers.

## Step 6 — Add the standard repo niceties (optional but recommended)

```bash
# Issue templates
mkdir -p .github/ISSUE_TEMPLATE
# (You can copy templates from any well-maintained open-source repo, or use GitHub's UI to add them via Settings → Features → Issues → Set up templates)

# A topics list for discoverability
gh repo edit --add-topic claude --add-topic agent --add-topic mcp --add-topic finops --add-topic aws --add-topic gcp --add-topic azure --add-topic skills --add-topic vantage

# Pin the docs site link to the repo description
gh repo edit --homepage "https://YOUR-USERNAME.github.io/cloud-operator-skill/"
```

## Step 7 — Update the skill itself

When you change the skill (`docs/skill/SKILL.md` or any reference), the docs site rebuilds automatically on push. There's nothing else to do for docs.

To re-package the skill as a `.skill` file for distribution:

```bash
# Using the upstream skill-creator
git clone https://github.com/anthropics/skills.git ~/skills
python -m scripts.package_skill /path/to/cloud-operator-skill/docs/skill/
```

The output `cloud-operator.skill` can be added to a release on GitHub:

```bash
gh release create v0.2.0 \
  --title "Cloud Operator v0.2 — Multi-cloud expansion" \
  --notes "See docs/evals/iteration-2.md for details" \
  cloud-operator.skill
```

Now users can download the `.skill` file directly from your release page.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Pages workflow fails | `mkdocs.yml` has unresolved `!!python/name:...` extension | Confirm `pymdown-extensions` is installed in the workflow (it is by default in `docs.yml`) |
| Site loads but search is empty | Search index didn't build | Re-run the workflow; check the `mkdocs build` log for plugin errors |
| 404s on internal links | Page paths in `mkdocs.yml` `nav:` don't match files in `docs/` | Run `mkdocs build --strict` locally to surface the bad refs |
| Mindmap doesn't render | Mermaid superfences config got dropped | Check `mkdocs.yml` has the `pymdownx.superfences` block with the `mermaid` custom_fence |
| `gh repo create` errors | Not authenticated | Run `gh auth login` |

## What's next

Once live, share the docs URL. It's the single best way for new contributors to discover the project, and the search makes it usable as a reference even for people who'd never read the whole thing.
