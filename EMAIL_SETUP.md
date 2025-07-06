# Email Configuration for Contact Form

## Setup Instructions

To enable email forwarding for the contact form, you need to configure SMTP settings in your Replit secrets.

### Required Secrets

Add these secrets in your Replit project:

1. **MAIL_USERNAME** - Your email address (e.g., your-app@gmail.com)
2. **MAIL_PASSWORD** - Your email password or app password
3. **MAIL_DEFAULT_SENDER** - Default sender email (can be same as MAIL_USERNAME)

### Gmail Setup (Recommended)

If using Gmail:
1. Create a Gmail account for your app
2. Enable 2-factor authentication
3. Generate an App Password (not your regular password)
4. Use the App Password for MAIL_PASSWORD

### Default Configuration

The contact form is configured to:
- Use Gmail SMTP (smtp.gmail.com:587)
- Forward messages to: `ruvel.ai.dev@gmail.com`
- Your email address is NOT displayed to users
- All contact form messages are forwarded securely

### Fallback Behavior

If email is not configured:
- Messages are logged to console
- User still sees success message
- No email is sent (graceful fallback)

## Testing

1. Set up the email secrets
2. Visit `/contact` page
3. Submit a test message
4. Check your inbox for the forwarded message

## Security Notes

- Your email address is never exposed to users
- All messages are forwarded through the server
- Users only see a generic success message
- Email configuration is environment-based and secure