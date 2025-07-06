from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_mail import Mail, Message
import logging
import os

contact_bp = Blueprint('contact', __name__)
logger = logging.getLogger(__name__)

@contact_bp.route('/contact')
def contact():
    """Display contact form"""
    return render_template('contact.html')

@contact_bp.route('/contact', methods=['POST'])
def send_contact():
    """Handle contact form submission"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validate required fields
        if not name or not email or not subject or not message:
            flash('All fields are required.', 'error')
            return redirect(url_for('contact.contact'))
        
        # Create email message
        msg = Message(
            subject=f"Contact Form: {subject}",
            sender=os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@worksheetconverter.com'),
            recipients=['ruvel.ai.dev@gmail.com']
        )
        
        # Email body
        msg.body = f"""
New contact form submission:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
Sent from AI Worksheet Converter contact form
        """
        
        # Send email
        mail = current_app.extensions.get('mail')
        if mail:
            mail.send(msg)
        else:
            # Fallback: log the message if mail is not configured
            logger.info(f"Contact form message: {msg.body}")
        
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        logger.info(f"Contact form submitted by {name} ({email})")
        
    except Exception as e:
        logger.error(f"Error sending contact email: {str(e)}")
        flash('There was an error sending your message. Please try again.', 'error')
    
    return redirect(url_for('contact.contact'))