import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="👋🏻 Hi WelcomeTo Combot Your Offline Computer Chatbot",
    layout="centered"
)

st.markdown("""
<style>
.title {
    color: #4fc3f7;
    font-size: 32px;
    font-weight: bold;
}
.user {
    color: #0d47a1;
    font-weight: bold;
}
.bot {
    color: #ff9800;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>👋🏻 Hi Welcome To Combot Your Offline Computer Chatbot</div>", unsafe_allow_html=True)
st.write("Ask any **computer-related question**. Answers come from local knowledge only.")

@st.cache_data
def load_knowledge():
    topics, sentences = [], []
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if "|" in line:
                topic, sentence = line.split("|", 1)
                topics.append(topic)
                sentences.append(sentence)
    return topics, sentences

topics, knowledge_base = load_knowledge()


# ---------------- TF-IDF LOGIC ----------------
def get_best_match(user_question, sentences):
    corpus = sentences + [user_question]
    vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
    tfidf = vectorizer.fit_transform(corpus)
    similarities = cosine_similarity(tfidf[-1], tfidf[:-1])[0]
    best_score = np.max(similarities)
    best_index = np.argmax(similarities)
    return best_score, best_index

def chatbot(user_input):
    user_input = user_input.lower().strip()

    if not user_input:
        return "Please type a computer-related question."
    original = user_input
    normalize_phrases = [
        "what is", "what is a", "define", "explain",
        "tell me about", "describe", "meaning of"
    ]
    for phrase in normalize_phrases:
        if user_input.startswith(phrase):
            user_input = user_input.replace(phrase, "").strip()
    user_input = user_input.replace("?", "").strip()
    
    for topic, sentence in zip(topics, knowledge_base):
        if topic.endswith("_definition"):
            concept = topic.replace("_definition", "").strip()
            if user_input == concept:
                return sentence.capitalize()
    score, index = get_best_match(user_input, knowledge_base)
    best_topic = topics[index].replace("_", " ")
    if score >= 0.50:
        return knowledge_base[index].capitalize()
    if 0.30 <= score < 0.50:
        return (
            "🤔 I found something related, but your question is unclear.\n\n"
            f"Are you asking about **{best_topic}**?\n\n"
            "Try asking:\n"
            f"- What is {best_topic}?\n"
            f"- Uses of {best_topic}\n"
            f"- Examples of {best_topic}"
        )
    return (
        "❌ I don't have this information in my local knowledge.\n\n"
        f"You asked: \"{original}\"\n"
        "Please:\n"
        "- Rephrase the question\n"
        "- Ask about one computer concept at a time\n"
        "- Use simple computer terms"
        "- use what is, define, explain"
    )

if "history" not in st.session_state:
    st.session_state.history = []
user_question = st.text_input("Type your question:")
if st.button("Ask"):
    response = chatbot(user_question)
    st.session_state.history.append(("You", user_question))
    st.session_state.history.append(("Bot", response))
st.divider()

for speaker, text in st.session_state.history:
    if speaker == "You":
        st.markdown(f"<span class='user'>🧑 You:</span> {text}", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='bot'>🤖 Bot:</span> {text}", unsafe_allow_html=True)
