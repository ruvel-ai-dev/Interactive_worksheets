from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from services.subscription_service import SubscriptionService
from models import User
from app import db
import logging

logger = logging.getLogger(__name__)

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/pricing')
def pricing():
    """Display pricing page"""
    return render_template('pricing.html')

@subscription_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Create subscription checkout session"""
    try:
        email = request.form.get('email')
        if not email:
            flash('Email is required', 'error')
            return redirect(url_for('subscription.pricing'))
        
        # Store email in session for later use
        session['user_email'] = email
        
        # Create checkout session
        checkout_session = SubscriptionService.create_checkout_session(email)
        
        return redirect(checkout_session.url, code=303)
    
    except Exception as e:
        logger.error(f"Error creating subscription: {str(e)}")
        flash('There was an error processing your subscription. Please try again.', 'error')
        return redirect(url_for('subscription.pricing'))

@subscription_bp.route('/success')
def success():
    """Handle successful subscription"""
    try:
        session_id = request.args.get('session_id')
        if not session_id:
            flash('Invalid session', 'error')
            return redirect(url_for('index'))
        
        # Handle successful payment
        user = SubscriptionService.handle_successful_payment(session_id)
        
        # Update session with user info
        session['user_email'] = user.email
        session['subscription_status'] = user.subscription_status
        
        flash('Subscription activated successfully! You now have unlimited access.', 'success')
        return render_template('subscription_success.html', user=user)
    
    except Exception as e:
        logger.error(f"Error handling successful subscription: {str(e)}")
        flash('There was an error activating your subscription. Please contact support.', 'error')
        return redirect(url_for('index'))

@subscription_bp.route('/cancel')
def cancel():
    """Handle subscription cancellation"""
    flash('Subscription cancelled. You can try again anytime.', 'info')
    return redirect(url_for('subscription.pricing'))

@subscription_bp.route('/manage')
def manage():
    """Display subscription management page"""
    email = session.get('user_email')
    if not email:
        flash('Please log in to manage your subscription', 'error')
        return redirect(url_for('subscription.pricing'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('subscription.pricing'))
    
    return render_template('manage_subscription.html', user=user)

@subscription_bp.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    """Cancel user's subscription"""
    try:
        email = session.get('user_email')
        if not email:
            return jsonify({'error': 'Not logged in'}), 401
        
        success = SubscriptionService.cancel_subscription(email)
        if success:
            return jsonify({'message': 'Subscription cancelled successfully'})
        else:
            return jsonify({'error': 'No active subscription found'}), 400
    
    except Exception as e:
        logger.error(f"Error cancelling subscription: {str(e)}")
        return jsonify({'error': 'Failed to cancel subscription'}), 500

@subscription_bp.route('/check-limit')
def check_limit():
    """Check user's usage limit"""
    email = session.get('user_email')
    if not email:
        return jsonify({'can_process': False, 'message': 'Please provide your email'})
    
    can_process = SubscriptionService.check_usage_limit(email)
    user = User.query.filter_by(email=email).first()
    
    if can_process:
        return jsonify({'can_process': True})
    else:
        return jsonify({
            'can_process': False,
            'worksheets_used': user.worksheets_processed if user else 0,
            'message': 'You have reached your free limit of 3 worksheets. Please upgrade to continue.'
        })