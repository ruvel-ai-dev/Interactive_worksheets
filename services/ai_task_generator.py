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
        You are an expert educational content creator. Carefully analyze the following educational content and create {num_tasks} interactive learning tasks that are DIRECTLY based on the specific information, facts, concepts, examples, and details provided in the content.

        IMPORTANT INSTRUCTIONS:
        1. Read the content thoroughly and identify specific facts, concepts, examples, numbers, processes, and details
        2. Create questions that test understanding of the ACTUAL content provided, not generic knowledge
        3. Use exact terms, names, numbers, and examples from the original content
        4. If the content contains exercises, problems, or examples, create tasks based on those specific items
        5. Make sure every question can only be answered by someone who has read this specific content

        Content to analyze:
        {text}

        Generate tasks in this exact JSON format:
        {{
            "tasks": [
                {{
                    "task_type": "multiple_choice",
                    "question": "Based on the content, [specific question about actual content]",
                    "task_data": {{
                        "options": ["[correct answer from content]", "[plausible wrong answer]", "[plausible wrong answer]", "[plausible wrong answer]"],
                        "correct_answer": 0,
                        "explanation": "According to the content, [explanation citing specific details]"
                    }}
                }},
                {{
                    "task_type": "fill_blank",
                    "question": "[Use actual sentences or concepts from the content with blanks]: ___.",
                    "task_data": {{
                        "correct_answers": ["[exact term/phrase from content]"],
                        "case_sensitive": false,
                        "explanation": "This term appears specifically in the content when discussing [specific context]"
                    }}
                }},
                {{
                    "task_type": "short_answer",
                    "question": "Based on the content provided, explain [specific concept/process mentioned in the content].",
                    "task_data": {{
                        "sample_answer": "[Answer using information directly from the content]",
                        "key_points": ["[specific point 1 from content]", "[specific point 2 from content]"],
                        "max_length": 300
                    }}
                }},
                {{
                    "task_type": "drag_drop",
                    "question": "Match the [specific items mentioned in content] with their [corresponding information from content].",
                    "task_data": {{
                        "items": ["[actual item 1 from content]", "[actual item 2 from content]"],
                        "targets": ["[corresponding info 1 from content]", "[corresponding info 2 from content]"],
                        "correct_matches": {{"[actual item 1]": "[corresponding info 1]", "[actual item 2]": "[corresponding info 2]"}}
                    }}
                }}
            ]
        }}

        REQUIREMENTS:
        - Every question must reference specific information from the provided content
        - Use actual numbers, names, terms, examples, and facts from the content
        - Create realistic wrong answers for multiple choice that seem plausible but are incorrect
        - For fill-in-blank, use actual sentences or key phrases from the content
        - For drag-and-drop, use real relationships, categories, or matches found in the content
        - Ensure tasks test comprehension of the specific material, not general knowledge
        
        If the content contains math problems, science experiments, historical events, vocabulary terms, or specific procedures, make sure to create tasks directly testing those specific elements.
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
