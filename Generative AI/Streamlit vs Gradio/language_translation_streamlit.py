import streamlit as st
from transformers import MarianMTModel, MarianTokenizer

# Load translation model and tokenizer
model_name = "Helsinki-NLP/opus-mt-en-de"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)


# Define translation function
def translate_to_german(text):
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    return tokenizer.decode(translated[0], skip_special_tokens=True)


# Streamlit app layout
st.title("English to German Translator")
st.write("Enter an English sentence, and see the German translation on the right.")

# Create two columns: one for input and one for output
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input (English)")
    # Text input box
    english_text = st.text_area("Enter English text here", height=200)

with col2:
    st.subheader("Output (German)")
    # Placeholder for the output text box
    translation_placeholder = st.empty()

# Translate and display result when button is clicked
if st.button("Translate"):
    if english_text:
        german_translation = translate_to_german(english_text)
        # Display the German translation in the output text box
        translation_placeholder.text_area(
            "Translated Text", value=german_translation, height=200
        )
    else:
        st.write("Please enter some text.")
