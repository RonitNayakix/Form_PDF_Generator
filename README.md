## 📄 Dynamic Form-Based PDF Generator (Streamlit App)
# 📌 Project Overview

This project is a dynamic PDF generation system built using Streamlit and Python.

It allows:
1. Admin users to upload and manage document templates (DOCX)
2. Automatic extraction of placeholders like {{Name}}, {{Amount}}
3. End users to fill a form generated from those placeholders
4. Generate professionally formatted PDFs without LibreOffice
5. Fully cloud-deployable on Streamlit Cloud

# 🎯 Key Features

# 👨‍💼 Admin Panel
1. Upload DOCX templates
2. Automatically extract placeholders ({{FieldName}})
3. Store templates permanently
4. Preview template content
5. Admin access is password-protected

# 👤 User Panel
1. Dynamic form auto-generated from template fields
2. User manually enters PDF File Name
3. One-click PDF generation
4. Clean, styled PDF output

# ☁️ Cloud Ready
1. No LibreOffice dependency
2. Uses Python-only PDF generation
3. Works on Streamlit Cloud, Docker, or local machine

# 🏗️ Project Architecture

form_pdf_generator/
│
├── app.py                  # Main Streamlit app
├── templates/              # Stored DOCX templates (admin uploads)
├── output/                 # Generated PDFs
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation (this file)

# 🧩 How It Works (Flow)

1. Admin uploads DOCX template
2. App scans the document for placeholders:
   {{Name}}, {{City}}, {{Amount}}
3. Fields are auto-generated into a form
4. User fills values + PDF name
5. App replaces placeholders
6. PDF is generated using reportlab

# 🛠️ Tech Stack

# Layer - Technology
1. UI	- Streamlit
2. DOCX Parsing - python-docx
3. PDF Generation - reportlab
4. Backend Logic - Python
5. Hosting - Streamlit Cloud
6. Version Control - GitHub

# 📦 Installation (Local Setup)

1️⃣ Clone the Repository
git clone https://github.com/your-username/form_pdf_generator.git
cd form_pdf_generator

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the App
streamlit run app.py

# 📄 DOCX Template Format

Use placeholders like:

```text
Dear {{Name}},

Your loan amount is {{Amount}}.
City: {{City}}

Regards,
Company Name
```
⚠️ Placeholder names must match exactly (case-sensitive).

# 🔐 Admin Access

1. Admin section is protected
2. Admin can:
   a. Upload templates
   b. View template preview
   c. Manage available formats
3. Password can be configured inside app.py

# 🧪 Sample Data Flow
# Field - Example
1. Name - Ramesh
2. City - Bhubaneswar
3. Amount - 500000
4. PDF Name - AFPL-01

# 📄 Output:

AFPL-01.pdf

# 🚀 Deployment on Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Select repository
4. Set app.py as entry file
5. Deploy 🎉
No system dependencies required.

# ⚠️ Limitations

1. DOCX formatting is partially preserved (text-focused)
2. Images inside DOCX are not rendered in preview
3. PDF layout is text-based (not WYSIWYG)

# 🔮 Future Enhancements

1. Template versioning
2. Multi-page PDFs
3. Role-based authentication
4. HTML template support
5. PDF preview before download

# 👨‍💻 Maintainer
Ronit
Data Engineer | Python | Streamlit | Automation

# ⭐ If You Like This Project

Please ⭐ star the repository and feel free to fork or contribute.
