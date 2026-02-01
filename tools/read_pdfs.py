import sys
import os

try:
    from pypdf import PdfReader
    print("pypdf imported successfully", flush=True)
    
    # Base path - adjust if needed
    base_path = r'c:\Users\takahashi\GitHub\modeling-vs-model_free\reference_papers'
    
    # Papers to read
    papers = [
        '2018, Alejandro Panjkovich.pdf',
        '2021, Petr V. Konarev.pdf', 
        '2021, Steve P. Meisburger.pdf',
        '2021, Steve P. Meisburger-support.pdf',
        '2024, Jesse B. Hopkins.pdf',
        '2004, Joaquim Jaumot.pdf',
        '2018, Mackenzie J. Parker.pdf',
        '2018, Mackenzie J. Parker-appendix.pdf',
        '2025, Boyang Zhang.pdf'
    ]
    
    all_texts = []
    
    for paper in papers:
        print(f"Reading {paper}...", flush=True)
        pdf_path = os.path.join(base_path, paper)
        
        if not os.path.exists(pdf_path):
            print(f"WARNING: {paper} not found, skipping...", flush=True)
            continue
            
        reader = PdfReader(pdf_path)
        text = '\n'.join([page.extract_text() for page in reader.pages])
        print(f"  {len(reader.pages)} pages, {len(text)} chars", flush=True)
        
        all_texts.append({
            'name': paper,
            'text': text,
            'pages': len(reader.pages)
        })
    
    # Write to file in tools folder
    print("Writing to file...", flush=True)
    output_path = r'c:\Users\takahashi\GitHub\modeling-vs-model_free\tools\extracted_papers.txt'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, paper_data in enumerate(all_texts, 1):
            f.write(f"PAPER {i}: {paper_data['name']}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Pages: {paper_data['pages']}\n\n")
            f.write(paper_data['text'])
            f.write("\n\n" + "=" * 80 + "\n\n\n")
    
    print(f"SUCCESS! Extracted {len(all_texts)} papers to tools/extracted_papers.txt", flush=True)
    
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
