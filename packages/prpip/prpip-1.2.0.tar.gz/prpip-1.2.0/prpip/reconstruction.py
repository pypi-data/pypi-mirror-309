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
        blink_length = end - start

        # Pre-blink and post-blink indices
        pre_start = max(0, start - 1)
        post_end = min(len(trial_data), end + 1)

        pre_blink_data = trial_data['Pupil Size'][pre_start:start]
        post_blink_data = trial_data['Pupil Size'][end:post_end]

        pre_value = pre_blink_data.iloc[-1] if len(pre_blink_data) > 0 else trial_data['Pupil Size'].mean()
        post_value = post_blink_data.iloc[0] if len(post_blink_data) > 0 else trial_data['Pupil Size'].mean()

        if blink_length > 50:
            t = np.arange(0, blink_length)
            recovery_curve = pre_value + (post_value - pre_value) * (1 - np.exp(-t / tau))
            noise = np.random.normal(0, noise_scale * abs(post_value - pre_value), blink_length)
            interpolated_pupil[start:end] = recovery_curve + noise
        else:
            t = np.linspace(0, 1, blink_length)
            recovery_curve = pre_value * (1 - t) + post_value * t
            interpolated_pupil[start:end] = recovery_curve

        if start > 0:
            transition_length = min(10, start)
            transition_in = np.linspace(interpolated_pupil[start - 1], interpolated_pupil[start], transition_length)
            interpolated_pupil[start - transition_length:start] = transition_in

        if end < len(trial_data) - 1:
            transition_length = min(10, len(trial_data) - end - 1)
            transition_out = np.linspace(interpolated_pupil[end - 1], interpolated_pupil[end], transition_length)
            interpolated_pupil[end:end + transition_length] = transition_out

    interpolated_pupil = interpolated_pupil.interpolate(method='linear').fillna(method='ffill').fillna(method='bfill')
    return interpolated_pupil
