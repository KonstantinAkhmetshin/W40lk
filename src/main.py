from llms.gpt_facade import get_qa_system
from llms.gpt_enum import GPT

def main():
    # Initialize the QA system
    qa_system = get_qa_system(GPT.GPT_4O_MINI)

    while True:
        # Get user input
        user_input = input("Enter your query (or 'quit' to exit): ")

        if user_input.lower() == 'quit':
            break

        # Process the query
        result = qa_system("start character creation")

            # Handle character creation result
        print("Character Creation Result:")
        print(result["character_creation"])
            
        if result["parsed_json"]:
            print("\nParsed Character Stats:")
            print(json.dumps(result["parsed_json"], indent=2))
        else:
            print("\nCouldn't parse character stats as JSON.")
       
if __name__ == "__main__":
    main()