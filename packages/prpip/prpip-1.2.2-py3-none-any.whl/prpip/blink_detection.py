def detect_blinks(trial_data, blink_threshold=0):
    """
    Identifies blink intervals in trial data based on a pupil size threshold.

    Parameters:
    - trial_data: DataFrame containing the trial data with a 'Pupil Size' column.
    - blink_threshold: Threshold for detecting blinks (default is 0).

    Returns:
    - List of tuples (start, end) representing blink intervals.
    """
    blink_intervals = []
    in_blink = False
    for idx, pupil_size in trial_data['Pupil Size'].items():
        if pupil_size <= blink_threshold and not in_blink:
            in_blink = True
            start_idx = idx
        elif pupil_size > blink_threshold and in_blink:
            in_blink = False
            end_idx = idx
            blink_intervals.append((start_idx, end_idx))
    if in_blink:
        blink_intervals.append((start_idx, len(trial_data)))
    return blink_intervals
