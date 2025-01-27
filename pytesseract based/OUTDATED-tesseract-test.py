import pytesseract
import cv2
from tkinter import filedialog
from PIL import Image

# Set the path to Tesseract executable (modify as per your installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_path):
    """
    Extracts text from an image using Tesseract OCR.
    :param image_path: Path to the image file.
    :return: Extracted text.
    """
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)

        # Convert to grayscale for better OCR accuracy
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to clean up the image
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Use Tesseract to extract text
        extracted_text = pytesseract.image_to_string(thresh)

        return extracted_text
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    print("Select an image file to process...")

    # Open a file dialog to select the image
    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=(("Image Files", "*.jpg *.png *.jpeg"), ("All Files", "*.*")),
    )

    if not image_path:
        print("No file selected. Exiting.")
    else:
        print(f"Processing image: {image_path}")
        text = extract_text_from_image(image_path)

        if text:
            print("\nExtracted Text:")
            print(text)
        else:
            print("No text extracted.")
