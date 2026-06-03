# OCR Ultra-Tall PDF Screenshots

Common scenario: user screenshots a long article on phone → converts to PDF → sends to Hermes.
The PDF contains a single embedded JPEG that can be 540×30,000+ pixels.

## Detection

```python
import fitz
doc = fitz.open(pdf_path)
page = doc[0]
images = page.get_images()
if images:
    base = doc.extract_image(images[0][0])
    w, h = base["width"], base["height"]
    if h > 4000:  # ultra-tall
        # need chunked OCR
```

## Chunked OCR

Tesseract times out on tall images. Slice into 4000px horizontal strips:

```python
from PIL import Image
img = Image.open(saved_jpeg)
for y in range(0, img.height, 4000):
    chunk = img.crop((0, y, img.width, min(y+4000, img.height)))
    chunk.save(f'/tmp/c_{y}.png')
    # OCR each chunk, concatenate results
```

## Full pipeline

```python
import fitz, subprocess
from PIL import Image

doc = fitz.open(pdf_path)
images = doc[0].get_images()
xref = images[0][0]
base = doc.extract_image(xref)

# Save embedded image
with open('/tmp/tall_img.jpeg', 'wb') as f:
    f.write(base['image'])

# Chunk and OCR
img = Image.open('/tmp/tall_img.jpeg')
results = []
for y in range(0, img.height, 4000):
    bottom = min(y + 4000, img.height)
    chunk = img.crop((0, y, img.width, bottom))
    chunk.save(f'/tmp/c_{y}.png')
    r = subprocess.run(['tesseract', f'/tmp/c_{y}.png', 'stdout', '-l', 'chi_sim'],
                      capture_output=True, text=True, timeout=120)
    if r.stdout.strip():
        results.append(r.stdout.strip())

full_text = '\n'.join(results)
```

## Pitfalls

- **Don't OCR the full image** — Tesseract will silently timeout or produce empty output
- **Use 4000px chunks**, not 5000+ — larger chunks still time out
- **extract_image is on Document, not Page** — `doc.extract_image(xref)`, not `page.extract_image(xref)`
- **Check for embedded images first** — `page.get_images()` may return 0, fallback to `page.get_pixmap(dpi=250)` and OCR that
- DeepSeek models lack vision support — this OCR pipeline is mandatory for image content
