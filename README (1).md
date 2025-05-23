# 🏘️ REInA - Real Estate Investment Analyzer

REInA is a Python-based CLI tool for identifying and visualizing top-performing ZIP codes in the U.S. real estate market. It combines proximity-based search, regional insights, and scoring algorithms to help real estate investors make smarter location-based decisions.

---

## 📁 Project Structure

```
REInA/
├── main.py                  # CLI tool to find top investment ZIPs
├── tsv_scraper.py           # Converts Redfin TSV to SQLite database
├── uszips generator.py      # Generates ZIP info using pgeocode (optional fallback)
├── dbprinttest.py           # Utility/debug functions for DB and ZIP CSV
├── us_zips.csv              # ZIP info CSV (lat/lng/state/city)
├── redfin_data.tsv          # Input real estate TSV (external)
├── reina_redfinzipdata.db   # SQLite DB storing cleaned real estate metrics
├── requirements.txt         # Python dependencies
└── README.md                # Documentation (you're reading it!)
```

---

## 💡 Features

- 🔍 **Search by ZIP**: Find top ZIPs for investment around a given ZIP radius.
- 🗺️ **Search by City/State**: Get highest scoring ZIP codes in a selected city or state.
- 📊 **Investment Scoring**: Considers Days on Market (DOM), inventory, homes sold, and median prices.
- 📈 **Visual Output**: Bar chart visualization of top ZIP codes with color coding.
- 🧰 **Utility Scripts**:
  - Convert TSV data to DB (`tsv_scraper.py`)
  - Generate ZIP data with fallback (`uszips generator.py`)
  - Print/debug DB contents (`dbprinttest.py`)

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Dhasvanth-mg/REInA.git
cd REInA
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install pandas numpy geopy matplotlib pgeocode
```

### 3. Prepare Datasets

- `us_zips.csv`: Already included, or generate using:
  ```bash
  python "uszips generator.py"
  ```

- `reina_redfinzipdata.db`: Convert a Redfin TSV file using:
  ```bash
  python "tsv_scraper.py"
  ```
  Make sure `redfin_data.tsv` is in the same directory.

---

## 🚀 Running REInA

```bash
python main.py
```

### CLI Options:

- `zip` → Search by ZIP code and radius
- `city` → Show top ZIPs within a given city
- `state` → Show top ZIPs within a U.S. state
- `quit` → Exit CLI

---

## 🧪 Example

```
Reina Real Estate CLI
Type:
  zip    → to search nearby ZIPs
  city   → to search top ZIPs in a city
  state  → to search top ZIPs in a state
  quit   → to exit

Enter command (zip/city/state/quit): zip
Enter ZIP code: 94103
Enter radius in miles (default 20): 15
```

---

## 📊 Output Sample

```
Top Investment Regions:
  zipcode  median_price  investment_score  homes_sold  inventory  dom
0   94110        950000              84.1         120         60   45
1   94114        870000              77.3         105         55   52
...
```

---

## 🧩 Utilities

- `dbprinttest.py`: Debug SQLite content and structure
- `uszips generator.py`: Regenerate `us_zips.csv` using `pgeocode` if original file is unavailable

---

## 📌 Notes

- Data must be preloaded and clean (ZIPs should be 5-digit).
- Currently supports only U.S. ZIP codes.
- Default dataset sources assumed to be Redfin and Kaggle.

---

## 🧠 Author

Created by **Dhasvanth Muthukumar Gokila**  
GitHub: [Dhasvanth-mg](https://github.com/Dhasvanth-mg)

---

## 📃 License

This project is under the MIT License. See `LICENSE` file for details.