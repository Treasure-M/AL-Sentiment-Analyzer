🧠 AI-Powered Sentiment Analysis Web App

Team members

• Treasure Mashabane 
• Thabo Mavundla 
• Ditshego Kgwadi
• Rebafenyi Mudau 

An instinctive web application for conducting sentiment analysis on text. This tool provides a user-friendly interface to classify text as Positive, Neutral, or Negative, complete with explanations for the sentiment. It supports three major functionalities: exploring single pieces of text, processing complete files (`.txt` or `.csv`), and comparing the sentiments of two distinct texts side-by-side.

This application is created utilizing Python and leverages the [Gradio](https://www.gradio.app/) framework for the user interface and the [Mistral AI](https://mistral.ai/) prototype via the [OpenRouter API](https://openrouter.ai/) for its analytical power.

✨ Features

* 🔹 Manual Input: Quickly examine the sentiment of any text by just typing or pasting it into the intake box.
* 📂 File Upload: Process numerous lines of text at once by uploading a `.txt` file (with each line of text on a new line) or a `.csv` file (using the first column for text). The app supplies a summary of the outcomes in a table and visualizes the sentiment allocation with a pie chart.
* ⚖️ Comparative Analysis: Instantly compare the sentiments of two separate pieces of text. The results are shown with individual descriptions and a comparative bar chart.
* 🤖 AI-Driven Explanations: For every analysis, the app supplies a one-sentence explanation for the given sentiment, presenting deeper insight into the category.
* 📈 Data Visualization: Interactive charts from [Plotly](https://plotly.com/) are developed to assist in visualizing the sentiment allocation in your data.

🛠️ Setup and Installation

To get this application operating on your local machine, follow these actions.

1. Clone the Repository**

First, clone this repository to your local machine using git:

```bash
git clone [https://github.com/your-username/sentiment-analysis-app.git](https://github.com/your-username/sentiment-analysis-app.git)
cd sentiment-analysis-app

2. Create a Virtual Environment

It is highly advised to build a virtual environment to manage the project's dependencies.
Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies

Install all the required Python packages using the 
requirements.txt file. 


Bash

pip install -r requirements.txt

4. Set Up Environment Variables

This application requires an API key from OpenRouter to function.
Create a file named .env in the root directory of the project.
Add your API key to this file as follows:
OPENROUTER_API_KEY="your_openrouter_api_key_here"

5. Run the Application

With the setup complete, you can now launch the Gradio web application.
Bash

python SentimentAnalyser.py
The application will attempt to launch on port 7860 and will try other ports if it is in use. You can access the web app by navigating to the local URL provided in the terminal (e.g., http://localhost:7860).

🚀 How to Use

For Manual Analysis:
Navigate to the Manual Input tab.
Enter the text you want to analyze in the textbox.
Click the "Analyze Sentiment" button to see the result and explanation.
For File Analysis:
Navigate to the File Upload tab.
Upload your .txt or .csv file. For sample data, you can use the included data. 
sentiments.txt file. 


Click the "Process File" button. The results will be displayed in a table, along with a pie chart showing the sentiment distribution.
For Comparative Analysis:
Navigate to the Comparative Analysis tab.
Enter the two pieces of text you wish to compare in their respective textboxes.
Click the "Compare Sentiments" button to view the sentiment classifications, explanations, and a comparison chart.

📦 Dependencies

This project relies on the following Python libraries:
gradio 
pandas 
plotly 
requests 
python-dotenv 
numpy 
python-multipart 

All dependencies are listed in the 
requirements.txt file. 
