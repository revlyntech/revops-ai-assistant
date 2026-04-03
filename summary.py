import json
from llm import call_llm_json

def smart_fallback(data, company_name):
    """
    Use scraped website text to create dynamic fallback if LLM fails
    """
    content = data.get("content", "").lower()
    meta_desc = data.get("meta_description", "")

    industry = "Technology"

    if "fintech" in content:
        industry = "Fintech"
    elif "health" in content or "medical" in content:
        industry = "Healthcare"
    elif "restaurant" in content or "food" in content:
        industry = "Restaurant Tech"
    elif "software" in content or "saas" in content:
        industry = "SaaS"
    elif "marketing" in content:
        industry = "Marketing Tech"

    return {
        "company_summary": meta_desc or f"{company_name} operates in the {industry} space.",
        "industry": industry,
        "estimated_size": "10-200 employees",
        "location": "Unknown",
        "revenue_range": "$1M-$20M",
        "outreach_email": (
            f"Hi {company_name} team,\n\n"
            f"I noticed your strong work in {industry.lower()} and thought there could be a great fit with how RevOps Central helps automate lead qualification and improve GTM workflows.\n\n"
            f"Would you be open to a quick 15-minute conversation next week?"
        )
    }

def generate_summary(data, company_name):
    # Fallback used only if scraping totally fails
    if not data['content']:
        return smart_fallback(data, company_name) 

    prompt = f"""
    Analyze the following company website content. 

    Company: {company_name}
    Website content: {data['content']}
    Meta Description: {data['meta_description']}

    Task 1: Generate a highly accurate, 2-sentence company summary highlighting their core value proposition.
    Task 2: Write a highly professional, concise B2B cold email to their VP of Operations. 
    The email must:
    - Have a personalized opening based on their website content.
    - Be under 4 sentences.
    - Focus on how RevOps Central can automate their lead qualification and scale their GTM workflows.
    - End with a low-friction call to action.

    Return a JSON object exactly matching this schema:
    {{
      "company_summary": "detailed 2-sentence summary",
      "industry": "specific industry name (e.g., B2B SaaS, HealthTech)",
      "estimated_size": "employee range",
      "location": "country or region",
      "revenue_range": "estimated revenue range",
      "outreach_email": "professional personalized cold email"
    }}
    """

    response = call_llm_json(prompt)

    if response:
        try:
            return json.loads(response)
        except Exception:
            pass
            
    return smart_fallback(data, company_name)