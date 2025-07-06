import os
import stripe
from flask import session
from datetime import datetime, timedelta
from app import db
from models import User

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class SubscriptionService:
    """Service for handling Stripe subscriptions"""
    
    # Get domain for redirect URLs
    @staticmethod
    def get_domain():
        """Get the current domain for Stripe redirects"""
        domain = os.environ.get('REPLIT_DEV_DOMAIN')
        if not domain:
            domains = os.environ.get('REPLIT_DOMAINS', '').split(',')
            domain = domains[0] if domains else 'localhost:5000'
        return domain
    
    @staticmethod
    def create_checkout_session(user_email, price_id="price_1234567890"):
        """Create a Stripe checkout session for subscription"""
        try:
            domain = SubscriptionService.get_domain()
            
            # Create or get customer
            customer = SubscriptionService.get_or_create_customer(user_email)
            
            checkout_session = stripe.checkout.Session.create(
                customer=customer.id,
                line_items=[
                    {
                        'price': price_id,  # You'll need to create this in Stripe dashboard
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=f'https://{domain}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'https://{domain}/subscription/cancel',
                allow_promotion_codes=True,
                billing_address_collection='auto',
                customer_update={
                    'address': 'auto',
                    'name': 'auto'
                }
            )
            
            return checkout_session
        except Exception as e:
            raise Exception(f"Error creating checkout session: {str(e)}")
    
    @staticmethod
    def get_or_create_customer(email):
        """Get or create a Stripe customer"""
        try:
            # Check if customer exists
            customers = stripe.Customer.list(email=email, limit=1)
            
            if customers.data:
                return customers.data[0]
            
            # Create new customer
            customer = stripe.Customer.create(
                email=email,
                description=f"Worksheet Converter User - {email}"
            )
            
            return customer
        except Exception as e:
            raise Exception(f"Error handling customer: {str(e)}")
    
    @staticmethod
    def handle_successful_payment(session_id):
        """Handle successful payment and update user subscription"""
        try:
            # Retrieve the session
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Get customer and subscription
            customer_id = session.customer
            subscription_id = session.subscription
            
            # Get customer email
            customer = stripe.Customer.retrieve(customer_id)
            email = customer.email
            
            # Get subscription details
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Update or create user in database
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email)
                db.session.add(user)
            
            # Update subscription info
            user.stripe_customer_id = customer_id
            user.stripe_subscription_id = subscription_id
            user.subscription_status = 'active'
            user.subscription_start_date = datetime.fromtimestamp(subscription.current_period_start)
            user.subscription_end_date = datetime.fromtimestamp(subscription.current_period_end)
            
            db.session.commit()
            
            return user
        except Exception as e:
            raise Exception(f"Error handling successful payment: {str(e)}")
    
    @staticmethod
    def cancel_subscription(user_email):
        """Cancel a user's subscription"""
        try:
            user = User.query.filter_by(email=user_email).first()
            if not user or not user.stripe_subscription_id:
                return False
            
            # Cancel the subscription in Stripe
            stripe.Subscription.modify(
                user.stripe_subscription_id,
                cancel_at_period_end=True
            )
            
            # Update user status
            user.subscription_status = 'canceled'
            db.session.commit()
            
            return True
        except Exception as e:
            raise Exception(f"Error canceling subscription: {str(e)}")
    
    @staticmethod
    def get_or_create_user(email):
        """Get or create a user by email"""
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
        return user
    
    @staticmethod
    def check_usage_limit(email):
        """Check if user has exceeded their usage limit"""
        user = SubscriptionService.get_or_create_user(email)
        return user.can_process_worksheet()
    
    @staticmethod
    def increment_usage(email):
        """Increment user's worksheet processing count"""
        user = SubscriptionService.get_or_create_user(email)
        user.increment_usage()
        return user