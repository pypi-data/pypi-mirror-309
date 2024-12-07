import subprocess
from pathlib import Path


def git_repo_name(repo: Path) -> str:
    """
    Get the name of the git repository.
    """
    results = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    results.check_returncode()
    return Path(results.stdout.strip()).name


def git_list_files(repo: Path) -> list[Path]:
    """
    List all files in a git repository.
    """
    results = subprocess.run(
        ["git", "ls-files"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    results.check_returncode()
    return [repo / path for path in results.stdout.splitlines() if path]
