# Email Verification Setup

The AI Worksheet Converter uses email verification to prevent abuse and ensure authentic user registration. Here's how to configure it:

## Development Mode
In development (no email configured), verification URLs are logged to console instead of sent via email.

## Production Setup
To enable email verification in production, set these environment variables:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

## Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" for this application
3. Use the app password as MAIL_PASSWORD (not your regular password)

## Alternative Email Providers
- **SendGrid**: Use their SMTP settings
- **Mailgun**: Use their SMTP settings
- **AWS SES**: Use their SMTP settings

## Security Features
- Tokens expire after 24 hours
- Only verified emails can upload worksheets
- Prevents fake email abuse
- Secure token generation using secrets module

## How It Works
1. User enters email on upload form
2. System checks if email is verified
3. If not verified, sends verification email
4. User clicks link to verify
5. System marks email as verified
6. User can now upload worksheets

## Testing
In development, check console logs for verification URLs when testing with fake emails.