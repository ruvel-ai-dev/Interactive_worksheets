import logging
from models import Task, Worksheet, db

logger = logging.getLogger(__name__)

class TaskConverter:
    """Service for converting AI-generated tasks to database models"""
    
    @staticmethod
    def save_tasks_to_database(worksheet_id, tasks_data):
        """Save generated tasks to database"""
        try:
            # Clear existing tasks for this worksheet
            Task.query.filter_by(worksheet_id=worksheet_id).delete()
            
            saved_tasks = []
            for task_data in tasks_data:
                task = Task(
                    worksheet_id=worksheet_id,
                    task_type=task_data['task_type'],
                    question=task_data['question'],
                    task_data=task_data['task_data'],
                    order_index=task_data['order_index']
                )
                db.session.add(task)
                saved_tasks.append(task)
            
            db.session.commit()
            logger.info(f"Saved {len(saved_tasks)} tasks for worksheet {worksheet_id}")
            return saved_tasks
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving tasks to database: {str(e)}")
            raise Exception(f"Failed to save tasks: {str(e)}")
    
    @staticmethod
    def get_tasks_for_worksheet(worksheet_id):
        """Retrieve all tasks for a specific worksheet"""
        try:
            tasks = Task.query.filter_by(worksheet_id=worksheet_id).order_by(Task.order_index).all()
            return [task.to_dict() for task in tasks]
        except Exception as e:
            logger.error(f"Error retrieving tasks: {str(e)}")
            raise Exception(f"Failed to retrieve tasks: {str(e)}")
    
    @staticmethod
    def update_worksheet_status(worksheet_id, status):
        """Update worksheet processing status"""
        try:
            worksheet = Worksheet.query.get(worksheet_id)
            if worksheet:
                worksheet.processing_status = status
                db.session.commit()
                logger.info(f"Updated worksheet {worksheet_id} status to {status}")
            else:
                logger.warning(f"Worksheet {worksheet_id} not found")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating worksheet status: {str(e)}")
            raise Exception(f"Failed to update worksheet status: {str(e)}")
