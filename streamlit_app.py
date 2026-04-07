import streamlit as st
from urllib.parse import urlparse
import time
import os
import tempfile
from fpdf import FPDF
from app import run_agent

st.set_page_config(
    page_title="RevOps AI | Mini Sales Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        .stDeployButton {display: none;}
        footer {visibility: hidden;}
        header {background-color: transparent !important;}
        .header-container {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .icp-badge-yes {
            background-color: rgba(36, 172, 85, 0.15);
            border-radius: 8px;
            padding: 12px 20px;
            color: #24AC55;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(36, 172, 85, 0.3);
        }
        .icp-badge-maybe {
            background-color: rgba(245, 158, 11, 0.15);
            border-radius: 8px;
            padding: 12px 20px;
            color: #F59E0B;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .icp-badge-no {
            background-color: rgba(239, 68, 68, 0.15);
            border-radius: 8px;
            padding: 12px 20px;
            color: #EF4444;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .status-dot {
            height: 12px;
            width: 12px;
            border-radius: 50%;
            display: inline-block;
        }
        .dot-yes { background-color: #24AC55; box-shadow: 0 0 8px #24AC55; }
        .dot-maybe { background-color: #F59E0B; box-shadow: 0 0 8px #F59E0B; }
        .dot-no { background-color: #EF4444; box-shadow: 0 0 8px #EF4444; }
        .stProgress > div > div > div > div { background-color: #3b82f6; }
    </style>
""", unsafe_allow_html=True)

def generate_pdf(company_name, result):
    pdf = FPDF()
    pdf.add_page()
    
    try:
        pdf.image("assets/Logo_RevOps.png", x=85, y=10, w=40)
        pdf.set_y(35) 
    except Exception:
        pdf.set_y(20)
        
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "RevOps Central | AI Sales Analysis Report", ln=True, align="C")
    pdf.ln(8)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Target Company: {company_name}", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, f"Summary: {result.get('company_summary', 'N/A')}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Firmographics:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"- Industry: {result.get('industry', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"- Size: {result.get('estimated_size', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"- Location: {result.get('location', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"- Revenue: {result.get('revenue_range', 'N/A')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ICP Qualification:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"- Fit: {result.get('icp_fit', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"- Score: {result.get('icp_score', 'N/A')}/100", ln=True)
    pdf.multi_cell(0, 8, f"- Match Drivers: {result.get('reason', 'N/A')}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "AI-Generated Outreach Email:", ln=True)
    pdf.set_font("Arial", '', 11)
    
    email_text = result.get("outreach_email", "")
    pdf.multi_cell(0, 6, email_text)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            pdf_bytes = f.read()
    os.unlink(tmp.name)
    
    return pdf_bytes

col_logo, col_title = st.columns([1.5, 8.5])
with col_logo:
    try:
        st.image("assets/Logo_RevOps.png", width=250)
    except Exception:
        st.write("⚡") 

with col_title:
    st.markdown("<h1 style='margin-bottom: -10px; margin-top: 15px;'>RevOps Central | Mini AI Sales Assistant</h1>", unsafe_allow_html=True)
    st.caption("AI-powered lead enrichment, ICP scoring, and personalized outreach")

st.divider()

with st.sidebar:
    st.markdown("### Lead Input")
    website = st.text_input("Company Website", placeholder="https://www.remitap.com/")
    
    st.markdown("### Custom ICP Criteria")
    
    industry_options = [
        "SaaS", "Fintech", "HealthTech", "EdTech", "E-commerce", 
        "AI/ML", "Cybersecurity", "Logistics", "Real Estate", "Other"
    ]
    target_industries = st.multiselect(
        "Target Industries", 
        options=industry_options, 
        default=["SaaS", "Fintech"] 
    )
    custom_industry = st.text_input("Add Custom Industry", placeholder="e.g. Web3, AgTech")
    if custom_industry:
        target_industries.append(custom_industry)
    
    c1, c2 = st.columns(2)
    with c1:
        min_size = st.number_input("Min Staff", 1, 10000, 10)
    with c2:
        max_size = st.number_input("Max Staff", 1, 10000, 200)
    
    location_options = [
        "United States", "Canada", "United Kingdom", "Europe", 
        "India", "Australia", "Asia Pacific", "Global"
    ]
    target_locations = st.multiselect(
        "Target Locations", 
        options=location_options, 
        default=["United States"]
    )
    custom_location = st.text_input("Add Custom Location", placeholder="e.g. Germany, Tokyo")
    if custom_location:
        target_locations.append(custom_location)
    
    r1, r2 = st.columns(2)
    with r1:
        min_revenue = st.number_input("Min Rev ($M)", 1, 1000, 5)
    with r2:
        max_revenue = st.number_input("Max Rev ($M)", 1, 5000, 100)
    
    st.write("") 
    submitted = st.button("Analyze Lead", use_container_width=True, type="primary")

if submitted and website:
    domain = urlparse(website).netloc.replace("www.", "")
    if not domain:
        domain = website.replace("www.", "").split('/')[0]
    company_name = domain.split(".")[0].title()

    custom_icp = {
        "industry": target_industries,
        "min_size": min_size,
        "max_size": max_size,
        "location": target_locations,
        "min_revenue": min_revenue,
        "max_revenue": max_revenue
    }

    input_data = {
        "company_name": company_name,
        "website": website
    }

    with st.spinner(f"Agent is analyzing {company_name}..."):
        result = run_agent(input_data, custom_icp)
        time.sleep(0.5)

    st.success("Analysis Complete")

    col_insights, col_icp = st.columns([1.4, 1], gap="large")

    with col_insights:
        st.markdown("### Company Insights")
        st.info(result.get("company_summary", "No summary available."))
        
        st.markdown(f"**Industry:** {result.get('industry', 'Unknown')}")
        st.markdown(f"**Estimated Size:** {result.get('estimated_size', 'Unknown')}")
        st.markdown(f"**Location:** {result.get('location', 'Unknown')}")
        st.markdown(f"**Revenue Range:** {result.get('revenue_range', 'Unknown')}")

    with col_icp:
        st.markdown("### ICP Qualification")
        
        fit_status = result.get('icp_fit', 'Maybe')
        score = result.get('icp_score', 0)
        
        if fit_status.lower() == "yes":
            badge_class, dot_class = "icp-badge-yes", "dot-yes"
        elif fit_status.lower() == "no":
            badge_class, dot_class = "icp-badge-no", "dot-no"
        else:
            badge_class, dot_class = "icp-badge-maybe", "dot-maybe"

        st.markdown(f"""
            <div class="{badge_class}">
                <span class="status-dot {dot_class}"></span>
                ICP Fit: {fit_status}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"### ICP Score: {score}/100")
        st.progress(min(score / 100.0, 1.0))
        
        confidence = min(score + 10, 95) 
        st.markdown(f"### Confidence Meter: {confidence}%")
        st.progress(confidence / 100.0)

        if result.get("reason"):
            st.caption(f"**Match Drivers:** {result.get('reason')}")

    st.divider()

    st.markdown("### Personalized Outreach")
    st.text_area("Generated Email Draft", result.get("outreach_email", ""), height=220, label_visibility="collapsed")

    st.divider()
    st.markdown("### Next Steps")

    pdf_bytes = generate_pdf(company_name, result)
    st.download_button(
        label="📄 Export Report to PDF",
        data=pdf_bytes,
        file_name=f"{company_name}_RevOps_Analysis.pdf",
        mime="application/pdf"
    )

elif submitted and not website:
    st.error("Please enter a valid website URL in the sidebar to begin analysis.")
