import streamlit as st
import pandas as pd
import numpy as np
import time
import uuid

# --- Page Configuration ---
st.set_page_config(
    page_title="Airline Baggage Handling Simulation",
    page_icon="✈️",
    layout="wide",
)

# --- Helper Functions ---
def get_short_id():
    """Generates a short, unique ID for bags."""
    return str(uuid.uuid4())[:8].upper()

# --- Initialize Session State ---
def initialize_state():
    """Initializes the session state variables if they don't exist."""
    if 'baggage_queue' not in st.session_state:
        # Start with a few bags in the queue
        st.session_state.baggage_queue = [get_short_id() for _ in range(3)]

    if 'misplaced_stack' not in st.session_state:
        # Start with a couple of misplaced bag reports
        st.session_state.misplaced_stack = [get_short_id() for _ in range(2)]

    if 'passenger_db' not in st.session_state:
        # Pre-populate a dictionary of passengers
        st.session_state.passenger_db = {
            "PAX-001": {"name": "John Doe", "flight": "UA123", "destination": "SFO", "bag_id": get_short_id()},
            "PAX-002": {"name": "Jane Smith", "flight": "DL456", "destination": "JFK", "bag_id": get_short_id()},
            "PAX-003": {"name": "Peter Jones", "flight": "AA789", "destination": "LAX", "bag_id": get_short_id()}
        }

    if 'efficiency_data' not in st.session_state:
        # Create initial data for the efficiency graph
        st.session_state.efficiency_data = pd.DataFrame({
            'Hour': list(range(1, 6)),
            'Bags Processed': np.random.randint(80, 150, size=5)
        })

# Call the initialization function at the start of the script
initialize_state()


# --- UI Functions for Each Data Structure Page ---

def page_queue():
    """Renders the baggage processing queue simulation page."""
    st.header("1. Baggage Processing Queue (FIFO)")
    st.info("""
    A **Queue** is a linear data structure following the **First-In, First-Out (FIFO)** principle. Like a line at a checkout counter, the first item added is the first one to be removed.

    **Use Case:** This perfectly models the main baggage processing line. Bags are checked in (added to the end of the queue) and are later processed for loading (removed from the front) in the same order.
    """, icon="➡️")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Actions")
        new_bag_id = st.text_input("Enter New Baggage ID", value=get_short_id(), key="new_bag")
        if st.button("✈️ Add Bag to Queue"):
            st.session_state.baggage_queue.append(new_bag_id)
            st.success(f"Bag `{new_bag_id}` added to the queue.")
            time.sleep(0.5)
            st.rerun()

        if st.button("✅ Process Next Bag"):
            if st.session_state.baggage_queue:
                processed_bag = st.session_state.baggage_queue.pop(0)
                st.info(f"Processed Bag: `{processed_bag}`")
            else:
                st.warning("The baggage queue is empty!")
            time.sleep(0.5)

    with col2:
        st.subheader("Current Baggage Queue Visualization")
        if not st.session_state.baggage_queue:
            st.info("Queue is empty. All bags have been processed!")
        else:
            st.markdown("`[Front of Queue]` ->")
            queue_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; padding: 10px; border: 2px solid #555; border-radius: 10px; background-color: #f0f2f6;'>"
            for bag in st.session_state.baggage_queue:
                queue_html += f"<div style='background-color: #4A90E2; color: white; padding: 15px 20px; border-radius: 8px; font-weight: bold; font-family: monospace;'>🧳 {bag}</div>"
            queue_html += "</div>"
            st.markdown(queue_html, unsafe_allow_html=True)
            st.markdown("`<- [Back of Queue]`")


def page_stack():
    """Renders the misplaced baggage stack simulation page."""
    st.header("2. Misplaced Baggage Stack (LIFO)")
    st.info("""
    A **Stack** is a linear data structure following the **Last-In, First-Out (LIFO)** principle. Like a stack of plates, you add a new plate to the top and also remove one from the top.

    **Use Case:** This is useful for managing misplaced baggage reports. As new reports come in, they are added to the top of the stack. The resolution team typically works on the most recent cases first, so they would take a report from the top to investigate.
    """, icon="📚")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Actions")
        misplaced_bag_id = st.text_input("Enter Misplaced Bag ID", value=get_short_id(), key="misplaced_bag")
        if st.button("❗️ Report Misplaced Bag"):
            st.session_state.misplaced_stack.append(misplaced_bag_id)
            st.success(f"Report for bag `{misplaced_bag_id}` added to the stack.")
            time.sleep(0.5)
            st.rerun()

        if st.button("🔍 Investigate Last Report"):
            if st.session_state.misplaced_stack:
                investigated_bag = st.session_state.misplaced_stack.pop()
                st.info(f"Investigating report for Bag: `{investigated_bag}`")
            else:
                st.warning("No misplaced baggage reports to investigate!")
            time.sleep(0.5)

    with col2:
        st.subheader("Current Misplaced Reports Stack")
        if not st.session_state.misplaced_stack:
            st.success("No reports in the stack. Great work!")
        else:
            st.markdown("`[Top of Stack]`")
            stack_html = "<div style='display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 10px; border: 2px solid #555; border-radius: 10px; background-color: #f0f2f6;'>"
            for bag in reversed(st.session_state.misplaced_stack):
                stack_html += f"<div style='background-color: #D0021B; color: white; padding: 15px 20px; border-radius: 8px; font-weight: bold; font-family: monospace; width: 80%; text-align: center;'>📝 {bag}</div>"
            stack_html += "</div>"
            st.markdown(stack_html, unsafe_allow_html=True)


def page_hash_table():
    """Renders the passenger lookup (hash table) simulation page."""
    st.header("3. Passenger Information (Hash Table / Dictionary)")
    st.info("""
    A **Hash Table** (a `dictionary` in Python) stores data in **key-value** pairs. It uses a hash function to map keys to values, allowing for extremely fast data retrieval (average time complexity of O(1)).

    **Use Case:** Ideal for quickly retrieving passenger info. Using a unique Passenger ID as the key, the system can instantly pull up all associated details (name, flight, destination) without searching through a long list.
    """, icon="🔑")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Find Passenger by ID")
        passenger_id_to_find = st.selectbox(
            "Select a Passenger ID to look up",
            options=list(st.session_state.passenger_db.keys())
        )

        if st.button("👤 Find Passenger Details"):
            if passenger_id_to_find in st.session_state.passenger_db:
                details = st.session_state.passenger_db[passenger_id_to_find]
                st.success(f"Passenger Found for ID: `{passenger_id_to_find}`")
                st.json(details)
            else:
                st.error("Passenger ID not found in the database.")

    with col2:
        st.subheader("Underlying Data Structure (Dictionary)")
        st.json(st.session_state.passenger_db)


def page_graph():
    """Renders the efficiency graph visualization page."""
    st.header("4. Efficiency Analysis (Graph)")
    st.info("""
    A **Graph** is a non-linear data structure of nodes and edges. A line chart, as used here, is a simple form of a graph that visualizes the relationship between two variables.

    **Use Case:** We can track operational efficiency over time. By plotting the number of bags processed per hour, airport management can quickly identify peak times, spot bottlenecks, and analyze trends to optimize resource allocation.
    """, icon="📊")

    st.subheader("Bags Processed Per Hour")

    chart = st.line_chart(
        st.session_state.efficiency_data.set_index('Hour')
    )

    if st.button("📈 Simulate Next Hour"):
        last_hour = st.session_state.efficiency_data['Hour'].max()
        new_hour = last_hour + 1
        new_processed_count = np.random.randint(80, 150)
        
        new_data = pd.DataFrame({'Hour': [new_hour], 'Bags Processed': [new_processed_count]})
        
        # In a real app, you would append to the existing DataFrame.
        # For Streamlit's st.line_chart.add_rows, we pass only the new data.
        st.session_state.efficiency_data = pd.concat([st.session_state.efficiency_data, new_data], ignore_index=True)
        
        # Update the chart with the new row
        chart.add_rows(new_data.set_index('Hour'))
        st.success(f"Simulated Hour {new_hour}: Processed {new_processed_count} bags.")

    st.subheader("Data Table")
    st.dataframe(st.session_state.efficiency_data, use_container_width=True)

# --- Main App Logic ---

st.title("✈️ Airline Baggage Handling System Simulation")
st.markdown("This application demonstrates how different data structures are used to efficiently manage an airline's baggage handling process. Choose a simulation from the sidebar to begin.")

# Sidebar for navigation
pages = {
    "Queue (FIFO)": page_queue,
    "Stack (LIFO)": page_stack,
    "Hash Table (Dictionary)": page_hash_table,
    "Graph (Efficiency)": page_graph
}

st.sidebar.title("Data Structure Simulations")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Call the function for the selected page
page_function = pages[selection]
page_function()

st.sidebar.markdown("---")
st.sidebar.info("Each page provides a simulation and an explanation of a key data structure used in complex systems like airline operations.")
