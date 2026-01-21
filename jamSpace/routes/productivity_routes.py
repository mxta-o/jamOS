from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
from datetime import datetime, date, timedelta
import os

productivity_bp = Blueprint('productivity', __name__)

# Simple data storage (in production, use a proper database)
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

@productivity_bp.route('/pomodoro')
def pomodoro():
    return render_template('apps/pomodoro.html')

# Habit Tracker Routes
@productivity_bp.route('/habit-tracker')
def habit_tracker():
    habits = load_habits()
    return render_template('apps/habit_tracker.html', habits=habits)

@productivity_bp.route('/add-habit', methods=['POST'])
def add_habit():
    habit_name = request.form.get('habit')
    if habit_name:
        habits = load_habits()
        new_habit = {
            'name': habit_name,
            'created_date': date.today().isoformat(),
            'completed_dates': []
        }
        habits.append(new_habit)
        save_habits(habits)
        flash('Habit added successfully!', 'success')
    return redirect(url_for('productivity.habit_tracker'))

@productivity_bp.route('/toggle-habit', methods=['POST'])
def toggle_habit():
    habit_index = int(request.form.get('habit_index'))
    today = date.today().isoformat()
    
    habits = load_habits()
    if 0 <= habit_index < len(habits):
        completed_dates = habits[habit_index]['completed_dates']
        if today in completed_dates:
            completed_dates.remove(today)
        else:
            completed_dates.append(today)
        save_habits(habits)
    
    return redirect(url_for('productivity.habit_tracker'))

@productivity_bp.route('/delete-habit', methods=['POST'])
def delete_habit():
    habit_index = int(request.form.get('habit_index'))
    habits = load_habits()
    if 0 <= habit_index < len(habits):
        habits.pop(habit_index)
        save_habits(habits)
        flash('Habit deleted successfully!', 'success')
    return redirect(url_for('productivity.habit_tracker'))

# Focus Logger Routes
@productivity_bp.route('/focus-logger')
def focus_logger():
    sessions = load_focus_sessions()
    today = date.today().isoformat()
    return render_template('apps/focus_logger.html', sessions=sessions, today=today)

@productivity_bp.route('/add-focus-session', methods=['POST'])
def add_focus_session():
    session_data = {
        'title': request.form.get('title'),
        'duration': int(request.form.get('duration')),
        'category': request.form.get('category'),
        'date': request.form.get('date'),
        'time': request.form.get('time'),
        'notes': request.form.get('notes', ''),
        'datetime': f"{request.form.get('date')} {request.form.get('time')}"
    }
    
    sessions = load_focus_sessions()
    sessions.append(session_data)
    save_focus_sessions(sessions)
    flash('Focus session logged!', 'success')
    return redirect(url_for('productivity.focus_logger'))

@productivity_bp.route('/delete-focus-session', methods=['POST'])
def delete_focus_session():
    session_id = int(request.form.get('session_id'))
    sessions = load_focus_sessions()
    if 0 <= session_id < len(sessions):
        sessions.pop(session_id)
        save_focus_sessions(sessions)
        flash('Session deleted!', 'success')
    return redirect(url_for('productivity.focus_logger'))

# Time Capsule Routes
@productivity_bp.route('/time-capsule')
def time_capsule():
    capsules = load_time_capsules()
    today = date.today().isoformat()
    
    # Process capsules to add computed fields
    for capsule in capsules:
        open_date = datetime.strptime(capsule['open_date'], '%Y-%m-%d').date()
        created_date = datetime.strptime(capsule['created_date'], '%Y-%m-%d').date()
        
        capsule['days_until_open'] = (open_date - date.today()).days
        capsule['days_since_created'] = (date.today() - created_date).days
        
        if open_date <= date.today() and capsule.get('status') != 'opened':
            capsule['status'] = 'ready'
        elif capsule.get('status') != 'opened':
            capsule['status'] = 'sealed'
    
    # Find next capsule to open
    next_capsule_date = None
    sealed_capsules = [c for c in capsules if c.get('status') == 'sealed']
    if sealed_capsules:
        next_capsule = min(sealed_capsules, key=lambda x: x['open_date'])
        next_capsule_date = next_capsule['open_date']
    
    return render_template('apps/time_capsule.html', 
                         capsules=capsules, 
                         today=today,
                         next_capsule_date=next_capsule_date)

@productivity_bp.route('/add-time-capsule', methods=['POST'])
def add_time_capsule():
    capsule_data = {
        'title': request.form.get('title'),
        'message': request.form.get('message'),
        'open_date': request.form.get('open_date'),
        'category': request.form.get('category'),
        'created_date': date.today().isoformat(),
        'status': 'sealed'
    }
    
    capsules = load_time_capsules()
    capsules.append(capsule_data)
    save_time_capsules(capsules)
    flash('Time capsule sealed! 🔒', 'success')
    return redirect(url_for('productivity.time_capsule'))

@productivity_bp.route('/open-capsule', methods=['POST'])
def open_capsule():
    capsule_id = int(request.form.get('capsule_id'))
    capsules = load_time_capsules()
    if 0 <= capsule_id < len(capsules):
        capsules[capsule_id]['status'] = 'opened'
        capsules[capsule_id]['opened_date'] = date.today().isoformat()
        save_time_capsules(capsules)
        flash('Time capsule opened! 🎁', 'success')
    return redirect(url_for('productivity.time_capsule'))

@productivity_bp.route('/delete-capsule', methods=['POST'])
def delete_capsule():
    capsule_id = int(request.form.get('capsule_id'))
    capsules = load_time_capsules()
    if 0 <= capsule_id < len(capsules):
        capsules.pop(capsule_id)
        save_time_capsules(capsules)
        flash('Time capsule deleted!', 'success')
    return redirect(url_for('productivity.time_capsule'))

# Time Block Planner Routes
@productivity_bp.route('/time-blocks')
def time_blocks():
    selected_date = request.args.get('date', date.today().isoformat())
    blocks = load_time_blocks()
    
    # Filter blocks for selected date
    daily_blocks = [b for b in blocks if b.get('date') == selected_date]
    
    # Calculate stats
    total_hours = sum(b.get('duration', 0) for b in daily_blocks)
    work_blocks = len([b for b in daily_blocks if b.get('category') == 'work'])
    personal_blocks = len([b for b in daily_blocks if b.get('category') == 'personal'])
    
    # Format date for display
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    current_date_formatted = date_obj.strftime('%A, %B %d, %Y')
    
    return render_template('apps/time_blocks.html', 
                         blocks=daily_blocks,
                         current_date=selected_date,
                         current_date_formatted=current_date_formatted,
                         total_hours=total_hours,
                         work_blocks=work_blocks,
                         personal_blocks=personal_blocks)

@productivity_bp.route('/add-time-block', methods=['POST'])
def add_time_block():
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    
    # Calculate duration
    start_dt = datetime.strptime(start_time, '%H:%M')
    end_dt = datetime.strptime(end_time, '%H:%M')
    duration = (end_dt - start_dt).seconds / 3600
    
    block_data = {
        'title': request.form.get('title'),
        'category': request.form.get('category'),
        'start_time': start_time,
        'end_time': end_time,
        'duration': duration,
        'notes': request.form.get('notes', ''),
        'date': request.form.get('date')
    }
    
    blocks = load_time_blocks()
    blocks.append(block_data)
    save_time_blocks(blocks)
    flash('Time block added!', 'success')
    return redirect(url_for('productivity.time_blocks', date=request.form.get('date')))

@productivity_bp.route('/delete-time-block', methods=['POST'])
def delete_time_block():
    block_id = int(request.form.get('block_id'))
    blocks = load_time_blocks()
    if 0 <= block_id < len(blocks):
        blocks.pop(block_id)
        save_time_blocks(blocks)
        flash('Time block deleted!', 'success')
    return redirect(url_for('productivity.time_blocks'))

# Helper functions for data management
def load_habits():
    try:
        with open(f'{DATA_DIR}/habits.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_habits(habits):
    with open(f'{DATA_DIR}/habits.json', 'w') as f:
        json.dump(habits, f)

def load_focus_sessions():
    try:
        with open(f'{DATA_DIR}/focus_sessions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_focus_sessions(sessions):
    with open(f'{DATA_DIR}/focus_sessions.json', 'w') as f:
        json.dump(sessions, f)

def load_time_capsules():
    try:
        with open(f'{DATA_DIR}/time_capsules.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_time_capsules(capsules):
    with open(f'{DATA_DIR}/time_capsules.json', 'w') as f:
        json.dump(capsules, f)

def load_time_blocks():
    try:
        with open(f'{DATA_DIR}/time_blocks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_time_blocks(blocks):
    with open(f'{DATA_DIR}/time_blocks.json', 'w') as f:
        json.dump(blocks, f)
