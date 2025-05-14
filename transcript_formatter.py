# transcript_formatter.py
from ollama import Client
import os

class TranscriptFormatter:
    def __init__(self, model="gemma3:12b", base_url="http://localhost:11434/"):
        self.model = model
        self.client = Client(host=base_url)

    def format_transcript(self, raw_text, max_retries=3):
        prompt = f"""You are an assistant that formats raw audio transcripts into clean, readable dialogue scripts.
Your task is to improve readability by:
– Clearly labelling each speaker (e.g., Peter, Sarah, Narrator)
– Applying correct punctuation and line breaks
– Italicising all narration or non-verbal elements (e.g., [laughter], Narrator: You now have 30 seconds…)

🔹 Important guidelines:
– Do not paraphrase, rewrite, or shorten the text
– Do not summarise or turn the content into test questions
– Preserve the exact original wording
– Only enhance formatting and clarity

The result should look like a dialogue or script, similar to a screenplay or play format.

Transcript:
{raw_text}
"""

        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    options={
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_ctx": 4096,
                        "repeat_penalty": 1.1,
                        "stop": ["</s>"]
                    }
                )
                return response.message.content.strip()
            except Exception as e:
                print(f"[Attempt {attempt}] Error formatting transcript: {e}")
        return "Error: Unable to format transcript after multiple attempts."


def load_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None


def save_text_to_file(text, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Formatted transcript saved to '{output_path}'")
    except Exception as e:
        print(f"Error saving to file '{output_path}': {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Format a raw transcript into dialogue format using a local LLM.")
    parser.add_argument("input_file", help="Path to the input .txt file with unformatted transcript")
    parser.add_argument("-o", "--output", help="Path to save the formatted transcript (optional)")

    args = parser.parse_args()

    raw_text = load_text_from_file(args.input_file)
    if raw_text is None:
        exit(1)

    formatter = TranscriptFormatter()
    formatted = formatter.format_transcript(raw_text)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        base, ext = os.path.splitext(args.input_file)
        output_path = f"{base}_formatted{ext}"

    save_text_to_file(formatted, output_path)
