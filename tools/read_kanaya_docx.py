"""
金谷氏のおうかがい.docx 専用読み取りスクリプト

Usage:
    & "C:\Program Files\Python313\python.exe" tools\read_kanaya_docx.py
"""

import sys
import os
from pathlib import Path

def main():
    try:
        from docx import Document
        print("python-docx imported successfully", flush=True)
        
        # Paths
        script_dir = Path(__file__).parent
        docx_path = script_dir / 'documents' / '金谷氏のおうかがい.docx'
        output_path = script_dir / '金谷氏のおうかがい_extracted.txt'
        
        if not docx_path.exists():
            print(f"ERROR: File not found: {docx_path}", flush=True)
            sys.exit(1)
        
        print(f"\nReading: {docx_path.name}", flush=True)
        print("=" * 80, flush=True)
        
        # Read document
        doc = Document(docx_path)
        
        # Extract all paragraphs
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():  # Skip empty paragraphs
                paragraphs.append(para.text)
        
        full_text = '\n\n'.join(paragraphs)
        
        print(f"Sections: {len(doc.sections)}", flush=True)
        print(f"Paragraphs: {len(paragraphs)}", flush=True)
        print(f"Characters: {len(full_text)}", flush=True)
        print("=" * 80, flush=True)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"金谷氏のおうかがい.docx - Extracted Text\n")
            f.write("=" * 80 + "\n\n")
            f.write(full_text)
        
        print(f"\n✓ SUCCESS! Written to: {output_path}", flush=True)
        print("=" * 80, flush=True)
        print("\nCONTENT:\n", flush=True)
        print("=" * 80, flush=True)
        print(full_text, flush=True)
        print("\n" + "=" * 80, flush=True)
        print("END OF DOCUMENT", flush=True)
        
    except ImportError:
        print("ERROR: python-docx not installed", file=sys.stderr, flush=True)
        print('Install with: & "C:\\Program Files\\Python313\\python.exe" -m pip install python-docx', flush=True)
        sys.exit(1)
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
