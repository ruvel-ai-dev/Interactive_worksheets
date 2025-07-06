import json
import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class AITaskGenerator:
    """Service for generating interactive tasks using OpenAI GPT-4"""
    
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")
        )
    
    def generate_tasks_from_text(self, text, num_tasks=5):
        """Generate interactive tasks from extracted text using OpenAI"""
        try:
            prompt = self._create_task_generation_prompt(text, num_tasks)
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational content creator. "
                                 "Generate interactive learning tasks based on the provided text. "
                                 "Always respond with valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=2000,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return self._validate_and_format_tasks(result)
            
        except Exception as e:
            logger.error(f"Error generating tasks with OpenAI: {str(e)}")
            raise Exception(f"Failed to generate tasks: {str(e)}")
    
    def _create_task_generation_prompt(self, text, num_tasks):
        """Create a detailed prompt for task generation"""
        return f"""
        Based on the following educational content, generate {num_tasks} interactive learning tasks.
        
        Content:
        {text}
        
        Generate tasks in the following JSON format:
        {{
            "tasks": [
                {{
                    "task_type": "multiple_choice",
                    "question": "What is the main concept discussed?",
                    "task_data": {{
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "Brief explanation of the correct answer"
                    }}
                }},
                {{
                    "task_type": "fill_blank",
                    "question": "Complete the sentence: The main idea is ___.",
                    "task_data": {{
                        "correct_answers": ["answer1", "answer2"],
                        "case_sensitive": false,
                        "explanation": "Brief explanation"
                    }}
                }},
                {{
                    "task_type": "short_answer",
                    "question": "Explain the concept in your own words.",
                    "task_data": {{
                        "sample_answer": "Sample answer for reference",
                        "key_points": ["point1", "point2"],
                        "max_length": 200
                    }}
                }},
                {{
                    "task_type": "drag_drop",
                    "question": "Match the terms with their definitions.",
                    "task_data": {{
                        "items": ["Term 1", "Term 2"],
                        "targets": ["Definition 1", "Definition 2"],
                        "correct_matches": {{"Term 1": "Definition 1", "Term 2": "Definition 2"}}
                    }}
                }}
            ]
        }}
        
        Task types to use:
        - multiple_choice: 4 options, 1 correct answer
        - fill_blank: Fill in the blank questions
        - short_answer: Open-ended questions
        - drag_drop: Matching exercises
        
        Make sure all tasks are educational, relevant to the content, and appropriately challenging.
        """
    
    def _validate_and_format_tasks(self, ai_response):
        """Validate and format the AI response"""
        try:
            if 'tasks' not in ai_response:
                raise ValueError("Invalid response format: missing 'tasks' key")
            
            tasks = ai_response['tasks']
            formatted_tasks = []
            
            for i, task in enumerate(tasks):
                # Validate required fields
                if 'task_type' not in task or 'question' not in task or 'task_data' not in task:
                    logger.warning(f"Skipping invalid task at index {i}: missing required fields")
                    continue
                
                # Validate task type
                valid_types = ['multiple_choice', 'fill_blank', 'short_answer', 'drag_drop']
                if task['task_type'] not in valid_types:
                    logger.warning(f"Skipping task with invalid type: {task['task_type']}")
                    continue
                
                formatted_task = {
                    'task_type': task['task_type'],
                    'question': task['question'],
                    'task_data': task['task_data'],
                    'order_index': i
                }
                
                formatted_tasks.append(formatted_task)
            
            return formatted_tasks
            
        except Exception as e:
            logger.error(f"Error validating tasks: {str(e)}")
            raise Exception(f"Failed to validate generated tasks: {str(e)}")
