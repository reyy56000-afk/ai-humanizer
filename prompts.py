"""
Prompt templates for AI Humanizer.
Contains predefined prompts for different use cases.
"""

HUMANIZE_PROMPT = """You are an expert writing assistant specializing in making AI-generated content sound naturally human-written.

Rewrite the following text to sound like it was written by a human, while maintaining:
- The original meaning and intent
- All factual accuracy
- Professional tone (if applicable)
- Key information and data

Guidelines:
- Improve sentence flow and readability
- Vary sentence lengths and structures
- Remove repetitive words and phrases
- Add natural transitions where needed
- Use contractions appropriately
- Avoid over-formal language
- Keep paragraphs well-structured
- Don't add new information
- Don't change the core message

Text to humanize:
{text}

Provide ONLY the humanized text, without any explanation or preamble."""

DETECTOR_PROMPT = """Analyze the following text and determine if it appears to be written by an AI or a human.

Provide your analysis in the following format:
- Probability (percentage): How likely it is to be AI-generated
- Key indicators: List the main characteristics that suggest AI or human writing
- Verdict: AI-generated or Human-written
- Explanation: Brief explanation of your assessment

Text to analyze:
{text}"""

IMPROVE_PROMPT = """You are a professional editor. Improve the following text for clarity, engagement, and professionalism.

Focus on:
- Grammar and punctuation
- Word choice and vocabulary
- Sentence structure and flow
- Paragraph organization
- Tone and style
- Readability

Text to improve:
{text}

Provide ONLY the improved text, without any explanation or preamble."""

SUMMARIZE_PROMPT = """Summarize the following text concisely while maintaining all important information.

Keep the summary to about 30% of the original length.
Maintain the original tone and key facts.

Text to summarize:
{text}

Provide ONLY the summary, without any explanation or preamble."""

TONE_ADJUST_PROMPT = """Rewrite the following text with a {tone} tone.

Tone options: professional, casual, formal, friendly, persuasive, technical

Current text:
{text}

Provide ONLY the rewritten text with the requested tone, without any explanation or preamble."""
