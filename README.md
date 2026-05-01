
---

## 📊 Model Performance

### Clinical Model (Random Forest)

| Metric | Value |
|--------|-------|
| Accuracy | 81.4% |
| Cross-validation (5-fold) | 82.4% (±1.7%) |
| Precision (Simple) | 81.4% |
| Recall (Simple) | 79% |
| Precision (Complex) | 83% |
| Recall (Complex) | 89% |

### X-ray Model (EfficientNetB0 + PCA + RF)

| Metric | Value |
|--------|-------|
| Accuracy | 67.7% |
| Precision | 71.3% |
| Recall | 54.3% |
| Confusion Matrix | Simple: 98 correct, 23 false alarm; Complex: 57 correct, 48 missed |

### Multimodal Ensemble (Late Fusion)

| Metric | Value |
|--------|-------|
| Accuracy | 82.4% |
| Clinical Weight | 91% |
| X-ray Weight | 9% |
| Test Set Size | 46 aligned patients |
| True Negatives | 22 |
| False Positives | 3 |
| False Negatives | 4 |
| True Positives | 17 |

### Feature Importance (Clinical Model)

| Feature | Importance |
|---------|------------|
| Pain Scale | **58.7%** |
| Heart Rate | 10.8% |
| Age | 10.2% |
| Systolic BP | 10.2% |
| Diastolic BP | 10.1% |

**Interpretation:** Pain scale dominates prediction, which aligns with clinical expectation that patient-reported pain is the strongest indicator of fracture severity.

---

## 🌍 18 African Countries Represented

| Country | Patients | Country | Patients |
|---------|----------|---------|----------|
| Tanzania | 96 | Kenya | 65 |
| South Africa | 76 | Uganda | 63 |
| Ghana | 75 | Mali | 61 |
| Zambia | 75 | Egypt | 59 |
| Burkina Faso | 72 | Ethiopia | 59 |
| Zimbabwe | 68 | Ivory Coast | 57 |
| Senegal | 66 | Nigeria | 52 |
| | | Botswana | 51 |
| | | Cameroon | 47 |
| | | Morocco | 46 |
| | | Rwanda | 41 |

**Total:** 1,129 patients

---

## 🖥️ Technology Stack

### Backend & ML
- **Python 3.11** – Core programming language
- **Scikit-learn 1.3+** – Random Forest, PCA, Logistic Regression, StandardScaler
- **TensorFlow 2.13+ / Keras** – EfficientNetB0, image preprocessing
- **Pandas / NumPy** – Data manipulation and numerical computing
- **Joblib** – Model serialization and persistence

### Frontend & Web Application
- **Streamlit 1.28+** – Interactive web framework
- **Pillow (PIL)** – Image processing
- **Matplotlib / Seaborn** – Visualization (notebook only)

### Dataset & APIs
- **Hugging Face Datasets** – African Medical Multimodal Fracture dataset
- **Unsplash API** – Background images for UI

### Development Tools
- **Jupyter Notebook** – Model development and experimentation
- **VS Code** – Web application development
- **GitHub** – Version control and collaboration

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git (optional, for cloning)

### Clone the Repository
```bash
git clone https://github.com/mrselemogo777-gif/african-fracture-ai.git
cd african-fracture-ai
