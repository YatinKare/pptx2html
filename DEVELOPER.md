# Developer Guide

This document is the **single source of truth** for contributing to this project. It explains the entire development workflow, from picking up a task to shipping a release, and covers branching, tagging, commit messages, GitHub Projects, CI/CD, docs, and versioning.

---

## 1. GitHub Projects + Task Flow

We use **GitHub Projects** as the source of truth for all work items (features, bug fixes, chores, docs, tests). All issues live in GitHub Issues and are linked to the Project board.

### Board Columns

* **To Do** – Work is agreed upon but not started.
* **In Progress** – You are actively coding/testing this.
* **In Review** – PR is open and awaiting review/tests.
* **Done** – Merged into `main` and milestone acceptance criteria met.

### WIP (Work in Progress) Limits

* **Max 2 cards** in **In Progress** per developer.
* Finish something before starting another.

### Labels

We use labels for clarity:

* **Type:** `type:feat`, `type:fix`, `type:chore`, `type:test`, `type:docs`.
* **Area:** `area:opc`, `area:oxml`, `area:model`, `area:render`, `area:fonts`, `area:ci`, `area:docs`, etc.
* **Priority:** `prio:p0` (critical), `prio:p1` (important), `prio:p2` (nice to have).

### Picking up a task

1. Choose a **To Do** card.
2. Assign yourself.
3. Move it to **In Progress**.
4. Create a branch for it (see branching rules below).

---

## 2. Git Branching & Feature Development

We use a **trunk-based** model: `main` is always releasable.

### Branch naming

* `feat/<short-description>` – New feature (e.g., `feat/background-renderer`).
* `fix/<short-description>` – Bug fix (e.g., `fix/crop-math`).
* `docs/<short-description>` – Documentation changes.
* `chore/<short-description>` – CI/config/tooling changes.

### Workflow

1. **Create branch:**

   ```bash
   git checkout -b feat/my-feature
   ```
2. **Develop locally:**

   * Run pre-commit hooks:

     ```bash
     pre-commit run --all-files
     ```
   * Run tests:

     ```bash
     uv run pytest
     ```
3. **Commit using Conventional Commits** (see section 2.1).
4. **Push branch:**

   ```bash
   git push -u origin feat/my-feature
   ```
5. **Open PR:**

   * Link the issue (`Closes #<issue-number>`).
   * Move card to **In Review**.
6. **Merge when CI passes and review is complete.**
7. Move card to **Done**.

### 2.1 Commit Messages

We use the **Conventional Commits** format for all commits:

```
<type>(<scope>): <short description>
```

**Types:**

* `feat` – New feature.
* `fix` – Bug fix.
* `docs` – Documentation only.
* `style` – Formatting/style changes (no code logic changes).
* `refactor` – Code changes that neither fix a bug nor add a feature.
* `test` – Adding or modifying tests.
* `chore` – Maintenance tasks, tooling, CI/CD changes.

**Scope:** Optional, identifies the area affected (e.g., `render`, `opc`).

**Description:**

* Keep under 72 characters.
* Imperative mood (e.g., “add support” not “added support”).

**Examples:**

* `feat(render): add background.png rendering for patterns`
* `fix(opc): correct slide ordering bug`
* `docs: update developer guide with commit message rules`

If needed, include a blank line after the first line, followed by a longer body explaining **what** and **why** (not how).

---

## 3. Tagging & Versioning

We follow **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`

### 3.1 Tagging Rules

* All release tags must be **annotated** and start with `v`:

  * Example: `v1.2.3`
* The version in `pyproject.toml` **must match** the tag version (enforced by CI).
* Tag format options:

  1. **Stable release:**

     * `v1.0.0` – First stable release.
     * `v1.2.3` – Patch/bugfix release.
  2. **Pre-release:**

     * `v1.2.0a1` – Alpha 1.
     * `v1.2.0b1` – Beta 1.
     * `v1.2.0rc1` – Release Candidate 1.
  3. **Post-release:**

     * `v1.2.0.post1` – Post-release build.
  4. **Development release:**

     * `v1.2.0.dev1` – Development version.

### 3.2 Version bumping options

* **Manual bump:**
  Edit `pyproject.toml` or run:

  ```bash
  uv version --bump patch --no-sync
  ```
* **Bump types:**

  * `major` – Breaking changes.
  * `minor` – Backward-compatible features.
  * `patch` – Bug fixes.
  * `alpha`, `beta`, `rc` – Pre-releases.
  * `post` – Post-release updates.
  * `dev` – Development build.
  * `stable` – Move pre-release to stable.

---

## 4. Release Process

### Automatic (Preferred)

1. Go to **Actions → Bump version & tag (uv)**.
2. Choose bump type (`patch`, `minor`, `major`, etc.).
3. Workflow:

   * Updates `pyproject.toml` version.
   * Commits change.
   * Creates annotated tag `vX.Y.Z`.
   * Pushes commit & tag.
4. Tag push triggers **Publish workflow**:

   * Checks tag matches `pyproject.toml`.
   * Builds with `uv build --no-sources`.
   * Validates with `uvx twine check`.
   * Publishes to PyPI (Trusted Publisher).
   * Smoke-installs from PyPI to verify.

### Manual

```bash
uv version --bump patch --no-sync
VERSION=$(uv version | awk '{print $NF}')
git commit -am "chore(release): v$VERSION"
git tag v$VERSION
git push && git push origin v$VERSION
```

---

## 5. Continuous Integration (CI)

All PRs trigger GitHub Actions to:

1. Install deps via `uv sync`.
2. Lint (`ruff check`), format check (`ruff format`), type check (`mypy`).
3. Run tests (`pytest`).
4. Run snapshot tests for rendering outputs.

A PR **cannot** be merged unless CI is green.

---

## 6. Continuous Delivery (CD)

CD is handled via the **Publish workflow** triggered by tag pushes.

* OIDC Trusted Publisher → No API token storage.
* Fails if tag and version mismatch.
* Publishes to PyPI.
* Smoke-tests install.

---

## 7. Documentation Workflow

* Docs live in `/docs`.
* Built with `mkdocs-material` + `mkdocstrings`.
* CI builds docs on every push/PR.
* Deploys to GitHub Pages on push to `main`.

To preview locally:

```bash
uv sync --all-extras
uv run mkdocs serve
```

---

## 8. Pre-commit Hooks

Pre-commit is required for consistent style.

* Runs `ruff` (lint + format) and `mypy` locally.
* Install hooks:

```bash
pre-commit install
```

* Run on demand:

```bash
pre-commit run --all-files
```

---

## 9. Summary: Two Common Workflows

### 9.1 Feature / Bug Fix

```bash
# 1. Pick card → move to In Progress → branch
git checkout -b feat/my-feature

# 2. Code + test locally
pre-commit run --all-files
uv run pytest

# 3. Commit + push
git commit -m "feat(area): short desc"
git push -u origin feat/my-feature

# 4. Open PR → link issue → wait for green CI → merge → Done
```

### 9.2 New Version Release

**Automatic:**

* Actions → Bump version & tag (uv) → choose bump type → done.

**Manual:**

```bash
uv version --bump patch --no-sync
VERSION=$(uv version | awk '{print $NF}')
git commit -am "chore(release): v$VERSION"
git tag v$VERSION
git push && git push origin v$VERSION
```

---

Follow this guide for all contributions. If in doubt, ask in the issue or PR thread before starting work.
