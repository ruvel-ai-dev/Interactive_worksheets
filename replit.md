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
- **AITaskGenerator**: Integrates with OpenAI's GPT-4o model to generate educational tasks from extracted text
- **TaskConverter**: Manages conversion of AI-generated tasks to database models and retrieval operations

### Database Models
- **Worksheet**: Stores uploaded file metadata, extracted text, and processing status
- **Task**: Stores generated interactive tasks with JSON data structure for task-specific information
- **TaskResponse**: Prepared for future student response tracking (currently unused)

### Route Blueprints
- **upload_bp**: Handles file upload and processing workflow
- **tasks_bp**: Manages task viewing and API endpoints for task interaction

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

### Frontend Libraries
- **Bootstrap**: UI framework with custom dark theme
- **Feather Icons**: Icon library for consistent UI elements
- **Custom JavaScript**: Task interaction and validation logic

### External APIs
- **OpenAI GPT-4o**: Core AI service for generating educational tasks from text content

## Deployment Strategy

The application is configured for cloud deployment with:

- **Environment Variables**: Configurable database URL, OpenAI API key, and session secret
- **ProxyFix Middleware**: Handles HTTPS URL generation in production environments
- **SQLAlchemy Engine Options**: Connection pooling and health checks for database reliability
- **File Upload Limits**: 16MB maximum file size with secure filename handling
- **Upload Directory**: Configurable file storage location

Database configuration supports both SQLite (development) and PostgreSQL (production) via environment variable configuration.

## Changelog

- July 06, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.