import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_synthetic_data(output_path):
    """
    Generate synthetic stock data with clear cycles.
    
    Parameters:
    output_path (str): Path to save the CSV file
    """
    # Generate dates for 3 years of daily data
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 1, 1)
    
    # Create date range
    dates = []
    current_date = start_date
    while current_date < end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Generate time indices
    t = np.array([(d - start_date).days for d in dates])
    
    # Base price
    base_price = 100.0
    
    # Generate price with multiple cycles
    # 30-day cycle (monthly)
    monthly_cycle = 5.0 * np.sin(2 * np.pi * t / 30)
    
    # 90-day cycle (quarterly)
    quarterly_cycle = 10.0 * np.sin(2 * np.pi * t / 90)
    
    # 365-day cycle (yearly)
    yearly_cycle = 20.0 * np.sin(2 * np.pi * t / 365)
    
    # Random noise
    noise = np.random.normal(0, 2, len(t))
    
    # Linear trend
    trend = 0.05 * t
    
    # Combine components
    prices = base_price + monthly_cycle + quarterly_cycle + yearly_cycle + trend + noise
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'price': prices
    })
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Synthetic data saved to {output_path}")

def create_example_directory():
    """Create directory for example data files if it doesn't exist."""
    directory = os.path.join('static', 'examples')
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

if __name__ == '__main__':
    # Create examples directory
    examples_dir = create_example_directory()
    
    # Generate synthetic data
    synthetic_path = os.path.join(examples_dir, 'synthetic_example.csv')
    generate_synthetic_data(synthetic_path)
    
    # Note: You would also need to download or generate:
    # - S&P 500 data for sp500_example.csv
    # - Bitcoin data for bitcoin_example.csv
    # These could be downloaded from public APIs or financial data providers
    print("Example data generation complete.")