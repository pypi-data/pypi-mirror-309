import pandas as pd
from .blink_detection import detect_blinks
from .reconstruction import reconstruct_pupil

def process_eye_tracker_data(input_file, output_file=None, blink_threshold=0, tau=50, noise_scale=0.05, newfile=True):
    """
    Processes an eye tracker data file by detecting blinks, applying the novel reconstruction method,
    and optionally saving the reconstructed data as a new file or replacing the blinks in the original data.

    Parameters:
    - input_file: Path to the input CSV file containing eye tracker data.
    - output_file: Path to save the output CSV file with reconstructed pupil size (if newfile=True).
    - blink_threshold: Threshold for detecting blinks (default is 0, where pupil size is 0 during a blink).
    - tau: Recovery time constant for logarithmic recovery.
    - noise_scale: Scale of Gaussian noise to mimic natural pupil fluctuations.
    - newfile: If True, saves the reconstructed data to a new file. If False, replaces blinks in the original data.

    Returns:
    - DataFrame: The processed DataFrame (with reconstructed data).
    """
    data = pd.read_csv(input_file)

    if 'Pupil Size' not in data.columns or 'Trial' not in data.columns:
        raise ValueError("The input file must contain 'Pupil Size' and 'Trial' columns.")

    processed_data = pd.DataFrame()
    for trial in data['Trial'].unique():
        trial_data = data[data['Trial'] == trial].reset_index(drop=True)
        blink_intervals = detect_blinks(trial_data, blink_threshold)
        reconstructed_pupil = reconstruct_pupil(trial_data, blink_intervals, tau, noise_scale)

        if newfile:
            trial_data['Reconstructed Pupil Size'] = reconstructed_pupil
        else:
            trial_data['Pupil Size'] = reconstructed_pupil

        processed_data = pd.concat([processed_data, trial_data], ignore_index=True)

    if newfile and output_file:
        processed_data.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
    else:
        print("Reconstructed data applied to original column.")

    return processed_data
