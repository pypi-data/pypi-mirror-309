import pandas as pd
from .blink_detection import detect_blinks
from .reconstruction import reconstruct_pupil

def process_pupil(data, trial=None, tau=50, noise_scale=0.05, blink_threshold=0):
    """
    Processes the eye tracker data for detecting blinks and reconstructing pupil size.

    Parameters:
    - data: DataFrame containing eye tracker data.
    - trial: Specific trial number to process. If None, processes all trials.
    - tau: Recovery time constant (default: 50).
    - noise_scale: Noise scale to mimic natural pupil fluctuations (default: 0.05).
    - blink_threshold: Threshold for detecting blinks (default: 0).

    Returns:
    - DataFrame with reconstructed pupil size.
    """
    if trial is not None:
        data = data[data['Trial'] == trial].reset_index(drop=True)

    # Detect blinks
    blink_intervals = detect_blinks(data, blink_threshold)

    # Reconstruct pupil size
    data['Reconstructed Pupil Size'] = reconstruct_pupil(data, blink_intervals, tau, noise_scale)

    return data
