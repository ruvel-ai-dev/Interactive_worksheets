/**
 * TaskManager - Handles interactive task functionality
 */
class TaskManager {
    constructor() {
        this.tasks = [];
        this.completedTasks = new Set();
        this.initialize();
    }

    static init(tasksData) {
        const manager = new TaskManager();
        manager.tasks = tasksData;
        manager.setupEventListeners();
        manager.initializeDragAndDrop();
        return manager;
    }

    initialize() {
        // Initialize Feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    setupEventListeners() {
        // Check answer buttons
        document.querySelectorAll('.check-answer-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const taskId = e.target.dataset.taskId;
                this.checkAnswer(taskId);
            });
        });

        // Reset buttons
        document.querySelectorAll('.reset-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const taskId = e.target.dataset.taskId;
                this.resetTask(taskId);
            });
        });

        // Auto-save for text inputs
        document.querySelectorAll('input[type="text"], textarea').forEach(input => {
            input.addEventListener('input', () => {
                this.saveProgress();
            });
        });
    }

    async checkAnswer(taskId) {
        const task = this.tasks.find(t => t.id == taskId);
        if (!task) return;

        const answer = this.getTaskAnswer(taskId, task.task_type);
        const feedbackElement = document.getElementById(`feedback_${taskId}`);
        const taskCard = document.querySelector(`[data-task-id="${taskId}"]`);

        try {
            // For demo purposes, we'll do client-side checking
            // In production, you'd send this to the server
            const result = this.validateAnswer(task, answer);
            
            this.showFeedback(feedbackElement, result);
            this.updateTaskStatus(taskCard, result.is_correct);
            
            if (result.is_correct) {
                this.completedTasks.add(taskId);
            } else {
                this.completedTasks.delete(taskId);
            }
            
            this.updateProgress();
            
        } catch (error) {
            console.error('Error checking answer:', error);
            this.showError(feedbackElement, 'Error checking answer. Please try again.');
        }
    }

    getTaskAnswer(taskId, taskType) {
        switch (taskType) {
            case 'multiple_choice':
                const selectedOption = document.querySelector(`input[name="task_${taskId}"]:checked`);
                return selectedOption ? parseInt(selectedOption.value) : null;
            
            case 'fill_blank':
                const fillInput = document.getElementById(`task_${taskId}_answer`);
                return fillInput ? fillInput.value.trim() : '';
            
            case 'short_answer':
                const textArea = document.getElementById(`task_${taskId}_answer`);
                return textArea ? textArea.value.trim() : '';
            
            case 'drag_drop':
                const matches = {};
                const dropTargets = document.querySelectorAll(`#task_${taskId}_targets .drop-target`);
                dropTargets.forEach(target => {
                    const targetName = target.dataset.target;
                    const droppedItem = target.querySelector('.dropped-item .draggable-item');
                    if (droppedItem) {
                        matches[droppedItem.dataset.item] = targetName;
                    }
                });
                return matches;
            
            default:
                return null;
        }
    }

    validateAnswer(task, answer) {
        const taskData = task.task_data;
        
        switch (task.task_type) {
            case 'multiple_choice':
                const isCorrect = answer === taskData.correct_answer;
                return {
                    is_correct: isCorrect,
                    feedback: taskData.explanation || (isCorrect ? 'Correct!' : 'Incorrect. Try again.'),
                    correct_answer: taskData.correct_answer
                };
            
            case 'fill_blank':
                const correctAnswers = taskData.correct_answers || [];
                const caseSensitive = taskData.case_sensitive || false;
                
                let isMatch = false;
                if (caseSensitive) {
                    isMatch = correctAnswers.includes(answer);
                } else {
                    isMatch = correctAnswers.some(ca => ca.toLowerCase() === answer.toLowerCase());
                }
                
                return {
                    is_correct: isMatch,
                    feedback: taskData.explanation || (isMatch ? 'Correct!' : 'Incorrect. Try again.'),
                    correct_answers: correctAnswers
                };
            
            case 'short_answer':
                // For short answers, we'll just check if there's content
                // In a real app, you'd use NLP or manual review
                const hasContent = answer.length > 10;
                return {
                    is_correct: hasContent,
                    feedback: hasContent ? 'Good answer! Remember to check with your teacher.' : 'Please provide a more detailed answer.',
                    sample_answer: taskData.sample_answer
                };
            
            case 'drag_drop':
                const correctMatches = taskData.correct_matches || {};
                const userMatches = answer;
                
                let correctCount = 0;
                let totalCount = Object.keys(correctMatches).length;
                
                for (const [item, target] of Object.entries(correctMatches)) {
                    if (userMatches[item] === target) {
                        correctCount++;
                    }
                }
                
                const allCorrect = correctCount === totalCount;
                return {
                    is_correct: allCorrect,
                    feedback: allCorrect ? 'Perfect! All matches are correct.' : `${correctCount} out of ${totalCount} matches are correct.`,
                    correct_matches: correctMatches
                };
            
            default:
                return {
                    is_correct: false,
                    feedback: 'Unknown task type.'
                };
        }
    }

    showFeedback(feedbackElement, result) {
        feedbackElement.innerHTML = `
            <div class="d-flex align-items-center">
                <i data-feather="${result.is_correct ? 'check-circle' : 'x-circle'}" class="me-2"></i>
                <div>
                    <strong>${result.is_correct ? 'Correct!' : 'Incorrect'}</strong>
                    <div class="mt-1">${result.feedback}</div>
                </div>
            </div>
        `;
        
        feedbackElement.className = `task-feedback ${result.is_correct ? 'correct' : 'incorrect'}`;
        feedbackElement.style.display = 'block';
        
        // Re-initialize feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    showError(feedbackElement, message) {
        feedbackElement.innerHTML = `
            <div class="d-flex align-items-center">
                <i data-feather="alert-circle" class="me-2"></i>
                <div>
                    <strong>Error</strong>
                    <div class="mt-1">${message}</div>
                </div>
            </div>
        `;
        
        feedbackElement.className = 'task-feedback incorrect';
        feedbackElement.style.display = 'block';
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    updateTaskStatus(taskCard, isCorrect) {
        taskCard.className = taskCard.className.replace(/\b(correct|incorrect)\b/g, '');
        taskCard.classList.add(isCorrect ? 'correct' : 'incorrect');
    }

    updateProgress() {
        const totalTasks = this.tasks.length;
        const completedCount = this.completedTasks.size;
        const percentage = totalTasks > 0 ? (completedCount / totalTasks) * 100 : 0;
        
        const progressBar = document.getElementById('progressBar');
        const completedTasksElement = document.getElementById('completedTasks');
        
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
            progressBar.setAttribute('aria-valuenow', percentage);
        }
        
        if (completedTasksElement) {
            completedTasksElement.textContent = completedCount;
        }
    }

    resetTask(taskId) {
        const task = this.tasks.find(t => t.id == taskId);
        if (!task) return;

        // Clear answers based on task type
        switch (task.task_type) {
            case 'multiple_choice':
                document.querySelectorAll(`input[name="task_${taskId}"]`).forEach(input => {
                    input.checked = false;
                });
                break;
            
            case 'fill_blank':
                const fillInput = document.getElementById(`task_${taskId}_answer`);
                if (fillInput) fillInput.value = '';
                break;
            
            case 'short_answer':
                const textArea = document.getElementById(`task_${taskId}_answer`);
                if (textArea) textArea.value = '';
                break;
            
            case 'drag_drop':
                this.resetDragDrop(taskId);
                break;
        }

        // Clear feedback
        const feedbackElement = document.getElementById(`feedback_${taskId}`);
        if (feedbackElement) {
            feedbackElement.style.display = 'none';
        }

        // Reset task card status
        const taskCard = document.querySelector(`[data-task-id="${taskId}"]`);
        if (taskCard) {
            taskCard.className = taskCard.className.replace(/\b(correct|incorrect)\b/g, '');
        }

        // Update progress
        this.completedTasks.delete(taskId);
        this.updateProgress();
    }

    resetDragDrop(taskId) {
        const itemsContainer = document.getElementById(`task_${taskId}_items`);
        const targetsContainer = document.getElementById(`task_${taskId}_targets`);
        
        if (!itemsContainer || !targetsContainer) return;

        // Move all items back to the items container
        const droppedItems = targetsContainer.querySelectorAll('.draggable-item');
        droppedItems.forEach(item => {
            itemsContainer.appendChild(item);
        });

        // Clear all drop targets
        const dropTargets = targetsContainer.querySelectorAll('.drop-target .dropped-item');
        dropTargets.forEach(target => {
            target.innerHTML = '';
        });
    }

    initializeDragAndDrop() {
        // Initialize drag and drop for all drag-drop tasks
        document.querySelectorAll('.draggable-item').forEach(item => {
            item.addEventListener('dragstart', this.handleDragStart.bind(this));
            item.addEventListener('dragend', this.handleDragEnd.bind(this));
        });

        document.querySelectorAll('.drop-target').forEach(target => {
            target.addEventListener('dragover', this.handleDragOver.bind(this));
            target.addEventListener('drop', this.handleDrop.bind(this));
            target.addEventListener('dragenter', this.handleDragEnter.bind(this));
            target.addEventListener('dragleave', this.handleDragLeave.bind(this));
        });
    }

    handleDragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.dataset.item);
        e.target.classList.add('dragging');
    }

    handleDragEnd(e) {
        e.target.classList.remove('dragging');
    }

    handleDragOver(e) {
        e.preventDefault();
    }

    handleDragEnter(e) {
        e.preventDefault();
        e.currentTarget.classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.currentTarget.classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
        
        const itemData = e.dataTransfer.getData('text/plain');
        const droppedItem = document.querySelector(`[data-item="${itemData}"]`);
        const dropTarget = e.currentTarget.querySelector('.dropped-item');
        
        if (droppedItem && dropTarget) {
            // Remove item from its current location
            const currentParent = droppedItem.parentNode;
            
            // If there's already an item in the target, move it back
            const existingItem = dropTarget.querySelector('.draggable-item');
            if (existingItem) {
                currentParent.appendChild(existingItem);
            }
            
            // Add the dragged item to the target
            dropTarget.appendChild(droppedItem);
        }
    }

    saveProgress() {
        // Save progress to localStorage for persistence
        const progress = {
            timestamp: Date.now(),
            completed: Array.from(this.completedTasks),
            answers: this.getAllAnswers()
        };
        
        localStorage.setItem('worksheet_progress', JSON.stringify(progress));
    }

    getAllAnswers() {
        const answers = {};
        this.tasks.forEach(task => {
            const answer = this.getTaskAnswer(task.id, task.task_type);
            if (answer !== null && answer !== '' && answer !== undefined) {
                answers[task.id] = answer;
            }
        });
        return answers;
    }

    loadProgress() {
        const savedProgress = localStorage.getItem('worksheet_progress');
        if (savedProgress) {
            try {
                const progress = JSON.parse(savedProgress);
                // Restore completed tasks
                this.completedTasks = new Set(progress.completed || []);
                this.updateProgress();
                
                // You could restore answers here if needed
                // This would require more complex logic to set form values
            } catch (error) {
                console.error('Error loading progress:', error);
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // TaskManager will be initialized in the template with task data
});
