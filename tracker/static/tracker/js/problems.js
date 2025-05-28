// Group problems by topic and difficulty
function groupProblems() {
    const problems = document.querySelectorAll('.problem-item');
    const topicsMap = {};

    problems.forEach(problem => {
        const topic = problem.dataset.topic;
        const difficulty = problem.dataset.difficulty;
        
        if (!topicsMap[topic]) {
            topicsMap[topic] = {};
        }
        if (!topicsMap[topic][difficulty]) {
            topicsMap[topic][difficulty] = [];
        }
        topicsMap[topic][difficulty].push(problem);
    });

    return topicsMap;
}

// Toggle collapse for sections
function toggleCollapse(element) {
    const content = element.nextElementSibling;
    const icon = element.querySelector('.collapse-icon');
    
    if (content.style.display === 'none' || !content.style.display) {
        content.style.display = 'block';
        icon.textContent = '▼';
        element.classList.add('active');
    } else {
        content.style.display = 'none';
        icon.textContent = '▶';
        element.classList.remove('active');
    }
}

// Search suggestions functionality
let searchTimeout;

function updateSearchSuggestions() {
    const input = document.getElementById('problemSearch');
    const searchTerm = input.value.toLowerCase();
    const suggestionBox = document.getElementById('searchSuggestions');
    
    if (!searchTerm) {
        suggestionBox.innerHTML = '';
        suggestionBox.classList.add('d-none');
        return;
    }

    // Get all problem rows
    const problems = Array.from(document.querySelectorAll('#problemsTable tbody tr'))
        .map(row => ({
            element: row,
            text: row.querySelector('td:nth-child(2)').textContent, // Problem name column
            topic: row.dataset.topic,
            difficulty: row.dataset.difficulty
        }))
        .filter(({ text }) => text.toLowerCase().includes(searchTerm));

    // Clear previous suggestions
    suggestionBox.innerHTML = '';

    // Add new suggestions
    problems.slice(0, 5).forEach(({ text, element, topic, difficulty }) => {
        const div = document.createElement('div');
        div.className = 'suggestion-item';
        div.innerHTML = `
            <span class="problem-name">${text}</span>
            <span class="problem-meta">
                <span class="topic">${topic}</span>
                <span class="difficulty badge bg-${getDifficultyClass(difficulty)}">${difficulty}</span>
            </span>
        `;

        div.addEventListener('mousedown', (e) => {
            e.preventDefault();
            input.value = text;
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            element.classList.add('highlight');
            setTimeout(() => element.classList.remove('highlight'), 2000);
            suggestionBox.classList.add('d-none');
        });
        
        suggestionBox.appendChild(div);
    });

    suggestionBox.classList.remove('d-none');
}

// Helper function to get Bootstrap class for difficulty badges
function getDifficultyClass(difficulty) {
    switch (difficulty.toLowerCase()) {
        case 'easy': return 'success';
        case 'medium': return 'warning';
        case 'hard': return 'danger';
        default: return 'secondary';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('problemSearch');
    const suggestionBox = document.getElementById('searchSuggestions');

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(updateSearchSuggestions, 300);
        });
        
        // Close suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !suggestionBox.contains(e.target)) {
                suggestionBox.classList.add('d-none');
            }
        });
    }

    // Topic and difficulty filters
    const topicFilter = document.getElementById('topicFilter');
    const difficultyFilter = document.getElementById('difficultyFilter');

    function applyFilters() {
        const selectedTopic = topicFilter.value.toLowerCase();
        const selectedDifficulty = difficultyFilter.value.toLowerCase();

        document.querySelectorAll('#problemsTable tbody tr').forEach(row => {
            const topic = row.dataset.topic.toLowerCase();
            const difficulty = row.dataset.difficulty.toLowerCase();
            const topicMatch = !selectedTopic || topic === selectedTopic;
            const difficultyMatch = !selectedDifficulty || difficulty === selectedDifficulty;

            if (topicMatch && difficultyMatch) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    if (topicFilter) topicFilter.addEventListener('change', applyFilters);
    if (difficultyFilter) difficultyFilter.addEventListener('change', applyFilters);

    // Set up collapsible sections
    document.querySelectorAll('.topic-header, .difficulty-header').forEach(header => {
        header.addEventListener('click', () => toggleCollapse(header));
    });

    // Set up search functionality
    const searchInput = document.getElementById('searchInput');
    const searchSuggestions = document.getElementById('searchSuggestions');
    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.toLowerCase();
        
        if (!query) {
            searchSuggestions.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(() => {
            const problems = Array.from(document.querySelectorAll('.problem-item'))
                .filter(item => {
                    const name = item.querySelector('.problem-name').textContent.toLowerCase();
                    return name.includes(query);
                })
                .slice(0, 5);

            searchSuggestions.innerHTML = '';
            
            if (problems.length > 0) {
                problems.forEach(problem => {
                    const div = document.createElement('div');
                    div.className = 'suggestion-item';
                    div.textContent = problem.querySelector('.problem-name').textContent;
                    
                    div.addEventListener('click', () => {
                        // Expand parent sections
                        let parent = problem.parentElement;
                        while (parent && !parent.classList.contains('problems-container')) {
                            if (parent.style.display === 'none') {
                                const header = parent.previousElementSibling;
                                header.click();
                            }
                            parent = parent.parentElement;
                        }
                        
                        // Scroll to problem and highlight
                        problem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        problem.classList.add('highlight');
                        setTimeout(() => problem.classList.remove('highlight'), 2000);
                        
                        // Clear search
                        searchInput.value = '';
                        searchSuggestions.style.display = 'none';
                    });
                    
                    searchSuggestions.appendChild(div);
                });
                searchSuggestions.style.display = 'block';
            } else {
                searchSuggestions.style.display = 'none';
            }
        }, 300);
    });

    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
            searchSuggestions.style.display = 'none';
        }
    });

    // Handle progress toggle
    document.querySelectorAll('.progress-toggle').forEach(toggle => {
        toggle.addEventListener('change', function() {
            const problemId = this.dataset.problemId;
            fetch('/update_progress/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    problem_id: problemId,
                    is_completed: this.checked
                })
            });
        });
    });

    // Handle notes
    document.querySelectorAll('.note-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const problemId = this.dataset.problemId;
            const note = this.dataset.note;
            
            // Set up modal
            const modal = new bootstrap.Modal(document.getElementById('noteModal'));
            document.getElementById('noteText').value = note;
            
            // Set up save handler
            window.saveNote = function() {
                const noteText = document.getElementById('noteText').value;
                fetch('/save_note/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({
                        problem_id: problemId,
                        note: noteText
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        btn.dataset.note = noteText;
                        modal.hide();
                    }
                });
            };
            
            modal.show();
        });
    });
}); 