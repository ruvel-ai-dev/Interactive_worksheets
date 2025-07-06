import os
import logging
from flask import Blueprint, request, jsonify, current_app, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from services.file_processor import FileProcessor
from services.ai_task_generator import AITaskGenerator
from services.task_converter import TaskConverter
from services.subscription_service import SubscriptionService
from models import Worksheet, db

logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        # Get user email from form
        user_email = request.form.get('email')
        
        if not user_email:
            flash('Email is required. Please provide your email address.', 'error')
            return redirect(url_for('index'))
        
        # Check usage limits
        if not SubscriptionService.check_usage_limit(user_email):
            flash('You have reached your free limit of 3 worksheets. Please upgrade to Premium for unlimited access.', 'error')
            return redirect(url_for('subscription.pricing'))
        
        # Check if file is present
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not FileProcessor.is_allowed_file(file.filename):
            flash('File type not allowed. Please upload PDF or DOCX files.', 'error')
            return redirect(url_for('index'))
        
        # Store user email in session
        session['user_email'] = user_email
        
        # Get or create user and link to worksheet
        user = SubscriptionService.get_or_create_user(user_email)
        
        # Process the file
        file_info = FileProcessor.process_file(file, current_app.config['UPLOAD_FOLDER'])
        
        # Create worksheet record
        worksheet = Worksheet(
            filename=file_info['filename'],
            original_filename=file.filename,
            file_type=file_info['file_type'],
            extracted_text=file_info['extracted_text'],
            processing_status='processing',
            user_id=user.id
        )
        
        db.session.add(worksheet)
        db.session.commit()
        
        logger.info(f"Created worksheet record with ID: {worksheet.id}")
        
        # Generate 15 tasks using AI
        try:
            ai_generator = AITaskGenerator()
            tasks_data = ai_generator.generate_tasks_from_text(file_info['extracted_text'], num_tasks=15)
            
            # Save tasks to database
            TaskConverter.save_tasks_to_database(worksheet.id, tasks_data)
            TaskConverter.update_worksheet_status(worksheet.id, 'completed')
            
            # Increment user's usage count
            SubscriptionService.increment_usage(user_email)
            
            flash('Worksheet processed successfully!', 'success')
            return redirect(url_for('tasks.view_tasks', worksheet_id=worksheet.id))
            
        except Exception as e:
            logger.error(f"Error generating tasks: {str(e)}")
            TaskConverter.update_worksheet_status(worksheet.id, 'failed')
            flash(f'Error generating tasks: {str(e)}', 'error')
            return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        flash(f'Error uploading file: {str(e)}', 'error')
        return redirect(url_for('index'))

@upload_bp.route('/api/upload', methods=['POST'])
def api_upload_file():
    """API endpoint for file upload (for future AJAX use)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not FileProcessor.is_allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Process the file
        file_info = FileProcessor.process_file(file, current_app.config['UPLOAD_FOLDER'])
        
        # Create worksheet record
        worksheet = Worksheet(
            filename=file_info['filename'],
            original_filename=file.filename,
            file_type=file_info['file_type'],
            extracted_text=file_info['extracted_text'],
            processing_status='processing'
        )
        
        db.session.add(worksheet)
        db.session.commit()
        
        # Generate 15 tasks using AI
        ai_generator = AITaskGenerator()
        tasks_data = ai_generator.generate_tasks_from_text(file_info['extracted_text'], num_tasks=15)
        
        # Save tasks to database
        TaskConverter.save_tasks_to_database(worksheet.id, tasks_data)
        TaskConverter.update_worksheet_status(worksheet.id, 'completed')
        
        return jsonify({
            'message': 'File processed successfully',
            'worksheet_id': worksheet.id,
            'tasks_count': len(tasks_data)
        })
        
    except Exception as e:
        logger.error(f"API upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500
