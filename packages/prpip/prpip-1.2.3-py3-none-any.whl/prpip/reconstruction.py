import numpy as np

def reconstruct_pupil(trial_data, blink_intervals, tau=50, noise_scale=0.05):
    """
    Reconstructs pupil size during blinks using a physiologically inspired approach.

    Parameters:
    - trial_data: DataFrame containing trial data with 'Pupil Size' column.
    - blink_intervals: List of (start, end) tuples representing blink intervals.
    - tau: Recovery time constant for logarithmic recovery.
    - noise_scale: Scale of Gaussian noise to mimic natural pupil fluctuations.

    Returns:
    - Reconstructed pupil size series.
    """
    interpolated_pupil = trial_data['Pupil Size'].copy()

    for start, end in blink_intervals:
        # Convert floating-point indices to positional indices
        start_idx = trial_data.index.get_loc(start)
        end_idx = trial_data.index.get_loc(end)
        
        if start_idx >= end_idx or end_idx > len(trial_data):
            continue  # Skip invalid intervals

        blink_length = end_idx - start_idx

        # Pre-blink and post-blink values
        pre_value = interpolated_pupil.iloc[start_idx - 1] if start_idx > 0 else interpolated_pupil.mean()
        post_value = interpolated_pupil.iloc[end_idx] if end_idx < len(interpolated_pupil) else interpolated_pupil.mean()

        # Generate recovery curve
        if blink_length > 50:
            t = np.arange(0, blink_length)
            recovery_curve = pre_value + (post_value - pre_value) * (1 - np.exp(-t / tau))
            recovery_curve += np.random.normal(0, noise_scale * abs(post_value - pre_value), blink_length)
        else:
            t = np.linspace(0, 1, blink_length)
            recovery_curve = pre_value * (1 - t) + post_value * t

        # Assign the recovery curve to the blink interval
        interpolated_pupil.iloc[start_idx:end_idx] = recovery_curve

    # Fill NaNs for boundary conditions
    interpolated_pupil = interpolated_pupil.interpolate(method='linear').ffill().bfill()

    return interpolated_pupil