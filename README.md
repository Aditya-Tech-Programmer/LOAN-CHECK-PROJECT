# LOAN-CHECK-PROJECT

# LoanCheck — Personal Loan Eligibility & Affordability Dashboard

A Streamlit-based educational fintech prototype that helps explore personal-loan eligibility, estimated EMIs, FOIR, repayment schedules, and alternative loan scenarios through a polished dashboard.

> **Disclaimer:** LoanCheck is an educational project, not a real lending service. It does not approve or sanction loans, verify PAN, fetch a credit-bureau report, or connect to a bank/NBFC. All decisions are based on the configurable rules in this demo.

## ✨ Key Features

- **Eligibility Engine:** Evaluate an applicant using age, employment, income, CIBIL score, requested amount, tenure, and existing EMIs.
- **EMI Studio:** Calculate monthly EMI, total interest, total repayment, and view an amortisation schedule with an outstanding-balance chart.
- **Application History:** Review applications processed during the current Streamlit session and export records as CSV.
- **PDF Test Applicants:** Run the six sample profiles supplied with the project brief and export results as CSV or JSON.
- **Smart Insights:** View rule-based observations about credit bands, repayment burden, and eligibility findings.
- **Loan Scenario Lab:** Compare alternative loan amounts and repayment terms.
- **Affordability Planner:** Estimate an affordable loan amount under the configured FOIR limit.
- **Policy Guide:** Explore eligibility conditions, credit bands, and interest rates.
- **Requirements Checklist:** Review the major requirements from the supplied project brief.
- **Premium UI:** Dark emerald and graphite colours, gradient accents, styled metric cards, and progress feedback.

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- JSON

The current application uses rule-based calculations. No API key is required.

## 📋 Demo Eligibility Policy

| Parameter | Configured rule |
|---|---|
| Age | 21–60 years |
| Employment | Salaried or self-employed |
| Minimum monthly income | ₹25,000 |
| Minimum CIBIL score | 650 |
| Maximum FOIR | 50% |
| Loan amount | ₹50,000–₹25,00,000 |
| Allowed tenure | 12, 24, 36, 48, 60 months |

### Credit Score Bands

| CIBIL Score | Credit Band | Annual Interest Rate |
|---|---|---:|
| 750–900 | Excellent | 11.0% |
| 700–749 | Good | 13.5% |
| 650–699 | Fair | 16.0% |
| 300–649 | Poor | Not eligible under the demo policy |

FOIR is calculated as:

`FOIR (%) = (Existing EMIs + New EMI) / Monthly Income × 100`

These are illustrative project rules, not universal lending requirements.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd <YOUR-REPOSITORY-FOLDER>
```

Replace the placeholders with your GitHub repository URL and folder name.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
streamlit run app.py
```

Open the local URL printed in your terminal, usually `http://localhost:8501`.

## 🧪 Sample Test Applicants

The test page contains six sample profiles:

1. Rohan Mehta — salaried, CIBIL 780
2. Sneha Kulkarni — salaried, CIBIL 720, existing EMIs
3. Priya Nair — self-employed, CIBIL 680
4. Vikram Joshi — age 63, for rejection testing
5. Arjun Deshpande — CIBIL 640, for poor-credit testing
6. Kavya Rao — student with income below the configured minimum

These are synthetic examples for testing, not real customer records.

## 📁 Project Structure

```text
LoanCheck/
├── app.py
├── requirements.txt
├── README.md
└── screenshots/   # Optional: add app screenshots
```

If you are also submitting the console-based version required by the project brief, include `loancheck.py` in your repository.

## ⚠️ Limitations

- Application history is stored in Streamlit session state and is not a permanent database.
- The app does not verify PAN or connect to a real credit-bureau service.
- Eligibility decisions are based only on configured demo rules.
- Outputs are not financial advice or real loan-sanction decisions.
- Test the main workflows in your target environment before presenting the project.

## 🔮 Future Improvements

- Persistent database storage
- User authentication and role-based access
- Automated tests for eligibility boundaries and EMI calculations
- Downloadable PDF reports
- Authorized credit-data integrations
- Audit logs and configurable policy settings

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run and test the main workflows.
5. Submit a pull request describing your changes and the tests performed.

## 📄 License

No license is specified by default. Add a `LICENSE` file before inviting others to reuse or redistribute the project.

---

Built as a Python + Streamlit learning project for transparent, rule-based personal-loan eligibility exploration.
