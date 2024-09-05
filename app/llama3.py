from transformers import pipeline

class Llama3Model:
    def __init__(self):
        # Load Llama3 model (use Hugging Face transformers)
        self.model = pipeline('text-generation', model='path/to/local/llama3')

    def generate_summary(self, content: str):
        # Generate a summary from the book content
        return self.model(content, max_length=150, do_sample=True)[0]['generated_text']
