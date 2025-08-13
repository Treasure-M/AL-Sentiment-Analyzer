import gradio as gr
import pandas as pd
import plotly.express as px
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Create static files directory and manifest.json if missing
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
manifest_path = static_dir / "manifest.json"
if not manifest_path.exists():
    manifest_path.write_text("""{
"name": "Sentiment Analyzer",
"short_name": "SentimentApp",
"start_url": ".",
"display": "standalone"
}""")

def analyze_sentiment(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://your-app-url.com",
        "X-Title": "Sentiment Analyzer",
        "Content-Type": "application/json"
    }
    prompt = f"""Classify the sentiment of the following text as ONLY one of: [Positive/Neutral/Negative].
Respond EXACTLY in this format:
Sentiment:
Explanation: <1-sentence reason>
Text: \"\"\"{text}\"\"\""""
    payload = {
        "model": "mistralai/mistral-small-3.2-24b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        if "Sentiment:" in content:
            sentiment = content.split("Sentiment:")[1].split("\n")[0].strip()
            explanation = content.split("Explanation:")[1].strip() if "Explanation:" in content else "No explanation provided."
            return sentiment, explanation
        return "Unknown", content
    except requests.exceptions.HTTPError as e:
        return "API Error", f"HTTP Error: {e.response.text}"
    except Exception as e:
        return "Error", str(e)

def process_single_text(text):
    if not text.strip():
        return "Error", "Empty input text"
    sentiment, explanation = analyze_sentiment(text)
    return f"Sentiment: {sentiment}", f"Explanation: {explanation}"

def process_file(file):
    try:
        # Get file path from uploaded file
        file_path = file.name if not hasattr(file, "file") else file.file.name
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            texts = df.iloc[:, 0].astype(str).tolist()
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
        results = []
        for text in texts:
            sentiment, explanation = analyze_sentiment(text)
            results.append({'Text': text, 'Sentiment': sentiment, 'Explanation': explanation})
        result_df = pd.DataFrame(results)
        sentiment_counts = result_df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig = px.pie(sentiment_counts, names='Sentiment', values='Count', title='Sentiment Distribution')
        return result_df, fig
    except Exception as e:
        return pd.DataFrame({'Error': [str(e)]}), None

def compare_texts(text1, text2):
    sentiment1, explanation1 = analyze_sentiment(text1)
    sentiment2, explanation2 = analyze_sentiment(text2)
    comparison_data = pd.DataFrame({
        'Text': ['Text 1', 'Text 2'],
        'Sentiment': [sentiment1, sentiment2]
    })
    fig = px.bar(
        comparison_data,
        x='Text',
        color='Sentiment',
        title='Comparative Sentiment Analysis',
        barmode='group',
        text='Sentiment',
        color_discrete_map={
            'Positive': 'green',
            'Neutral': 'gray',
            'Negative': 'red'
        }
    )
    return (
        f"Text 1 Sentiment: {sentiment1}\nExplanation: {explanation1}",
        f"Text 2 Sentiment: {sentiment2}\nExplanation: {explanation2}",
        fig
    )

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 AI Sentiment Analysis Web App")

    with gr.Tab("🔹 Manual Input"):
        text_input = gr.Textbox(label="Enter Text", placeholder="Type or paste text here...")
        analyze_button = gr.Button("Analyze Sentiment")
        sentiment_output = gr.Textbox(label="Sentiment")
        explanation_output = gr.Textbox(label="Explanation")
        analyze_button.click(process_single_text, inputs=text_input, outputs=[sentiment_output, explanation_output])

    with gr.Tab("📂 File Upload"):
        file_input = gr.File(label="Upload a CSV or TXT file (First column should contain the text)")
        process_button = gr.Button("Process File")
        file_output = gr.Dataframe(label="Sentiment Results")
        chart_output = gr.Plot(label="Sentiment Distribution Chart")
        process_button.click(process_file, inputs=file_input, outputs=[file_output, chart_output])

    with gr.Tab("⚖️ Comparative Analysis"):
        text1_input = gr.Textbox(label="Enter First Text")
        text2_input = gr.Textbox(label="Enter Second Text")
        compare_button = gr.Button("Compare Sentiments")
        compare_result1 = gr.Textbox(label="Text 1 Sentiment & Explanation")
        compare_result2 = gr.Textbox(label="Text 2 Sentiment & Explanation")
        compare_chart = gr.Plot(label="Comparison Chart")
        compare_button.click(compare_texts, inputs=[text1_input, text2_input],
                             outputs=[compare_result1, compare_result2, compare_chart])
                             
    @demo.app.get("/manifest.json")
    def serve_manifest():
        return open(manifest_path, "r").read()


if __name__ == "__main__":
    ports = [7860, 7861, 7862, 7863, 7864]  
    
    for port in ports:
        try:
            print(f"Attempting to launch on port {port}...")
            demo.launch(server_name="0.0.0.0", server_port=port, share=True)
            print(f"App is running at http://localhost:{port}")
            break 
        except OSError as e:
            if "address already in use" in str(e).lower():
                print(f"Port {port} is in use. Trying the next port...")
            else:
                print(f"An unexpected error occurred: {e}")
                break
    else:
        print("Failed to launch the application on all specified ports.")