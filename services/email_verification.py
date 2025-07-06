"""
Email verification service to prevent fake email usage
"""
import secrets
import logging
import os
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Message
logger = logging.getLogger(__name__)

class EmailVerificationService:
    """Service for handling email verification"""
    
    @staticmethod
    def generate_verification_token():
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_verification_request(email):
        """Create a new email verification request"""
        try:
            from app import db
            from models import EmailVerification
            
            # Clean up old unverified requests for this email
            db.session.query(EmailVerification).filter_by(
                email=email, 
                verified=False
            ).delete()
            
            # Generate new token
            token = EmailVerificationService.generate_verification_token()
            expires_at = datetime.utcnow() + timedelta(hours=24)
            
            verification = EmailVerification(
                email=email,
                token=token,
                expires_at=expires_at
            )
            
            db.session.add(verification)
            db.session.commit()
            
            return token
            
        except Exception as e:
            logger.error(f"Error creating verification request: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def send_verification_email(email, token):
        """Send verification email to user"""
        try:
            mail = current_app.extensions.get('mail')
            if not mail:
                logger.warning("Mail not configured - verification email not sent")
                return False
            
            # Get domain from Replit environment
            domain = os.environ.get('REPLIT_DEV_DOMAIN') or os.environ.get('REPLIT_DOMAINS', '').split(',')[0] or 'localhost:5000'
            verification_url = f"https://{domain}/verify-email/{token}"
            
            msg = Message(
                subject="Verify Your Email - AI Worksheet Converter",
                recipients=[email],
                body=f"""
Hi there!

Welcome to AI Worksheet Converter! To complete your registration and start using our service, please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

If you didn't create an account with us, please ignore this email.

Best regards,
AI Worksheet Converter Team
                """
            )
            
            # For development, just log the verification URL instead of sending email
            if not current_app.config.get('MAIL_USERNAME'):
                logger.info(f"DEVELOPMENT MODE - Email verification URL: {verification_url}")
                return True
            
            mail.send(msg)
            logger.info(f"Verification email sent to {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending verification email to {email}: {e}")
            return False
    
    @staticmethod
    def verify_email_token(token):
        """Verify an email token and return the email if valid"""
        try:
            from app import db
            from models import EmailVerification
            
            verification = db.session.query(EmailVerification).filter_by(
                token=token,
                verified=False
            ).first()
            
            if not verification:
                return None, "Invalid or already used verification token"
            
            if verification.expires_at < datetime.utcnow():
                return None, "Verification token has expired"
            
            # Mark as verified
            verification.verified = True
            db.session.commit()
            
            logger.info(f"Email verified successfully: {verification.email}")
            return verification.email, None
            
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None, "Error verifying email"
    
    @staticmethod
    def is_email_verified(email):
        """Check if an email has been verified"""
        try:
            from app import db
            from models import EmailVerification
            
            verification = db.session.query(EmailVerification).filter_by(
                email=email,
                verified=True
            ).first()
            
            return verification is not None
            
        except Exception as e:
            logger.error(f"Error checking email verification: {e}")
            return False
    
    @staticmethod
    def cleanup_expired_tokens():
        """Clean up expired verification tokens"""
        try:
            from app import db
            from models import EmailVerification
            
            expired_count = db.session.query(EmailVerification).filter(
                EmailVerification.expires_at < datetime.utcnow(),
                EmailVerification.verified == False
            ).delete()
            
            db.session.commit()
            logger.info(f"Cleaned up {expired_count} expired verification tokens")
            
        except Exception as e:
            logger.error(f"Error cleaning up expired tokens: {e}")
            db.session.rollback()