from app import db
from datetime import datetime
from sqlalchemy import Text, JSON, Column, Integer, String, DateTime, Boolean

class Worksheet(db.Model):
    """Model for storing uploaded worksheets and their metadata"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # 'pdf' or 'docx'
    extracted_text = db.Column(Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    processing_status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Link to user
    
    # Relationship to tasks
    tasks = db.relationship('Task', backref='worksheet', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    """Model for storing generated interactive tasks"""
    id = db.Column(db.Integer, primary_key=True)
    worksheet_id = db.Column(db.Integer, db.ForeignKey('worksheet.id'), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # multiple_choice, fill_blank, short_answer, drag_drop
    question = db.Column(Text, nullable=False)
    task_data = db.Column(JSON)  # Store task-specific data (options, correct answers, etc.)
    order_index = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert task to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'task_type': self.task_type,
            'question': self.question,
            'task_data': self.task_data,
            'order_index': self.order_index
        }

class TaskResponse(db.Model):
    """Model for storing student responses to tasks (for future use)"""
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    student_id = db.Column(db.String(100))  # For future user management
    response_data = db.Column(JSON)
    is_correct = db.Column(db.Boolean)
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    """Model for storing user information and subscription status"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    subscription_status = db.Column(db.String(20), default='free')  # free, active, past_due, canceled
    stripe_customer_id = db.Column(db.String(255))
    stripe_subscription_id = db.Column(db.String(255))
    subscription_start_date = db.Column(db.DateTime)
    subscription_end_date = db.Column(db.DateTime)
    worksheets_processed = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_premium(self):
        """Check if user has active premium subscription"""
        return self.subscription_status == 'active'
    
    def can_process_worksheet(self):
        """Check if user can process another worksheet"""
        if self.is_premium():
            return True
        return self.worksheets_processed < 3  # Free users get 3 worksheets
    
    def increment_usage(self):
        """Increment worksheet processing count"""
        self.worksheets_processed += 1
        self.last_active = datetime.utcnow()
        db.session.commit()

class EmailVerification(db.Model):
    """Model for storing email verification tokens"""
    __tablename__ = 'email_verification'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    token = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
