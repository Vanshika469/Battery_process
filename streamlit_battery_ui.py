import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import json
import io
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="🔋 Battery Cell Analysis System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main > div {
        padding: 2rem 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        animation: slideDown 0.8s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .cell-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #e6f2ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .task-card {
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #48bb78;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideInRight 0.5s ease-out;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #718096;
        font-weight: 500;
    }
    
    .success-message {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        animation: pulse 0.5s ease-out;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        animation: shake 0.5s ease-out;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 8px;
    }
    
    .stNumberInput > div > div > input {
        background: white;
        border-radius: 8px;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .export-section {
        background: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        text-align: center;
        margin: 2rem 0;
    }
    
    .stDataFrame {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'tasks_data' not in st.session_state:
    st.session_state.tasks_data = {}
if 'cell_counter' not in st.session_state:
    st.session_state.cell_counter = 0
if 'task_counter' not in st.session_state:
    st.session_state.task_counter = 0

def generate_cell_data(cell_type, cell_id):
    """Generate cell data based on type"""
    voltage = 3.2 if cell_type == "lfp" else 3.6
    min_voltage = 2.8 if cell_type == "lfp" else 3.2
    max_voltage = 3.6 if cell_type == "lfp" else 4.0
    current = round(random.uniform(0.0, 5.0), 2)  # Random current for demo
    temp = round(random.uniform(25, 40), 1)
    capacity = round(voltage * current, 2)
    
    return {
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "min_voltage": min_voltage,
        "max_voltage": max_voltage,
        "type": cell_type
    }

def create_cell_visualization():
    """Create interactive cell data visualization"""
    if not st.session_state.cells_data:
        st.info("📊 No cell data available. Add some cells to see the visualization!")
        return
    
    # Prepare data for visualization
    cell_names = list(st.session_state.cells_data.keys())
    voltages = [st.session_state.cells_data[cell]["voltage"] for cell in cell_names]
    currents = [st.session_state.cells_data[cell]["current"] for cell in cell_names]
    temps = [st.session_state.cells_data[cell]["temp"] for cell in cell_names]
    capacities = [st.session_state.cells_data[cell]["capacity"] for cell in cell_names]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Voltage (V)', 'Current (A)', 'Temperature (°C)', 'Capacity (Wh)'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Add voltage bar chart
    fig.add_trace(
        go.Bar(x=cell_names, y=voltages, name="Voltage", 
               marker_color='rgb(102, 126, 234)', showlegend=False),
        row=1, col=1
    )
    
    # Add current bar chart
    fig.add_trace(
        go.Bar(x=cell_names, y=currents, name="Current", 
               marker_color='rgb(255, 99, 132)', showlegend=False),
        row=1, col=2
    )
    
    # Add temperature bar chart
    fig.add_trace(
        go.Bar(x=cell_names, y=temps, name="Temperature", 
               marker_color='rgb(255, 159, 64)', showlegend=False),
        row=2, col=1
    )
    
    # Add capacity bar chart
    fig.add_trace(
        go.Bar(x=cell_names, y=capacities, name="Capacity", 
               marker_color='rgb(75, 192, 192)', showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="Battery Cell Analysis Dashboard",
        title_x=0.5,
        title_font_size=20,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Update axes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig

def create_comparison_chart():
    """Create comparison chart for different cell types"""
    if not st.session_state.cells_data:
        return None
    
    df_data = []
    for cell_name, cell_data in st.session_state.cells_data.items():
        df_data.append({
            'Cell': cell_name,
            'Type': cell_data['type'].upper(),
            'Voltage': cell_data['voltage'],
            'Current': cell_data['current'],
            'Temperature': cell_data['temp'],
            'Capacity': cell_data['capacity']
        })
    
    df = pd.DataFrame(df_data)
    
    # Create scatter plot
    fig = px.scatter(df, x='Voltage', y='Temperature', size='Capacity', 
                     color='Type', hover_data=['Cell', 'Current'],
                     title="Cell Performance Comparison",
                     template="plotly_white")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def export_to_csv(data, filename):
    """Export data to CSV format"""
    if isinstance(data, dict):
        # Convert dictionary to DataFrame
        if 'cells_data' in filename:
            df_data = []
            for cell_name, cell_data in data.items():
                row = {'Cell_ID': cell_name}
                row.update(cell_data)
                df_data.append(row)
            df = pd.DataFrame(df_data)
        else:  # tasks data
            df_data = []
            for task_name, task_data in data.items():
                row = {'Task_ID': task_name}
                row.update(task_data)
                df_data.append(row)
            df = pd.DataFrame(df_data)
    else:
        df = data
    
    return df.to_csv(index=False)

def export_to_json(data):
    """Export data to JSON format"""
    return json.dumps(data, indent=2)

# Main App Header
st.markdown("""
<div class="main-header">
    <h1>🔋 Battery Cell Analysis System</h1>
    <p>Advanced Battery Management & Task Processing Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox(
    "Choose a section:",
    ["🏠 Dashboard", "🔋 Cell Management", "⚡ Task Management", "📈 Data Analysis", "📁 Export Data"]
)

if page == "🏠 Dashboard":
    st.markdown("## 📊 System Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="stat-value">{}</div>
            <div class="stat-label">Total Cells</div>
        </div>
        """.format(len(st.session_state.cells_data)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="stat-value">{}</div>
            <div class="stat-label">Active Tasks</div>
        </div>
        """.format(len(st.session_state.tasks_data)), unsafe_allow_html=True)
    
    with col3:
        avg_temp = 0
        if st.session_state.cells_data:
            avg_temp = round(sum(cell["temp"] for cell in st.session_state.cells_data.values()) / len(st.session_state.cells_data), 1)
        st.markdown("""
        <div class="metric-card">
            <div class="stat-value">{}°C</div>
            <div class="stat-label">Avg Temperature</div>
        </div>
        """.format(avg_temp), unsafe_allow_html=True)
    
    with col4:
        total_capacity = 0
        if st.session_state.cells_data:
            total_capacity = round(sum(cell["capacity"] for cell in st.session_state.cells_data.values()), 2)
        st.markdown("""
        <div class="metric-card">
            <div class="stat-value">{} Wh</div>
            <div class="stat-label">Total Capacity</div>
        </div>
        """.format(total_capacity), unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔋 Add Sample Cells", help="Add sample battery cells for testing"):
            for i in range(3):
                st.session_state.cell_counter += 1
                cell_type = random.choice(["lfp", "nmc"])
                cell_key = f"cell_{st.session_state.cell_counter}_{cell_type}"
                st.session_state.cells_data[cell_key] = generate_cell_data(cell_type, st.session_state.cell_counter)
            st.success("✅ Sample cells added successfully!")
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("📊 Generate Report", help="Generate comprehensive analysis report"):
            if st.session_state.cells_data:
                st.success("📈 Report generated! Check the Data Analysis section.")
            else:
                st.warning("⚠️ No data available. Add some cells first!")
    
    with col3:
        if st.button("🗑️ Clear All Data", help="Clear all cells and tasks"):
            st.session_state.cells_data = {}
            st.session_state.tasks_data = {}
            st.session_state.cell_counter = 0
            st.session_state.task_counter = 0
            st.success("🧹 All data cleared!")
            time.sleep(1)
            st.rerun()
    
    # Recent Activity
    if st.session_state.cells_data or st.session_state.tasks_data:
        st.markdown("## 📝 Recent Activity")
        
        if st.session_state.cells_data:
            st.markdown("### 🔋 Recent Cells")
            recent_cells = list(st.session_state.cells_data.keys())[-3:]  # Last 3 cells
            for cell in recent_cells:
                cell_data = st.session_state.cells_data[cell]
                st.markdown(f"""
                <div class="cell-card">
                    <strong>{cell}</strong> - {cell_data['type'].upper()}<br>
                    <small>Voltage: {cell_data['voltage']}V | Temp: {cell_data['temp']}°C | Capacity: {cell_data['capacity']}Wh</small>
                </div>
                """, unsafe_allow_html=True)
        
        if st.session_state.tasks_data:
            st.markdown("### ⚡ Recent Tasks")
            recent_tasks = list(st.session_state.tasks_data.keys())[-3:]  # Last 3 tasks
            for task in recent_tasks:
                task_data = st.session_state.tasks_data[task]
                st.markdown(f"""
                <div class="task-card">
                    <strong>{task}</strong> - {task_data['task_type']}<br>
                    <small>Status: Active | Type: {task_data['task_type']}</small>
                </div>
                """, unsafe_allow_html=True)

elif page == "🔋 Cell Management":
    st.markdown("## 🔋 Battery Cell Management")
    
    # Cell Input Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ➕ Add New Cell")
        
        # Single cell addition
        cell_type = st.selectbox(
            "Select Cell Type:",
            ["lfp", "nmc"],
            format_func=lambda x: "LFP (Lithium Iron Phosphate)" if x == "lfp" else "NMC (Nickel Manganese Cobalt)"
        )
        
        if st.button("Add Single Cell", type="primary"):
            st.session_state.cell_counter += 1
            cell_key = f"cell_{st.session_state.cell_counter}_{cell_type}"
            st.session_state.cells_data[cell_key] = generate_cell_data(cell_type, st.session_state.cell_counter)
            st.success(f"✅ Cell {cell_key} added successfully!")
            time.sleep(1)
            st.rerun()
        
        st.markdown("---")
        
        # Bulk cell addition
        st.markdown("### 📦 Bulk Add Cells")
        num_cells = st.number_input("Number of cells to add:", min_value=1, max_value=50, value=5)
        bulk_cell_type = st.selectbox(
            "Cell type for bulk addition:",
            ["lfp", "nmc"],
            format_func=lambda x: "LFP (Lithium Iron Phosphate)" if x == "lfp" else "NMC (Nickel Manganese Cobalt)",
            key="bulk_type"
        )
        
        if st.button("Add Multiple Cells"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(num_cells):
                st.session_state.cell_counter += 1
                cell_key = f"cell_{st.session_state.cell_counter}_{bulk_cell_type}"
                st.session_state.cells_data[cell_key] = generate_cell_data(bulk_cell_type, st.session_state.cell_counter)
                
                progress = (i + 1) / num_cells
                progress_bar.progress(progress)
                status_text.text(f"Adding cell {i + 1} of {num_cells}...")
                time.sleep(0.1)  # Smooth animation
            
            progress_bar.empty()
            status_text.empty()
            st.success(f"✅ {num_cells} cells added successfully!")
            time.sleep(1)
            st.rerun()
    
    with col2:
        st.markdown("### 📊 Cell Statistics")
        
        if st.session_state.cells_data:
            # Cell type distribution
            cell_types = [cell["type"] for cell in st.session_state.cells_data.values()]
            type_counts = pd.Series(cell_types).value_counts()
            
            fig_pie = px.pie(values=type_counts.values, names=type_counts.index,
                            title="Cell Type Distribution",
                            color_discrete_sequence=['#667eea', '#764ba2'])
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Statistics table
            stats_data = {
                'Metric': ['Total Cells', 'LFP Cells', 'NMC Cells', 'Avg Voltage', 'Avg Temperature', 'Total Capacity'],
                'Value': [
                    len(st.session_state.cells_data),
                    sum(1 for cell in st.session_state.cells_data.values() if cell['type'] == 'lfp'),
                    sum(1 for cell in st.session_state.cells_data.values() if cell['type'] == 'nmc'),
                    f"{round(sum(cell['voltage'] for cell in st.session_state.cells_data.values()) / len(st.session_state.cells_data), 2)}V",
                    f"{round(sum(cell['temp'] for cell in st.session_state.cells_data.values()) / len(st.session_state.cells_data), 1)}°C",
                    f"{round(sum(cell['capacity'] for cell in st.session_state.cells_data.values()), 2)}Wh"
                ]
            }
            st.dataframe(pd.DataFrame(stats_data), hide_index=True)
        else:
            st.info("📊 No cells added yet. Add some cells to see statistics!")
    
    # Display Current Cells
    if st.session_state.cells_data:
        st.markdown("### 🔋 Current Cells")
        
        # Search and filter
        search_term = st.text_input("🔍 Search cells:", placeholder="Enter cell name or type...")
        
        filtered_cells = st.session_state.cells_data
        if search_term:
            filtered_cells = {k: v for k, v in st.session_state.cells_data.items() 
                            if search_term.lower() in k.lower() or search_term.lower() in v['type'].lower()}
        
        # Display cells in a grid
        cells_per_row = 2
        cell_list = list(filtered_cells.items())
        
        for i in range(0, len(cell_list), cells_per_row):
            cols = st.columns(cells_per_row)
            for j, (cell_name, cell_data) in enumerate(cell_list[i:i+cells_per_row]):
                with cols[j]:
                    st.markdown(f"""
                    <div class="cell-card">
                        <h4>{cell_name}</h4>
                        <p><strong>Type:</strong> {cell_data['type'].upper()}</p>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value">{cell_data['voltage']}</div>
                                <div class="stat-label">Voltage (V)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{cell_data['current']}</div>
                                <div class="stat-label">Current (A)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{cell_data['temp']}</div>
                                <div class="stat-label">Temp (°C)</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">{cell_data['capacity']}</div>
                                <div class="stat-label">Capacity (Wh)</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🗑️ Remove", key=f"remove_{cell_name}"):
                        del st.session_state.cells_data[cell_name]
                        st.success(f"✅ {cell_name} removed!")
                        time.sleep(1)
                        st.rerun()

elif page == "⚡ Task Management":
    st.markdown("## ⚡ Task Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ➕ Add New Task")
        
        task_type = st.selectbox(
            "Select Task Type:",
            ["", "CC_CV", "IDLE", "CC_CD"],
            format_func=lambda x: {
                "": "Select a task type",
                "CC_CV": "CC_CV (Constant Current/Constant Voltage)",
                "IDLE": "IDLE (No Operation)",
                "CC_CD": "CC_CD (Constant Current/Constant Discharge)"
            }[x]
        )
        
        if task_type:
            if task_type == "CC_CV":
                st.markdown("#### CC_CV Parameters")
                cc_input = st.text_input("CC/CP Value:", placeholder="e.g., 5A or 10W")
                cv_voltage = st.number_input("CV Voltage (V):", min_value=0.0, step=0.1, format="%.1f")
                current = st.number_input("Current (A):", min_value=0.0, step=0.1, format="%.1f")
                capacity = st.number_input("Capacity:", min_value=0.0, step=0.1, format="%.1f")
                time_seconds = st.number_input("Time (seconds):", min_value=0, step=1)
                
                task_data = {
                    "task_type": "CC_CV",
                    "cc_cp": cc_input,
                    "cv_voltage": cv_voltage,
                    "current": current,
                    "capacity": capacity,
                    "time_seconds": time_seconds
                }
                
            elif task_type == "IDLE":
                st.markdown("#### IDLE Parameters")
                time_seconds = st.number_input("Time (seconds):", min_value=0, step=1, key="idle_time")
                
                task_data = {
                    "task_type": "IDLE",
                    "time_seconds": time_seconds
                }
                
            elif task_type == "CC_CD":
                st.markdown("#### CC_CD Parameters")
                cc_input = st.text_input("CC/CP Value:", placeholder="e.g., 5A or 10W", key="cccd_input")
                voltage = st.number_input("Voltage (V):", min_value=0.0, step=0.1, format="%.1f", key="cccd_voltage")
                capacity = st.number_input("Capacity:", min_value=0.0, step=0.1, format="%.1f", key="cccd_capacity")
                time_seconds = st.number_input("Time (seconds):", min_value=0, step=1