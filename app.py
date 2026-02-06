import streamlit as st
import os
import re
import mammoth
from jinja2 import Template
from weasyprint import HTML

# ===============================
# CONFIG
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(BASE_DIR, "work")
PDF_DIR = os.path.join(WORK_DIR, "pdf_output")
TEMPLATE_HTML = os.path.join(WORK_DIR, "template.html")

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(WORK_DIR, exist_ok=True)

# ===============================
# CSS STYLING
# ===============================
st.markdown("""
<style>
body {
    background: linear-gradient(120deg,#f6f9ff,#e3ecff);
}
.card {
    background:white;
    padding:25px;
    border-radius:12px;
    box-shadow:0 8px 25px rgba(0,0,0,0.1);
}
h1, h2 {
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# HELPERS
# ===============================
def extract_placeholders(html):
    return sorted(set(re.findall(r"{{(.*?)}}", html)))

def save_template(docx_file):
    result = mammoth.convert_to_html(docx_file)
    html = result.value
    with open(TEMPLATE_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return extract_placeholders(html)

# ===============================
# APP UI
# ===============================
st.title("📄 Smart PDF Generator")

tabs = st.tabs(["👤 User", "🔐 Admin"])

# ===============================
# USER TAB
# ===============================
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Fill Details")

    if not os.path.exists(TEMPLATE_HTML):
        st.warning("Template not uploaded yet.")
    else:
        with open(TEMPLATE_HTML, "r", encoding="utf-8") as f:
            html_template = f.read()

        fields = extract_placeholders(html_template)
        template = Template(html_template)

        user_data = {}
        for field in fields:
            user_data[field] = st.text_input(field)

        pdf_name = st.text_input("PDF Name")

        if st.button("🚀 Generate PDF"):
            if not pdf_name:
                st.error("Please enter PDF Name")
            else:
                rendered = template.render(**user_data)
                pdf_path = os.path.join(PDF_DIR, f"{pdf_name}.pdf")
                HTML(string=rendered).write_pdf(pdf_path)

                st.success("PDF Generated Successfully!")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇ Download PDF",
                        f,
                        file_name=f"{pdf_name}.pdf",
                        mime="application/pdf"
                    )
    st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# ADMIN TAB (LOCKED)
# ===============================
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Admin Panel")

    password = st.text_input("Admin Password", type="password")

    if password == st.secrets["ADMIN_PASSWORD"]:
        docx_file = st.file_uploader("Upload DOCX Template", type=["docx"])

        if docx_file:
            fields = save_template(docx_file)
            st.success("Template uploaded successfully!")
            st.info("Detected Fields:")
            st.write(fields)
    elif password:
        st.error("Invalid Password")

    st.markdown('</div>', unsafe_allow_html=True)
