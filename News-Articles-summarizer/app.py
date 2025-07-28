import tkinter as tk
from newspaper import Article
from textblob import TextBlob
import nltk

# Download punkt tokenizer (only once)
nltk.download('punkt')

# Function to process the article
def summarize():
    url = utext.get("1.0", "end").strip()
    if not url:
        return

    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    # Enable and insert data
    title.config(state='normal')
    title.delete("1.0", "end")
    title.insert("1.0", article.title)
    title.config(state='disabled')

    author.config(state='normal')
    author.delete("1.0", "end")
    author.insert("1.0", ", ".join(article.authors))
    author.config(state='disabled')

    publication.config(state='normal')
    publication.delete("1.0", "end")
    publication.insert("1.0", str(article.publish_date))
    publication.config(state='disabled')

    summary.config(state='normal')
    summary.delete("1.0", "end")
    summary.insert("1.0", article.summary)
    summary.config(state='disabled')

    # Sentiment Analysis
    blob = TextBlob(article.text)
    polarity = blob.sentiment.polarity

    sentiment.config(state='normal')
    sentiment.delete("1.0", "end")
    sentiment.insert("1.0", "Positive 😊" if polarity > 0 else "Negative 😞" if polarity < 0 else "Neutral 😐")
    sentiment.config(state='disabled')


# UI Setup
root = tk.Tk()
root.title("News Article Summarizer")
root.geometry("1200x700")

# Title
tk.Label(root, text="Title", font=("Arial", 14, "bold")).pack()
title = tk.Text(root, height=1, width=140)
title.config(state='disabled', bg='#dddddd')
title.pack()

# Authors
tk.Label(root, text="Authors", font=("Arial", 12)).pack()
author = tk.Text(root, height=1, width=140)
author.config(state='disabled', bg='#dddddd')
author.pack()

# Publication Date
tk.Label(root, text="Publication Date", font=("Arial", 12)).pack()
publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg='#dddddd')
publication.pack()

# Summary
tk.Label(root, text="Summary", font=("Arial", 12)).pack()
summary = tk.Text(root, height=10, width=140)
summary.config(state='disabled', bg='#dddddd')
summary.pack()

# Sentiment
tk.Label(root, text="Sentiment Analysis", font=("Arial", 12)).pack()
sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state='disabled', bg='#dddddd')
sentiment.pack()

# URL Input
tk.Label(root, text="URL", font=("Arial", 12)).pack()
utext = tk.Text(root, height=1, width=140)
utext.pack()

# Summarize Button
tk.Button(root, text="Summarize", command=summarize, bg="blue", fg="white", font=("Arial", 12, "bold")).pack()

root.mainloop()
