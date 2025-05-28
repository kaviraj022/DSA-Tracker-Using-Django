// Track changed problems
let changedProblems = new Set();

// Handle editable fields
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.editable').forEach(field => {
        field.addEventListener('change', function() {
            changedProblems.add(this.dataset.id);
            this.classList.add('border-warning');
        });
    });
});

// Save all changes
function saveAllChanges() {
    const updates = Array.from(changedProblems).map(problemId => {
        const fields = document.querySelectorAll(`[data-id="${problemId}"]`);
        const data = {};
        fields.forEach(field => {
            data[field.dataset.field] = field.value;
        });
        return { id: problemId, ...data };
    });

    fetch('/admin/update_problems/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ problems: updates })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            changedProblems.clear();
            document.querySelectorAll('.editable').forEach(field => {
                field.classList.remove('border-warning');
            });
            showAlert('Changes saved successfully', 'success');
        } else {
            showAlert('Error saving changes: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        showAlert('Error saving changes: ' + error.message, 'danger');
    });
}

// Delete problem
function deleteProblem(problemId) {
    if (confirm('Are you sure you want to delete this problem? This will also delete all related notes and progress.')) {
        fetch(`/admin/problem/delete/${problemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const problemItem = document.querySelector(`[data-id="${problemId}"]`).closest('.problem-item');
                problemItem.remove();
                
                // Update problem counts
                updateProblemCounts();
                showAlert('Problem deleted successfully', 'success');
            } else {
                showAlert('Error deleting problem: ' + (data.error || 'Unknown error'), 'danger');
            }
        })
        .catch(error => {
            showAlert('Error deleting problem: ' + error.message, 'danger');
        });
    }
}

// Update problem counts after deletion
function updateProblemCounts() {
    document.querySelectorAll('.topic-section').forEach(topicSection => {
        const topicCount = topicSection.querySelectorAll('.problem-item').length;
        topicSection.querySelector('.problem-count').textContent = `(${topicCount})`;

        topicSection.querySelectorAll('.difficulty-section').forEach(diffSection => {
            const diffCount = diffSection.querySelectorAll('.problem-item').length;
            diffSection.querySelector('.problem-count').textContent = `(${diffCount})`;
        });
    });
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const alertsContainer = document.querySelector('.messages');
    if (!alertsContainer) {
        const container = document.createElement('div');
        container.className = 'messages position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    document.querySelector('.messages').appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
} 