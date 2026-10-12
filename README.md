# 🏃 Sports Injury Risk Detection (SIRD) from Video

An end-to-end, multi-role AI platform that analyzes athletic motion videos to identify biomechanical anomalies, calculate multi-joint kinematic deviations, and predict injury probabilities using **MediaPipe Pose Tracking** and **trained Random Forest Machine Learning models**.

---

## 🌟 Key Features

- **Computer Vision Kinematic Pose Tracking**:
  - 33-landmark 3D spatial joint tracking powered by Google MediaPipe Tasks.
  - Frame-by-frame 3D vector calculations for knee valgus, pelvic tilt, trunk lean, ground impact flexion, and bilateral asymmetry.
  - High-visibility skeletal rendering with browser-native H.264 (`yuv420p`) encoding.
  - Live webcam video recording and instant ML analysis directly from the browser.

- **Machine Learning Risk Prediction**:
  - 6 trained Random Forest Regressor/Classifier models predicting risks for:
    - **ACL Injury Risk**
    - **Hamstring Injury Risk**
    - **Ankle Sprain Risk**
    - **Shoulder Injury Risk**
    - **Lower Back Injury Risk**
    - **Overuse Injury Risk**
  - **Explainable AI (XAI)** rationale articulating why specific kinematic metrics triggered risk flags.
  - **Anomaly Detection Engine** flagging severe outliers in movement patterns.

- **AI Exercise Recommendation Agent**:
  - Dynamically prescribes targeted clinical protocols (e.g., *VMO & Gluteus Medius Activation*, *Soft-Landing Plyometrics*) mapped to the athlete's detected movement flaws.
  - Supports custom prescription authoring by Coaches and Physiotherapists.

- **Role-Based Workspaces**:
  - **Athlete**: Movement analysis, body heatmaps, radar joint charts, video upload history, and physical profile settings.
  - **Coach**: Team roster risk overview, athlete performance tracking, and training drill prescription.
  - **Physiotherapist**: Clinical rehabilitation tracking, recovery monitoring, and movement flaw correction.
  - **Sports Scientist**: Anonymized research dataset analytics, kinematic scatter matrix charts, and cohort data export.
  - **Administrator**: User account management, role assignment, and system health metrics.

- **Reporting & Export**:
  - Automated PDF assessment report generation via ReportLab.
  - Research CSV telemetry exports for sports science cohorts.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Motor (Async MongoDB), PyMongo, MediaPipe, OpenCV, Scikit-learn, ImageIO, ReportLab.
- **Frontend**: React 19, Vite, Lucide React Icons, Canvas-based biomechanical rendering.
- **Database**: MongoDB Atlas.
- **Authentication**: JWT & Google OAuth2.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- MongoDB Atlas cluster URI

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env   # (or cp .env.example .env on Unix)

# Start backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
Open your browser at [http://localhost:5173](http://localhost:5173)

---

## 🧪 Testing

The platform includes an automated 21-point end-to-end verification suite testing all authentication flows, video uploads, MediaPipe pose pipelines, report generation, and multi-role endpoints:

```bash
cd backend
python test_suite_runner.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
