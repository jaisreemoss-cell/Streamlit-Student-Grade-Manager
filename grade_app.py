import streamlit as st


def get_letter_grade(mark: float) -> str:
    """Returns the letter grade based on a numerical mark."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def main():
    st.set_page_config(
        page_title="Student Grade Management",
        page_icon="🎓",
        layout="wide",
    )

    # Inject Custom CSS for an attractive UI
    st.markdown(
        """
        <style>
        /* Modern font & body styling */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Gradient header card */
        .app-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        .app-header h1 {
            color: #ffffff !important;
            margin-bottom: 0.2rem;
            font-size: 2.2rem;
            font-weight: 700;
        }
        .app-header p {
            color: #e0e6ed !important;
            font-size: 1rem;
            margin-bottom: 0;
        }

        /* Metric card styling */
        [data-testid="stMetric"] {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 12px 16px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            text-align: center;
        }
        [data-testid="stMetricLabel"] {
            color: #64748b !important;
            font-weight: 600;
            font-size: 0.85rem;
        }
        [data-testid="stMetricValue"] {
            color: #1e293b !important;
            font-weight: 700;
        }

        /* Table styling polish */
        [data-testid="stTable"] {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }

        /* Primary Form Button Styling */
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize st.session_state for storing student records
    if "students" not in st.session_state:
        st.session_state.students = []

    # Modern Custom Header
    st.markdown(
        """
        <div class="app-header">
            <h1>🎓 Student Grade Management System</h1>
            <p>Track student performance, view statistics, and monitor grades effortlessly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1, 2], gap="large")

    # --- LEFT COLUMN: Form to Add Student ---
    with left_col:
        st.subheader("➕ Add New Student")

        # clear_on_submit=True resets inputs to empty automatically when submitted
        with st.form("add", clear_on_submit=True):
            name = st.text_input("Name", placeholder="e.g. Alice").strip()
            mark = st.number_input(
                "Mark",
                min_value=0,
                max_value=100,
                step=1,
                value=0,
                help="Enter a score between 0 and 100.",
            )

            submitted = st.form_submit_button("Add Student", use_container_width=True)

            if submitted:
                if not name:
                    st.error("Please enter a valid student name.")
                else:
                    grade = get_letter_grade(float(mark))
                    st.session_state.students.append(
                        {"Name": name, "Mark": float(mark), "Grade": grade}
                    )
                    st.success(f"Added **{name}** with mark **{mark}** (Grade: **{grade}**)")

        # Clear records button
        if st.session_state.students:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear All Records", use_container_width=True):
                st.session_state.students = []
                st.rerun()

    # --- RIGHT COLUMN: Metrics & Student Table ---
    with right_col:
        st.subheader("📊 Class Overview")

        if st.session_state.students:
            # Extract marks using pure Python list comprehensions
            marks = [s["Mark"] for s in st.session_state.students]

            avg_mark = sum(marks) / len(marks)
            highest_mark = max(marks)
            lowest_mark = min(marks)

            # Display Key Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Students", len(st.session_state.students))
            m2.metric("Class Average", f"{avg_mark:.2f}")
            m3.metric("Highest Mark", f"{highest_mark:.1f}")
            m4.metric("Lowest Mark", f"{lowest_mark:.1f}")

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📋 Student List")

            # Display using st.table directly with the list of dicts
            st.table(st.session_state.students)
        else:
            st.info("No student records available yet. Add a student using the form on the left.")


if __name__ == "__main__":
    main()

# before session_state - the field never get clear, so we need to clear the field manually.