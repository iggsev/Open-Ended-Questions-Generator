import random
import openai
import nltk

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY_HERE"

# Load NLTK word categories
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
word_categories = {
    'noun': ['NN', 'NNS', 'NNP', 'NNPS'],
    'verb': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
    'adjective': ['JJ', 'JJR', 'JJS'],
    'adverb': ['RB', 'RBR', 'RBS']
}

# Define a function to generate random open-ended questions
def generate_question():
    # Define a list of question formats
    question_formats = [
        "What is the {noun} that {verb}?",
        "How does {noun} {verb}?",
        "What are some {adjective} ways to {verb} {noun}?",
        "Why is {noun} {adjective}?",
        "What can you tell me about {noun} that {verb}?"
    ]
    
    # Choose a random question format
    question_format = random.choice(question_formats)
    
    # Replace {noun}, {verb}, {adjective}, and {adverb} placeholders with random words of the corresponding category
    tagged_words = nltk.corpus.brown.tagged_words()
    noun = random.choice([word for word, tag in tagged_words if tag in word_categories['noun']])
    verb = random.choice([word for word, tag in tagged_words if tag in word_categories['verb']])
    adjective = random.choice([word for word, tag in tagged_words if tag in word_categories['adjective']])
    adverb = random.choice([word for word, tag in tagged_words if tag in word_categories['adverb']])
    question = question_format.format(noun=noun, verb=verb, adjective=adjective, adverb=adverb)
    
    return question

# Define a function to evaluate the coherence of a question using GPT-3
def evaluate_coherence(question):
    # Generate GPT-3 prompt to evaluate the coherence of the question
    prompt = f"Please rate the coherence of the following question on a scale of 0 to 1:\n{question}\nCoherence score:"
    
    # Call the OpenAI GPT-3 API to generate a coherence score
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5
    )
    
    # Extract the coherence score from the GPT-3 response
    coherence_score = float(response.choices[0].text)
    
    return coherence_score

# Define a function to run the program
def run_program(num_questions, coherence_threshold):
    # Generate random open-ended questions and evaluate their coherence
    coherent_questions = []
    for i in range(num_questions):
        question = generate_question()
        coherence_score = evaluate_coherence(question)
        if coherence_score >= coherence_threshold:
            coherent_questions.append((question, coherence_score))
    
    # Print out the coherent questions and their coherence scores
    for question, coherence_score in coherent_questions:
        print(f"{question} (Coherence score: {coherence_score:.2f})")

# Run the program with 10 random questions and a coherence threshold of 0.5
run_program(num_questions=10, coherence_threshold=0.5)