import re
import csv
import logging
import tkinter as tk
from tkinter import filedialog
from typing import Dict, Any, List


# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)


def log_debug_info(step: str, data: Any) -> None:
    """
    Log debugging information at each step of parsing.

    Args:
        step (str): Description of the step being logged.
        data (Any): Data to log.
    """
    logging.debug(f"{step}: {data}")


# Function to clean and normalize text
def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra spaces and fixing common OCR issues.

    Args:
        text (str): Raw text.

    Returns:
        str: Cleaned and normalized text.
    """
    text = re.sub(r"\s{2,}", " ", text)  # Replace multiple spaces with one
    return text.strip()


# Function to parse fields in a line
def parse_fields(line: str) -> Dict[str, Any]:
    """
    Parse fields in a line separated by '|'.

    Args:
        line (str): A single line of text from the receipt.

    Returns:
        dict: Parsed item details or an empty dict if parsing fails.
    """
    fields = [field.strip() for field in line.split("|") if field.strip()]
    if len(fields) >= 3:  # Ensure at least item name, price, and tax class
        try:
            price = float(fields[-2])  # Second last field as price
            tax_class = fields[-1].upper()  # Last field as tax class
            item_name = " ".join(fields[:-2])  # Rest as item name
            return {"name": item_name, "price": price, "tax_class": tax_class}
        except ValueError:
            return {}  # Skip invalid rows
    return {}  # Return empty if insufficient fields


# Function to process receipt text
def parse_aldi_receipt(text: str) -> Dict[str, Any]:
    """
    Parse the Aldi receipt text to extract items, prices, tax classifications, and totals.

    Args:
        text (str): Extracted text from the receipt.

    Returns:
        dict: Parsed receipt details with items, prices, tax info, and totals.
    """
    text = clean_text(text)  # Clean the input text
    lines = text.split("\n")  # Split text into lines

    items = []
    subtotal = 0.0
    total = 0.0

    temp_buffer = ""  # Temporary buffer for incomplete rows

    for line in lines:
        # Check if line contains a valid row using '|' as delimiter
        if "|" in line:
            if temp_buffer:
                line = temp_buffer + " " + line  # Combine with buffered line
                temp_buffer = ""  # Clear the buffer

            parsed_item = parse_fields(line)
            if parsed_item:  # Valid item parsed
                items.append(parsed_item)
            else:
                temp_buffer = line  # Store in buffer for the next line
        else:
            temp_buffer += " " + line  # Accumulate in buffer

        # Check for subtotal and total patterns
        if "SUBTOTAL" in line.upper():
            match = re.search(r"SUBTOTAL[\s|]+([\d\.]+)", line, re.IGNORECASE)
            if match:
                subtotal = float(match.group(1))
        elif "TOTAL" in line.upper():
            match = re.search(r"TOTAL[\s|]+\$?([\d\.]+)", line, re.IGNORECASE)
            if match:
                total = float(match.group(1))

    # If buffer still has content, attempt to parse it
    if temp_buffer:
        parsed_item = parse_fields(temp_buffer)
        if parsed_item:
            items.append(parsed_item)

    return {"items": items, "subtotal": subtotal, "total": total}


# Function to save parsed data to CSV
def save_to_csv(parsed_data: Dict[str, Any], filename: str) -> None:
    """
    Save the parsed receipt data to a CSV file.

    Args:
        parsed_data (dict): Parsed receipt data.
        filename (str): Name of the CSV file to save.
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["Item Name", "Price", "Taxable", "Quantity"])

        # Write items
        for item in parsed_data["items"]:
            writer.writerow(
                [item["name"], item["price"], item["tax_class"], "1"]
            )  # Default quantity to 1

        # Write totals
        writer.writerow([])  # Empty row for separation
        writer.writerow(["Subtotal", parsed_data["subtotal"]])
        writer.writerow(["Total", parsed_data["total"]])


# Main execution block
if __name__ == "__main__":
    # Use tkinter to choose file
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select Receipt Text File", filetypes=[("Text Files", "*.txt")]
    )

    if not file_path:
        print("No file selected.")
    else:
        try:
            with open(file_path, "r") as file:
                receipt_text = file.read()

            # Parse the receipt
            parsed_receipt = parse_aldi_receipt(receipt_text)

            # Debugging output
            log_debug_info("Parsed Receipt", parsed_receipt)

            # Save to CSV
            save_to_csv(parsed_receipt, "aldi_receipt.csv")

            print("Parsed receipt saved to aldi_receipt.csv")
        except FileNotFoundError:
            print("The specified file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
