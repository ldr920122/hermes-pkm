# PDF Text Extraction on macOS

base macOS does not ship `pdftotext`. The fallback chain is:

1. **pdftotext** (poppler-utils) — fastest, best layout preservation
   ```bash
   brew install poppler
   pdftotext -layout input.pdf -
   ```

2. **pymupdf (fitz)** — pure Python, good for scripts
   ```bash
   pip3 install pymupdf
   ```
   ```python
   import fitz
   doc = fitz.open(path)
   text = ''
   for page in doc:
       text += page.get_text()
   doc.close()
   ```

3. **textutil** — does NOT handle PDF. Only `.doc`, `.docx`, `.rtf`, `.html`, `.odt`.

4. **python-docx** — does NOT handle PDF. Only `.docx`.

## Image-only pages

Some PDFs (especially Chinese government/organization notifications) have scanned
image pages with no selectable text. Detect them:

```python
import fitz
doc = fitz.open(path)
for i in range(doc.page_count):
    t = doc[i].get_text().strip()
    imgs = doc[i].get_images()
    if not t and imgs:
        print(f'Page {i+1}: image-only, {len(imgs)} image(s) — needs OCR')
    elif t:
        print(f'Page {i+1}: {len(t)} chars')
```

To extract an image for later OCR (e.g. via vision tools):

```python
page = doc[0]  # 0-indexed
pix = page.get_pixmap(dpi=200)
pix.save('/tmp/page.png')
```

The text pages (typically attachments/appendices after the body) are usually
sufficient to identify grant directions, deadlines, and requirements. Only
resort to OCR if critical info (deadline, eligibility) lives in the image pages.

## Detection script

```python
import subprocess

def extract_pdf_text(path):
    # Try pdftotext first
    try:
        result = subprocess.run(['pdftotext', '-layout', path, '-'],
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except:
        pass

    # Fallback to pymupdf
    try:
        import fitz
        doc = fitz.open(path)
        text = ''.join(page.get_text() for page in doc)
        doc.close()
        return text
    except ImportError:
        pass

    raise RuntimeError('No PDF extraction method available. Install pdftotext (brew install poppler) or pymupdf (pip3 install pymupdf)')
```
