import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json

def create_time_series_plot(dates, prices, title="Stock Price Time Series"):
    """
    Create an interactive time series plot of stock prices.
    
    Parameters:
    dates (list): List of date strings
    prices (list): List of stock prices
    title (str, optional): Plot title
    
    Returns:
    str: JSON representation of the Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=prices,
            mode='lines',
            name='Stock Price',
            line=dict(color='blue', width=2)
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return json.dumps(fig.to_dict())

def create_power_spectrum_plot(frequencies, power_spectrum, title="Power Spectrum"):
    """
    Create an interactive plot of the power spectrum.
    
    Parameters:
    frequencies (list): List of frequencies
    power_spectrum (list): List of power spectrum values
    title (str, optional): Plot title
    
    Returns:
    str: JSON representation of the Plotly figure
    """
    # Skip the DC component (zero frequency)
    if len(frequencies) > 1:
        frequencies = frequencies[1:]
        power_spectrum = power_spectrum[1:]
    
    # Convert frequencies to periods (in days)
    periods = [1/f if f > 0 else float('inf') for f in frequencies]
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=periods,
            y=power_spectrum,
            mode='lines',
            name='Power Spectrum',
            line=dict(color='red', width=2)
        )
    )
    
    # Add markers for peaks
    peaks = find_peaks_indices(power_spectrum)
    peak_periods = [periods[i] for i in peaks]
    peak_powers = [power_spectrum[i] for i in peaks]
    
    fig.add_trace(
        go.Scatter(
            x=peak_periods,
            y=peak_powers,
            mode='markers',
            name='Dominant Cycles',
            marker=dict(
                color='orange',
                size=10,
                line=dict(width=2, color='darkred')
            )
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title='Period (Days)',
        yaxis_title='Power',
        xaxis_type='log',  # Logarithmic scale for better visualization
        template='plotly_white',
        hovermode='closest'
    )
    
    # Add annotations for top peaks
    top_peaks = sorted(peaks, key=lambda i: power_spectrum[i], reverse=True)[:5]
    for i, peak_idx in enumerate(top_peaks):
        if peak_idx < len(periods):
            period = periods[peak_idx]
            power = power_spectrum[peak_idx]
            
            fig.add_annotation(
                x=period,
                y=power,
                text=f"{period:.1f} days",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )
    
    return json.dumps(fig.to_dict())

def find_peaks_indices(arr, min_distance=5):
    """
    Find indices of peaks in an array.
    
    Parameters:
    arr (list): Input array
    min_distance (int, optional): Minimum distance between peaks
    
    Returns:
    list: Indices of peaks
    """
    # Simple peak finding algorithm
    peaks = []
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i-1] and arr[i] > arr[i+1]:
            peaks.append(i)
    
    # Filter peaks by minimum distance
    if len(peaks) > 1:
        filtered_peaks = [peaks[0]]
        for peak in peaks[1:]:
            if peak - filtered_peaks[-1] >= min_distance:
                filtered_peaks.append(peak)
        return filtered_peaks
    
    return peaks

def create_combined_plot(dates, prices, frequencies, power_spectrum):
    """
    Create a combined plot with time series and power spectrum.
    
    Parameters:
    dates (list): List of date strings
    prices (list): List of stock prices
    frequencies (list): List of frequencies
    power_spectrum (list): List of power spectrum values
    
    Returns:
    str: JSON representation of the Plotly figure
    """
    # Create a subplot with 2 rows
    fig = make_subplots(
        rows=2, 
        cols=1,
        subplot_titles=("Stock Price Time Series", "Power Spectrum"),
        vertical_spacing=0.15
    )
    
    # Add time series plot
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=prices,
            mode='lines',
            name='Stock Price',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )
    
    # Skip the DC component (zero frequency)
    if len(frequencies) > 1:
        frequencies = frequencies[1:]
        power_spectrum = power_spectrum[1:]
    
    # Convert frequencies to periods (in days)
    periods = [1/f if f > 0 else float('inf') for f in frequencies]
    
    # Add power spectrum plot
    fig.add_trace(
        go.Scatter(
            x=periods,
            y=power_spectrum,
            mode='lines',
            name='Power Spectrum',
            line=dict(color='red', width=2)
        ),
        row=2, col=1
    )
    
    # Add markers for peaks
    peaks = find_peaks_indices(power_spectrum)
    peak_periods = [periods[i] for i in peaks]
    peak_powers = [power_spectrum[i] for i in peaks]
    
    fig.add_trace(
        go.Scatter(
            x=peak_periods,
            y=peak_powers,
            mode='markers',
            name='Dominant Cycles',
            marker=dict(
                color='orange',
                size=10,
                line=dict(width=2, color='darkred')
            )
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=800,
        template='plotly_white',
        hovermode='closest'
    )
    
    # Update x-axis properties
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Period (Days)", type="log", row=2, col=1)
    
    # Update y-axis properties
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Power", row=2, col=1)
    
    return json.dumps(fig.to_dict())