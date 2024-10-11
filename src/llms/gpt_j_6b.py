from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline

def get_language_model_gpt_j_6b():
    model_name = "EleutherAI/gpt-j-6B"  
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=200
    )
    
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm
