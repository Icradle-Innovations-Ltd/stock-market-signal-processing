import numpy as np
import pandas as pd
from scipy import signal
import os
from datetime import datetime

def load_stock_data(file_path):
    """
    Load stock data from a CSV file.
    
    Parameters:
    file_path (str): Path to the CSV file containing stock data
    
    Returns:
    pandas.DataFrame: DataFrame containing the stock data
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Validate column names
        required_columns = {'date', 'price'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        return df
    except pd.errors.EmptyDataError:
        raise ValueError("The uploaded file is empty.")
    except pd.errors.ParserError:
        raise ValueError("The uploaded file is not a valid CSV.")
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {str(e)}")

def preprocess_data(df):
    """
    Preprocess the stock data for FFT analysis.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing stock data
    
    Returns:
    tuple: (dates, prices, interpolated_dates, interpolated_prices)
    """
    # Extract dates and prices
    dates = df['date'].values
    prices = df['price'].values
    
    # Check for missing values
    if np.isnan(prices).any():
        # Interpolate missing values
        valid_indices = ~np.isnan(prices)
        valid_dates = dates[valid_indices]
        valid_prices = prices[valid_indices]
        
        # Create a time series with uniform intervals
        start_date = valid_dates.min()
        end_date = valid_dates.max()
        
        # Create a date range with daily frequency
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Interpolate prices for the uniform date range
        interpolated_prices = np.interp(
            np.array([(d - start_date).total_seconds() for d in date_range]),
            np.array([(d - start_date).total_seconds() for d in valid_dates]),
            valid_prices
        )
        
        return dates, prices, date_range, interpolated_prices
    
    return dates, prices, dates, prices

def compute_fft(prices):
    """
    Compute the Fast Fourier Transform of the price data.
    
    Parameters:
    prices (numpy.ndarray): Array of stock prices
    
    Returns:
    tuple: (frequencies, power_spectrum)
    """
    # Remove linear trend to focus on cyclical patterns
    detrended_prices = signal.detrend(prices)
    
    # Apply window function to reduce spectral leakage
    windowed_prices = detrended_prices * signal.windows.hann(len(detrended_prices))
    
    # Compute FFT
    fft_result = np.fft.rfft(windowed_prices)
    
    # Calculate power spectrum (magnitude squared)
    power_spectrum = np.abs(fft_result) ** 2
    
    # Calculate frequencies
    n = len(prices)
    sample_freq = 1.0  # Assuming 1 data point per day
    frequencies = np.fft.rfftfreq(n, d=1/sample_freq)
    
    return frequencies, power_spectrum

def find_dominant_cycles(frequencies, power_spectrum, max_cycles=5):
    """
    Find the dominant cycles in the power spectrum.
    
    Parameters:
    frequencies (numpy.ndarray): Array of frequencies
    power_spectrum (numpy.ndarray): Array of power spectrum values
    max_cycles (int, optional): Maximum number of dominant cycles to return
    
    Returns:
    list: List of dominant cycles as (period, power) tuples
    """
    # Skip the DC component (zero frequency)
    if len(frequencies) > 1:
        frequencies = frequencies[1:]
        power_spectrum = power_spectrum[1:]
    
    # Find peaks in the power spectrum
    peaks, _ = signal.find_peaks(power_spectrum)
    
    # If no peaks found, return empty list
    if len(peaks) == 0:
        return []
    
    # Get the indices of peaks sorted by power
    sorted_peak_indices = sorted(peaks, key=lambda i: power_spectrum[i], reverse=True)
    
    # Calculate periods (1/frequency) and normalize power
    max_power = np.max(power_spectrum)
    dominant_cycles = []
    
    for i in sorted_peak_indices[:max_cycles]:
        if frequencies[i] > 0:  # Avoid division by zero
            period = 1.0 / frequencies[i]
            normalized_power = power_spectrum[i] / max_power
            dominant_cycles.append((period, normalized_power))
    
    return dominant_cycles

def analyze_stock_data(file_path):
    """
    Analyze stock data using FFT.
    
    Parameters:
    file_path (str): Path to the CSV file containing stock data
    
    Returns:
    dict: Analysis results including time series, FFT, and dominant cycles
    """
    # Load data
    df = load_stock_data(file_path)
    
    # Preprocess data
    dates, prices, uniform_dates, uniform_prices = preprocess_data(df)
    
    # Compute FFT
    frequencies, power_spectrum = compute_fft(uniform_prices)
    
    # Find dominant cycles
    dominant_cycles = find_dominant_cycles(frequencies, power_spectrum)
    
    # Convert NumPy arrays to lists for JSON serialization
    result = {
        'dates': [pd.Timestamp(d).strftime('%Y-%m-%d') for d in dates],
        'prices': prices.tolist(),
        'uniform_dates': [pd.Timestamp(d).strftime('%Y-%m-%d') for d in uniform_dates],
        'uniform_prices': uniform_prices.tolist(),
        'frequencies': frequencies.tolist(),
        'power_spectrum': power_spectrum.tolist(),
        'dominant_cycles': dominant_cycles
    }
    
    return result