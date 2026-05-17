---
name: git-push
description: Use ONLY when working on the conky-lyric-spotify project (Python scripts, Conky configs, startup scripts, README, CHANGELOG, git). Automatically stage, commit, and push changes to the GitHub remote after every file modification.
---

# Git Auto-Push

This skill ensures every change to the `conky-lyric-spotify` project is committed and pushed to GitHub.

## Security Rules

| Do NOT commit | Reason |
|---------------|--------|
| `.env` | Contains Spotify cookies / secrets |
| `*.log` | Log files |
| `__pycache__/` | Python bytecode |
| `.cache/` | API response caches |
| Any `.env.*` that is not `.env.example` | Other env files could contain secrets |

## Workflow

Every time you modify a file in this project:

1. **Check for sensitive files** — verify `.env`, `*key*`, `*secret*`, `*credential*`, `*cookie*` are NEVER staged
2. **Stage changes** — `git add -A` (skips gitignored files)
3. **Review staged** — `git status` and `git diff --cached` to confirm no secrets
4. **Commit** — with a descriptive message summarizing what changed and why
5. **Push** — `git push origin main`

## Commit Message Format

```
<type>: <short description>

<optional body with details>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `chore`

## Remote

```
origin  https://github.com/mrdodgerx/conky-lyric-spotify.git (push)
```

Always push to `origin main` after committing.
