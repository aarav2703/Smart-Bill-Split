import os
from tkinter import filedialog, Tk
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import cv2


def extract_text_with_trocr(image_path):
    """
    Extracts text from an image using TrOCR.
    :param image_path: Path to the image file.
    :return: Extracted text.
    """
    try:
        # Load the model and processor
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained(
            "microsoft/trocr-base-handwritten"
        )

        # Load and preprocess the image
        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(images=image, return_tensors="pt").pixel_values

        # Perform OCR
        generated_ids = model.generate(pixel_values)
        extracted_text = processor.batch_decode(
            generated_ids, skip_special_tokens=True
        )[0]

        return extracted_text
    except Exception as e:
        print(f"Error during text extraction: {e}")
        return None


def save_text_to_file(text, image_path):
    """
    Saves the extracted text to the ./data directory with a name derived from the image file.
    :param text: The text to save.
    :param image_path: Path to the original image file.
    """
    try:
        # Create the ./data directory if it doesn't exist
        os.makedirs("./results/trOCR", exist_ok=True)

        # Get the base name of the image file without extension
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        # Define the save path
        save_path = os.path.join("./results/trOCR", f"{base_name}_text.txt")

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
        text = extract_text_with_trocr(image_path)

        if text:
            print("\nExtracted Text:")
            print(text)

            # Automatically save the text
            save_text_to_file(text, image_path)
        else:
            print("No text extracted.")
