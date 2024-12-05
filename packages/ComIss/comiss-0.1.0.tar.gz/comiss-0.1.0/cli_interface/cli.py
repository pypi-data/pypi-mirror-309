# cli.py

"""
This script provides a command-line interface for generating commit messages 
and filtering git commit history.

Functions:
- load_environment(): Loads environment variables.
- main(): Handles user interactions for generating commit messages or filtering
 commits based on the provided command.
"""



import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
from dotenv import load_dotenv
from rich import print as rich_print
from cli_interface.user_interface import UserInterface
from cli_interface.message_maker import MessageMaker
from git_scripts.git_diff_fetcher import GitDiffFetcher
from git_scripts.git_history_analyzer import GitHistoryAnalyzer
from git_scripts.retroactive_commit import RetroactiveCommit
from rich import print

def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        rich_print("Error: OPENAI_API_KEY not found in environment variables.")
        sys.exit(1)

def main(): # pylint: disable=too-many-branches
    load_environment()

    ui = UserInterface()
    args = ui.parse_args()

    git_fetcher = GitDiffFetcher()
    git_analyzer = GitHistoryAnalyzer()
    retro_commit = RetroactiveCommit()

    if args.command == 'commit':
        changes = git_fetcher.get_staged_diff()
        if not changes:
            rich_print("No changes detected.")
            return

        # Map 'c' to 'complex' and 's' to 'simple'
        template_map = {'c': 'complex', 's': 'simple'}
        selected_template = template_map.get(args.template, 'simple')

        message_maker = MessageMaker(template=selected_template)

        commit_message = message_maker.generate_message(changes)

        while True:
            if not commit_message:
                ui.show_error("Failed to generate commit message.")
                return

            ui.display_commit_message(commit_message)

            user_input = ui.prompt_user_action()

            if user_input == 'a':
                # Commit the changes using the generated commit message
                try:
                    subprocess.run(["git", "commit", "-m", commit_message], check=True)
                    rich_print(f"Changes committed with message: {commit_message}")
                except subprocess.CalledProcessError as e:
                    ui.show_error(f"Error committing changes: {e}")
                break
            if user_input == 'r':
                # Regenerate the commit message
                feedback = ui.prompt_feedback()
                commit_message = message_maker.generate_message(changes,
                feedback, old_message=commit_message)
            elif user_input == 'e':
                try:
                    commit_message = ui.prompt_manual_edit(commit_message)
                except Exception as e:
                    print(e)
            elif user_input == 'q':
                rich_print("Quitting without committing changes.")
                break
            else:
                ui.show_error("Invalid input. Please try again.")
    elif args.command == 'filter':
        filtered_commits = git_analyzer.filter_commits(
            change_type=args.change_type,
            impact_area=args.impact_type
        )
        if filtered_commits:
            ui.display_commits_paginated(filtered_commits)
        else:
            rich_print("[bold red][bold red]No commits found matching the criteria.[/bold red][/bold red]")
    elif args.command == 'retro':
        try:
            retro_commit.generate_commit_message()
            # Notify the user to force push the changes
            print("\nAll commits have been updated with new messages.")
            print("To apply these changes to your remote repository, use:\n")
            print("    git push --force\n")
            print("Note: Force pushing rewrites history on the remote repository, so ensure this is safe to do.")
        except Exception as e:
            print(f"An error occurred during retroactive commit: {e}")
    else:
        # If no command is provided, show help
        ui.parser.print_help()

if __name__ == "__main__":
    main()
