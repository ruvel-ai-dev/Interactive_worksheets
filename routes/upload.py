import os
import logging
from flask import Blueprint, request, jsonify, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
from services.file_processor import FileProcessor
from services.ai_task_generator import AITaskGenerator
from services.task_converter import TaskConverter
from models import Worksheet, db

logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
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
        
        logger.info(f"Created worksheet record with ID: {worksheet.id}")
        
        # Generate tasks using AI
        try:
            ai_generator = AITaskGenerator()
            tasks_data = ai_generator.generate_tasks_from_text(file_info['extracted_text'])
            
            # Save tasks to database
            TaskConverter.save_tasks_to_database(worksheet.id, tasks_data)
            TaskConverter.update_worksheet_status(worksheet.id, 'completed')
            
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
        
        # Generate tasks using AI
        ai_generator = AITaskGenerator()
        tasks_data = ai_generator.generate_tasks_from_text(file_info['extracted_text'])
        
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
