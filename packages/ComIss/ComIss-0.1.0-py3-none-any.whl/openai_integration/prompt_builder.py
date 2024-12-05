# openai_integration/prompt_builder.py

import textwrap


class PromptBuilder:
    def __init__(self, template='simple'):
        self.template = template

    def construct_prompt(self, changes, feedback=None, old_message=None):
        # Base instructions
        base_instructions = textwrap.dedent("""
            You are an AI assistant tasked with generating commit messages based strictly on the provided git diff changes.
            Please adhere to the following instructions carefully and do not deviate from the format or include any additional information.

            **Format:**
            <ChangeType> | <ImpactArea>: <TLDR>

            **Instructions:**
        """)

        # Detailed instructions
        detailed_instructions = textwrap.dedent("""
            - **ChangeType**: Select **only one** from [feature, bugfix, refactor, docs, test, chore].
            - **ImpactArea**: Specify the affected part of the project (e.g., 'frontend', 'backend', 'database', 'user interface').
            - **TLDR**: Write a concise, one-line summary of the changes in imperative mood (e.g., 'Fix crash when user inputs empty string').
            - Do not include any details beyond the TLDR unless instructed.
            - **Do not** add any sections or information not specified in the format.
        """)

        # Combine base instructions with detailed instructions
        base_prompt = f"{base_instructions}\n{detailed_instructions}\n"

        # Additional instructions for 'complex' template
        if self.template == 'complex':
            complex_instructions = textwrap.dedent("""
                
                After the TLDR, provide a detailed description of the changes starting on a new line.
                The detailed description should explain what was changed and why, using clear and concise language.
            """)
            base_prompt += complex_instructions

        # Examples section
        examples = textwrap.dedent("""
            **Examples:**
            feature | backend: Add user authentication module
            bugfix | frontend: Fix alignment issue on login page
            refactor | database: Optimize query performance
        """).strip()

        base_prompt += "\n\n" + examples + "\n"

        # Git Diff Changes section
        git_diff_section = textwrap.dedent(f"""
            **Git Diff Changes:**
            ```
            {changes}
            ```
        """)

        user_message = git_diff_section

        # Previous Commit Message and User Feedback sections (if provided)
        if feedback and old_message:
            previous_commit = textwrap.dedent(f"""
                
                **Previous Commit Message:**
                {old_message}

                **User Feedback:**
                {feedback}
                Please revise the commit message accordingly, strictly following the format and instructions.
            """)
            user_message += previous_commit

        # Combine base_prompt with user_message
        full_prompt = f"{base_prompt}{user_message}"

        return full_prompt
