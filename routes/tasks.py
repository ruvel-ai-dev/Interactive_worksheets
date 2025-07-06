import logging
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from services.task_converter import TaskConverter
from models import Worksheet, Task

logger = logging.getLogger(__name__)

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/<int:worksheet_id>')
def view_tasks(worksheet_id):
    """Display interactive tasks for a worksheet"""
    try:
        # Get worksheet info
        worksheet = Worksheet.query.get_or_404(worksheet_id)
        
        # Get tasks for this worksheet
        tasks_data = TaskConverter.get_tasks_for_worksheet(worksheet_id)
        
        if not tasks_data:
            flash('No tasks found for this worksheet', 'warning')
            return redirect(url_for('index'))
        
        logger.info(f"Rendering template with {len(tasks_data)} tasks")
        return render_template('tasks.html', 
                             worksheet=worksheet, 
                             tasks=tasks_data)
        
    except Exception as e:
        logger.error(f"Error viewing tasks: {str(e)}")
        flash(f'Error loading tasks: {str(e)}', 'error')
        return redirect(url_for('index'))

@tasks_bp.route('/api/tasks/<int:worksheet_id>')
def api_get_tasks(worksheet_id):
    """API endpoint to get tasks for a worksheet"""
    try:
        tasks = TaskConverter.get_tasks_for_worksheet(worksheet_id)
        return jsonify({'tasks': tasks})
    except Exception as e:
        logger.error(f"API error getting tasks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/api/tasks/<int:task_id>/check', methods=['POST'])
def api_check_answer(task_id):
    """API endpoint to check student answer (for future use)"""
    try:
        task = Task.query.get_or_404(task_id)
        student_answer = request.json.get('answer')
        
        # Basic answer checking logic
        is_correct = False
        feedback = ""
        
        if task.task_type == 'multiple_choice':
            correct_answer = task.task_data.get('correct_answer')
            is_correct = student_answer == correct_answer
            feedback = task.task_data.get('explanation', '')
        
        elif task.task_type == 'fill_blank':
            correct_answers = task.task_data.get('correct_answers', [])
            case_sensitive = task.task_data.get('case_sensitive', False)
            
            if case_sensitive:
                is_correct = student_answer in correct_answers
            else:
                is_correct = student_answer.lower() in [ans.lower() for ans in correct_answers]
            
            feedback = task.task_data.get('explanation', '')
        
        return jsonify({
            'is_correct': is_correct,
            'feedback': feedback,
            'correct_answer': task.task_data.get('correct_answer') if task.task_type == 'multiple_choice' else None
        })
        
    except Exception as e:
        logger.error(f"Error checking answer: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/worksheets')
def list_worksheets():
    """List all uploaded worksheets"""
    try:
        worksheets = Worksheet.query.order_by(Worksheet.upload_date.desc()).all()
        return render_template('worksheets.html', worksheets=worksheets)
    except Exception as e:
        logger.error(f"Error listing worksheets: {str(e)}")
        flash(f'Error loading worksheets: {str(e)}', 'error')
        return redirect(url_for('index'))
