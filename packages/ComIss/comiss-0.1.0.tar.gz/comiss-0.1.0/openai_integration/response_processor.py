# openai_integration/response_processor.py

import re

class ResponseProcessor:
    def __init__(self):
        pass

    def process_response(self, raw_response):
        if not raw_response:
            return None

        # Remove any leading/trailing whitespace
        response_text = raw_response.strip()

        # Define a regex pattern to match the commit message format
        pattern = (
            r"^\s*(?P<ChangeType>feat|feature|bugfix|fix|refactor|docs|doc|test|tests|chore)"
            r"\s*\|\s*(?P<ImpactArea>[\w\s\-]+):\s*(?P<TLDR>.+?)(?:\n|$)"
        )

        # Match against the main components of the commit message
        match = re.match(pattern, response_text, re.IGNORECASE)

        if not match:
            # If the main components do not match, reject the input
            print("Generated commit message does not match the required format.")
            print("Response from GPT:\n", response_text)
            return None

        # Ensure there are no extra sections beyond the matched portion
        remaining_text = response_text[match.end():].strip()
        if remaining_text and not remaining_text.startswith("\n"):
            # If there's unexpected content beyond the matched portion, return None
            print("Generated commit message contains unexpected extra sections.")
            print("Response from GPT:\n", response_text)
            return None

        # Extract the summary components
        change_type = match.group('ChangeType').strip().lower()
        impact_area = match.group('ImpactArea').strip().lower()
        tldr = match.group('TLDR').strip()

        # Validate the impact area to ensure it’s not missing or empty
        if not impact_area:
            print("Commit message is missing an impact area.")
            print("Response from GPT:\n", response_text)
            return None

        # Normalize ChangeType
        change_type_mapping = {
            'feat': 'feature',
            'fix': 'bugfix',
            'doc': 'docs',
            'tests': 'test',
        }
        change_type = change_type_mapping.get(change_type, change_type)

        # Build the commit message
        if remaining_text.startswith("\n"):
            # There is a detailed description
            detailed_description = remaining_text.lstrip('\n').strip()
            commit_message = f"{change_type} | {impact_area}: {tldr}\n\n{detailed_description}"
        else:
            # No detailed description
            commit_message = f"{change_type} | {impact_area}: {tldr}"

        return commit_message
