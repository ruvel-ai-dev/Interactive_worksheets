#!/usr/bin/env python3
"""
Test script to create a premium user and test the complete workflow
"""

import sys
import os
sys.path.append('.')

from app import create_app, db
from models import User, EmailVerification
from datetime import datetime, timedelta

def setup_premium_user():
    app = create_app()
    
    with app.app_context():
        # Create verified email
        verification = EmailVerification(
            email='test.premium@example.com',
            token='verified_token',
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=24),
            verified=True,
            attempts=0
        )
        
        # Create premium user
        user = User(
            email='test.premium@example.com',
            subscription_status='active',
            stripe_customer_id='cus_test123',
            stripe_subscription_id='sub_test123',
            worksheets_processed=0,
            created_date=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        
        try:
            db.session.add(verification)
            db.session.add(user)
            db.session.commit()
            print("✅ Created premium user with verified email")
            return True
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = setup_premium_user()
    sys.exit(0 if success else 1)