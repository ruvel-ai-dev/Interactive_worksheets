# AI Worksheet Converter

AI Worksheet Converter is a Flask web application that transforms traditional PDF or DOCX worksheets into interactive tasks using OpenAI's GPT‑4o model. It supports multiple task types, a subscription system powered by Stripe, and an email verification workflow to prevent misuse.

## Features

- **Upload Worksheets**: Accepts PDF, DOCX, and DOC files up to 16MB.
- **AI Task Generation**: Extracts text and generates multiple choice, fill‑in‑the‑blank, short answer, and drag‑and‑drop activities.
- **Usage Limits & Subscriptions**: Free tier allows three worksheets; premium users get unlimited conversions via Stripe payments (USD or GBP).
- **Email Verification**: Users verify their email before processing worksheets to curb fake sign‑ups.
- **Caching Layer**: Recently generated tasks are cached on disk to speed up repeat requests.
- **Simple UI**: Responsive Bootstrap templates with JavaScript enhancements for checking answers and tracking progress.

## Getting Started

### Requirements

- Python 3.11+
- A virtual environment (recommended)
- OpenAI and Stripe accounts

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourname/ai-worksheet-converter.git
   cd ai-worksheet-converter
   ```

2. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # or `uv pip install -r uv.lock`
   ```

3. **Configure environment variables**

   Create a `.env` file or export the following variables:

   ```bash
   OPENAI_API_KEY=your-openai-key
   STRIPE_SECRET_KEY=your-stripe-key
   SESSION_SECRET=change-this-secret
   DATABASE_URL=sqlite:///worksheet_converter.db  # or your PostgreSQL URL

   # Optional (for email verification)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=you@example.com
   MAIL_PASSWORD=app-password
   MAIL_DEFAULT_SENDER=noreply@example.com
   ```

### Running the Application

Start the Flask app with:

```bash
python main.py
```

Visit `http://localhost:5000` in your browser to upload a worksheet. After uploading and verifying your email, the app generates interactive tasks that can be completed directly in the browser.

## Project Structure

```
app.py                 # Application factory and configuration
main.py                # Entry point used by gunicorn or Flask
models.py              # SQLAlchemy models
routes/                # Blueprint route handlers
services/              # Business logic (AI generation, file processing, etc.)
templates/             # Jinja2 templates
static/                # CSS and JS assets
uploads/               # Uploaded files (gitignored)
cache/                 # Cached tasks (gitignored)
```

Additional documentation:

- `DEPLOYMENT_GUIDE.md` – steps for deploying to Replit with a custom domain.
- `STRIPE_SETUP.md` – instructions for configuring Stripe pricing.
- `EMAIL_SETUP.md` – configuring email verification.
- `SECURITY_CHECKLIST.md` – overview of security considerations.

## License
This project is provided under the MIT License.
