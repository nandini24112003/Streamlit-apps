import streamlit as st
import pandas as pd
import requests
import py3Dmol

st.title("PDB Viewer with 3D Structure")

# Input PDB ID
pdb_id = st.text_input("Enter PDB ID (e.g., 1CRN)")

if pdb_id:
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    response = requests.get(url)

    if response.status_code == 200:
        pdb_text = response.text
        atom_lines = [line for line in pdb_text.splitlines() if line.startswith("ATOM")]

        if atom_lines:
            # Extract coordinates
            columns = ["Atom", "X", "Y", "Z"]
            rows = [
                [line[12:16].strip(),
                 float(line[30:38]),
                 float(line[38:46]),
                 float(line[46:54])]
                for line in atom_lines
            ]
            df = pd.DataFrame(rows, columns=columns)
            st.subheader("Extracted ATOM Coordinates")
            st.dataframe(df)

            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, f"{pdb_id}_atom_coordinates.csv", "text/csv")

            # 3D Viewer
            st.subheader("3D Structure Viewer")
            view = py3Dmol.view(width=600, height=400)
            view.addModel(pdb_text, "pdb")
            view.setStyle({"stick": {}})
            view.zoomTo()
            viewer_html = view._make_html()
            st.components.v1.html(viewer_html, height=400, scrolling=False)
        else:
            st.warning("No ATOM records found.")
    else:
        st.error("Failed to fetch PDB file. Please check the ID.")