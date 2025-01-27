import tkinter as tk
from tkinter import ttk, messagebox
import csv


class BillSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Splitter")
        self.root.geometry("1500x1000")  # Increased size for better layout

        # Initialize data structures
        self.participants = []
        self.categories = {"Groceries (non-taxable)": 0.0}
        self.item_splits = {}  # Key: unique item identifier, Value: item details

        # Setup the main layout with a canvas and scrollbar
        self.setup_main_layout()

        # Setup all sections
        self.setup_participants_section()
        self.setup_items_section()
        self.setup_categories_section()
        self.setup_final_bill_section()

    def setup_main_layout(self):
        # Create a canvas with a scrollbar for the scrollable frame
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(
            self.root, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def setup_participants_section(self):
        # Participants section
        self.participants_frame = tk.LabelFrame(
            self.scrollable_frame, text="Participants", padx=10, pady=10
        )
        self.participants_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Number of Participants
        num_people_label = tk.Label(
            self.participants_frame,
            text="Number of people:",
            font=("Arial", 12, "bold"),
        )
        num_people_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.num_people_entry = tk.Entry(self.participants_frame, font=("Arial", 12))
        self.num_people_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        add_participants_btn = tk.Button(
            self.participants_frame,
            text="Add Participants",
            command=self.add_participants,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        add_participants_btn.grid(
            row=1, column=0, columnspan=2, pady=10, padx=5, sticky="w"
        )

        # Frame to hold participant name entries
        self.participant_names_frame = tk.Frame(self.participants_frame)
        self.participant_names_frame.grid(
            row=2, column=0, columnspan=2, pady=10, padx=5, sticky="w"
        )

        # Button to show participant checkboxes
        show_checkboxes_btn = tk.Button(
            self.participants_frame,
            text="Show Participant Checkboxes",
            command=self.show_participant_checkboxes,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        show_checkboxes_btn.grid(
            row=3, column=0, columnspan=2, pady=5, padx=5, sticky="w"
        )

        # Frame to hold participant checkboxes
        self.participant_checkboxes_frame = tk.Frame(self.participants_frame)
        self.participant_checkboxes_frame.grid(
            row=4, column=0, columnspan=2, pady=10, padx=5, sticky="w"
        )

    def add_participants(self):
        try:
            num_people = int(self.num_people_entry.get())
            if num_people <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid number of people (positive integer)."
            )
            return

        # Clear existing entries
        for widget in self.participant_names_frame.winfo_children():
            widget.destroy()
        self.participants.clear()

        # Create entry fields for participant names
        for i in range(num_people):
            label = tk.Label(
                self.participant_names_frame,
                text=f"Participant {i + 1} Name:",
                font=("Arial", 12, "bold"),
            )
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tk.Entry(self.participant_names_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.participants.append(entry)

    def show_participant_checkboxes(self):
        # Clear existing checkboxes
        for widget in self.participant_checkboxes_frame.winfo_children():
            widget.destroy()

        self.participant_vars = []  # To store variables associated with checkboxes

        # Create checkboxes for each participant
        for i, entry in enumerate(self.participants):
            name = entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Participant names cannot be empty!")
                return
            var = tk.IntVar()
            checkbox = tk.Checkbutton(
                self.participant_checkboxes_frame,
                text=name,
                variable=var,
                font=("Arial", 12),
            )
            checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.participant_vars.append((name, var))

    def setup_items_section(self):
        # Items section
        self.items_frame = tk.LabelFrame(
            self.scrollable_frame, text="Items", padx=10, pady=10
        )
        self.items_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

        # Item Name
        item_name_label = tk.Label(
            self.items_frame, text="Item Name:", font=("Arial", 12, "bold")
        )
        item_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.item_name_entry = tk.Entry(self.items_frame, font=("Arial", 12))
        self.item_name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Item Price
        item_price_label = tk.Label(
            self.items_frame, text="Item Price ($):", font=("Arial", 12, "bold")
        )
        item_price_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.item_price_entry = tk.Entry(self.items_frame, font=("Arial", 12))
        self.item_price_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Item Quantity
        item_quantity_label = tk.Label(
            self.items_frame, text="Item Quantity:", font=("Arial", 12, "bold")
        )
        item_quantity_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.item_quantity_entry = tk.Entry(self.items_frame, font=("Arial", 12))
        self.item_quantity_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Category
        category_label = tk.Label(
            self.items_frame, text="Category:", font=("Arial", 12, "bold")
        )
        category_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.category_var = tk.StringVar(value="Groceries (non-taxable)")
        self.category_dropdown = ttk.Combobox(
            self.items_frame,
            textvariable=self.category_var,
            values=list(self.categories.keys()),
            state="readonly",
            width=30,
            font=("Arial", 12),
        )
        self.category_dropdown.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Add Item Button
        add_item_btn = tk.Button(
            self.items_frame,
            text="Add Item",
            command=self.add_item,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        add_item_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky="w")

        # Info Label
        quantity_info_label = tk.Label(
            self.items_frame,
            text="For each participant, enter the quantity or leave blank for equal split",
            font=("Arial", 12, "bold"),
        )
        quantity_info_label.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w"
        )

        # Listbox to show added items
        self.added_items_box = tk.Listbox(
            self.items_frame, width=100, height=10, font=("Arial", 12)
        )
        self.added_items_box.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def add_item(self):
        # Collect responsible participants
        responsible_people = [
            name for name, var in self.participant_vars if var.get() == 1
        ]

        if not responsible_people:
            messagebox.showerror(
                "Error", "At least one participant must be selected for each item."
            )
            return

        item_name = self.item_name_entry.get().strip()
        if not item_name:
            messagebox.showerror("Error", "Item name cannot be empty.")
            return

        try:
            item_price = float(self.item_price_entry.get())
            if item_price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid non-negative price.")
            return

        try:
            item_quantity = int(self.item_quantity_entry.get())
            if item_quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid quantity (positive integer)."
            )
            return

        category = self.category_var.get()
        tax_rate = self.categories.get(category, 0.0)

        # Create a unique identifier for the item
        item_id = f"{item_name}_{len(self.item_splits) + 1}"

        # Create a sub-frame for split inputs
        split_frame = tk.LabelFrame(
            self.items_frame, text=f"Split for '{item_name}'", padx=10, pady=10
        )
        split_frame.grid(
            row=len(self.item_splits) + 7,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="w",
        )

        split_entries = {}

        for i, person in enumerate(responsible_people):
            split_label = tk.Label(
                split_frame, text=f"{person}'s Quantity:", font=("Arial", 12)
            )
            split_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            split_entry = tk.Entry(split_frame, font=("Arial", 12))
            split_entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            split_entries[person] = split_entry

        # Store item details
        self.item_splits[item_id] = {
            "name": item_name,
            "price": item_price,
            "quantity": item_quantity,
            "category": category,
            "tax_rate": tax_rate,
            "responsible_people": responsible_people,
            "split_entries": split_entries,
        }

        # Add item to the listbox
        self.added_items_box.insert(
            tk.END,
            f"{item_name} - ${item_price:.2f} x {item_quantity} - {category} - Split among {', '.join(responsible_people)}",
        )

        # Clear item entry fields
        self.item_name_entry.delete(0, tk.END)
        self.item_price_entry.delete(0, tk.END)
        self.item_quantity_entry.delete(0, tk.END)

    def setup_categories_section(self):
        # Category management section
        self.categories_frame = tk.LabelFrame(
            self.scrollable_frame, text="Category Management", padx=10, pady=10
        )
        self.categories_frame.grid(
            row=0, column=1, rowspan=2, padx=20, pady=10, sticky="nw"
        )

        # New Category Name
        category_name_label = tk.Label(
            self.categories_frame, text="Category Name:", font=("Arial", 12, "bold")
        )
        category_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=(10, 0))

        self.category_name_entry = tk.Entry(self.categories_frame, font=("Arial", 12))
        self.category_name_entry.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Tax Rate
        tax_rate_label = tk.Label(
            self.categories_frame, text="Tax Rate (%):", font=("Arial", 12, "bold")
        )
        tax_rate_label.grid(row=2, column=0, sticky="w", padx=5, pady=(10, 0))

        self.tax_rate_entry = tk.Entry(self.categories_frame, font=("Arial", 12))
        self.tax_rate_entry.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        # Add Category Button
        add_category_btn = tk.Button(
            self.categories_frame,
            text="Add Category",
            command=self.add_category,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        add_category_btn.grid(row=4, column=0, pady=10, padx=5, sticky="w")

        # Listbox to show added categories
        self.added_categories_box = tk.Listbox(
            self.categories_frame, height=6, width=40, font=("Arial", 12)
        )
        self.added_categories_box.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    def add_category(self):
        new_category = self.category_name_entry.get().strip()
        if not new_category:
            messagebox.showerror("Error", "Category name cannot be empty.")
            return

        try:
            tax_rate = float(self.tax_rate_entry.get())
            if tax_rate < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid non-negative tax rate.")
            return

        if new_category in self.categories:
            messagebox.showerror("Error", "This category already exists.")
            return

        self.categories[new_category] = tax_rate
        self.category_dropdown["values"] = list(self.categories.keys())
        self.added_categories_box.insert(tk.END, f"{new_category} - Tax: {tax_rate}%")

        # Clear input fields
        self.category_name_entry.delete(0, tk.END)
        self.tax_rate_entry.delete(0, tk.END)

    def setup_final_bill_section(self):
        # Final bill section
        self.final_bill_frame = tk.LabelFrame(
            self.scrollable_frame, text="Final Bill", padx=10, pady=10
        )
        self.final_bill_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        # Discount
        discount_label = tk.Label(
            self.final_bill_frame,
            text="Apply Discount (%):",
            font=("Arial", 12, "bold"),
        )
        discount_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.discount_entry = tk.Entry(self.final_bill_frame, font=("Arial", 12))
        self.discount_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Show Split Button
        show_split_btn = tk.Button(
            self.final_bill_frame,
            text="Show Split",
            command=self.show_split,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        show_split_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=5, sticky="w")

        # Treeview for displaying detailed splits
        self.result_box = ttk.Treeview(
            self.final_bill_frame,
            columns=(
                "Participant",
                "Total Before Tax",
                "Taxable Amount",
                "Tax Paid",
                "Total Owed",
            ),
            show="headings",
        )
        self.result_box.heading("Participant", text="Participant")
        self.result_box.heading("Total Before Tax", text="Total Before Tax")
        self.result_box.heading("Taxable Amount", text="Taxable Amount")
        self.result_box.heading("Tax Paid", text="Tax Paid")
        self.result_box.heading("Total Owed", text="Total Owed")

        # Configure column widths
        self.result_box.column("Participant", anchor="center", width=150)
        self.result_box.column("Total Before Tax", anchor="center", width=150)
        self.result_box.column("Taxable Amount", anchor="center", width=150)
        self.result_box.column("Tax Paid", anchor="center", width=150)
        self.result_box.column("Total Owed", anchor="center", width=150)

        self.result_box.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Aggregate Details Labels
        self.total_amount_label = tk.Label(
            self.final_bill_frame,
            text="Total Amount: $0.00",
            font=("Arial", 12, "bold"),
        )
        self.total_amount_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.taxable_amount_label = tk.Label(
            self.final_bill_frame,
            text="Total Taxable Amount: $0.00",
            font=("Arial", 12, "bold"),
        )
        self.taxable_amount_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.non_taxable_amount_label = tk.Label(
            self.final_bill_frame,
            text="Total Non-Taxable Amount: $0.00",
            font=("Arial", 12, "bold"),
        )
        self.non_taxable_amount_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)

        self.amount_before_discount_label = tk.Label(
            self.final_bill_frame,
            text="Amount Before Discount: $0.00",
            font=("Arial", 12, "bold"),
        )
        self.amount_before_discount_label.grid(
            row=6, column=0, sticky="w", padx=5, pady=5
        )

        self.amount_after_discount_label = tk.Label(
            self.final_bill_frame,
            text="Amount After Discount: $0.00",
            font=("Arial", 12, "bold"),
        )
        self.amount_after_discount_label.grid(
            row=7, column=0, sticky="w", padx=5, pady=5
        )

        # Export and Reset Buttons
        export_btn = tk.Button(
            self.final_bill_frame,
            text="Export to CSV",
            command=self.export_to_csv,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        export_btn.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        reset_btn = tk.Button(
            self.final_bill_frame,
            text="Reset Bill",
            command=self.reset_bill,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        reset_btn.grid(row=8, column=1, padx=10, pady=10, sticky="e")

    def calculate_final_bill(self):
        # Initialize totals with detailed breakdown
        totals = {
            entry.get().strip(): {
                "total_before_tax": 0.0,
                "taxable": 0.0,
                "tax": 0.0,
                "total_owed": 0.0,
            }
            for entry in self.participants
        }

        # Initialize aggregate variables
        aggregate_total_before_tax = 0.0
        aggregate_taxable = 0.0
        aggregate_non_taxable = 0.0
        aggregate_tax_paid = 0.0
        aggregate_total = 0.0

        # Handle empty discount field by setting discount to 0 if left blank
        try:
            discount = (
                float(self.discount_entry.get()) / 100
                if self.discount_entry.get()
                else 0.0
            )
            if not (0 <= discount < 1):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid discount value between 0 and 100."
            )
            return None

        # Iterate through each item to calculate splits
        for item_id, details in self.item_splits.items():
            price = details["price"]
            quantity = details["quantity"]
            category = details["category"]
            tax_rate = details["tax_rate"]
            responsible_people = details["responsible_people"]
            split_entries = details["split_entries"]

            total_price = price * quantity
            tax_amount = total_price * (tax_rate / 100) if tax_rate > 0 else 0.0
            total_price_with_tax = total_price + tax_amount

            # Apply discount
            total_price_with_tax *= 1 - discount
            tax_amount *= 1 - discount

            # Update aggregate amounts before discount
            aggregate_total_before_tax += price * quantity

            # Calculate specified and unspecified quantities
            specified_quantities = 0.0
            unspecified_participants = []
            per_person_quantity = {}

            for person in responsible_people:
                qty_entry = split_entries[person].get().strip()
                if qty_entry:
                    try:
                        qty = float(qty_entry)
                        if qty < 0:
                            raise ValueError
                        per_person_quantity[person] = qty
                        specified_quantities += qty
                    except ValueError:
                        messagebox.showerror(
                            "Error",
                            f"Please enter a valid non-negative quantity for {person} in item '{details['name']}'.",
                        )
                        return None
                else:
                    unspecified_participants.append(person)

            # Calculate equal split for unspecified quantities
            remaining_quantity = quantity - specified_quantities
            if remaining_quantity < 0:
                messagebox.showerror(
                    "Error",
                    f"The total specified quantities for item '{details['name']}' exceed the total quantity.",
                )
                return None

            equal_split = (
                remaining_quantity / len(unspecified_participants)
                if unspecified_participants
                else 0.0
            )

            for person in unspecified_participants:
                per_person_quantity[person] = equal_split

            # Now, calculate each person's share based on their quantity
            for person, qty in per_person_quantity.items():
                if quantity == 0:
                    person_share_before_tax = 0.0
                    taxable_share = 0.0
                    tax_share = 0.0
                    person_total = 0.0
                else:
                    person_share_before_tax = (qty / quantity) * total_price
                    taxable_share = (
                        (qty / quantity) * total_price if tax_rate > 0 else 0.0
                    )
                    tax_share = (qty / quantity) * tax_amount if tax_rate > 0 else 0.0
                    person_total = person_share_before_tax + tax_share

                totals[person]["total_before_tax"] += person_share_before_tax
                totals[person]["taxable"] += taxable_share
                totals[person]["tax"] += tax_share
                totals[person]["total_owed"] += person_total

                # Update aggregate amounts
                aggregate_taxable += taxable_share
                aggregate_tax_paid += tax_share
                aggregate_non_taxable += person_share_before_tax - taxable_share
                aggregate_total += person_total

        # Update aggregate labels
        aggregate_amount_before_discount = aggregate_total_before_tax
        aggregate_amount_after_discount = (
            aggregate_total_before_tax * (1 - discount) + aggregate_tax_paid
        )

        self.total_amount_label.config(
            text=f"Total Amount (Before Discount): ${aggregate_total_before_tax:.2f}"
        )
        self.taxable_amount_label.config(
            text=f"Total Taxable Amount: ${aggregate_taxable:.2f}"
        )
        self.non_taxable_amount_label.config(
            text=f"Total Non-Taxable Amount: ${aggregate_non_taxable:.2f}"
        )
        self.amount_before_discount_label.config(
            text=f"Amount Before Discount: ${aggregate_amount_before_discount:.2f}"
        )
        self.amount_after_discount_label.config(
            text=f"Amount After Discount: ${aggregate_amount_after_discount:.2f}"
        )

        return totals

    def show_split(self):
        # Clear previous results
        for item in self.result_box.get_children():
            self.result_box.delete(item)

        totals = self.calculate_final_bill()

        if totals:
            for person, amounts in totals.items():
                self.result_box.insert(
                    "",
                    "end",  # Use "end" as the index
                    values=(
                        person,
                        f"${amounts['total_before_tax']:.2f}",
                        f"${amounts['taxable']:.2f}",
                        f"${amounts['tax']:.2f}",
                        f"${amounts['total_owed']:.2f}",
                    ),
                )

    def export_to_csv(self):
        totals = self.calculate_final_bill()
        if not totals:
            return

        try:
            with open("final_bill.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "Participant",
                        "Total Before Tax",
                        "Taxable Amount",
                        "Tax Paid",
                        "Total Owed",
                    ]
                )
                for person, amounts in totals.items():
                    writer.writerow(
                        [
                            person,
                            f"${amounts['total_before_tax']:.2f}",
                            f"${amounts['taxable']:.2f}",
                            f"${amounts['tax']:.2f}",
                            f"${amounts['total_owed']:.2f}",
                        ]
                    )
            messagebox.showinfo(
                "Export Success", "Bill has been exported to 'final_bill.csv'."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {e}")

    def reset_bill(self):
        # Clear all data structures
        self.item_splits.clear()

        # Clear participant entries
        for entry in self.participants:
            entry.delete(0, tk.END)

        # Clear participant checkboxes
        for widget in self.participant_checkboxes_frame.winfo_children():
            widget.destroy()

        # Clear split frames
        for widget in self.items_frame.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                widget.destroy()

        # Clear added items listbox
        self.added_items_box.delete(0, tk.END)

        # Clear discount entry
        self.discount_entry.delete(0, tk.END)

        # Reset categories
        self.categories = {"Groceries (non-taxable)": 0.0}
        self.category_dropdown["values"] = list(self.categories.keys())
        self.category_dropdown.set("Groceries (non-taxable)")
        self.added_categories_box.delete(0, tk.END)

        # Clear Treeview
        for item in self.result_box.get_children():
            self.result_box.delete(item)

        # Reset aggregate labels
        self.total_amount_label.config(text="Total Amount (Before Discount): $0.00")
        self.taxable_amount_label.config(text="Total Taxable Amount: $0.00")
        self.non_taxable_amount_label.config(text="Total Non-Taxable Amount: $0.00")
        self.amount_before_discount_label.config(text="Amount Before Discount: $0.00")
        self.amount_after_discount_label.config(text="Amount After Discount: $0.00")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = BillSplitterApp(root)
    app.run()
