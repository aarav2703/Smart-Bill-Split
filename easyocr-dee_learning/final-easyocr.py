import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import easyocr
import cv2
from tkinter import filedialog, Tk


def extract_text_with_easyocr(image_path):
    """
    Extracts text from an image using EasyOCR.
    :param image_path: Path to the image file.
    :return: Extracted text and bounding box data.
    """
    try:
        # Initialize the EasyOCR reader
        reader = easyocr.Reader(["en"], gpu=False)  # Set gpu=True if GPU is available

        # Read the text from the image
        results = reader.readtext(image_path)

        # Combine all detected text into a single string
        extracted_text = "\n".join([result[1] for result in results])

        return extracted_text, results
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def save_annotated_image(image_path, results, output_dir="./results/easyOCR"):
    """
    Saves the annotated image with bounding boxes and text overlay.
    :param image_path: Path to the original image file.
    :param results: OCR results containing bounding boxes, text, and confidence.
    :param output_dir: Directory to save the annotated image.
    """
    try:
        # Load the original image
        image = cv2.imread(image_path)

        # Draw bounding boxes and overlay text
        for bbox, text, confidence in results:
            # Extract the bounding box coordinates
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))

            # Draw the bounding box
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

            # Overlay the text and confidence score
            label = f"{text} ({confidence:.2f})"
            cv2.putText(
                image,
                label,
                (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2,
            )

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Save the annotated image
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        save_path = os.path.join(output_dir, f"{base_name}_annotated.jpg")
        cv2.imwrite(save_path, image)

        print(f"Annotated image saved successfully to {save_path}")

        # Display the annotated image
        cv2.imshow("Annotated Image", image)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error saving or displaying annotated image: {e}")


def save_text_to_file(text, image_path):
    """
    Saves the extracted text to the ./data directory with a name derived from the image file.
    :param text: The text to save.
    :param image_path: Path to the original image file.
    """
    try:
        # Create the ./data directory if it doesn't exist
        os.makedirs("./results/easyOCR", exist_ok=True)

        # Get the base name of the image file without extension
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        # Define the save path
        save_path = os.path.join("./results/easyOCR", f"{base_name}_text.txt")

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
        text, results = extract_text_with_easyocr(image_path)

        if text:
            print("\nExtracted Text:")
            print(text)

            # Automatically save the text
            save_text_to_file(text, image_path)

            # Save and display the annotated image
            save_annotated_image(image_path, results)
        else:
            print("No text extracted.")
