import streamlit as st
import os
import re
import tempfile
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(page_title="Dynamic PDF Generator", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "template.docx")

ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123")

# ======================================================
# UTILS
# ======================================================
def extract_placeholders_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join(p.text for p in doc.paragraphs)
    return sorted(set(re.findall(r"{{(.*?)}}", text)))


def replace_placeholders(text, data):
    for k, v in data.items():
        text = text.replace(f"{{{{{k}}}}}", str(v))
    return text


def generate_pdf(content, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 50
    for line in content.split("\n"):
        c.drawString(40, y, line)
        y -= 18
        if y < 40:
            c.showPage()
            y = height - 50

    c.save()


def docx_to_text(docx_path):
    doc = Document(docx_path)
    return "\n".join(p.text for p in doc.paragraphs)

# ======================================================
# UI
# ======================================================
st.title("📄 Dynamic PDF Generator")

tabs = st.tabs(["👤 User", "🔐 Admin"])

# ======================================================
# ADMIN TAB
# ======================================================
with tabs[1]:
    st.subheader("🔐 Admin Panel")

    password = st.text_input("Admin Password", type="password")

    if password == ADMIN_PASSWORD:
        uploaded_docx = st.file_uploader(
            "Upload DOCX Template (use {{FieldName}})",
            type=["docx"]
        )

        if uploaded_docx:
            with open(TEMPLATE_PATH, "wb") as f:
                f.write(uploaded_docx.read())

            fields = extract_placeholders_from_docx(TEMPLATE_PATH)

            st.success("Template uploaded successfully!")
            st.write("📌 Extracted Fields:")
            st.code(", ".join(fields))

            st.info("⚠️ Required: include {{PDFName}} for output filename")
    else:
        st.warning("Admin access only")

# ======================================================
# USER TAB
# ======================================================
with tabs[0]:
    st.subheader("👤 User Form")

    if not os.path.exists(TEMPLATE_PATH):
        st.warning("Admin has not uploaded any template yet.")
    else:
        fields = extract_placeholders_from_docx(TEMPLATE_PATH)
        user_data = {}

        with st.form("user_form"):
            for field in fields:
                user_data[field] = st.text_input(field)

            submitted = st.form_submit_button("🚀 Generate PDF")

        if submitted:
            if "PDFName" not in user_data or not user_data["PDFName"]:
                st.error("❌ PDFName field is required")
            else:
                with tempfile.TemporaryDirectory() as tmpdir:
                    text = docx_to_text(TEMPLATE_PATH)
                    final_text = replace_placeholders(text, user_data)

                    pdf_path = os.path.join(
                        tmpdir, f"{user_data['PDFName']}.pdf"
                    )

                    generate_pdf(final_text, pdf_path)

                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "⬇️ Download PDF",
                            f,
                            file_name=f"{user_data['PDFName']}.pdf",
                            mime="application/pdf"
                        )

                st.success("✅ PDF generated successfully")
