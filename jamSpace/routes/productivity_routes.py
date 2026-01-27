from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
    # Default to monthly view in unified template
    return time_blocks_monthly()

@productivity_bp.route('/time-blocks/weekly')
def time_blocks_weekly():
    # Get the current week or specified week
    week_start = request.args.get('week_start')
    if week_start:
        try:
            current_week_start = datetime.strptime(week_start, '%Y-%m-%d').date()
        except ValueError:
            current_week_start = date.today()
            current_week_start = current_week_start - timedelta(days=current_week_start.weekday())
    else:
        current_week_start = date.today()
        current_week_start = current_week_start - timedelta(days=current_week_start.weekday())
    
    # Generate the 7 days of the week
    week_dates = []
    for i in range(7):
        week_date = current_week_start + timedelta(days=i)
        week_dates.append(week_date.isoformat())
    
    # Load all time blocks
    all_blocks = load_time_blocks()
    
    # Filter and expand blocks for this week
    week_blocks = []
    for block in all_blocks:
        if block.get('recurring'):
            # Check each day of the week for recurring blocks
            recurring_days = block.get('recurring_days', '').split(',')
            for date_str in week_dates:
                day_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                # Convert weekday: Python uses Mon=0, we use Sun=0
                adjusted_day = str((day_date.weekday() + 1) % 7)
                
                if adjusted_day in recurring_days:
                    expanded_block = block.copy()
                    expanded_block['date'] = date_str
                    expanded_block['is_recurring_instance'] = True
                    week_blocks.append(expanded_block)
        else:
            # Regular blocks - only include if within this week
            if block.get('date') in week_dates:
                week_blocks.append(block)
    
    # Format week display and navigation
    start_date = current_week_start
    end_date = current_week_start + timedelta(days=6)
    week_display = f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"
    
    # Calculate previous and next week dates
    prev_week = (current_week_start - timedelta(days=7)).isoformat()
    next_week = (current_week_start + timedelta(days=7)).isoformat()
    
    # Check if this is an AJAX request
    if request.args.get('ajax'):
        return jsonify({
            'blocks': week_blocks,
            'week_dates': week_dates,
            'week_display': week_display,
            'week_start': current_week_start.isoformat(),
            'prev_week': prev_week,
            'next_week': next_week,
            'today': date.today().isoformat()
        })
    
    return render_template('apps/time_blocks.html',
                         blocks=week_blocks,
                         week_dates=week_dates,
                         week_display=week_display,
                         week_start=current_week_start.isoformat(),
                         prev_week=prev_week,
                         next_week=next_week,
                         today=date.today().isoformat())

@productivity_bp.route('/time-blocks/monthly')
def time_blocks_monthly():
    # Get year and month from query params or default to current month
    year = int(request.args.get('year', date.today().year))
    month = int(request.args.get('month', date.today().month))
    
    # Get first day of the month and last day of the month
    first_day = date(year, month, 1)
    
    # Get the last day of the month
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    # Calculate calendar grid (start from Sunday before first day)
    start_day = first_day - timedelta(days=first_day.weekday() + 1)  # Go to Sunday
    if start_day.weekday() != 6:  # If not Sunday, go back to previous Sunday
        start_day = start_day - timedelta(days=(start_day.weekday() + 1))
    
    # Generate all days for the calendar (6 weeks)
    calendar_days = []
    current_date = start_day
    for _ in range(42):  # 6 weeks * 7 days
        calendar_days.append({
            'date': current_date.isoformat(),
            'day': current_date.day,
            'in_month': current_date.month == month
        })
        current_date += timedelta(days=1)
    
    # Load all blocks
    all_blocks = load_time_blocks()
    
    # Expand recurring blocks for the entire calendar view
    expanded_blocks = []
    for block in all_blocks:
        if block.get('recurring'):
            # Expand recurring block for each day it repeats in the calendar view
            recurring_days = block.get('recurring_days', '').split(',')
            for day_info in calendar_days:
                day_date = datetime.strptime(day_info['date'], '%Y-%m-%d').date()
                day_of_week = day_date.weekday()
                # Convert weekday: Python uses Mon=0, we use Sun=0
                adjusted_day = str((day_of_week + 1) % 7)
                
                if adjusted_day in recurring_days:
                    expanded_block = block.copy()
                    expanded_block['date'] = day_info['date']
                    expanded_block['is_recurring_instance'] = True
                    expanded_blocks.append(expanded_block)
        else:
            # Regular block
            expanded_blocks.append(block)
    
    # Format month name
    month_name = first_day.strftime('%B %Y')

    # Check if this is an AJAX request
    if request.args.get('ajax'):
        return jsonify({
            'blocks': expanded_blocks,
            'calendar_days': calendar_days,
            'current_month_display': month_name,
            'current_month': first_day.isoformat(),
            'today': date.today().isoformat()
        })
    
    return render_template('apps/time_blocks.html', 
                         blocks=expanded_blocks,
                         calendar_days=calendar_days,
                         current_month_display=month_name,
                         current_month=first_day.isoformat(),
                         today=date.today().isoformat())

@productivity_bp.route('/add-time-block', methods=['POST'])
def add_time_block():
    # Convert 12-hour format to 24-hour format
    start_hour = int(request.form.get('start_hour'))
    start_minute = request.form.get('start_minute')
    start_period = request.form.get('start_period')
    
    end_hour = int(request.form.get('end_hour'))
    end_minute = request.form.get('end_minute')
    end_period = request.form.get('end_period')
    
    # Convert to 24-hour format
    if start_period == 'PM' and start_hour != 12:
        start_hour += 12
    elif start_period == 'AM' and start_hour == 12:
        start_hour = 0
        
    if end_period == 'PM' and end_hour != 12:
        end_hour += 12
    elif end_period == 'AM' and end_hour == 12:
        end_hour = 0
    
    start_time = f"{start_hour:02d}:{start_minute}"
    end_time = f"{end_hour:02d}:{end_minute}"
    
    # Calculate duration
    start_dt = datetime.strptime(start_time, '%H:%M')
    end_dt = datetime.strptime(end_time, '%H:%M')
    duration = (end_dt - start_dt).seconds / 3600
    
    is_recurring = request.form.get('recurring') == 'true'
    recurring_days = request.form.get('recurring_days', '')
    
    block_data = {
        'title': request.form.get('title'),
        'category': request.form.get('category'),
        'start_time': start_time,
        'end_time': end_time,
        'duration': duration,
        'notes': request.form.get('notes', ''),
        'recurring': is_recurring,
        'recurring_days': recurring_days if is_recurring else '',
        'date': request.form.get('date') if not is_recurring else ''
    }
    
    blocks = load_time_blocks()
    blocks.append(block_data)
    save_time_blocks(blocks)
    
    # Return JSON response (compatible with both AJAX and regular form submissions)
    return jsonify({'success': True, 'message': 'Time block added!'})

@productivity_bp.route('/toggle-block-completion', methods=['POST'])
def toggle_block_completion():
    block_id = int(request.form.get('block_id'))
    completed = request.form.get('completed') == 'true'
    blocks = load_time_blocks()
    
    if 0 <= block_id < len(blocks):
        blocks[block_id]['completed'] = completed
        save_time_blocks(blocks)
        return '', 200
    return '', 400

@productivity_bp.route('/delete-time-block', methods=['POST'])
def delete_time_block():
    # Get block data instead of index to avoid index mismatches
    block_title = request.form.get('block_title')
    block_date = request.form.get('block_date')
    block_start_time = request.form.get('block_start_time')
    block_end_time = request.form.get('block_end_time')
    is_recurring = request.form.get('is_recurring') == 'true'
    
    blocks = load_time_blocks()
    deleted = False
    
    # Find and remove the matching block(s)
    if is_recurring:
        # For recurring blocks, remove the entire recurring pattern
        original_count = len(blocks)
        blocks = [b for b in blocks if not (
            b.get('title') == block_title and
            b.get('start_time') == block_start_time and
            b.get('end_time') == block_end_time and
            b.get('recurring') == True
        )]
        deleted = len(blocks) < original_count
    else:
        # For non-recurring blocks, find exact match by date, title, and time
        original_count = len(blocks)
        blocks = [b for b in blocks if not (
            b.get('title') == block_title and
            b.get('date') == block_date and
            b.get('start_time') == block_start_time and
            b.get('end_time') == block_end_time and
            not b.get('recurring')
        )]
        deleted = len(blocks) < original_count
    
    if deleted:
        save_time_blocks(blocks)
        message = 'Time block deleted successfully!'
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('ajax') or request.form.get('ajax'):
            return jsonify({'success': True, 'message': message})
        
        flash(message, 'success')
    else:
        message = 'Block not found or could not be deleted.'
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('ajax') or request.form.get('ajax'):
            return jsonify({'success': False, 'message': message})
        
        flash(message, 'error')
    
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
