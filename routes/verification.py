"""
Email verification routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from services.email_verification import EmailVerificationService
import logging

verification_bp = Blueprint('verification', __name__)
logger = logging.getLogger(__name__)

@verification_bp.route('/verify-email/<token>')
def verify_email(token):
    """Verify email address using token"""
    try:
        email, error = EmailVerificationService.verify_email_token(token)
        
        if error:
            flash(f'Email verification failed: {error}', 'error')
            return render_template('verification/verify_failed.html')
        
        # Store verified email in session
        session['user_email'] = email
        session['email_verified'] = True
        
        flash('Email verified successfully! You can now use the platform.', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Error in email verification: {e}")
        flash('An error occurred during verification. Please try again.', 'error')
        return render_template('verification/verify_failed.html')

@verification_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email"""
    try:
        email = request.form.get('email')
        if not email:
            flash('Email address is required', 'error')
            return redirect(url_for('index'))
        
        # Check if already verified
        if EmailVerificationService.is_email_verified(email):
            flash('This email is already verified', 'info')
            return redirect(url_for('index'))
        
        # Create new verification request
        token = EmailVerificationService.create_verification_request(email)
        
        # Send verification email
        if EmailVerificationService.send_verification_email(email, token):
            flash('Verification email sent! Please check your inbox.', 'success')
        else:
            flash('Failed to send verification email. Please try again later.', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Error resending verification: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@verification_bp.route('/verification-pending')
def verification_pending():
    """Show verification pending page"""
    email = session.get('pending_verification_email')
    return render_template('verification/pending.html', email=email)