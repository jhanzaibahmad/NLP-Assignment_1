# Pakistan Code Scraper

This project scrapes laws from the official [Pakistan Code](https://pakistancode.gov.pk/english/LGu0xVD.php) website.
It extracts categories, laws, and their details, downloads the associated PDF files, and saves everything in a structured JSON file.

---

## 📂 Project Structure

```
PakistanCodeScraper/
│── PakistanLaw_pdfs/           # Folder where PDFs will be saved
│── PakistanCode_21I-0792.json  # Final JSON output
│── scraper.py                   # Main scraper script
│── requirements.txt             # Dependencies
│── .gitignore                   # Ignored files/folders
│── README.md                    # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd PakistanCodeScraper
```

### 2. Create a Virtual Environment

```bash
# Create
python -m venv venv

# Activate
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Scraper

Run the script:

```bash
python scraper.py
```

The script will:

1. Scrape all law categories.
2. Collect law details.
3. Download PDFs into `PakistanLaw_pdfs/`.
4. Save final JSON as `PakistanCode_21I-0792.json`.

---

## 📦 Output

### Example JSON Entry

```json
{
  "Category": "Criminal Laws",
  "Total_Count": 69,
  "Laws_List": [
    {
      "Law_Name": "Abolition of the Punishment of Whipping Act, 1996",
      "Details": {
        "Category": "Criminal Laws",
        "Act_No": "VII of 1996",
        "Promulgation_Date": "December 01, 1996",
        "Pdf_File": "PakistanLaw_pdfs/Abolition of the Punishment of Whipping Act, 1996.pdf"
      }
    }
  ]
}
```

---

## 🛑 Notes

* Make sure you have **Google Chrome** and the correct version of **ChromeDriver** installed.
* Large PDF downloads may take time depending on your internet connection.
* Only PDF paths are stored in JSON, not their parsed content.

---

## ✨ Author

**Jahan Zaib Ahmed**
Roll No: 21I-0792
BSCS Final Year Project
