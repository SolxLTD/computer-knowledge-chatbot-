import streamlit as st
import math

def load_knowledge(file_path="knowledge.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    return sentences


def sentence_similarity(query, sentence):
    query_words = query.lower().split()
    sentence_words = sentence.lower().split()

    overlap = len(set(query_words) & set(sentence_words))

    return overlap / math.sqrt(len(sentence_words) + 1)


def get_response(query, sentences):
    best_sentence = None
    best_score = 0

    for sentence in sentences:
        score = sentence_similarity(query, sentence)
        if score > best_score:
            best_score = score
            best_sentence = sentence

    if best_sentence:
        return best_sentence
    else:
        return "I’m not sure about that, but I can learn more if you update my knowledge base!"


def main():
    st.title("💬 Simple Computer Chatbot")

    st.write("Ask me anything about computers!")

    sentences = load_knowledge()

    user_input = st.text_input("Your question:")

    if st.button("Ask"):
        if user_input.strip() == "":
            st.warning("Please type a question.")
        else:
            response = get_response(user_input, sentences)
            st.success(response)


if __name__ == "__main__":
    main()
