from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
import uuid
from utils.data_processing import analyze_stock_data
from utils.visualization import (
    create_time_series_plot, 
    create_power_spectrum_plot,
    create_combined_plot
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'csv'}

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing."""
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Check if the user submitted an empty form
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate a unique filename to prevent conflicts
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)
        
        try:
            # Process the file
            return redirect(url_for('results', filename=filename))
        except Exception as e:
            # Remove the file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            flash(f'Error processing file: {str(e)}')
            return redirect(request.url)
    else:
        flash('Invalid file format. Please upload a CSV file.')
        return redirect(request.url)

@app.route('/results')
def results():
    """Render the results page."""
    filename = request.args.get('filename')
    if not filename:
        flash('No file specified')
        return redirect(url_for('index'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        flash('File not found')
        return redirect(url_for('index'))
    
    # Render the results template
    return render_template('results.html', filename=filename)

@app.route('/api/analyze/<filename>')
def analyze(filename):
    """API endpoint to analyze stock data."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Analyze the stock data
        results = analyze_stock_data(file_path)
        
        # Create visualizations
        time_series_plot = create_time_series_plot(
            results['uniform_dates'], 
            results['uniform_prices']
        )
        power_spectrum_plot = create_power_spectrum_plot(
            results['frequencies'],
            results['power_spectrum']
        )
        combined_plot = create_combined_plot(
            results['uniform_dates'],
            results['uniform_prices'],
            results['frequencies'],
            results['power_spectrum']
        )
        
        # Format dominant cycles for display
        dominant_cycles_display = []
        for period, power in results['dominant_cycles']:
            if period >= 1:
                # For periods of days or longer
                if period >= 365:
                    years = period / 365
                    period_display = f"{years:.1f} years"
                elif period >= 30:
                    months = period / 30
                    period_display = f"{months:.1f} months"
                else:
                    period_display = f"{period:.1f} days"
            else:
                # For periods less than a day
                hours = period * 24
                period_display = f"{hours:.1f} hours"
            
            # Format power as percentage of maximum
            power_display = f"{power * 100:.1f}%"
            
            dominant_cycles_display.append({
                'period': period_display,
                'power': power_display
            })
        
        return jsonify({
            'time_series_plot': time_series_plot,
            'power_spectrum_plot': power_spectrum_plot,
            'combined_plot': combined_plot,
            'dominant_cycles': dominant_cycles_display
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples')
def get_examples():
    """API endpoint to get example datasets."""
    examples = [
        {
            'name': 'S&P 500 (2000-2020)',
            'description': 'Daily closing prices for the S&P 500 index from 2000 to 2020.',
            'url': url_for('static', filename='examples/sp500_example.csv')
        },
        {
            'name': 'Bitcoin (2017-2021)',
            'description': 'Daily closing prices for Bitcoin from 2017 to 2021.',
            'url': url_for('static', filename='examples/bitcoin_example.csv')
        },
        {
            'name': 'Synthetic Data (With Clear Cycles)',
            'description': 'Synthetic price data with clearly visible 30-day, 90-day and 365-day cycles.',
            'url': url_for('static', filename='examples/synthetic_example.csv')
        }
    ]
    return jsonify(examples)

@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    """Clean up uploaded files."""
    filename = request.json.get('filename')
    if filename:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)