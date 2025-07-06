# AI Worksheet Converter

Transform traditional educational worksheets into interactive learning experiences using artificial intelligence.

## Features

- **Smart File Processing**: Upload PDF and DOCX worksheets
- **AI-Powered Generation**: Creates 10-20 interactive questions using OpenAI GPT-4o
- **Multiple Question Types**: Multiple choice, fill-in-the-blank, short answer, and drag-and-drop
- **Subscription Model**: Free tier (3 conversions) and premium tier (unlimited)
- **Email Verification**: Prevents fake email abuse
- **Multi-Currency Support**: USD ($9.99) and GBP (£7.99) pricing
- **Real-time Feedback**: Instant answer validation and progress tracking

## Target Audience

- Homeschooling families
- 1-to-1 tutoring providers
- Educational content creators
- Teachers and educators

## Tech Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **AI Integration**: OpenAI GPT-4o
- **Payment Processing**: Stripe
- **Frontend**: Bootstrap, JavaScript
- **File Processing**: PyPDF2, python-docx
- **Email**: Flask-Mail with SMTP

## Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key
- Stripe account (for subscriptions)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-worksheet-converter.git
cd ai-worksheet-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY=your_openai_api_key
export STRIPE_SECRET_KEY=your_stripe_secret_key
export SESSION_SECRET=your_session_secret
export DATABASE_URL=your_database_url
```

4. Run the application:
```bash
python main.py
```

5. Visit `http://localhost:5000`

### Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `SESSION_SECRET`: Random secure string for sessions
- `DATABASE_URL`: PostgreSQL connection string

Optional (for email verification):
- `MAIL_SERVER`: SMTP server (default: smtp.gmail.com)
- `MAIL_PORT`: SMTP port (default: 587)
- `MAIL_USE_TLS`: Enable TLS (default: true)
- `MAIL_USERNAME`: SMTP username
- `MAIL_PASSWORD`: SMTP password

## Usage

1. **Sign Up**: Register with a valid email address
2. **Email Verification**: Click the verification link sent to your email
3. **Choose Plan**: Use free tier (3 conversions) or upgrade to premium
4. **Upload Worksheet**: Drag and drop PDF or DOCX files
5. **Generate Tasks**: AI creates 10-20 interactive questions
6. **Interactive Learning**: Students complete tasks with real-time feedback

## API Endpoints

- `GET /`: Home page
- `POST /upload`: Upload worksheet file
- `GET /worksheets`: List all worksheets
- `GET /tasks/<id>`: View interactive tasks
- `GET /pricing`: Subscription plans
- `POST /subscription/subscribe`: Create checkout session
- `GET /subscription/manage`: Manage subscription

## Project Structure

```
├── app.py                 # Flask application setup
├── main.py                # Entry point
├── models.py              # Database models
├── routes/                # Route handlers
│   ├── upload.py          # File upload handling
│   ├── tasks.py           # Task management
│   ├── subscription.py    # Payment processing
│   └── verification.py    # Email verification
├── services/              # Business logic
│   ├── ai_task_generator.py
│   ├── file_processor.py
│   ├── subscription_service.py
│   └── email_verification.py
├── templates/             # HTML templates
├── static/                # CSS, JS, images
└── uploads/               # User uploaded files
```

## Database Schema

- **User**: Email, subscription status, usage tracking
- **Worksheet**: File metadata, extracted text, processing status
- **Task**: Generated questions with JSON data structure
- **EmailVerification**: Secure verification tokens

## Security Features

- Email verification prevents fake accounts
- Environment variables for all secrets
- Secure file upload validation
- Usage limits and subscription management
- HTTPS in production

## Deployment

See `DEPLOYMENT_GUIDE.md` for detailed instructions on deploying to production with custom domains.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation files
- Review the deployment guide

## Acknowledgments

- OpenAI for GPT-4o API
- Stripe for payment processing
- Bootstrap for UI components
- Flask community for the framework