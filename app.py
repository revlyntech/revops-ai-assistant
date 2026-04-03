from enrichment import scrape_website
from summary import generate_summary
from icp import check_icp


def run_agent(input_data, custom_icp):
    company = input_data["company_name"]
    website = input_data["website"]

    enriched = scrape_website(website)
    summary_data = generate_summary(enriched, company)
    icp_result = check_icp(summary_data, custom_icp)

    return {
        **summary_data,
        **icp_result
    }