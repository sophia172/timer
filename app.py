import streamlit as st
import time
import datetime
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="Interval Timer",
    page_icon="⏰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .timer-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    
    .timer-display {
        font-size: 4rem;
        font-weight: bold;
        margin: 2rem 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    
    .timer-work {
        color: #4ade80;
    }
    
    .timer-break {
        color: #fb7185;
    }
    
    .phase-indicator {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    .loop-counter {
        font-size: 2.5rem;
        font-weight: bold;
        color: #60a5fa;
        text-align: center;
    }
    
    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        height: 15px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #4ade80, #22c55e);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        height: 3rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none;
        color: white !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    .stNumberInput > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    h1 {
        color: white;
        text-align: center;
        font-size: 3rem;
        font-weight: 300;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'timer_state' not in st.session_state:
    st.session_state.timer_state = {
        'is_running': False,
        'start_time': None,
        'current_phase': 'work',  # 'work' or 'break'
        'phase_start_time': None,
        'total_work_time': 50 * 60,  # 50 minutes in seconds
        'total_break_time': 10 * 60,  # 10 minutes in seconds
        'loop_count': 0,
        'work_minutes': 50,
        'work_seconds': 0,
        'break_minutes': 10,
        'break_seconds': 0,
        'last_beep_time': None
    }

def format_time(seconds):
    """Format seconds into MM:SS format"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def get_remaining_time():
    """Calculate remaining time for current phase"""
    if not st.session_state.timer_state['is_running']:
        return 0
    
    if st.session_state.timer_state['phase_start_time'] is None:
        return 0
    
    elapsed = time.time() - st.session_state.timer_state['phase_start_time']
    
    if st.session_state.timer_state['current_phase'] == 'work':
        total_time = st.session_state.timer_state['total_work_time']
    else:
        total_time = st.session_state.timer_state['total_break_time']
    
    remaining = max(0, total_time - elapsed)
    return remaining

def switch_phase():
    """Switch between work and break phases"""
    if st.session_state.timer_state['current_phase'] == 'work':
        st.session_state.timer_state['current_phase'] = 'break'
    else:
        st.session_state.timer_state['current_phase'] = 'work'
        st.session_state.timer_state['loop_count'] += 1
    
    st.session_state.timer_state['phase_start_time'] = time.time()
    st.session_state.timer_state['last_beep_time'] = time.time()

def start_timer():
    """Start the timer"""
    st.session_state.timer_state['is_running'] = True
    st.session_state.timer_state['start_time'] = time.time()
    st.session_state.timer_state['phase_start_time'] = time.time()
    st.session_state.timer_state['current_phase'] = 'work'

def stop_timer():
    """Stop the timer"""
    st.session_state.timer_state['is_running'] = False
    st.session_state.timer_state['start_time'] = None
    st.session_state.timer_state['phase_start_time'] = None

def reset_timer():
    """Reset the timer to initial state"""
    st.session_state.timer_state = {
        'is_running': False,
        'start_time': None,
        'current_phase': 'work',
        'phase_start_time': None,
        'total_work_time': st.session_state.timer_state['work_minutes'] * 60 + st.session_state.timer_state['work_seconds'],
        'total_break_time': st.session_state.timer_state['break_minutes'] * 60 + st.session_state.timer_state['break_seconds'],
        'loop_count': 0,
        'work_minutes': st.session_state.timer_state['work_minutes'],
        'work_seconds': st.session_state.timer_state['work_seconds'],
        'break_minutes': st.session_state.timer_state['break_minutes'],
        'break_seconds': st.session_state.timer_state['break_seconds'],
        'last_beep_time': None
    }

# Auto-refresh every second when timer is running
if st.session_state.timer_state['is_running']:
    st_autorefresh(interval=1000, limit=None, key="timer_refresh")

# Main app
st.markdown('<h1>⏰ Interval Timer</h1>', unsafe_allow_html=True)

# Timer display section
remaining_time = get_remaining_time()

# Check if phase should switch
if st.session_state.timer_state['is_running'] and remaining_time <= 0:
    switch_phase()
    remaining_time = get_remaining_time()

# Create timer display
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Phase indicator
    if st.session_state.timer_state['is_running']:
        if st.session_state.timer_state['current_phase'] == 'work':
            phase_text = "🔥 WORK TIME"
            timer_class = "timer-work"
        else:
            phase_text = "☕ BREAK TIME"
            timer_class = "timer-break"
    else:
        phase_text = "⏸️ READY TO START"
        timer_class = ""
    
    st.markdown(f'<div class="timer-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="phase-indicator">{phase_text}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="timer-display {timer_class}">{format_time(remaining_time)}</div>', unsafe_allow_html=True)
    
    # Progress bar
    if st.session_state.timer_state['is_running']:
        if st.session_state.timer_state['current_phase'] == 'work':
            total_time = st.session_state.timer_state['total_work_time']
        else:
            total_time = st.session_state.timer_state['total_break_time']
        
        progress = ((total_time - remaining_time) / total_time) * 100 if total_time > 0 else 0
        progress = min(100, max(0, progress))
    else:
        progress = 0
    
    st.markdown(f'''
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Settings section
st.markdown("## ⚙️ Timer Settings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔥 Work Time")
    work_minutes = st.number_input("Minutes", min_value=0, max_value=99, 
                                  value=st.session_state.timer_state['work_minutes'], 
                                  key="work_min", disabled=st.session_state.timer_state['is_running'])
    work_seconds = st.number_input("Seconds", min_value=0, max_value=59, 
                                  value=st.session_state.timer_state['work_seconds'], 
                                  key="work_sec", disabled=st.session_state.timer_state['is_running'])

with col2:
    st.markdown("### ☕ Break Time")
    break_minutes = st.number_input("Minutes", min_value=0, max_value=99, 
                                   value=st.session_state.timer_state['break_minutes'], 
                                   key="break_min", disabled=st.session_state.timer_state['is_running'])
    break_seconds = st.number_input("Seconds", min_value=0, max_value=59, 
                                   value=st.session_state.timer_state['break_seconds'], 
                                   key="break_sec", disabled=st.session_state.timer_state['is_running'])

# Update session state with new values
if not st.session_state.timer_state['is_running']:
    st.session_state.timer_state['work_minutes'] = work_minutes
    st.session_state.timer_state['work_seconds'] = work_seconds
    st.session_state.timer_state['break_minutes'] = break_minutes
    st.session_state.timer_state['break_seconds'] = break_seconds
    st.session_state.timer_state['total_work_time'] = work_minutes * 60 + work_seconds
    st.session_state.timer_state['total_break_time'] = break_minutes * 60 + break_seconds

# Control buttons
st.markdown("## 🎮 Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.timer_state['is_running']:
        if st.button("⏸️ PAUSE", key="pause_btn", use_container_width=True):
            stop_timer()
    else:
        if st.button("▶️ START", key="start_btn", use_container_width=True):
            start_timer()

with col2:
    if st.button("⏹️ STOP", key="stop_btn", use_container_width=True):
        stop_timer()

with col3:
    if st.button("🔄 RESET", key="reset_btn", use_container_width=True):
        reset_timer()

# Statistics section
st.markdown("## 📊 Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown("### 🔁 Completed Loops")
    st.markdown(f'<div class="loop-counter">{st.session_state.timer_state["loop_count"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    total_work_time = st.session_state.timer_state['loop_count'] * (st.session_state.timer_state['total_work_time'] / 60)
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown("### 🔥 Total Work Time")
    st.markdown(f'<div class="loop-counter">{total_work_time:.0f} min</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    total_break_time = st.session_state.timer_state['loop_count'] * (st.session_state.timer_state['total_break_time'] / 60)
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown("### ☕ Total Break Time")
    st.markdown(f'<div class="loop-counter">{total_break_time:.0f} min</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Sound notification (visual indicator since we can't play audio in Streamlit)
if (st.session_state.timer_state['last_beep_time'] is not None and 
    time.time() - st.session_state.timer_state['last_beep_time'] < 3):
    st.markdown("""
    <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); 
                color: white; padding: 1rem; border-radius: 10px; 
                text-align: center; font-size: 1.2rem; font-weight: bold;
                animation: pulse 1s infinite;">
        🔔 PHASE COMPLETE! 🔔
    </div>
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    </style>
    """, unsafe_allow_html=True)

# Instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    1. **Set Your Times**: Adjust work and break durations using the number inputs
    2. **Start Timer**: Click the START button to begin your first work session
    3. **Automatic Cycling**: The timer will automatically switch between work and break periods
    4. **Visual Notifications**: You'll see a notification when each phase completes
    5. **Track Progress**: Monitor your completed loops and total time in the statistics section
    6. **Controls**: Use PAUSE to temporarily stop, STOP to end current session, or RESET to start over
    
    **Perfect for**: Pomodoro Technique, focused work sessions, study breaks, or any interval training!
    """)
