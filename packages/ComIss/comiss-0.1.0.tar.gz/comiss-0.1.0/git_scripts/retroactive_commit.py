# git_scripts/retroactive_commit.py

import subprocess
from cli_interface.message_maker import MessageMaker
import os

class RetroactiveCommit:
    def __init__(self):
        self.message_maker = MessageMaker()

    def generate_commit_message(self):
        # Get a list of commit hashes
        commit_hashes = subprocess.check_output(['git', 'rev-list', '--reverse', 'HEAD']).decode().split()

        # Set GIT_SEQUENCE_EDITOR to automatically pick all commits
        env = os.environ.copy()
        env['GIT_SEQUENCE_EDITOR'] = 'sed -i -e "s/^pick /edit /"'

        # Start an interactive rebase
        subprocess.run(['git', 'rebase', '-i', '--root'], env=env, check=True)

        for commit_hash in commit_hashes:
            # Extract the diff for the commit if not provided
            diff = subprocess.check_output(['git', 'show', commit_hash]).decode()
            
            # Generate a commit message using the MessageMaker
            new_message = self.message_maker.generate_message(diff)
            
            # Amend the commit with the new message
            try:
                env['GIT_COMMITTER_DATE'] = subprocess.check_output(['git', 'log', '-1', '--format=%cD', commit_hash]).decode().strip()
                env['GIT_AUTHOR_DATE'] = subprocess.check_output(['git', 'log', '-1', '--format=%aD', commit_hash]).decode().strip()
            except subprocess.CalledProcessError:
                print(f"Could not retrieve dates for commit {commit_hash}. Using current date and time.")

            if new_message:
                subprocess.run(['git', 'commit', '--amend', '-m', new_message], env=env, check=True)
                print(f"Amended commit {commit_hash} with new message.")
            else:
                print(f"Generated commit message for {commit_hash} is None. Skipping amendment.")
            
            # Continue the rebase
            subprocess.run(['git', 'rebase', '--continue'], check=True)