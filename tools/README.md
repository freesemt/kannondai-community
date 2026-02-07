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
