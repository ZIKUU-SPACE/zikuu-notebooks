#!/usr/bin/env python3
"""
Update root README.md notebook list between markers.

Markers (must exist in README.md):
  <!-- ZIKUU_NOTEBOOKS_LIST:BEGIN -->
  <!-- ZIKUU_NOTEBOOKS_LIST:END -->

What it does:
- Scans top-level directories for .ipynb files
- Uses each module's README.md H1 as title if available
- Generates a Colab link per notebook
- Replaces only the content between markers

How it finds GitHub repo:
1) env: ZIKUU_GITHUB_REPO="OWNER/REPO"
2) git remote origin url (auto-parse)
If not found, it will still generate local links but Colab links will be omitted.

Usage:
  python scripts/update_readme.py
  ZIKUU_GITHUB_REPO="ZIKUU-SPACE/zikuu-notebooks" python scripts/update_readme.py
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional


BEGIN_MARKER = "<!-- ZIKUU_NOTEBOOKS_LIST:BEGIN -->"
END_MARKER = "<!-- ZIKUU_NOTEBOOKS_LIST:END -->"

EXCLUDE_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "scripts",
    ".idea",
    ".vscode",
}


@dataclass(frozen=True)
class NotebookItem:
    module_dir: str          # e.g., earth-observation-001-daichi2
    module_title: str        # from module README H1
    notebooks: list[str]     # notebook filenames relative to module dir


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def _get_repo_root(script_path: Path) -> Path:
    # scripts/update_readme.py -> repo root
    return script_path.resolve().parent.parent


def _first_h1_from_readme(readme_path: Path) -> Optional[str]:
    if not readme_path.exists():
        return None
    text = _read_text(readme_path)
    for line in text.splitlines():
        m = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _list_modules(repo_root: Path) -> list[NotebookItem]:
    items: list[NotebookItem] = []
    for p in sorted(repo_root.iterdir(), key=lambda x: x.name):
        if not p.is_dir():
            continue
        if p.name in EXCLUDE_DIRS:
            continue
        if p.name.startswith("."):
            continue

        # collect .ipynb in this module dir (non-recursive)
        notebooks = sorted([f.name for f in p.glob("*.ipynb") if f.is_file()])
        if not notebooks:
            continue

        title = _first_h1_from_readme(p / "README.md") or p.name
        items.append(NotebookItem(module_dir=p.name, module_title=title, notebooks=notebooks))

    return items


def _run_git(args: list[str], cwd: Path) -> Optional[str]:
    try:
        out = subprocess.check_output(["git", *args], cwd=str(cwd), stderr=subprocess.DEVNULL)
        return out.decode("utf-8", errors="replace").strip()
    except Exception:
        return None


def _parse_github_repo_from_remote(remote_url: str) -> Optional[str]:
    """
    Supports:
      https://github.com/OWNER/REPO.git
      https://github.com/OWNER/REPO
      git@github.com:OWNER/REPO.git
    Returns OWNER/REPO
    """
    remote_url = remote_url.strip()

    m = re.match(r"^https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", remote_url)
    if m:
        return f"{m.group(1)}/{m.group(2)}"

    m = re.match(r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$", remote_url)
    if m:
        return f"{m.group(1)}/{m.group(2)}"

    return None


def _detect_github_repo(repo_root: Path) -> Optional[str]:
    env_repo = os.getenv("ZIKUU_GITHUB_REPO", "").strip()
    if env_repo:
        return env_repo

    remote = _run_git(["config", "--get", "remote.origin.url"], cwd=repo_root)
    if remote:
        parsed = _parse_github_repo_from_remote(remote)
        if parsed:
            return parsed

    return None


def _colab_link(github_repo: str, notebook_path: str, branch: str = "main") -> str:
    # notebook_path like "earth-observation-001-daichi2/earth_observation_intro.ipynb"
    return f"https://colab.research.google.com/github/{github_repo}/blob/{branch}/{notebook_path}"


def _render_list(items: list[NotebookItem], github_repo: Optional[str]) -> str:
    if not items:
        return "- （まだNotebookがありません）\n"

    lines: list[str] = []
    # timestamp in JST-like display is handled by user timezone; keep UTC in file for stability
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines.append(f"更新: {now_utc}\n")

    for it in items:
        module_link = f"./{it.module_dir}/"
        lines.append(f"- **[{it.module_title}]({module_link})**")
        for nb in it.notebooks:
            rel_path = f"{it.module_dir}/{nb}"
            if github_repo:
                colab = _colab_link(github_repo, rel_path)
                lines.append(f"  - [{nb}]({colab})")
            else:
                # fallback: local link only
                lines.append(f"  - `{nb}`（Colabリンク生成には ZIKUU_GITHUB_REPO の設定が必要）")
        lines.append("")  # blank line between modules

    return "\n".join(lines).rstrip() + "\n"


def _replace_between_markers(readme_text: str, new_block: str) -> str:
    if BEGIN_MARKER not in readme_text or END_MARKER not in readme_text:
        raise RuntimeError("README.md にマーカーが見つかりません（BEGIN/END）")

    begin_idx = readme_text.index(BEGIN_MARKER) + len(BEGIN_MARKER)
    end_idx = readme_text.index(END_MARKER)

    if end_idx < begin_idx:
        raise RuntimeError("マーカーの順序が不正です（END が BEGIN より前）")

    before = readme_text[:begin_idx]
    after = readme_text[end_idx:]

    # Ensure exactly one blank line after BEGIN marker for cleanliness
    return before + "\n" + new_block + after


def main() -> None:
    script_path = Path(__file__)
    repo_root = _get_repo_root(script_path)
    readme_path = repo_root / "README.md"

    if not readme_path.exists():
        raise SystemExit(f"README.md が見つかりません: {readme_path}")

    github_repo = _detect_github_repo(repo_root)
    items = _list_modules(repo_root)
    new_block = _render_list(items, github_repo)

    original = _read_text(readme_path)
    updated = _replace_between_markers(original, new_block)

    if updated == original:
        print("README.md は更新不要でした。")
        return

    _write_text(readme_path, updated)
    print("README.md を更新しました。")
    if not github_repo:
        print("NOTE: Colabリンクを生成するには環境変数 ZIKUU_GITHUB_REPO=\"OWNER/REPO\" を設定してください。")


if __name__ == "__main__":
    main()
