<div align="center">
  <img alt="Rhine Lab archive terminal mark" height="128" src="img/logo.svg">
</div>

<h1 align="center">Rhine Lab Theme for DeepSeek Harness</h1>

<p align="center"><a href="README.md">简体中文</a> · English</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/github/license/ReLuckyLucy/dsh_Rhine_Lab_theme">
  <img alt="Top language" src="https://img.shields.io/github/languages/top/ReLuckyLucy/dsh_Rhine_Lab_theme">
  <img alt="Latest release" src="https://img.shields.io/github/v/release/ReLuckyLucy/dsh_Rhine_Lab_theme?include_prereleases">
  <img alt="Last commit" src="https://img.shields.io/github/last-commit/ReLuckyLucy/dsh_Rhine_Lab_theme">
</p>
<p align="center">
  <img alt="Code size" src="https://img.shields.io/github/languages/code-size/ReLuckyLucy/dsh_Rhine_Lab_theme">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/ReLuckyLucy/dsh_Rhine_Lab_theme">
  <img alt="Release downloads" src="https://img.shields.io/github/downloads/ReLuckyLucy/dsh_Rhine_Lab_theme/total">
  <img alt="Stars" src="https://img.shields.io/github/stars/ReLuckyLucy/dsh_Rhine_Lab_theme?style=social">
</p>

An Arknights Rhine Lab theme for the [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Web interface. It presents the conversation workspace as a research archive terminal while preserving Harness controls, layout, and settings flow.

- Warm paper, dense ink, and research orange for the light headquarters archive.
- Charcoal surfaces and cyan live-state accents for dark night operations.
- A native toggle in **Settings → General** to enable or disable the theme.
- Reduced nonessential decoration on narrow screens and support for reduced-motion preferences.

## 🔥 Quick start

**Requirements:** DeepSeek Harness installed with the Web profile available. This installs the current default branch from GitHub:

```sh
dsh plugin --profile web add github:ReLuckyLucy/dsh_Rhine_Lab_theme
```

Restart `dsh web`, refresh the browser, then enable Rhine Lab in **Settings → General**. To build and install from source:

```sh
git clone https://github.com/ReLuckyLucy/dsh_Rhine_Lab_theme.git
cd dsh_Rhine_Lab_theme
pnpm install
pnpm build
dsh plugin --profile web add .
```

Git installs use the committed `lib/` artifacts and do not require lifecycle-script approval in the target profile. `prepack` rebuilds the artifacts before an npm tarball is produced.

## 📜 Inputs and dependencies

The theme does not read user datasets or download models and external images. It uses the DeepSeek Harness Web plugin interface and theme tokens; its CSS is scoped to Harness page anchors. The preference is stored as `ui-theme-rhine-lab.enabled`. Harness continues to control the underlying Light, Dark, or System mode.

The compatibility target is **DeepSeek Harness 0.1.0-rc.5 Web**. If a page anchor is unavailable, only its decoration is omitted; Harness remains responsible for its own controls and layout.

## 🔛 Build, test, and package

```sh
pnpm install
pnpm test
pnpm build
npm pack --dry-run
```

Create an installable tarball:

```sh
pnpm pack
dsh plugin --profile web add ./dsh-theme-rhine-lab-0.2.1.tgz
```

Create a versioned source ZIP (the `VERSION` file must be present in the committed `HEAD`):

```sh
python scripts/package_source.py
```

The ZIP is written to `artifacts/` and contains only tracked files from that Git commit. Each push also uploads a GitHub Actions Artifact retained for 30 days. Pushing a `v` tag matching `VERSION` attaches the same source ZIP to a GitHub Release.

## 🪦 Screenshots

These screenshots show the theme running in the project’s actual test interface:

<p align="center"><img alt="Rhine Lab light headquarters archive" src="screenshots/light.png" width="84%"></p>
<p align="center"><img alt="Rhine Lab dark night operations" src="screenshots/dark.png" width="84%"></p>

## 📁 Project structure

```text
dsh_Rhine_Lab_theme/
├── .github/workflows/archive.yml  # Push archives and version Releases
├── img/                           # README mark
├── lib/                           # Committed runtime build
├── scripts/package_source.py      # Source ZIP from a Git commit
├── screenshots/                  # Actual theme captures
├── src/                           # Plugin source
├── tests/                         # Theme and archive tests
├── VERSION                        # Source archive version
├── README.md                      # Chinese project homepage
└── package.json                   # Plugin metadata (currently 0.2.1)
```

## 📦 Versioned archives

[`VERSION`](VERSION) is the archive version source and must match `package.json`. A push creates `dsh_Rhine_Lab_theme-vVERSION-SHORTSHA.zip`. Pushing the matching `vVERSION` tag creates a long-term GitHub Release with the same ZIP attached. Archives exclude uncommitted files, `node_modules`, and runtime environments.

## 📄 License

The code is licensed under the [MIT License](LICENSE). This is an unofficial fan-made theme. Arknights and Rhine Lab names and marks belong to Hypergryph / Yostar and their respective rights holders; this project is not affiliated with them.
