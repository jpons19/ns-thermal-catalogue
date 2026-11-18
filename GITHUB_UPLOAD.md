# Upload to GitHub: jpons19

Suggested repository: **jpons19/ns-thermal-catalogue**. The commands below assume this name; substitute a different name consistently if desired. These instructions create a repository of files, not a GitHub Projects task board.

## 1. Download and extract

Download `ns-thermal-catalogue-github.zip` and extract it. It contains one top-level directory, `ns-thermal-catalogue`.

On macOS, if the archive is in Downloads:

```bash
cd ~/Downloads
unzip ns-thermal-catalogue-github.zip
cd ns-thermal-catalogue
```

If Finder already extracted it, just enter that directory. The archive contains the project files and Git settings, but no `.git` directory or remote credentials.

## 2. Create an empty repository

Sign in at https://github.com/jpons19 and choose **New repository** (or visit https://github.com/new).

- Owner: `jpons19`
- Repository name: `ns-thermal-catalogue`
- Choose the visibility you want.
- Leave the options to initialize a README, `.gitignore` or license **off**: the local project already contains its README and Git settings.

Click **Create repository**. This package does not create or publish a repository automatically.

## 3. Commit and push

From the extracted project directory:

```bash
git init -b main
git add .
git commit -m "Add NS thermal catalogue, literature audit and reviewed uncertainty envelopes"
git remote add origin git@github.com:jpons19/ns-thermal-catalogue.git
git push -u origin main
```

Use your existing SSH authentication for `jpons19`. If Git asks for an author identity, set your chosen name and email for this repository with `git config user.name` and `git config user.email`, then repeat the commit. There is no need to change another computer's SSH key.

If you prefer HTTPS, replace the remote-add command with:

```bash
git remote add origin https://github.com/jpons19/ns-thermal-catalogue.git
```

Use your configured GitHub credential manager, GitHub CLI login or a personal access token when required; GitHub account passwords are not used as Git HTTPS credentials.

If a repository with this name already contains commits, clone it and copy these files into the clone, then commit normally. Do not force-push over its history or run `git init` inside another existing repository just to follow these commands.

## 4. Optional: publish the HTML catalogue

The package is ready for GitHub Pages:

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch **main**, folder **/docs**, and save.
4. Use the site URL GitHub reports. With the suggested repository name and the usual project-site URL it is:
   https://jpons19.github.io/ns-thermal-catalogue/

`docs/index.html` is the entry point, and `.nojekyll` keeps this a plain static site. The plot, audit and project README copies needed by this site are included under `docs/`.

Pages availability depends on repository visibility and your GitHub plan. Enabling Pages is a separate publishing step; choose it when you want the catalogue available as a website.

## 5. Subsequent updates

```bash
source .venv/bin/activate
python scripts/rebuild.py
python scripts/validate_project.py
git status
git add README.md docs data scripts figures PROVENANCE.md CHANGELOG.md
git commit -m "Update source review and uncertainty envelopes"
git push
```

Edit and inspect the scientific changes before staging. The Python environment and temporary files are ignored by Git. Generated figures are intentionally tracked so the catalogue can be viewed without running Python.

## Alternative: add to an existing repository

From a local clone of the repository you want to use, copy the **whole** `ns-thermal-catalogue` directory into a new subdirectory (for example `observations/ns-thermal-catalogue`), then:

```bash
git add observations/ns-thermal-catalogue
git commit -m "Add NS thermal catalogue review"
git push
```

Run the Python commands from inside that subdirectory. Its `docs/` folder will not automatically become the existing repository's GitHub Pages root; the existing site's publishing layout must be handled separately.

## Official documentation

- Local project to GitHub: https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github
- Pages publishing source: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
