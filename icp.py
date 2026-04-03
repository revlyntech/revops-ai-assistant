import re

def extract_numbers(text):
    return [int(x) for x in re.findall(r"\d+", str(text))]

def check_icp(summary_data, custom_icp):
    score = 0
    reasons = []

    # Data pulled from the LLM summary
    industry = summary_data.get("industry", "").lower()
    size = summary_data.get("estimated_size", "")
    location = summary_data.get("location", "").lower()
    revenue = summary_data.get("revenue_range", "")

    # 1. Check Industry (Now checks against a list of choices)
    target_industries = [ind.lower() for ind in custom_icp["industry"]]
    # Give points if ANY of the target industries match, OR if the user left the filter blank
    if not target_industries or any(target in industry for target in target_industries):
        score += 25
        reasons.append("industry match")

    # 2. Check Size
    size_numbers = extract_numbers(size)
    if size_numbers:
        if custom_icp["min_size"] <= size_numbers[0] <= custom_icp["max_size"]:
            score += 25
            reasons.append("size match")

    # 3. Check Location (Now checks against a list of choices)
    target_locations = [loc.lower() for loc in custom_icp["location"]]
    # Give points if ANY of the target locations match, OR if the user left the filter blank
    if not target_locations or any(target in location for target in target_locations):
        score += 25
        reasons.append("location match")

    # 4. Check Revenue
    revenue_numbers = extract_numbers(revenue)
    if revenue_numbers:
        if custom_icp["min_revenue"] <= revenue_numbers[0] <= custom_icp["max_revenue"]:
            score += 25
            reasons.append("revenue match")

    # Determine Fit
    fit = "Yes" if score >= 75 else "Maybe" if score >= 50 else "No"

    return {
        "icp_fit": fit,
        "icp_score": score,
        "reason": " | ".join(reasons) if reasons else "Weak match"
    }