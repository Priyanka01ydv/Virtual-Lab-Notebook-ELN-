import streamlit as st
import os
import datetime
from db import init_db, add_entry, get_entries, get_entry_by_id
from export import export_to_pdf

# Initialize DB
os.makedirs("data", exist_ok=True)
init_db()

st.set_page_config(page_title="Virtual Lab Notebook 📓", page_icon="📓", layout="wide")

st.title("Virtual Lab Notebook 📓")
st.markdown("A dreamy, digital place for your protocols, results & notes ✨")

menu = ["Add Entry", "View/Search Entries", "Export PDF"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Entry":
    st.subheader("➕ Add New Entry")
    title = st.text_input("Title")
    date = st.date_input("Date", datetime.date.today())
    category = st.selectbox("Category", ["Protocol", "Experiment", "Result", "Notes"])
    content = st.text_area("Content (Markdown supported)")
    if st.button("Save Entry"):
        if title and content:
            add_entry(title, str(date), category, content)
            st.success("Entry added successfully! 🌸")
        else:
            st.error("Please fill in all fields!")

elif choice == "View/Search Entries":
    st.subheader("🔍 View & Search Entries")
    search_query = st.text_input("Search by keyword")
    category_filter = st.selectbox("Filter by category", ["All", "Protocol", "Experiment", "Result", "Notes"])
    date_filter = st.date_input("Filter by date (optional)", value=None)
    entries = get_entries(search_query, category_filter, str(date_filter) if date_filter else None)
    if entries:
        for e in entries:
            eid, title, date, category, content = e
            with st.expander(f"{title} ({date}) - {category}"):
                st.markdown(content)
    else:
        st.info("No entries found 🌼")

elif choice == "Export PDF":
    st.subheader("📄 Export Entries as PDF")
    search_query = st.text_input("Search entries for export")
    entries = get_entries(search_query)
    if entries:
        selected_titles = st.multiselect("Select entries to export", [f"{e[1]} ({e[2]})" for e in entries])
        if st.button("Export Selected to PDF"):
            selected_entries = []
            for e in entries:
                if f"{e[1]} ({e[2]})" in selected_titles:
                    selected_entries.append((e[1], e[2], e[3], e[4]))
            if selected_entries:
                export_to_pdf("LabNotebook.pdf", selected_entries)
                with open("LabNotebook.pdf", "rb") as f:
                    st.download_button("Download PDF", f, file_name="LabNotebook.pdf")
            else:
                st.warning("No entries selected 🌸")
    else:
        st.info("No entries available for export 🌼")
