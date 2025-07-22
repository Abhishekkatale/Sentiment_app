import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
import speech_recognition as sr

# ----- PAGE CONFIG -----
st.set_page_config(page_title="Sentiment Analyzer ", page_icon="💬", layout="wide")

# ----- ENHANCED DARK THEME CSS WITH BOLD GRADIENTS & ANIMATIONS -----
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, 
        #0a0a0a 0%, 
        #1a1a2e 15%, 
        #16213e 30%, 
        #0f3460 45%,
        #1a1a2e 60%,
        #0a0a0a 75%,
        #16213e 90%,
        #1c1c1c 100%);
    background-size: 400% 400%;
    animation: gradientWave 15s ease infinite;
    color: #e8f4fd;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

/* ENHANCED ANIMATED GRADIENT */
@keyframes gradientWave {
    0% { background-position: 0% 50%; }
    25% { background-position: 100% 50%; }
    50% { background-position: 50% 100%; }
    75% { background-position: 0% 100%; }
    100% { background-position: 0% 50%; }
}

/* FLOATING PARTICLES EFFECT */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 60%, rgba(59, 130, 246, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 60% 30%, rgba(16, 185, 129, 0.08) 0%, transparent 50%);
    animation: floatingParticles 25s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes floatingParticles {
    0%, 100% { transform: translateY(0) scale(1) rotate(0deg); }
    25% { transform: translateY(-15px) scale(1.02) rotate(90deg); }
    50% { transform: translateY(-25px) scale(1.05) rotate(180deg); }
    75% { transform: translateY(-10px) scale(1.03) rotate(270deg); }
}

/* CLEAN HEADINGS WITH NORMAL TEXT */
h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 700;
    text-align: center;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

h1 { font-size: 3.2rem; }
h2 { font-size: 2.4rem; }
h3 { font-size: 1.9rem; }

/* REMOVE DEFAULT STREAMLIT STYLING */
section.main > div:first-child {
    background: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ENHANCED GLASSMORPHISM UI BLOCKS */
.stTextArea, .stFileUploader, .stRadio, .stDataFrame, .stSelectbox, .stButton, .stTextInput {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1.5rem auto !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    max-width: 800px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

/* HOVER EFFECTS FOR UI BLOCKS */
.stTextArea:hover, .stFileUploader:hover, .stButton:hover {
    transform: translateY(-5px) !important;
    box-shadow: 
        0 15px 45px rgba(99, 102, 241, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(139, 92, 246, 0.4) !important;
    background: rgba(255, 255, 255, 0.08) !important;
}

/* SHIMMER EFFECT FOR UI BLOCKS */
.stTextArea::before, .stFileUploader::before, .stButton::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.2), transparent);
    animation: shimmer 4s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* ENHANCED INPUT FIELDS */
textarea, input, .stTextInput > div > div > input {
    font-size: 1.2rem !important;
    background: rgba(255, 255, 255, 0.08) !important;
    color: #e8f4fd !important;
    border: 2px solid rgba(99, 102, 241, 0.3) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-align: left !important;
    backdrop-filter: blur(10px) !important;
}

textarea::placeholder, input::placeholder {
    color: rgba(232, 244, 253, 0.5) !important;
    font-weight: 500 !important;
}

/* FOCUS STATES */
textarea:focus, input:focus, .stTextInput > div > div > input:focus {
    background: rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
    border: 2px solid rgba(139, 92, 246, 0.6) !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
    transform: scale(1.02) !important;
}

/* ENHANCED TABS WITH ANIMATIONS */
.stTabs [data-baseweb="tab"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 15px 15px 0 0 !important;
    padding: 1rem 2rem !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: #e8f4fd !important;
    margin-right: 8px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-3px) !important;
    background: rgba(99, 102, 241, 0.1) !important;
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2) !important;
    color: #ffffff !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.15)) !important;
    color: #ffffff !important;
    box-shadow: 
        0 -4px 0 #8b5cf6 inset,
        0 15px 35px rgba(139, 92, 246, 0.3) !important;
    transform: translateY(-5px) !important;
}

/* SPECTACULAR BUTTON STYLING */
button[kind="primary"], .stButton > button {
    background: linear-gradient(135deg, 
        rgba(99, 102, 241, 0.8) 0%, 
        rgba(139, 92, 246, 0.7) 50%, 
        rgba(59, 130, 246, 0.6) 100%) !important;
    color: #ffffff !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    padding: 1rem 2.5rem !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(15px) !important;
    box-shadow: 
        0 10px 30px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    z-index: 1 !important;
    cursor: pointer !important;
}

/* BUTTON RIPPLE EFFECT */
button[kind="primary"]::before, .stButton > button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
    z-index: -1;
}

button[kind="primary"]:hover::before, .stButton > button:hover::before {
    width: 300px;
    height: 300px;
}

/* BUTTON HOVER & ACTIVE STATES */
button[kind="primary"]:hover, .stButton > button:hover {
    background: linear-gradient(135deg, 
        rgba(139, 92, 246, 0.9) 0%, 
        rgba(99, 102, 241, 0.8) 50%, 
        rgba(59, 130, 246, 0.7) 100%) !important;
    color: #ffffff !important;
    transform: translateY(-8px) scale(1.05) !important;
    box-shadow: 
        0 20px 50px rgba(139, 92, 246, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}

button[kind="primary"]:active, .stButton > button:active {
    transform: translateY(-2px) scale(0.98) !important;
    background: linear-gradient(135deg, 
        rgba(79, 70, 229, 0.95) 0%, 
        rgba(99, 102, 241, 0.85) 100%) !important;
}

/* PULSING ANIMATION FOR IMPORTANT BUTTONS */
@keyframes buttonPulse {
    0%, 100% { box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2); }
    50% { box-shadow: 0 15px 40px rgba(139, 92, 246, 0.4); }
}

button[kind="primary"], .stButton > button {
    animation: buttonPulse 3s ease-in-out infinite !important;
}

/* ENHANCED ALERT BOXES */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 16px !important;
    font-size: 1.2rem !important;
    font-weight: 500 !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    text-align: center !important;
    animation: slideInUp 0.5s ease-out !important;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stSuccess {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #6ee7b7 !important;
    border-color: rgba(16, 185, 129, 0.3) !important;
}

.stInfo {
    background: rgba(59, 130, 246, 0.15) !important;
    color: #93c5fd !important;
    border-color: rgba(59, 130, 246, 0.3) !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.15) !important;
    color: #fcd34d !important;
    border-color: rgba(245, 158, 11, 0.3) !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    color: #fca5a5 !important;
    border-color: rgba(239, 68, 68, 0.3) !important;
}

/* DATA FRAME ENHANCEMENTS */
.stDataFrame {
    border: 2px solid rgba(99, 102, 241, 0.3) !important;
    background: rgba(0, 0, 0, 0.2) !important;
}

.stDataFrame table {
    background: rgba(0, 0, 0, 0.3) !important;
    color: #e8f4fd !important;
}

.stDataFrame th {
    background: rgba(99, 102, 241, 0.2) !important;
    color: #ffffff !important;
}

.stDataFrame td {
    background: rgba(255, 255, 255, 0.02) !important;
    color: #e8f4fd !important;
}

/* MICROPHONE BUTTON SPECIAL STYLING */
button:contains("🎤") {
    background: linear-gradient(135deg, 
        rgba(236, 72, 153, 0.8) 0%, 
        rgba(168, 85, 247, 0.7) 100%) !important;
    animation: microphonePulse 1.5s ease-in-out infinite alternate !important;
}

@keyframes microphonePulse {
    from { transform: scale(1); }
    to { transform: scale(1.03); }
}

/* RADIO BUTTONS STYLING */
.stRadio > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
}

.stRadio label {
    color: #e8f4fd !important;
}

/* FILE UPLOADER STYLING */
.stFileUploader label {
    color: #e8f4fd !important;
}

/* RESPONSIVE DESIGN */
@media screen and (max-width: 768px) {
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 1.8rem !important; }
    
    .stTextArea, .stButton, .stTextInput {
        padding: 1.2rem !important;
        margin: 1rem !important;
    }
    
    button[kind="primary"], .stButton > button {
        font-size: 1.1rem !important;
        padding: 0.8rem 1.5rem !important;
    }
}

/* LOADING ANIMATION */
@keyframes loading {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* SMOOTH TRANSITIONS FOR ALL ELEMENTS */
* {
    transition: all 0.3s ease !important;
}

/* PLOTLY CHART CONTAINER DARK STYLING */
.js-plotly-plot {
    background: rgba(0, 0, 0, 0.3) !important;
    border-radius: 15px !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

SENTIMENT_COLORS = {
    "Positive": "#10b981",  # Emerald green
    "Negative": "#ef4444",  # Red
    "Neutral": "#6b7280"    # Gray
}

# Dark theme plotly template
DARK_PLOTLY_TEMPLATE = {
    'layout': {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': '#e8f4fd'},
        'colorway': ['#10b981', '#ef4444', '#6b7280', '#8b5cf6', '#3b82f6'],
        'title': {'font': {'color': '#ffffff', 'size': 18}},
        'xaxis': {
            'gridcolor': 'rgba(99, 102, 241, 0.2)',
            'linecolor': 'rgba(99, 102, 241, 0.3)',
            'tickcolor': '#e8f4fd',
            'tickfont': {'color': '#e8f4fd'}
        },
        'yaxis': {
            'gridcolor': 'rgba(99, 102, 241, 0.2)',
            'linecolor': 'rgba(99, 102, 241, 0.3)',
            'tickcolor': '#e8f4fd',
            'tickfont': {'color': '#e8f4fd'}
        }
    }
}

# ----- UTILITIES -----
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def get_polarity(text):
    return round(TextBlob(text).sentiment.polarity, 3)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"✅ Recognized: {text}")
            return text
        except Exception as e:
            st.error(f"❌ Could not understand: {e}")
            return ""

def analyze_text(text):
    sentiment = get_sentiment(text)
    polarity = get_polarity(text)
    return sentiment, polarity

def analyze_dataframe(df, text_col):
    df["Text"] = df[text_col].astype(str)
    df["Sentiment"] = df["Text"].apply(get_sentiment)
    df["Polarity"] = df["Text"].apply(get_polarity)
    return df

def plot_sentiment_pie(df):
    fig = px.pie(
        df,
        names="Sentiment",
        title="🎯 Sentiment Distribution",
        color="Sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        template="plotly_dark"
    )
    fig.update_layout(DARK_PLOTLY_TEMPLATE['layout'])
    fig.update_traces(textfont_size=14, textfont_color='white')
    return fig

def plot_sentiment_bar(df):
    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    fig = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        title="📊 Sentiment Distribution",
        color="Sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        template="plotly_dark"
    )
    fig.update_layout(DARK_PLOTLY_TEMPLATE['layout'])
    fig.update_traces(textfont_size=14, textfont_color='white')
    return fig

def final_summary(df):
    most_common = df["Sentiment"].value_counts().idxmax()
    if most_common == "Positive":
        st.success("🌟 Most of the reviews are **Positive**!")
    elif most_common == "Negative":
        st.error("😞 Most of the reviews are **Negative**.")
    else:
        st.info("😐 Most of the reviews are **Neutral**.")

# ----- MAIN UI -----
st.title("💬 Sentiment Analyzer Pro")
st.markdown("### ✨ Analyze text with style - featuring real-time sentiment analysis, speech recognition, and beautiful visualizations")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📝 Type or Speak", "📁 Upload CSV", "📊 Results Summary"])

# ----- TAB 1 -----
with tab1:
    st.header("📝 Sentiment from Input")
    input_mode = st.radio("Choose input method:", ["Type Text", "Use Microphone"], horizontal=True)

    if input_mode == "Type Text":
        user_input = st.text_area("Type something here 👇", height=150, placeholder="Enter your text here to analyze its sentiment...")
        if st.button("🔍 Analyze Text"):
            if user_input.strip():
                sentiment, polarity = analyze_text(user_input)
                st.success(f"**Sentiment:** {sentiment} (Score: `{polarity}`)")
            else:
                st.warning("Please enter some text to analyze.")
    else:
        if st.button("🎤 Start Microphone"):
            speech_text = recognize_speech()
            if speech_text:
                sentiment, polarity = analyze_text(speech_text)
                st.success(f"**Sentiment:** {sentiment} (Score: `{polarity}`)")

# ----- TAB 2 -----
with tab2:
    st.header("📁 Upload CSV File")
    uploaded_file = st.file_uploader("Upload a CSV with a 'review', 'text', or 'comment' column", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        possible_cols = [col for col in df.columns if any(key in col.lower() for key in ['review', 'text', 'comment'])]
        if possible_cols:
            review_col = possible_cols[0]
            st.success(f"Detected column: `{review_col}`")
            df = analyze_dataframe(df, review_col)

            st.dataframe(df[[review_col, "Sentiment", "Polarity"]].head(10))
            st.session_state["df"] = df
        else:
            st.error("No valid column found with text data.")

# ----- TAB 3 -----
with tab3:
    st.header("📊 Sentiment Visualization")
    if "df" in st.session_state:
        df = st.session_state["df"]
        final_summary(df)

        st.plotly_chart(plot_sentiment_pie(df), use_container_width=True)
        st.plotly_chart(plot_sentiment_bar(df), use_container_width=True)

        st.download_button(
            "⬇️ Download CSV with Sentiments",
            df.to_csv(index=False).encode("utf-8"),
            file_name="sentiment_results.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No data available yet. Upload a file in the previous tab.")