import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import pytesseract
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class BillSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Splitter with Image Processing")
        self.root.geometry("1500x1000")

        # Initialize data structures
        self.participants = []
        self.item_splits = {}

        # Setup the main layout
        self.setup_main_layout()

        # Setup sections
        self.setup_participants_section()
        self.setup_items_section()
        self.setup_image_upload_section()
        self.setup_final_bill_section()

    def setup_main_layout(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

    def setup_participants_section(self):
        self.participants_frame = tk.LabelFrame(
            self.main_frame, text="Participants", padx=10, pady=10
        )
        self.participants_frame.pack(fill="x", padx=10, pady=5)

        # Entry to add participants
        tk.Label(
            self.participants_frame, text="Number of Participants:", font=("Arial", 12)
        ).pack(side="left", padx=5)
        self.num_participants_entry = tk.Entry(
            self.participants_frame, font=("Arial", 12)
        )
        self.num_participants_entry.pack(side="left", padx=5)

        add_participants_button = tk.Button(
            self.participants_frame,
            text="Add Participants",
            font=("Arial", 12),
            command=self.add_participants,
        )
        add_participants_button.pack(side="left", padx=10)

        self.participant_list_frame = tk.Frame(self.participants_frame)
        self.participant_list_frame.pack(fill="x", pady=5)

    def add_participants(self):
        try:
            num_participants = int(self.num_participants_entry.get())
            if num_participants <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid number of participants."
            )
            return

        for widget in self.participant_list_frame.winfo_children():
            widget.destroy()

        self.participants = []
        for i in range(num_participants):
            participant_label = tk.Label(
                self.participant_list_frame,
                text=f"Participant {i + 1} Name:",
                font=("Arial", 12),
            )
            participant_label.grid(row=i, column=0, padx=5, pady=5)
            participant_entry = tk.Entry(
                self.participant_list_frame, font=("Arial", 12)
            )
            participant_entry.grid(row=i, column=1, padx=5, pady=5)
            self.participants.append(participant_entry)

    def setup_items_section(self):
        self.items_frame = tk.LabelFrame(
            self.main_frame, text="Items", padx=10, pady=10
        )
        self.items_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.items_frame, text="Item Name:", font=("Arial", 12)).grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.item_name_entry = tk.Entry(self.items_frame, font=("Arial", 12))
        self.item_name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        tk.Label(self.items_frame, text="Item Price ($):", font=("Arial", 12)).grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.item_price_entry = tk.Entry(self.items_frame, font=("Arial", 12))
        self.item_price_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        tk.Button(
            self.items_frame, text="Add Item", font=("Arial", 12), command=self.add_item
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def add_item(self):
        item_name = self.item_name_entry.get().strip()
        try:
            item_price = float(self.item_price_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid price.")
            return

        if not item_name:
            messagebox.showerror("Invalid Input", "Item name cannot be empty.")
            return

        self.item_splits[item_name] = item_price
        messagebox.showinfo(
            "Success", f"Item '{item_name}' added with price ${item_price:.2f}."
        )

    def setup_image_upload_section(self):
        self.image_upload_frame = tk.LabelFrame(
            self.main_frame, text="Upload Bill Image", padx=10, pady=10
        )
        self.image_upload_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            self.image_upload_frame,
            text="Upload Image",
            font=("Arial", 12),
            command=self.upload_and_process_image,
        ).pack(pady=10)

    def upload_and_process_image(self):
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=(("Image Files", "*.jpg *.png *.jpeg"), ("All Files", "*.*")),
        )
        if not image_path:
            return

        try:
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            text = pytesseract.image_to_string(thresh)
            self.process_extracted_text(text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")

    def process_extracted_text(self, text):
        """
        Process the text extracted from the image.
        Example: Extract item name, price, and tax type from text.
        """
        lines = text.split("\n")
        for line in lines:
            match = re.match(r"(.+?)\s+\$([\d\.]+)", line)
            if match:
                item_name = match.group(1).strip()
                try:
                    item_price = float(match.group(2).strip())
                except ValueError:
                    continue
                self.item_splits[item_name] = item_price

        messagebox.showinfo(
            "Processing Complete", "Bill details have been processed and added."
        )

    def setup_final_bill_section(self):
        self.final_bill_frame = tk.LabelFrame(
            self.main_frame, text="Final Bill", padx=10, pady=10
        )
        self.final_bill_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            self.final_bill_frame,
            text="Show Final Bill",
            font=("Arial", 12),
            command=self.show_final_bill,
        ).pack(pady=10)

    def show_final_bill(self):
        if not self.item_splits:
            messagebox.showinfo("No Items", "No items have been added yet.")
            return

        final_bill_text = "\n".join(
            [f"{name}: ${price:.2f}" for name, price in self.item_splits.items()]
        )
        messagebox.showinfo("Final Bill", final_bill_text)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = BillSplitterApp(root)
    app.run()
