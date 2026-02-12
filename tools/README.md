# Tools

This directory contains utility scripts for the kannondai-community project.

---

## Python Environment Policy

**This project uses the GLOBAL Python 3.13 environment** - NO virtual environments (.venv).

### Rationale:
- Community project with minimal dependencies
- Single-user workstation with controlled global environment
- Avoids complexity of venv management for lightweight work

### Windows-Specific Python Execution Notes

⚠️ **CRITICAL for Copilot/Future Users:**

1. **Correct Python Executable:**
   ```powershell
   & "C:\Program Files\Python313\python.exe" script.py
   ```
   - Windows Store Python launcher (`C:\Windows\System32\python`) is in PATH but not functional for our purposes
   - Always use the **full path** with `&` call operator in PowerShell

2. **PowerShell Syntax:**
   - Paths with spaces require quotes AND the `&` operator
   - ❌ WRONG: `"C:\Program Files\Python313\python.exe" script.py` (syntax error)
   - ✅ CORRECT: `& "C:\Program Files\Python313\python.exe" script.py`

3. **Checking Python Location:**
   ```powershell
   where.exe python
   # Output shows:
   # C:\Windows\System32\python          ← Windows Store launcher (avoid)
   # C:\Program Files\Python313\python.exe ← USE THIS
   ```

4. **Output Buffering Issue:**
   - Python output may not appear in terminal due to PowerShell buffering
   - Add `flush=True` to all `print()` statements for reliable output
   - Use `-u` flag for unbuffered output: `python -u script.py`

5. **Large File Operations (100+ line deletions):**
   - Copilot's `run_in_terminal` tool is unreliable on Windows (cannot capture output)
   - For file modifications, Copilot will create Python scripts and request manual execution
   - Always run with full Python path: `& "C:\Program Files\Python313\python.exe" script.py`
   - Close target files in VS Code before execution (Windows file locking)
   - Copy output back to Copilot to confirm success
   - Example: Deleting 500+ lines from markdown files for AI Context optimization

---

## `create_annual_report_part1_docx.py`

Python script to generate Word document for Annual Report Part 1.

**Purpose:** Convert markdown draft to formatted Word document with cover pages.

**Requirements:** 
- `python-docx` (already installed)

**Usage:**
```powershell
cd E:\GitHub\kannondai-community
& "C:\Program Files\Python313\python.exe" tools\create_annual_report_part1_docx.py
```

**Output:** `docs/community/2026__/annual_report_part1_v1.docx`

**Important Note - Cover Page Design:**

⚠️ **python-docx Limitation:** Cannot directly overlay text on images as background.

**Current Approach:**
- Script generates: Title (top) → Image (below) on cover page
- Manual adjustment needed for text overlay on image background

**Manual Steps in Word (if text overlay desired):**
1. Right-click image → **Text Wrapping** → **Behind Text**
2. **Insert** → **Text Box** → Add title text
3. Drag text box to position over image
4. Adjust font, color (white for visibility), and position

**Rationale:**
- python-docx high-level API doesn't support text boxes with positioning
- Direct XML manipulation (DrawingML) caused file corruption
- Simple layout + manual adjustment = reliable and flexible

---

## `read_docs.py`

Python script to extract text content from PDF and Word (.docx) files for Copilot context.

**Purpose:** Extract text from documents so GitHub Copilot can reference them in conversations for context-aware assistance.

**Requirements:** 
- `pypdf` - for PDF extraction
- `python-docx` - for Word document extraction

**Installation:**
```powershell
& "C:\Program Files\Python313\python.exe" -m pip install pypdf python-docx
```

### Manual Usage (for humans):

1. Place your PDF and/or .docx files in `tools/documents/`
2. Run the extraction script:
   ```powershell
   cd E:\GitHub\kannondai-community
   & "C:\Program Files\Python313\python.exe" tools\read_docs.py
   ```
3. Reference `tools/extracted_documents.txt` in Copilot conversations

### AI Assistant Usage (automatic):

**When user says "read the PDF/DOCX in documents/":**

1. **Detect binary file** - Don't use `read_file` on `.pdf`/`.docx` files
2. **Execute extraction automatically**:
   ```powershell
   & "C:\Program Files\Python313\python.exe" tools\read_docs.py
   ```
3. **Read output** - Content is in `tools/extracted_documents.txt`
4. **Return to user** - Present the extracted content seamlessly

**Key points for AI assistants:**
- User should not need to know about the extraction step
- Execute the script transparently when binary files are requested
- Only mention the tool if there's an error or missing dependency
- This provides seamless "read the PDF" experience

**Output:** `tools/extracted_documents.txt` - Combined text extraction of all documents in the `documents/` folder.

**Workflow:**
- Add new documents to `tools/documents/` as needed
- Re-run `read_docs.py` to update the extracted text
- Copilot can then reference the full context from your documents

**Note:** 
- `tools/documents/` is `.gitignore`d as a temporary workspace
- `tools/extracted_documents.txt` is also excluded (covered by `*.txt` rule)
- Documents are not committed to the repository

---

## `trim_file_template.py`

Generic Python template for large-scale file deletion operations (100+ lines).

**Purpose:** Provide a reliable method for AI-assisted large file operations on Windows, where Copilot's `run_in_terminal` tool cannot verify execution.

**Background:** 
- AI Context Standard Step 7 recommends splitting 500+ line documents for token efficiency
- `replace_string_in_file` struggles with 100+ line deletions
- Windows PowerShell terminal output capture is unreliable for verification
- Manual Python execution provides visible confirmation

**Usage Pattern (for AI assistants):**

1. **Copy template** to new script (e.g., `trim_specific_file.py`)
2. **Edit settings:**
   ```python
   file_path = r'e:\path\to\target\file.md'
   lines_to_keep = 175  # Keep first N lines
   ```
3. **Request user to execute:**
   ```
   Please run this command in PowerShell and copy the output:
   & "C:\Program Files\Python313\python.exe" tools\trim_specific_file.py
   ```
4. **Verify with user's output** (should show "✓ 完了: XXX行を削除しました")
5. **Confirm with read_file** after user reports success

**Features:**
- Pre-flight checks (file existence, current line count)
- Safe execution (warns if file already short enough)
- Clear error messages for PermissionError (file locks)
- Output with flush=True (ensures visibility in Windows)
- Diagnostic information (Python version, file path)

**When to use:**
- Deleting 100+ lines from markdown files
- Converting large documents to navigation hubs
- Any operation where `replace_string_in_file` would exceed recommended limits

**Example workflow (kannondai-community, 2026-02-08):**
```
Task: Reduce annual_report_philosophy.md from 726 lines to 175 lines
1. Created trim_philosophy.py from template
2. Created diagnose_file_access.py for pre-flight check
3. User executed both scripts manually (output visible)
4. Confirmed success: 551 lines deleted
5. Verified with read_file: 175 lines remaining
```

**Why not automated:**
- `run_in_terminal` cannot capture output on Windows PowerShell
- File may be locked by VS Code editor
- Python execution succeeds but Copilot cannot verify
- Manual execution ensures user sees success/error messages
- User can close files before execution if needed

---

## Troubleshooting: python-docx Word Generation Issues

Common issues encountered when generating Word documents with python-docx. Both issues documented here occurred on 2026-02-11 during annual report generation.

### Issue 1: Page Numbering Not Starting from 1

**Symptom:** Section page numbers don't reset to 1 even after setting `pgNumType`.

**Root Cause:** In python-docx, section properties (`sectPr`) are placed at the **end** of a section in Word's XML structure. Setting page numbering immediately after `doc.add_section()` has no effect because the section isn't finalized yet.

**Solution:** Set page numbering **immediately before creating the next section**.

```python
section_break2 = doc.add_section()  # Main content section
# ... add content ...
current_section = doc.sections[-1]  # Get current section
current_section._sectPr  # Configure page numbering HERE
section_break_part2 = doc.add_section()  # THEN create next section
```

**Details:** See extensive documentation in `create_annual_report_part1_docx_v2.py` file header docstring.

---

### Issue 2: Paragraph Formatting Applied to Wrong Paragraphs

**Symptom:** Yellow background and indentation intended for one paragraph appears on multiple paragraphs. First paragraph appears narrower than others.

**Root Cause:** Markdown parsing didn't treat `>` (empty quoted line) as a paragraph separator, causing multiple paragraphs to merge into one large paragraph. Special formatting (background color, indentation) then applied to the entire merged paragraph instead of just the intended portion.

**Solution:** In `extract_draft_content()`, treat `>` with empty content as a paragraph break:

```python
elif stripped.startswith('>'):
    text = stripped[1:].strip()
    if text:
        current_para.append(text)
    elif current_para:
        # Empty `>` line = paragraph break
        sections.append({'type': '段落', 'content': '\n'.join(current_para)})
        current_para = []
```

**Details:** See `extract_draft_content()` docstring in `create_annual_report_part1_docx_v2.py`.
