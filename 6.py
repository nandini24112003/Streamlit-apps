import streamlit as st
import pandas as pd

# Title for the app
st.title("PDB ATOM Coordinates Viewer")

# Upload PDB file
uploaded_file = st.file_uploader("Upload a PDB file", type="pdb")

if uploaded_file is not None:
    # Read and filter ATOM lines
    data = [line for line in uploaded_file if line.startswith(b"ATOM")]

    # Decode bytes and extract relevant columns
    columns = ["Atom", "X", "Y", "Z"]
    rows = [
        [line[12:16].decode().strip(), 
         float(line[30:38].decode()), 
         float(line[38:46].decode()), 
         float(line[46:54].decode())]
        for line in data
    ]

    # Create DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Display DataFrame
    st.subheader("Extracted ATOM Coordinates")
    st.dataframe(df)

    # Optional: download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "atom_coordinates.csv", "text/csv")