# AI Loan Eligibility Checker

An interactive, responsive BFSI (Banking, Financial Services, and Insurance) web application dedicated 100% to **AI Loan Eligibility Checking**. Users can interactively simulate loan eligibility in real time, adjust financial parameters via synchronized sliders, explore "What-If" scenarios, and receive educational guidance powered by Google Gemini AI.

---

> [!IMPORTANT]
> **Educational Financial Assistance Notice:**
> This platform is an educational simulation and preliminary assessment tool. It is **NOT** an official bank, credit bureau, or lender underwriting approval system. Results are strictly designated as **"Preliminary Eligibility Estimates"** or **"Educational Assessments"** and do not guarantee loan approvals.

---

## 1. Core Interactive Features

- **Real-Time Interactive Controls:**
  - Loan Category pills: Personal Loan, Home Loan, Vehicle Loan, Education Loan, Business Loan.
  - Live synchronized sliders and numerical inputs for:
    - Requested Loan Amount (₹10,000 to ₹1 Crore)
    - Desired Tenure (6 months to 30 years)
    - Expected Annual Interest Rate (1% to 30% p.a.)
    - Monthly Net Income (₹10,000 to ₹10 Lakhs)
    - Existing Monthly EMI Burden (₹0 to ₹2 Lakhs)
    - Credit Score (300 to 900)
    - Credit Limit & Utilization
    - Monthly Living Expenses
  - One-click presets: *Demo Profile*, *Home Loan Buyer*, *Auto Loan*, *High Debt Profile*.
- **Real-Time Preliminary Eligibility Verdict:**
  - Status classifications: *Strong Preliminary Profile* (Green), *Moderate Preliminary Profile* (Amber), or *Needs Improvement* (Red).
  - SVG Radial Speedometer Gauge visualizing credit score and rating tier.
  - Live calculations for Projected EMI, Debt-to-Income (DTI), Credit Utilization, and Disposable Cashflow Buffer.
- **5-Factor Evaluation Breakdown:**
  - Evaluates Income Level, Debt-to-Income (DTI), Credit Score Health, Revolving Credit Utilization, and EMI Affordability Ratio with color-coded status badges and detailed educational notes.
- **Interactive "What-If" Scenario Simulator:**
  - Live sliders to test:
    - *"What if I extend tenure by +12 to +60 months?"*
    - *"What if I pay down existing debt by ₹X?"*
    - *"What if my credit score gains +X points?"*
  - Instant one-click scenario application updating the live assessment.
- **Google Gemini AI Financial Insights:**
  - On-demand AI analysis delivering structured executive assessments, key factors, 5 step-by-step educational action items, and tenure trade-off guidance.

---

## 2. Technology Stack

- **Frontend:** React 19, Vite 6, Custom FinTech Design System (CSS3), Lucide Icons, SVG Speedometer Gauge
- **Backend:** Python, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0, SQLite (`credit_assistant.db`)
- **AI Integration:** Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`) with built-in educational fallback
- **Testing:** Pytest (14 automated tests)

---

## 3. Quick Start

### Running Backend
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API runs on: `http://127.0.0.1:8000`  
Swagger Documentation: `http://127.0.0.1:8000/docs`

### Running Frontend
```bash
cd frontend
npm run dev
```
Web application runs on: `http://127.0.0.1:5173/`

### Running Automated Tests
```bash
cd backend
python -m pytest tests/test_api.py -v
```

---

## 4. Educational Disclaimer

*This tool is intended strictly for preliminary educational assessment. It does not constitute formal underwriting, financial advisory services, or an offer of credit.*
