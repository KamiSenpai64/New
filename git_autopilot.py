#!/usr/bin/env python3
from git import Repo, GitCommandError
import sys
import os

MAIN_BRANCH = "main"

GITIGNORE_CONTENT = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
.env/

# IDEs / editors
.idea/
.vscode/
*.swp

# OS files
.DS_Store
Thumbs.db

# Termux / misc
*.termux
"""

def run_git_autopilot(commit_msg):
    repo = Repo('.')
    if repo.bare:
        print("[ERROR] No git repository found here.")
        sys.exit(1)

    current_branch = repo.active_branch.name
    print("INFO: Current branch:", current_branch)

    try:
        gitignore_path = ".gitignore"
        if not os.path.exists(gitignore_path):
            print("INFO: Creating .gitignore...")
            with open(gitignore_path, "w") as f:
                f.write(GITIGNORE_CONTENT)
            repo.git.add(gitignore_path)
            repo.index.commit("Add Python + Termux + IDE gitignore")
            print("INFO: .gitignore committed.")

        repo.git.add(all=True)
        print("INFO: Staged all changes.")

        if repo.index.diff("HEAD") or repo.untracked_files:
            repo.index.commit(commit_msg)
            print("INFO: Committed changes:", commit_msg)
        else:
            print("INFO: Nothing to commit.")

        print(f"INFO: Pulling & rebasing {current_branch} onto {MAIN_BRANCH}...")
        repo.git.fetch("origin")
        repo.git.rebase(f"origin/{MAIN_BRANCH}")

        print("INFO: Pushing", current_branch, "to origin...")
        repo.git.push("origin", current_branch)

        print("\nINFO: Current commit graph:")
        print(repo.git.log("--oneline", "--graph", "--all", "--decorate"))

        print("\nDONE: Repo updated with linear history.")

    except GitCommandError as e:
        print("ERROR: Git command failed:")
        print(e)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python git_autopilot.py \"Commit message\"")
        sys.exit(1)

    commit_msg = sys.argv[1]
    run_git_autopilot(commit_msg)


if __name__ == "__main__":
    main()

