import streamlit as st
import pandas as pd
import os


# --- Helper Functions ---
def load_csv(file_path):
    """Load the CSV file and return as a DataFrame, skipping the store info row if found."""
    df = pd.read_csv(file_path)
    # Skip the first row if it contains store info
    if (
        "Aldi's" in df.iloc[0]["Item Name"]
    ):  # Check if the first item's name has "Aldi's"
        df = df.iloc[1:].reset_index(drop=True)
    return df


def calculate_splits(df, item_assignments):
    """Calculate splits based on itemized data and assignments."""
    participant_splits = {}
    for _, row in df.iterrows():
        item_name = row["Item Name"]
        if item_assignments.get(item_name) == "excluded":
            continue  # Skip items marked as excluded

        assigned_participants = item_assignments.get(item_name, [])
        if not assigned_participants:
            continue  # Skip if no participants assigned

        item_total = row["Price"] * row["Quantity"]
        split_value = item_total / len(assigned_participants)

        for participant in assigned_participants:
            if participant not in participant_splits:
                participant_splits[participant] = 0.0
            participant_splits[participant] += split_value

    return participant_splits


def export_csv(participant_splits, file_name="final_split.csv"):
    """Export participant splits to a CSV file."""
    df = pd.DataFrame(
        list(participant_splits.items()), columns=["Participant", "Total Owed"]
    )
    df.to_csv(file_name, index=False)
    return file_name


# --- Streamlit Layout ---
st.title("Bill Splitter Dashboard")

# Local File Selection
st.sidebar.subheader("Select a CSV File")
csv_directory = "data/"  # Path to the folder containing CSV files
csv_files = [f for f in os.listdir(csv_directory) if f.endswith(".csv")]

if csv_files:
    selected_file = st.sidebar.selectbox("Available CSV Files", csv_files)
    if selected_file:
        file_path = os.path.join(csv_directory, selected_file)
        df = load_csv(file_path)

        # Participant Management (initialize participants before usage)
        st.sidebar.subheader("Participants")
        participants = st.sidebar.text_area(
            "Add participants (comma-separated):", "Alice, Bob"
        )
        participants = [
            name.strip() for name in participants.split(",") if name.strip()
        ]

        # Initialize Session State for Exclusion
        if "item_states" not in st.session_state:
            st.session_state.item_states = {
                row["Item Name"]: "included" for _, row in df.iterrows()
            }

        # Display Itemized Receipt
        st.subheader("Itemized Receipt (Editable)")
        item_assignments = {}  # Store assignments and exclusions

        for i, row in df.iterrows():
            item_name = row["Item Name"]
            if item_name in ["Subtotal", "Total"]:
                continue  # Skip subtotal and total

            # Add row-specific exclusion toggle
            col1, col2 = st.columns([2, 1])  # Create two columns for better alignment

            with col1:
                st.write(f"**{item_name}** - ${row['Price']} x {row['Quantity']}")

            with col2:
                # Toggle button to exclude/include the item
                if st.button(
                    "Exclude"
                    if st.session_state.item_states[item_name] == "included"
                    else "Include",
                    key=f"toggle_{item_name}",
                ):
                    st.session_state.item_states[item_name] = (
                        "excluded"
                        if st.session_state.item_states[item_name] == "included"
                        else "included"
                    )

                # Grey out excluded rows
                if st.session_state.item_states[item_name] == "excluded":
                    st.markdown(
                        f'<div style="color: grey; font-style: italic;">Excluded from split</div>',
                        unsafe_allow_html=True,
                    )

            # Multiselect for assigning participants (only if included)
            if st.session_state.item_states[item_name] == "included":
                assigned = st.multiselect(
                    f"Assign '{item_name}' to participants:",
                    participants,
                    key=item_name,
                )
                item_assignments[item_name] = assigned
            else:
                item_assignments[item_name] = "excluded"

        if participants:
            # Calculate Splits
            if st.button("Calculate Splits"):
                splits = calculate_splits(df, item_assignments)
                st.subheader("Final Split")
                st.table(
                    pd.DataFrame(
                        list(splits.items()), columns=["Participant", "Total Owed"]
                    )
                )

                # Export Splits
                if st.button("Export to CSV"):
                    file_name = export_csv(splits)
                    st.success(f"Splits exported to {file_name}")

else:
    st.error(f"No CSV files found in {csv_directory}. Please add files to this folder.")
