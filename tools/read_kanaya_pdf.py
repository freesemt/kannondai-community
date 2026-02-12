import sys
import os

try:
    from pypdf import PdfReader
    
    pdf_path = r'e:\GitHub\kannondai-community\tools\documents\金谷氏のおうかがい.pdf'
    output_path = r'e:\GitHub\kannondai-community\tools\金谷氏のおうかがい_extracted.txt'
    
    print(f"Reading {pdf_path}...", flush=True)
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}", flush=True)
        sys.exit(1)
    
    reader = PdfReader(pdf_path)
    print(f"Pages: {len(reader.pages)}", flush=True)
    print("=" * 80, flush=True)
    
    all_text = []
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        print(f"Page {i}: {len(text)} chars", flush=True)
        all_text.append(f"--- Page {i} ---\n{text}\n")
    
    # Write to file
    full_text = '\n'.join(all_text)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print("\n" + "=" * 80, flush=True)
    print(f"SUCCESS! Written to: {output_path}", flush=True)
    print(f"Total: {len(reader.pages)} pages, {len(full_text)} chars", flush=True)
    
    # Also print to console
    print("\n" + "=" * 80, flush=True)
    print("CONTENT:", flush=True)
    print("=" * 80, flush=True)
    print(full_text, flush=True)
    
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
