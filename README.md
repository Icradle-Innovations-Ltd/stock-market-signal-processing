# Stock Market Signal Processing Web App

## Overview

This web application analyzes stock market data using signal processing techniques, specifically Fourier Transforms, to identify cyclical patterns and trends. Users can upload CSV files containing historical stock price data and receive visualizations and insights about recurring market cycles.

## Features

- **Data Analysis**: Processes time series stock data using Fast Fourier Transform (FFT)
- **Interactive Visualizations**: Displays time series and power spectrum plots
- **Cycle Detection**: Identifies dominant cycles in the data and ranks them by strength
- **Educational Content**: Provides explanations about signal processing concepts

## New Features

- **Error Handling**: Improved error messages for invalid CSV files and server errors.
- **File Download**: Users can download their uploaded files for reference.
- **Logging**: Added logging for better debugging and monitoring.

## Project Structure

```
stock-market-signal-processing/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Stylesheet
│   ├── js/
│   │   └── main.js         # Client-side JavaScript
│   └── examples/           # Example datasets
├── templates/              # HTML templates
│   ├── index.html          # Upload page
│   └── results.html        # Results display page
├── uploads/                # Temporary storage for uploaded files
└── utils/                  # Utility modules
    ├── data_processing.py  # Data loading and FFT logic
    ├── visualization.py    # Plotly visualization generation
    └── generate_examples.py # Script to generate example data
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Icradle-Innovations-Ltd/stock-market-signal-processing.git
   cd stock-market-signal-processing
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Generate example datasets:
   ```
   python utils/generate_examples.py
   ```

6. Run the application:
   ```
   python app.py
   ```

7. Open your browser and navigate to `http://localhost:5000`

## Usage

1. On the homepage, upload a CSV file containing stock price data.
   - The CSV must have columns named "date" and "price"
   - The date should be in YYYY-MM-DD format
   - Price should be a numeric value

2. Click "Analyze Data" to process the file.

3. View the results page with visualizations:
   - Time series plot
   - Power spectrum showing frequency components
   - List of dominant cycles ranked by strength

4. Use the interpretation guide to understand the analysis results.

## Data Format

The application expects CSV files with the following format:

```
date,price
2020-01-01,100.25
2020-01-02,101.50
2020-01-03,99.75
...
```

Example datasets are provided in the `static/examples/` directory.

## Technical Details

- **Framework**: Flask
- **Data Processing**: NumPy, SciPy, Pandas
- **Visualization**: Plotly
- **Signal Processing**: Fast Fourier Transform (FFT)

## Troubleshooting

### ModuleNotFoundError: No module named 'flask'

If you encounter this error, it means the Flask module is not installed in your virtual environment. Follow these steps to resolve it:

1. Ensure your virtual environment is activated:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify that Flask is installed:
   ```bash
   pip show flask
   ```

   If Flask is not listed, try installing it manually:
   ```bash
   pip install flask
   ```

4. Run the application again:
   ```bash
   python app.py
   ```

### Invalid CSV Format

If you encounter an error about missing columns, ensure your CSV file has the following columns:
- `date`: Date in YYYY-MM-DD format
- `price`: Numeric stock price

### Internal Server Error

If the application crashes, check the logs for detailed error messages:
```bash
tail -f app.log
```

If the issue persists, ensure that you are using the correct Python version and that the virtual environment is properly set up.

## Developed By

The Bazaar Team:
- Amanya Peter
- Doreen Miracle
- Twinomugisha Nickson
- Asiimwe Shabellah
- Kangwagye Jonas
- Amon Muhwezi
- Maro Edly
- Nanjuki Daphine
- Rwendeire Joshua Truth
- Katusiime Moreen

## License

[MIT License](LICENSE)
