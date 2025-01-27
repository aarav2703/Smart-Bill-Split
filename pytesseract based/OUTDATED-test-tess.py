import os
import pytesseract
import cv2
import numpy as np
from tkinter import filedialog, Tk
from PIL import Image

# Set the path to Tesseract executable (modify as per your installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_path):
    """
    Preprocesses the image for better OCR results.
    :param image_path: Path to the image file.
    :return: Preprocessed image.
    """
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Denoise the image using median blur
        denoised = cv2.medianBlur(binary, 3)

        # Resize the image for better OCR accuracy
        resized = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # Deskew the image if it is skewed
        coords = np.column_stack(np.where(resized > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = resized.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed = cv2.warpAffine(
            resized, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )

        return deskewed
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None


def extract_text_from_image(image_path):
    """
    Extracts text from an image using Tesseract OCR.
    :param image_path: Path to the image file.
    :return: Extracted text.
    """
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)

        if processed_image is None:
            return None

        # Define custom Tesseract configuration
        custom_config = r"--oem 1 --psm 6"

        # Use Tesseract to extract text
        extracted_text = pytesseract.image_to_string(
            processed_image, config=custom_config
        )

        return extracted_text
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_text_to_file(text, image_path):
    """
    Saves the extracted text to the ./data directory with a name derived from the image file.
    :param text: The text to save.
    :param image_path: Path to the original image file.
    """
    try:
        # Create the ./data directory if it doesn't exist
        os.makedirs("./results/pytesseract", exist_ok=True)

        # Get the base name of the image file without extension
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        # Define the save path
        save_path = os.path.join("./results/pytesseract", f"{base_name}_text.txt")

        # Write the text to the file
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Text saved successfully to {save_path}")
    except Exception as e:
        print(f"Error saving text: {e}")


if __name__ == "__main__":
    # Hide the main tkinter root window
    root = Tk()
    root.withdraw()

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

            # Automatically save the text
            save_text_to_file(text, image_path)
        else:
            print("No text extracted.")
