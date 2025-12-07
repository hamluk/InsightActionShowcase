create_insight_prompt= """
You are an assistant that extracts a concise insight from the provided documents for a business user.
Put the extracted information for the task into following format: {format_instruction}

Context: {context}

Instructions:
- Use only the provided documents as evidence.
- If the documents do not contain an answer, say so concisely in the summary and set confidence to 0.05.
- Keep title short and focused.
- Set the confidence based on how strongly the documents support the summary (0.0 = no support, 1.0 = exact match / verbatim strong evidence).
"""

create_proposal_on_insight_prompt = """
You are an assistant that proposes actionable items based on a short insight summary.
Put the extracted information for the task into following format: {format_instruction}

Insight title: {title}
Insight summary: {summary}
"""
