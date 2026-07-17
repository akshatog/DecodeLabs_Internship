"""
Project 4: Building the Machine's Optic Nerve
DecodeLabs — Industrial Training Kit (Batch 2026)

Path 1: Optical Character Recognition (OCR)
Engine: pytesseract (Python wrapper for Google's Tesseract, CNN + BiLSTM
under the hood) — extracting machine-readable text from raw images.

The Gatekeeper Rule (4 validations your script must pass, slide 17):
  1. LIBRARY INTEGRATION   -> seamless, error-free pytesseract implementation
  2. PRE-PROCESSING INTEGRITY -> grayscale + adaptive thresholding to
                                  separate foreground text from noise
  3. ACCURACY BENCHMARKING -> minimum validated confidence of 80% (0.80)
                               on the final output — this is the hard
                               minimum standard set in the brief
  4. VISUAL CONFIRMATION   -> a pristine, legible output showing exactly
                               what passed and what got filtered out
"""

import cv2
import pytesseract
from pytesseract import Output

CONFIDENCE_THRESHOLD = 80  # The 80% Gate (slide 16) — hard minimum per spec


def load_image(path):
    """Load an image from disk with OpenCV (BGR format)."""
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Could not read image at: {path}")
    return image


def preprocess(image):
    """
    PHASE: Systematic Image Pre-Processing (slides 11-12)

    Step 1 — Grayscale: collapse the 3D RGB matrix into a 1D intensity
             matrix, removing distracting color data.
    Step 2 — Gaussian Blur: smooth out micro-imperfections and noise
             before we force the binary black/white decision.
    Step 3 — Adaptive Thresholding (Otsu's method): forces every pixel to
             choose a side — pure black or pure white — for maximum
             contrast on character contours.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Otsu's method auto-picks the cutoff intensity (the "Cutoff: 88" idea
    # from slide 12) instead of us hardcoding a threshold value.
    _, thresholded = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresholded


def run_ocr(processed_image, psm=6):
    """
    PHASE: Library Integration
    Run pytesseract on the pre-processed image and get word-level data
    (text + confidence per word), not just a flat string — we need the
    per-word confidence to apply the 80% gate.

    PSM modes (slide 10):
      --psm 3  : fully automatic, varied layouts (default)
      --psm 6  : single uniform block of text (good for clean documents)
      --psm 7  : single text line (plates, headers)
      --psm 11 : sparse, scattered text (invoices)
    """
    config = f"--psm {psm}"
    data = pytesseract.image_to_data(
        processed_image, config=config, output_type=Output.DICT
    )
    return data


def apply_confidence_gate(ocr_data, threshold=CONFIDENCE_THRESHOLD):
    """
    PHASE: Accuracy Benchmarking — The 80% Gate (slide 16)

      if confidence >= 0.80: draw_box_and_label()
      else: drop_detection()

    Tesseract reports confidence as 0-100 (not 0-1), and uses -1 for
    non-text regions (spaces, layout blocks) — those get dropped too.
    """
    accepted, rejected = [], []
    n_boxes = len(ocr_data["text"])

    for i in range(n_boxes):
        text = ocr_data["text"][i].strip()
        conf = int(float(ocr_data["conf"][i]))

        if not text or conf < 0:
            continue  # empty / non-text region, not a real detection

        entry = {
            "text": text,
            "confidence": conf,
            "bbox": (
                ocr_data["left"][i],
                ocr_data["top"][i],
                ocr_data["width"][i],
                ocr_data["height"][i],
            ),
        }

        if conf >= threshold:
            accepted.append(entry)
        else:
            rejected.append(entry)

    return accepted, rejected


def draw_annotations(image, accepted_words, output_path="ocr_output.png"):
    """
    PHASE: Visual Confirmation
    Draw a bounding box + label around every word that PASSED the 80%
    gate, and save a pristine annotated image as proof of the pipeline.
    """
    annotated = image.copy()
    for word in accepted_words:
        x, y, w, h = word["bbox"]
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 200, 0), 2)
        label = f"{word['text']} ({word['confidence']}%)"
        cv2.putText(
            annotated, label, (x, max(y - 6, 0)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1, cv2.LINE_AA
        )
    cv2.imwrite(output_path, annotated)
    return output_path


def recognize_text(image_path, psm=6, threshold=CONFIDENCE_THRESHOLD, save_annotated=True):
    """End-to-end pipeline: load -> preprocess -> OCR -> confidence gate -> display."""
    image = load_image(image_path)
    processed = preprocess(image)
    ocr_data = run_ocr(processed, psm=psm)
    accepted, rejected = apply_confidence_gate(ocr_data, threshold=threshold)

    print(f"=== OCR Results for '{image_path}' (PSM={psm}, threshold={threshold}%) ===\n")

    if accepted:
        full_text = " ".join(w["text"] for w in accepted)
        print("PASSED (>= threshold) — final machine-readable text:")
        print(f'  "{full_text}"\n')
        print("Word-level breakdown:")
        for w in accepted:
            print(f"  '{w['text']}'  confidence={w['confidence']}%  bbox={w['bbox']}")
    else:
        print("No words passed the confidence gate.")

    if rejected:
        print(f"\nDROPPED (< {threshold}% confidence, {len(rejected)} word(s)):")
        for w in rejected:
            print(f"  '{w['text']}'  confidence={w['confidence']}%")

    if save_annotated and accepted:
        out_path = draw_annotations(image, accepted)
        print(f"\nAnnotated visual confirmation saved to: {out_path}")

    return accepted, rejected


if __name__ == "__main__":
    import sys
    image_path = sys.argv[1] if len(sys.argv) > 1 else "sample_invoice.png"
    recognize_text(image_path)