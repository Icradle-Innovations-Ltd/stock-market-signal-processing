document.addEventListener('DOMContentLoaded', function() {
    // Handle file selection display
    const fileInput = document.getElementById('file');
    const fileName = document.getElementById('file-name');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                fileName.textContent = this.files[0].name;
            } else {
                fileName.textContent = 'No file selected';
            }
        });
    }
    
    // Load example datasets
    const exampleList = document.getElementById('example-list');
    if (exampleList) {
        fetch('/api/examples')
            .then(response => response.json())
            .then(examples => {
                exampleList.innerHTML = '';
                
                if (examples && examples.length > 0) {
                    examples.forEach(example => {
                        const card = document.createElement('div');
                        card.className = 'example-card';
                        
                        const title = document.createElement('h3');
                        title.textContent = example.name;
                        
                        const description = document.createElement('p');
                        description.textContent = example.description;
                        
                        const link = document.createElement('a');
                        link.href = example.url;
                        link.className = 'example-link';
                        link.textContent = 'Download Example';
                        link.setAttribute('download', '');
                        
                        card.appendChild(title);
                        card.appendChild(description);
                        card.appendChild(link);
                        
                        exampleList.appendChild(card);
                    });
                } else {
                    exampleList.innerHTML = '<p>No example datasets available.</p>';
                }
            })
            .catch(error => {
                console.error('Error loading examples:', error);
                exampleList.innerHTML = '<p>Failed to load example datasets.</p>';
            });
    }
    
    // Form validation
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            const fileInput = document.getElementById('file');
            
            // Check if a file is selected
            if (!fileInput.files || fileInput.files.length === 0) {
                event.preventDefault();
                alert('Please select a CSV file to upload.');
                return false;
            }
            
            // Check file extension
            const fileName = fileInput.files[0].name;
            const fileExt = fileName.split('.').pop().toLowerCase();
            
            if (fileExt !== 'csv') {
                event.preventDefault();
                alert('Only CSV files are allowed.');
                return false;
            }
            
            // File size validation (max 10MB)
            const maxSize = 10 * 1024 * 1024; // 10MB in bytes
            if (fileInput.files[0].size > maxSize) {
                event.preventDefault();
                alert('File size exceeds the limit of 10MB.');
                return false;
            }
            
            // Add loading state
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Uploading...';
            
            return true;
        });
    }
});

// Resize Plotly charts when window is resized
window.addEventListener('resize', function() {
    const plots = document.querySelectorAll('.plot');
    plots.forEach(function(plot) {
        if (plot.layout) {
            Plotly.relayout(plot.id, {
                'width': plot.offsetWidth,
                'height': plot.offsetHeight
            });
        }
    });
});