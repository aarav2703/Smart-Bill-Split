Smart Bill Splitting and Tax Analysis Project
Overview
This project builds a Smart Bill Splitting and Tax Analysis Tool, integrating OCR-based text extraction, regex-driven supermarket template parsing, and interactive dashboards. The tool simplifies splitting expenses, applies relevant taxes and discounts, and ensures reusable, modular code design.

The system supports multiple OCR methods, flexible participant management, and a user-friendly interface with reusable components, making it adaptable for future enhancements or other use cases.

Key Features
Advanced Text Extraction:

Utilized EasyOCR, Tesseract, TrOCR, and deep learning techniques to extract text from scanned bills and receipts.
Custom preprocessing for accuracy enhancement, including thresholding and noise removal.
Supermarket-Specific Parsing:

Regex-driven templates for parsing item names, quantities, and prices from extracted text.
Conversion of parsed data into CSV for downstream processing.
Interactive Visualization and Splitting:

Streamlit dashboard for splitting bills conveniently among participants.
Flexible UX design choices, including:
Horizontal participant name fields for space efficiency.
Customizable tax rates and categories.
Reusable models for splitting logic, making the application adaptable.
Tax and Discount Management:

Category-wise tax application based on Minnesota tax rules.
Percentage-based discounts applied before tax calculation.
Support for tax exemptions on groceries and similar items.
Reusable Components:

Modular code structure for easy updates and extensibility.
Functions and models reusable across different supermarket formats.
Enhanced UX/UI Design:

Scrollbars and dynamic layouts for screens with varying item lengths.
Color-coded buttons for clarity.
Reset and export options for better usability.

Technologies Used
OCR Tools: EasyOCR, Tesseract, TrOCR.
Regex Parsing: Supermarket-specific patterns for extracting relevant data.
Visualization: Streamlit, Matplotlib, Plotly for interactive dashboards and insights.
UX Design: Modular layouts with dynamic participant fields, scrollbars, and user-friendly button placements.

Customization
Add new supermarket templates by modifying regex_patterns in parse_text.py.
Update tax rules or categories directly via the Streamlit GUI.
Modify discount application logic in streamlit_dashboard.py.
Future Directions
API integration for real-time price updates from supermarkets.
Enhanced support for mobile platforms.
Machine learning models for auto-categorization of items.
