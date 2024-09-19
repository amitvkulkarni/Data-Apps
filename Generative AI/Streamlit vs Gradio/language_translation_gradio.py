import gradio as gr
from transformers import MarianMTModel, MarianTokenizer

# Load translation model and tokenizer
model_name = "Helsinki-NLP/opus-mt-en-de"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)


# Define translation function
def translate_to_german(text):
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    return tokenizer.decode(translated[0], skip_special_tokens=True)


# Gradio interface
iface = gr.Interface(
    fn=translate_to_german,
    inputs="text",
    outputs="text",
    title="English to German Translator",
    description="Enter an English sentence, and get the German translation!",
)

iface.launch(share=True)
