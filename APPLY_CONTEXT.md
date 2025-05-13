# Context for Using VS Code and Copilot

## Purpose
This context file is designed to guide interactions during a session, assuming the current state of Visual Studio Code and GitHub Copilot. The goal is to simplify the "Response → Apply" step in the "Prompt → Response → Apply → Review (Verify)" cycle.

## Assumptions
1. The current state of VS Code and Copilot is used as the basis for all practices.
2. The "Apply" button in the suggestion box is the primary method for applying changes.
3. Updates are typically made to the current file being worked on.

## Workflow
1. **Prompt**: The user provides instructions to Copilot.
2. **Response**: Copilot generates suggestions.
3. **Apply**: The user applies the suggestions using the "Apply" button in the suggestion box.
4. **Review (Verify)**: The user reviews and verifies the applied changes to ensure correctness and alignment with intent.

## Expectations
1. At the beginning of a session, this context will be reminded to the AI.
2. During the session, unless otherwise stated, the AI will respond in a way that assumes the user will use the "Apply" button to apply changes.
3. The AI will simplify responses to focus on guiding the user to use the "Apply" button effectively.

## Practices
1. **Prompting**:
   - Provide clear and specific instructions to guide Copilot in generating relevant suggestions.
   - Use comments or partial code snippets to provide context for Copilot.

2. **Applying Suggestions**:
   - Use the "Apply" button in the suggestion box to apply changes directly to the current file.
   - For more control, manually adjust the applied changes as needed.

3. **Reviewing Changes**:
   - Always review the applied changes for correctness, security, and alignment with your intent.
   - Use version control (e.g., Git) to track changes and revert if necessary.

4. **Managing Context**:
   - Save important instructions, decisions, and code snippets in a context file for future reference.
   - Update the context file when switching tasks or files to reflect the new focus.

## Limitations
1. The "Apply" button applies suggestions as-is and may require manual adjustments for complex changes.
2. Copilot does not currently support advanced features like "Apply to Selected Range" or change previews.
3. User judgment is essential for handling complex or context-sensitive changes.

## Goal
The goal of this context is to streamline the workflow and make the "Response → Apply" step as simple and efficient as possible, leveraging the current capabilities of VS Code and Copilot.