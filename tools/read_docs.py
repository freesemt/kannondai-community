"""
Document Text Extractor for Copilot Context

Extracts text from PDF and Word (.docx) files in the documents/ folder
and saves them to a single text file for easy Copilot reference.

Requirements:
- pypdf
- python-docx

Usage:
    cd E:\GitHub\kannondai-community
    & "C:\Program Files\Python313\python.exe" tools\read_docs.py
"""

import sys
import os
from pathlib import Path

def main():
    try:
        # Import libraries
        from pypdf import PdfReader
        print("pypdf imported successfully", flush=True)
        
        try:
            from docx import Document
            print("python-docx imported successfully", flush=True)
            docx_available = True
        except ImportError:
            print("WARNING: python-docx not available. Install with:", flush=True)
            print('  & "C:\\Program Files\\Python313\\python.exe" -m pip install python-docx', flush=True)
            docx_available = False
        
        # Setup paths
        script_dir = Path(__file__).parent
        documents_dir = script_dir / 'documents'
        output_file = script_dir / 'extracted_documents.txt'
        
        if not documents_dir.exists():
            print(f"ERROR: {documents_dir} does not exist", flush=True)
            print("Please create the directory and add your PDF/docx files there.", flush=True)
            sys.exit(1)
        
        # Find all PDF and docx files
        pdf_files = sorted(documents_dir.glob('*.pdf'))
        docx_files = sorted(documents_dir.glob('*.docx')) if docx_available else []
        
        all_files = [(f, 'pdf') for f in pdf_files] + [(f, 'docx') for f in docx_files]
        all_files.sort(key=lambda x: x[0].name)
        
        if not all_files:
            print(f"No PDF or docx files found in {documents_dir}", flush=True)
            print("Add your documents and run again.", flush=True)
            sys.exit(0)
        
        print(f"\nFound {len(pdf_files)} PDF(s) and {len(docx_files)} docx file(s)", flush=True)
        print("-" * 60, flush=True)
        
        all_texts = []
        
        # Process each file
        for file_path, file_type in all_files:
            print(f"Reading {file_path.name}...", flush=True)
            
            try:
                if file_type == 'pdf':
                    reader = PdfReader(file_path)
                    text = '\n'.join([page.extract_text() for page in reader.pages])
                    page_count = len(reader.pages)
                    
                elif file_type == 'docx':
                    doc = Document(file_path)
                    paragraphs = [para.text for para in doc.paragraphs]
                    text = '\n'.join(paragraphs)
                    page_count = len(doc.sections)  # Approximate
                
                print(f"  {page_count} pages/sections, {len(text)} chars", flush=True)
                
                all_texts.append({
                    'name': file_path.name,
                    'type': file_type.upper(),
                    'text': text,
                    'pages': page_count
                })
                
            except Exception as e:
                print(f"  ERROR reading {file_path.name}: {e}", flush=True)
                continue
        
        # Write to output file
        print("\n" + "=" * 60, flush=True)
        print("Writing extracted text to file...", flush=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("EXTRACTED DOCUMENTS FOR COPILOT CONTEXT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {Path.cwd()}\n")
            f.write(f"Total documents: {len(all_texts)}\n")
            f.write("=" * 80 + "\n\n\n")
            
            for i, doc_data in enumerate(all_texts, 1):
                f.write(f"DOCUMENT {i}: {doc_data['name']} ({doc_data['type']})\n")
                f.write("=" * 80 + "\n")
                f.write(f"Pages/Sections: {doc_data['pages']}\n")
                f.write(f"Characters: {len(doc_data['text'])}\n\n")
                f.write(doc_data['text'])
                f.write("\n\n" + "=" * 80 + "\n\n\n")
        
        print(f"✓ SUCCESS! Extracted {len(all_texts)} document(s)", flush=True)
        print(f"✓ Output: {output_file.relative_to(Path.cwd())}", flush=True)
        print("\nYou can now reference this file in your Copilot conversations.", flush=True)
        
    except ImportError as e:
        print(f"ERROR: Missing required library - {e}", file=sys.stderr, flush=True)
        print("\nInstall missing libraries:", flush=True)
        print('  & "C:\\Program Files\\Python313\\python.exe" -m pip install pypdf python-docx', flush=True)
        sys.exit(1)
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
