
## **prpip**
**Reconstruct pupil size during blinks in eye-tracking data** with a physiologically inspired approach.

### **Features**
- Automatically detects blink intervals in eye-tracking data.
- Reconstructs pupil size during blinks using:
  - **Logarithmic recovery** for long blinks (>50 ms).
  - **Linear blending** for short blinks (<50 ms).
  - Adds **stochastic variability** to mimic natural pupil fluctuations.
- Processes individual trials or entire datasets.
- Flexible output:
  - Add a new column for reconstructed data.
  - Replace the original pupil size column with reconstructed values.

---

## **Changelog**

<details>
  <summary>See the Changes in versions</summary>

### **Version 0.0.post1**
- Initial release of `prpip`.
- Implemented logarithmic recovery for long blinks and linear blending for short blinks.
- Added stochastic variability to mimic natural pupil fluctuations.
- Supported batch processing of datasets and individual trials.

### **Version 1.1.0dev1 - Pre-Release**
- Enhanced noise scaling for long-blink reconstructions.
- Added advanced parameter customization (`tau`, `noise_scale`).
- Improved boundary smoothing for blink transitions.

### **Version 1.2.1**
- Introduced additional output format options.
- Optimized performance for large datasets.

## **Version 1.2.3**
- Added a check in detect_blinks to print a message when no blinks are detected in the trial data.
- Improved handling of floating-point time indices during pupil reconstruction, ensuring compatibility with non-integer time formats.
- Fixed minor bugs related to batch processing of trials.
- Improved error messages for invalid inputs, making debugging easier for users.

</details>


### **Installation**
Install the latest version of `prpip` from PyPI:

```bash
pip install prpip
```

---

### **Quick Start**

#### **1. Import the Package**
```python
from prpip import process_pupil
```

#### **2. Process an Entire Dataset**
```python
import pandas as pd

# Load the dataset
data = pd.read_csv("input.csv")

# Process all trials in the dataset
processed_data = process_pupil(data)

# Save the processed data
processed_data.to_csv("reconstructed.csv", index=False)
```

#### **3. Process a Specific Trial**
```python
# Process only Trial 88
processed_trial = process_pupil(data, trial=88)

# Save the reconstructed trial
processed_trial.to_csv("trial_88_reconstructed.csv", index=False)
```

#### **4. Plot the Results**
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
plt.plot(processed_trial['Timestamp'], processed_trial['Pupil Size'], label='Original Pupil Size', alpha=0.7)
plt.plot(processed_trial['Timestamp'], processed_trial['Reconstructed Pupil Size'], label='Reconstructed Pupil Size', linestyle='--')
plt.xlabel('Timestamp', fontsize=14)
plt.ylabel('Pupil Size', fontsize=14)
plt.title('Original vs Reconstructed Pupil Size (Trial 88)', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
```

---

### **Input Requirements**
The input data must be a Pandas DataFrame or CSV file with the following columns:
- **`Trial`**: Identifies the trial number.
- **`Pupil Size`**: The measured pupil size.

### **Output**
The output DataFrame includes a new column:
- **`Reconstructed Pupil Size`**: Contains the reconstructed values during blinks.

Alternatively, you can replace the original `Pupil Size` column with the reconstructed values.

---

### **Advanced Parameters**
You can customize reconstruction behavior by adjusting the following optional parameters:

- **`trial`**:
  Specify a trial number to process. If `None`, all trials are processed.

- **`blink_threshold`**:
  Threshold for detecting blinks. Default is `0` (blinks occur when `Pupil Size` is 0).

- **`tau`**:
  Recovery time constant for logarithmic reconstruction. Default is `50`.

- **`noise_scale`**:
  Scale of Gaussian noise added to long-blink reconstructions. Default is `0.05`.

#### Example:
```python
processed_data = process_pupil(
    data,
    trial=88,
    blink_threshold=0,
    tau=60,
    noise_scale=0.1
)
```

---

### **License**
This project is licensed under the **MIT License**.

---

### **Contributing**
We welcome contributions! To contribute:
1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request.

---

### **Author**
- **Mohammad Ahsan Khodami**
- Email: [ahsan.khodami@gmail.com](mailto:ahsan.khodami@gmail.com)
- GitHub: [AhsanKhodami](https://github.com/AhsanKhodami)

---

### **Example Input and Output**
#### **Input:**
| Trial | Timestamp | Pupil Size |
|-------|-----------|------------|
| 1     | 0         | 4500       |
| 1     | 10        | 0          |
| 1     | 20        | 0          |
| 1     | 30        | 4800       |

#### **Output:**
| Trial | Timestamp | Pupil Size | Reconstructed Pupil Size |
|-------|-----------|------------|--------------------------|
| 1     | 0         | 4500       | 4500                    |
| 1     | 10        | 0          | 4600                    |
| 1     | 20        | 0          | 4700                    |
| 1     | 30        | 4800       | 4800                    |
```