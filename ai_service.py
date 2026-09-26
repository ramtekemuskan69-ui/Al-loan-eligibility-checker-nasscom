import json
import logging
from typing import Dict, Any, Optional
from .config import settings
from .schemas import AIRecommendationsResponse

logger = logging.getLogger(__name__)

FALLBACK_DISCLAIMER = "Educational financial guidance only. Not financial advice or a guarantee of loan approval."

def build_educational_fallback(profile_data: Dict[str, Any]) -> AIRecommendationsResponse:
    """
    Generate deterministic, personalized educational BFSI advice
    when the Gemini API is unreachable or key is not provided.
    """
    score = profile_data.get("credit_score", 700)
    income = profile_data.get("monthly_income", 50000)
    existing_emi = profile_data.get("existing_emi", 0)
    expenses = profile_data.get("monthly_expenses", 20000)
    credit_limit = profile_data.get("credit_limit", 100000)
    credit_used = profile_data.get("credit_used", 30000)
    missed_payments = profile_data.get("missed_payments", 0)
    requested_amount = profile_data.get("requested_amount", 500000)
    tenure = profile_data.get("tenure", 36)

    dti = (existing_emi / income * 100) if income > 0 else 0
    utilization = (credit_used / credit_limit * 100) if credit_limit > 0 else 0
    disposable = income - expenses - existing_emi

    # Assessment wording
    if score >= 750 and dti < 35 and utilization < 30:
        overall = (
            f"Your financial profile exhibits strong credit discipline with a credit score of {score} "
            f"and an optimal debt-to-income ratio of {dti:.1f}%. You maintain a healthy disposable monthly buffer "
            f"of ₹{disposable:,.0f}."
        )
    elif score >= 650 and dti < 50:
        overall = (
            f"Your preliminary profile demonstrates moderate stability with a credit score of {score} "
            f"and DTI of {dti:.1f}%. While baseline metrics are balanced, optimizing credit card balances and "
            f"limiting new obligations will strengthen borrower positioning."
        )
    else:
        overall = (
            f"Your current financial metrics highlight opportunities to enhance credit health before "
            f"formal loan origination. With a credit score of {score} and {missed_payments} missed payment(s), "
            f"consolidating dues and reducing utilization should be top priorities."
        )

    # Key factors
    key_factors = [
        f"Credit Score ({score}/900): Represents historical payment reliability.",
        f"Revolving Credit Utilization ({utilization:.1f}%): Target below 30% of credit limit for optimal score impact.",
        f"Debt-to-Income Ratio ({dti:.1f}%): Measures existing monthly debt obligations against current earnings.",
        f"Repayment Record: {missed_payments} missed payment incident(s) reported in profile history.",
        f"Monthly Cashflow Surplus: ₹{disposable:,.0f} remaining after expenses and current EMIs."
    ]

    # Recommendations
    recs = []
    if utilization > 30:
        recs.append(f"Reduce credit card utilization from {utilization:.1f}% to under 30% by paying down balances early.")
    else:
        recs.append("Maintain credit utilization below 30% to continuously support positive credit scoring.")

    if missed_payments > 0:
        recs.append("Automate calendar reminders or auto-debits to guarantee on-time payments for all debt facilities.")
    else:
        recs.append("Preserve your 100% on-time payment track record across all revolving and term facilities.")

    if dti > 35:
        recs.append("Consider accelerating repayments on high-interest loans to compress your aggregate DTI.")
    else:
        recs.append("Keep monthly debt commitments comfortably below 35% of income to retain financial resilience.")

    recs.append("Avoid making multiple simultaneous formal loan inquiries within brief intervals to prevent hard inquiries.")
    recs.append("Maintain an emergency fund equivalent to 3 to 6 months of living expenses alongside planned loan obligations.")

    # EMI guidance
    emi_guidance = (
        f"For a requested principal of ₹{requested_amount:,.0f} over {tenure} months, verify that your projected "
        f"monthly installment comfortably remains within 30% to 40% of your disposable income (₹{disposable:,.0f}). "
        f"A longer tenure reduces monthly outflow but accumulates higher overall interest charges."
    )

    return AIRecommendationsResponse(
        overall_assessment=overall,
        key_factors=key_factors,
        recommendations=recs,
        emi_guidance=emi_guidance,
        disclaimer=FALLBACK_DISCLAIMER
    )


def get_ai_recommendations(profile_data: Dict[str, Any]) -> AIRecommendationsResponse:
    """
    Retrieve AI-powered educational recommendations using Gemini API,
    with seamless fallback if the API key is not configured or an error occurs.
    """
    api_key = settings.GEMINI_API_KEY.strip() if settings.GEMINI_API_KEY else ""

    if not api_key:
        logger.info("GEMINI_API_KEY not configured. Returning rule-based educational guidance.")
        return build_educational_fallback(profile_data)

    prompt_content = f"""
You are an educational financial assistant. Analyze the supplied financial profile and explain the factors that may affect a preliminary loan assessment. Provide general educational guidance. Do not guarantee loan approval, predict approval with certainty, recommend a specific lender, or present the response as professional financial advice.

User Profile:
- Monthly Income: ₹{profile_data.get('monthly_income', 0)}
- Other Income: ₹{profile_data.get('other_income', 0)}
- Monthly Living Expenses: ₹{profile_data.get('monthly_expenses', 0)}
- Existing Monthly EMI: ₹{profile_data.get('existing_emi', 0)}
- Credit Score: {profile_data.get('credit_score', 0)}
- Credit Limit: ₹{profile_data.get('credit_limit', 0)}
- Credit Used: ₹{profile_data.get('credit_used', 0)}
- Missed Payments: {profile_data.get('missed_payments', 0)}
- Existing Loans: {profile_data.get('existing_loans', 0)}
- Requested Loan Amount: ₹{profile_data.get('requested_amount', 500000)}
- Desired Tenure: {profile_data.get('tenure', 36)} months
- Loan Type: {profile_data.get('loan_type', 'Personal Loan')}

You must return a valid JSON object with EXACTLY this structure (no markdown formatting, no backticks, just raw JSON):
{{
  "overall_assessment": "string educational assessment",
  "key_factors": [
    "string factor 1",
    "string factor 2",
    "string factor 3",
    "string factor 4",
    "string factor 5"
  ],
  "recommendations": [
    "string recommendation 1",
    "string recommendation 2",
    "string recommendation 3",
    "string recommendation 4",
    "string recommendation 5"
  ],
  "emi_guidance": "string educational guidance on EMI, interest, and tenure trade-offs",
  "disclaimer": "Educational financial guidance only. Not financial advice or a guarantee of loan approval."
}}
"""

    try:
        # Try google.genai or google.generativeai
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_content,
            )
            raw_text = response.text
        except Exception:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=api_key)
            model = legacy_genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt_content)
            raw_text = response.text

        # Clean markdown code blocks if present
        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        data = json.loads(cleaned_text)

        return AIRecommendationsResponse(
            overall_assessment=str(data.get("overall_assessment", "")),
            key_factors=list(data.get("key_factors", [])),
            recommendations=list(data.get("recommendations", [])),
            emi_guidance=str(data.get("emi_guidance", "")),
            disclaimer=str(data.get("disclaimer", FALLBACK_DISCLAIMER))
        )
    except Exception as e:
        logger.warning(f"Error querying Gemini API: {str(e)}. Using educational fallback.")
        return build_educational_fallback(profile_data)
