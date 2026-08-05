# Academic Performance & Grading Analyzer

An elegant, production-ready, modular Python system designed to ingest student gradebook data, calculate complex weighted academic metrics, and generate a self-contained, interactive minimalist dark-themed HTML report.

## 🌟 Features   

- **Modular Architecture:** Complete decoupling of data parsing, business logic/analytics, and frontend UI presentation.
- **Robust Data Sanitization:** Defensive parsing engine that handles missing entries, trims whitespace, and validates schema integrity automatically.
- **Dynamic Schema Configuration:** Grading scales, passing thresholds, and assessment weights are completely driven by an external JSON configuration file.
- **Minimalist Aesthetic Dark Mode:** A premium charcoal and slate visual layout focused on structural grid alignment and typographic hierarchy.
- **Interactive UI:** Native, client-side searching and table sorting implemented using pure vanilla JavaScript.

---

## 📂 Project Architecture

```text 
academic_analyzer/
│
├── config/
│   └── grading_schema.json    # Rules engine (weights, max marks, grade scales)
│
├── data/
│   └── sample_grades.csv      # Raw student gradebook dataset
│
├── src/
│   ├── __init__.py            # Exposes core directory as a Python package
│   ├── parser.py              # CSV cleaning, parsing, and validation layer
│   ├── analytics.py           # Pandas engine computing statistics & totals
│   └── generator.py           # Jinja2 template compiler & CSS injector
│
├── templates/
│   ├── dashboard.html         # HTML layout template
│   └── styles.css             # Premium dark-theme stylesheet
│
├── outputs/
│   └── gradebook_report.html  # Generated standalone interactive web report
│
├── .gitignore                 # Prevents pushing caches or private data
├── main.py                    # System orchestrator and entry point
└── README.md                  # System documentation
