import fitz
import pytesseract

from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import re

# --------------------------------------------------
# TESSERACT OCR CONFIGURATION
# --------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# --------------------------------------------------
# CHECK WHETHER EXTRACTED TEXT IS GOOD
# --------------------------------------------------

def text_quality(text):

    if not text:
        return 0

    text = text.strip()

    if len(text) < 20:
        return 0

    total_chars = len(text)

    useful_chars = len(
        re.findall(r"[A-Za-z0-9]", text)
    )

    return useful_chars / total_chars


# --------------------------------------------------
# CLEAN OCR TEXT
# --------------------------------------------------

def clean_text(text):

    if not text:
        return ""

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove strange control characters
    text = re.sub(
        r"[^\x09\x0A\x0D\x20-\x7E₹]",
        " ",
        text
    )

    # Fix spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    return text.strip()


# --------------------------------------------------
# OCR A SINGLE PAGE
# --------------------------------------------------

def perform_ocr(page):

    print("Running OCR on page...")

    # Render page at high resolution
    pix = page.get_pixmap(
        matrix=fitz.Matrix(3, 3),
        alpha=False
    )

    image_bytes = pix.tobytes("png")

    image = Image.open(
        BytesIO(image_bytes)
    )

    # Convert to grayscale
    image = image.convert("L")

    # Improve contrast
    image = ImageEnhance.Contrast(image).enhance(2.0)

    # Sharpen image
    image = image.filter(
        ImageFilter.SHARPEN
    )

    # OCR configuration
    config = "--oem 3 --psm 6"

    ocr_text = pytesseract.image_to_string(
        image,
        config=config
    )

    return clean_text(ocr_text)


# --------------------------------------------------
# EXTRACT TEXT FROM PDF
# --------------------------------------------------

def extract_text(pdf_path):

    final_text = ""

    try:

        document = fitz.open(pdf_path)

        print("===================================")
        print("PDF opened successfully")
        print("Number of pages:", len(document))
        print("===================================")

        for page_number, page in enumerate(
            document,
            start=1
        ):

            print(
                f"\n========== PAGE {page_number} =========="
            )

            # ------------------------------------------
            # STEP 1: NORMAL PDF TEXT EXTRACTION
            # ------------------------------------------

            native_text = page.get_text(
                "text"
            ).strip()

            quality = text_quality(
                native_text
            )

            print(
                "Native text length:",
                len(native_text)
            )

            print(
                "Text quality:",
                round(quality, 2)
            )

            # ------------------------------------------
            # STEP 2: DECIDE WHETHER OCR IS REQUIRED
            # ------------------------------------------

            if quality >= 0.55:

                print(
                    "Good text layer detected."
                )

                page_text = native_text

            else:

                print(
                    "Poor or missing text layer."
                )

                print(
                    "Using Tesseract OCR..."
                )

                page_text = perform_ocr(
                    page
                )

                print(
                    "OCR text length:",
                    len(page_text)
                )

            # ------------------------------------------
            # STEP 3: ADD PAGE TEXT
            # ------------------------------------------

            if page_text:

                final_text += (
                    f"\n[Page {page_number}]\n"
                )

                final_text += (
                    page_text + "\n"
                )

        document.close()

        # ------------------------------------------
        # FINAL CLEANING
        # ------------------------------------------

        final_text = clean_text(
            final_text
        )

        print("\n===================================")
        print("FINAL EXTRACTED TEXT")
        print("===================================")

        print(final_text)

        print("\n===================================")
        print(
            "FINAL TEXT LENGTH:",
            len(final_text)
        )
        print("===================================")

        return final_text

    except Exception as e:

        print(
            "\nPDF EXTRACTION ERROR:"
        )

        print(
            type(e).__name__,
            str(e)
        )

        return ""