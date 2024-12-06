
## **prpip**
**Reconstruct pupil size during blinks in eye-tracking data** with a physiologically inspired approach.

---

### **Features**
- Detects blink intervals in eye-tracking data.
- Reconstructs pupil size during blinks using:
  - **Logarithmic recovery** for long blinks (>50 ms).
  - **Polynomial blending** for short blinks (<50 ms).
  - Adds **stochastic variability** to mimic natural pupil fluctuations.
- Supports processing individual trials or entire datasets.
- Flexible output:
  - Save reconstructed data to a new file.
  - Replace blinks in the original dataset.

---

### **Installation**
Install the latest version of `prpip` from PyPI:

```bash
pip install prpip
```

---

### **Quick Start**

#### **1. Import the Package**
```python
import prpip as pr
```

#### **2. Process Eye-Tracker Data**
```python
# Process and save reconstructed data to a new file
pr.process_eye_tracker_data(
    input_file="input.csv",
    output_file="reconstructed.csv",
    newfile=True  # Save as a new file
)
```

#### **3. Replace Blinks in Original Data**
```python
# Replace blinks in the original dataset
processed_data = pr.process_eye_tracker_data(
    input_file="input.csv",
    newfile=False  # Replace blinks in the original data
)
```

---

### **Input File Requirements**
The input file must be a CSV with the following columns:
- **`Trial`**: Identifies the trial number.
- **`Pupil Size`**: The measured pupil size.

### **Output**
The output can either:
- Add a new column `Reconstructed Pupil Size` (if `newfile=True`).
- Replace the `Pupil Size` column with reconstructed values (if `newfile=False`).

---

### **Advanced Parameters**
You can customize the behavior of the reconstruction:

- **`blink_threshold`**:
  Threshold for detecting blinks. Default is `0` (blinks occur when `Pupil Size` is 0).

- **`tau`**:
  Recovery time constant for logarithmic reconstruction. Default is `50`.

- **`noise_scale`**:
  Scale of Gaussian noise added to long-blink reconstructions. Default is `0.05`.

#### Example:
```python
pr.process_eye_tracker_data(
    input_file="input.csv",
    output_file="reconstructed.csv",
    blink_threshold=0,
    tau=60,
    noise_scale=0.1,
    newfile=True
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
| Trial | Trial Time | Pupil Size |
|-------|------------|------------|
| 1     | 0          | 4500       |
| 1     | 10         | 0          |
| 1     | 20         | 0          |
| 1     | 30         | 4800       |

#### **Output:**
| Trial | Trial Time | Pupil Size | Reconstructed Pupil Size |
|-------|------------|------------|--------------------------|
| 1     | 0          | 4500       | 4500                    |
| 1     | 10         | 0          | 4600                    |
| 1     | 20         | 0          | 4700                    |
| 1     | 30         | 4800       | 4800                    |
