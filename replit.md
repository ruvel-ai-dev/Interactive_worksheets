# AI Worksheet Converter

## Overview

The AI Worksheet Converter is a Flask-based web application that transforms traditional educational worksheets (PDF/DOCX) into interactive learning experiences using artificial intelligence. The application extracts text from uploaded documents and generates various types of interactive tasks including multiple choice, fill-in-the-blank, short answer, and drag-and-drop exercises.

## System Architecture

The application follows a modular Flask architecture with clear separation of concerns:

- **Flask Web Framework**: Serves as the main application framework with Blueprint-based route organization
- **SQLAlchemy ORM**: Handles database operations with a declarative base model structure
- **Service Layer**: Encapsulates business logic for file processing, AI task generation, and task management
- **Template System**: Uses Jinja2 templates with Bootstrap for responsive UI
- **Background Processing**: Handles file upload and AI task generation workflow

## Key Components

### Backend Services
- **FileProcessor**: Handles file upload validation and text extraction from PDF/DOCX files using PyPDF2 and python-docx
- **AITaskGenerator**: Integrates with OpenAI's GPT-4o model to generate 10-20 educational tasks from extracted text with intelligent variation
- **TaskConverter**: Manages conversion of AI-generated tasks to database models and retrieval operations
- **EmailVerificationService**: Prevents fake email abuse through secure token-based email verification system

### Database Models
- **Worksheet**: Stores uploaded file metadata, extracted text, and processing status
- **Task**: Stores generated interactive tasks with JSON data structure for task-specific information
- **TaskResponse**: Prepared for future student response tracking (currently unused)
- **User**: Stores user information, subscription status, and usage tracking
- **EmailVerification**: Stores secure verification tokens with 24-hour expiration to prevent fake email usage

### Route Blueprints
- **upload_bp**: Handles file upload and processing workflow with subscription limits
- **tasks_bp**: Manages task viewing and API endpoints for task interaction
- **subscription_bp**: Manages Stripe payments, subscription management, and user accounts

### Frontend Components
- **Bootstrap-based UI**: Dark theme with responsive design
- **Interactive Task System**: JavaScript-powered task management with real-time feedback
- **File Upload Interface**: Drag-and-drop file upload with validation

## Data Flow

1. **File Upload**: User uploads PDF/DOCX file through web interface
2. **Text Extraction**: FileProcessor extracts text content from uploaded document
3. **Database Storage**: Worksheet record created with extracted text and metadata
4. **AI Processing**: AITaskGenerator sends extracted text to OpenAI GPT-4o for task generation
5. **Task Storage**: Generated tasks are converted and stored in database via TaskConverter
6. **Task Display**: Tasks are rendered in interactive web interface with JavaScript enhancements

## External Dependencies

### Python Packages
- **Flask**: Web framework and extensions (SQLAlchemy, etc.)
- **OpenAI**: GPT-4o API integration for task generation
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **Werkzeug**: File handling utilities
- **Stripe**: Payment processing and subscription management

### Frontend Libraries
- **Bootstrap**: UI framework with custom dark theme
- **Feather Icons**: Icon library for consistent UI elements
- **Custom JavaScript**: Task interaction and validation logic

### External APIs
- **OpenAI GPT-4o**: Core AI service for generating educational tasks from text content
- **Stripe**: Payment processing and subscription management service

## Deployment Strategy

The application is configured for cloud deployment with:

- **Environment Variables**: Configurable database URL, OpenAI API key, and session secret
- **ProxyFix Middleware**: Handles HTTPS URL generation in production environments
- **SQLAlchemy Engine Options**: Connection pooling and health checks for database reliability
- **File Upload Limits**: 16MB maximum file size with secure filename handling
- **Upload Directory**: Configurable file storage location

Database configuration supports both SQLite (development) and PostgreSQL (production) via environment variable configuration.

## Changelog

- July 06, 2025: Initial setup and core functionality
- July 06, 2025: Fixed template rendering issues with dictionary key access 
- July 06, 2025: Significantly improved AI task generation to create content-specific questions based on actual worksheet material rather than generic questions
- July 06, 2025: Added complete subscription system with Stripe integration, usage limits, and premium features
- July 06, 2025: Added multi-currency support (USD $9.99, GBP £7.99) with dynamic pricing page
- July 06, 2025: Added professional contact form with email forwarding to ruvel.ai.dev@gmail.com (email not exposed to users)
- July 06, 2025: Added user-friendly error pages (404, 500) and performance caching system for AI-generated tasks
- July 06, 2025: Enhanced AI task generation to create 10-20 questions with intelligent variation for limited content
- July 06, 2025: Implemented comprehensive email verification system to prevent fake email abuse and ensure authentic user registration

## User Preferences

Preferred communication style: Simple, everyday language.

## Testing Status

**Latest End-to-End Test (July 06, 2025):**
- ✅ Email verification system prevents fake email abuse
- ✅ Stripe integration creates real checkout sessions ($9.99 USD)
- ✅ Premium users bypass usage limits with unlimited access
- ✅ File upload accepts PDF/DOCX with proper validation
- ✅ AI task generation creates 15 intelligent questions per worksheet
- ✅ Database integration stores users, worksheets, tasks, and verification tokens
- ✅ Complete workflow from email verification → payment → upload → task generation

## Deployment

The application is ready for production deployment with custom domain support. See `DEPLOYMENT_GUIDE.md` for detailed instructions on:
- Setting up custom domains through Replit
- Configuring DNS records
- Environment variables for production
- SSL certificate setup
- Monitoring and scaling options