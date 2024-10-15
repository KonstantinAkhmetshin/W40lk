import json
import re

def parse_json(text):
        # Step 1: Extract JSON using regex
    json_match = re.search(r'{.*}', text, re.DOTALL)

    if json_match:
        json_str = json_match.group()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
    else:
        print("No JSON found in the response.")
