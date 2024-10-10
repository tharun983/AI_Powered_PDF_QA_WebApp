
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Function to preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Tokenize the text into words
    tokens = word_tokenize(text)
    
    # Remove punctuation and non-alphabetic tokens
    words = [word for word in tokens if word.isalpha()]
    
    # Remove stopwords (common words like 'the', 'and', etc.)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    # Lemmatize the words (convert to base form)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    
    # Return the cleaned and preprocessed text as a single string
    return ' '.join(lemmatized_words)

# Function to read input text, preprocess it, and save the result
def preprocess_pdf_text(input_txt_file, output_txt_file):
    # Read the input text file
    with open(input_txt_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Preprocess the text
    cleaned_text = preprocess_text(text)
    
    # Write the cleaned text to the output file
    with open(output_txt_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

# Specify the input and output files
input_txt_file = 'output.txt'  # Assuming output.txt is your extracted text from PDF
output_txt_file = 'preprocessed_output.txt'

# Preprocess the text
preprocess_pdf_text(input_txt_file, output_txt_file)
