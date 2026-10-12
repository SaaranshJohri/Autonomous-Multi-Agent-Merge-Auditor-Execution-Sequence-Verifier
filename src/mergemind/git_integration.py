
"""Git-aware three-way analysis for Python files."""

import subprocess
from pathlib import Path

from .merge_analyzer import analyze_merge_from_code


def _git(repo_root, *args, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if check and result.returncode != 0:
        message = result.stderr.strip() or "Git command failed"
        raise RuntimeError(message)

    return result


def _source_at(repo_root, ref, path):
    result = _git(
        repo_root,
        "show",
        f"{ref}:{path}",
        check=False,
    )

    # A file may not exist in one version, for example
    # when a developer added or deleted it.
    if result.returncode != 0:
        return ""

    return result.stdout


def analyze_git_merge(base_ref, head_ref="HEAD"):
    """Compare a target branch and incoming branch using their merge base."""

    repo_root = Path(
        _git(Path.cwd(), "rev-parse", "--show-toplevel").stdout.strip()
    )

    merge_base = _git(
        repo_root,
        "merge-base",
        base_ref,
        head_ref,
    ).stdout.strip()

    if not merge_base:
        raise RuntimeError("Could not find a common Git merge base.")

    changed_files = set()

    # Include Python files changed on either side of the merge base.
    for ref in (base_ref, head_ref):
        output = _git(
            repo_root,
            "diff",
            "--name-only",
            "-z",
            merge_base,
            ref,
        ).stdout

        changed_files.update(
            path
            for path in output.split("\0")
            if path and path.lower().endswith(".py")
        )

    reports = []
    errors = []
    all_conflicts = []

    for path in sorted(changed_files):
        base_code = _source_at(repo_root, merge_base, path)
        target_code = _source_at(repo_root, base_ref, path)
        incoming_code = _source_at(repo_root, head_ref, path)

        try:
            result = analyze_merge_from_code(
                base_code,
                target_code,
                incoming_code,
            )
        except SyntaxError as exc:
            errors.append({
                "file": path,
                "error": f"Syntax error at line {exc.lineno}: {exc.msg}",
            })
            continue

        conflicts = []

        for conflict in result.get("conflicts", []):
            item = dict(conflict)
            item["file"] = path
            conflicts.append(item)
            all_conflicts.append(item)

        reports.append({
            "file": path,
            "summary": result.get("summary", {}),
            "conflicts": conflicts,
        })

    return {
        "repository": str(repo_root),
        "target_ref": base_ref,
        "incoming_ref": head_ref,
        "merge_base": merge_base,
        "changed_python_files": sorted(changed_files),
        "analyzed_file_count": len(reports),
        "file_reports": reports,
        "conflicts": all_conflicts,
        "errors": errors,
        "summary": {
            "conflict_count": len(all_conflicts),
            "direct_conflicts": sum(
                c.get("type") != "semantic_dependency_conflict"
                for c in all_conflicts
            ),
            "semantic_conflicts": sum(
                c.get("type") == "semantic_dependency_conflict"
                for c in all_conflicts
            ),
            "status": (
                "analysis_errors"
                if errors
                else "conflicts_detected"
                if all_conflicts
                else "no_conflicts"
            ),
        },
    }
