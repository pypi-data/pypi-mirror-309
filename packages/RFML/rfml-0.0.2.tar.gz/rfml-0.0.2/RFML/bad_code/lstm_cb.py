import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Sample conversational data
conversations = [
    ["Hi", "Hello! How can I help you?"],
    ["What is your name?", "I am an AI chatbot."],
    ["Tell me a joke.", "Why don’t scientists trust atoms? Because they make up everything!"],
    ["Bye", "Goodbye! Have a great day!"]
]

# Flatten the data into input-output pairs
inputs = [conv[0] for conv in conversations]
responses = [conv[1] for conv in conversations]

# Tokenization and Vocabulary
tokenizer = Tokenizer()
tokenizer.fit_on_texts(inputs + responses)
vocab_size = len(tokenizer.word_index) + 1

# Convert texts to sequences
input_sequences = tokenizer.texts_to_sequences(inputs)
response_sequences = tokenizer.texts_to_sequences(responses)

# Pad sequences to have consistent length
max_seq_len = max(max(len(seq) for seq in input_sequences), max(len(seq) for seq in response_sequences))
input_sequences = pad_sequences(input_sequences, maxlen=max_seq_len, padding='post')
response_sequences = pad_sequences(response_sequences, maxlen=max_seq_len, padding='post')

# Prepare input (X) and output (y)
X = input_sequences
y = np.array(response_sequences)

# Build the LSTM Model
model = Sequential([
    Embedding(vocab_size, 64, input_length=max_seq_len),
    LSTM(128, return_sequences=True),
    Dense(vocab_size, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Reshape y to match sparse categorical requirements
y = y[..., np.newaxis]

# Train the model
model.fit(X, y, epochs=100, batch_size=32, verbose=2)

# Function to generate responses
def generate_response(input_text):
    input_seq = tokenizer.texts_to_sequences([input_text])
    padded_input = pad_sequences(input_seq, maxlen=max_seq_len, padding='post')
    predictions = model.predict(padded_input)
    predicted_seq = np.argmax(predictions[0], axis=1)
    response = " ".join(tokenizer.index_word.get(idx, "") for idx in predicted_seq).strip()
    return response

# Test the chatbot
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Chatbot: Goodbye!")
        break
    response = generate_response(user_input)
    print(f"Chatbot: {response}")
