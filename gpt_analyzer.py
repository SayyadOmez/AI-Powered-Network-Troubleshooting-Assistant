import os
from openai import OpenAI

# Paste your actual OpenAI API key here
client = OpenAI(api_key="OpenAI API key")  # Replace with your key

def analyze_logs_with_gpt(log_text):
    prompt = f"""
You are a network troubleshooting assistant. Analyze the following network log and:
1. Identify the problem in simple terms.
2. Suggest the likely cause.
3. Recommend a solution.

Network Log:
{log_text}

Respond clearly and concisely.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful network assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"
