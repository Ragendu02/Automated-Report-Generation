
import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# Load Data
df = pd.read_csv("customers-100.csv")
df['Subscription Date'] = pd.to_datetime(df['Subscription Date'], errors='coerce')
df['Email Domain'] = df['Email'].apply(lambda x: x.split('@')[-1])

# Dashboard Title
st.title("📊 Customer Dashboard with PDF Report")

# Metrics
st.subheader("📈 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Unique Countries", df['Country'].nunique())
col3.metric("Unique Companies", df['Company'].nunique())

# Top countries
st.subheader("🌍 Top Countries")
top_countries = df['Country'].value_counts().head(5)
st.bar_chart(top_countries)

# Top cities
st.subheader("🏙️ Top Cities")
top_cities = df['City'].value_counts().head(5)
st.bar_chart(top_cities)

# Top email domains
st.subheader("📧 Top Email Domains")
top_domains = df['Email Domain'].value_counts().head(5)
st.bar_chart(top_domains)

# Date range
st.subheader("📅 Subscription Date Range")
st.write(f"From **{df['Subscription Date'].min().date()}** to **{df['Subscription Date'].max().date()}**")

# Filter
st.subheader("🔍 Filter by Country")
country_filter = st.selectbox("Choose a Country", sorted(df['Country'].unique()))
filtered_df = df[df['Country'] == country_filter]
st.dataframe(filtered_df)

# PDF Generator Function
def create_pdf(dataframe, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Customer Data Report", ln=True, align='C')

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for line in summary:
        pdf.cell(200, 10, line, ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Top 5 Countries", ln=True)
    for i, (country, count) in enumerate(top_countries.items(), 1):
        pdf.cell(200, 10, f"{i}. {country}: {count} customers", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, "Top 5 Cities", ln=True)
    for i, (city, count) in enumerate(top_cities.items(), 1):
        pdf.cell(200, 10, f"{i}. {city}: {count} customers", ln=True)

    # ✅ Fix: Export PDF to string and convert to BytesIO
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer

# Generate Summary
summary_lines = [
    f"Total Customers: {len(df)}",
    f"Unique Countries: {df['Country'].nunique()}",
    f"Unique Companies: {df['Company'].nunique()}",
    f"Subscription Date Range: {df['Subscription Date'].min().date()} to {df['Subscription Date'].max().date()}",
]

# Download Button
st.subheader("📥 Download PDF Report")
if st.button("Generate PDF Report"):
    pdf_buffer = create_pdf(df, summary_lines)
    st.download_button(
        label="📄 Download PDF",
        data=pdf_buffer,
        file_name="customer_report.pdf",
        mime="application/pdf"
    )
