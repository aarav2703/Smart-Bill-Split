import os
import pytesseract
import cv2
from tkinter import filedialog, Tk


# Set the path to Tesseract executable (modify as per your installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_with_confidence(image_path):
    """
    Extracts text from an image and provides bounding boxes with confidence levels.
    :param image_path: Path to the image file.
    :return: Extracted text and bounding box data.
    """
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)

        # Convert to grayscale for better OCR accuracy
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to clean up the image
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Get OCR data with bounding boxes and confidence levels
        ocr_data = pytesseract.image_to_data(
            thresh, output_type=pytesseract.Output.DICT
        )

        return ocr_data
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_annotated_image(image_path, ocr_data, output_dir="./results/pytesseract"):
    """
    Saves the annotated image with bounding boxes and text overlay.
    :param image_path: Path to the original image file.
    :param ocr_data: OCR data containing bounding boxes, text, and confidence.
    :param output_dir: Directory to save the annotated image.
    """
    try:
        # Load the original image
        image = cv2.imread(image_path)

        # Iterate through the OCR data and annotate the image
        for i in range(len(ocr_data["text"])):
            if int(ocr_data["conf"][i]) > 0:  # Consider only positive confidence levels
                x, y, w, h = (
                    ocr_data["left"][i],
                    ocr_data["top"][i],
                    ocr_data["width"][i],
                    ocr_data["height"][i],
                )
                text = ocr_data["text"][i]
                conf = float(ocr_data["conf"][i])

                # Draw the bounding box
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Overlay the text and confidence score
                label = f"{text} ({conf:.2f})"
                cv2.putText(
                    image,
                    label,
                    (x, y - 10),
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
        ocr_data = extract_text_with_confidence(image_path)

        if ocr_data:
            # Combine the extracted text for display
            extracted_text = "\n".join(
                [text for text in ocr_data["text"] if text.strip()]
            )
            print("\nExtracted Text:")
            print(extracted_text)

            # Save and display the annotated image
            save_annotated_image(image_path, ocr_data)
        else:
            print("No text extracted.")
