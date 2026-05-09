import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Project Tracker", layout="wide")
st.title("📋 Project Management Dashboard")

# Initialize session state for data storage
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=["Task", "Assignee", "Progress Notes", "Status", "Due Date"])

# --- Sidebar: Add New Task ---
st.sidebar.header("Add New Task")
with st.sidebar.form("task_form", clear_on_submit=True):
    task_name = st.text_input("Task Name")
    Progress_Notes = st.text_input("Progress Notes")
    assignee = st.selectbox("Assignee", ["Kimo", "Alice", "Bob", "Charlie", "Unassigned"])
    status = st.select_slider("Initial Status", options=["Backlog", "In Progress", "In Review", "Approved", "Completed"])
    due_date = st.date_input("Due Date", date.today())
    
    submit = st.form_submit_button("Add Task")
    if submit and task_name:
        new_row = {"Task": task_name, "Progress Notes": Progress_Notes, "Assignee": assignee, "Status": status, "Due Date": due_date}
        st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Added: {task_name}")

# --- Main Dashboard ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Current Project Tasks")
    # Editable dataframe allows users to update status directly
    edited_df = st.data_editor(st.session_state.tasks, num_rows="dynamic", use_container_width=True)
    st.session_state.tasks = edited_df

with col2:
    st.subheader("Progress Overview")
    if not st.session_state.tasks.empty:
        status_counts = st.session_state.tasks['Status'].value_counts()
        st.bar_chart(status_counts)
    else:
        st.info("No tasks added yet.")

# Optional: Export functionality
if not st.session_state.tasks.empty:
    csv = st.session_state.tasks.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Project Plan (CSV)", data=csv, file_name="project_plan.csv", mime="text/csv")
