import feedparser
import torch
import re
import schedule
import time
import os
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import defaultdict
from transformers import pipeline
from transformers import BartForConditionalGeneration, BartTokenizer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from bs4 import BeautifulSoup
import numpy as np
import pickle
import html



def get_feeds_from_excel(file_name):
    df = pd.read_excel(file_name)
    feeds = df.iloc[:,0].tolist()
    return feeds

def get_feed_entries(feeds):
    entries = []
    for feed in feeds:
        d = feedparser.parse(feed)
        for entry in d.entries:
            title = entry.title if hasattr(entry, 'title') else ''
            description = entry.description if hasattr(entry, 'description') else ''
            url = entry.link if hasattr(entry, 'link') else ''
            published = entry.published if hasattr(entry, 'published') else ''

            title = html.unescape(title)
            description = html.unescape(description)
            
            soup_title = BeautifulSoup(title, "html.parser")
            title = soup_title.get_text()

            soup_description = BeautifulSoup(description, "html.parser")
            description = soup_description.get_text()

            if description:
                entries.append({'title': title, 'description': description, 'url': url, 'published': published})
    return entries

def group_similar(entries, similarity_threshold=0.3):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([entry['title'] for entry in entries])
    cosine_similarities = linear_kernel(tfidf, tfidf)
    
    groups = defaultdict(list)
    grouped_indices = set()
    for idx, similarities in enumerate(cosine_similarities):
        for other_idx, score in enumerate(similarities):
            if idx != other_idx and score > similarity_threshold:
                if idx not in grouped_indices:
                    groups[idx].append(other_idx)
                    grouped_indices.add(other_idx)

    return groups, grouped_indices


def paraphrase_text(input_text, max_length=1024):
    model = BartForConditionalGeneration.from_pretrained('eugenesiow/bart-paraphrase')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    tokenizer = BartTokenizer.from_pretrained('eugenesiow/bart-paraphrase')

    tokens = tokenizer.tokenize(input_text)
    token_chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
    paraphrased_chunks = []

    for token_chunk in token_chunks:
        batch = tokenizer(token_chunk, return_tensors='pt', padding=True, truncation=True, max_length=max_length)
        generated_ids = model.generate(batch['input_ids'])
        paraphrased_chunks.extend(tokenizer.batch_decode(generated_ids, skip_special_tokens=True))

    paraphrased_text = " ".join(paraphrased_chunks)
    paraphrased_text = paraphrased_text.replace('Ġ', ' ')
    return paraphrased_text.encode('utf-8', 'ignore').decode('utf-8')



def paraphrase_and_summarize_groups(entries, groups):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    for idx, similar_idxs in groups.items():
        titles_to_summarize = [entries[idx]['title']]
        descriptions_to_summarize = [entries[idx]['description']]

        for similar_idx in similar_idxs:
            titles_to_summarize.append(entries[similar_idx]['title'])
            descriptions_to_summarize.append(entries[similar_idx]['description'])

        print('=== Working on: ' + titles_to_summarize[0] + ' ===')

        all_descriptions = ' \n'.join(descriptions_to_summarize)

        title_paraphrased = paraphrase_text(titles_to_summarize[0])
        description_summary = summarizer(all_descriptions[:1024], do_sample=False)

        entries[idx]['paraphrased_title'] = title_paraphrased
        entries[idx]['summarized_description'] = re.sub(r'\s+\.', '.', description_summary[0]['summary_text'])


    return entries, groups


def paraphrase_and_summarize_ungrouped(entries, grouped_indices):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    for idx, entry in enumerate(entries):
        if idx not in grouped_indices:
            print('=== Working on: ' + entry['title'] + ' ===')

            title_paraphrased = paraphrase_text(entry['title'])
            description_summary = summarizer(entry['description'][:1024], do_sample=False)

            entry['paraphrased_title'] = title_paraphrased
            entry['summarized_description'] = re.sub(r'\s+\.', '.', description_summary[0]['summary_text'])
    return entries


def predict_category(entries):
    
    for entry in entries:
        headline = entry['title']

        vocab_size = 5000
        max_length = 20

        model = tf.keras.models.load_model('model.h5')

        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        sequences = tokenizer.texts_to_sequences([headline])
        padded_sequences = pad_sequences(sequences, padding='post', maxlen=max_length)

        prediction = model.predict(padded_sequences)

        predicted_index = np.argmax(prediction)

        # Define the labels
        labels = {'sports': 0, 'tech': 1, 'world': 2, 'health': 3, 'entertainment': 4}

        predicted_category = [key for key, value in labels.items() if value == predicted_index][0]

        entry['predicted_category'] = predicted_category

    return entries



def generate_html(entries, groups, grouped_indices):
    html = ""
    for idx, similar_idxs in groups.items():
        html += "<div class='item'>"
        html += f'<h2><a href="{entries[idx]["url"]}" target="_blank">{entries[idx]["paraphrased_title"]}</a></h2>'
        html += f'<div class="description">{entries[idx]["summarized_description"]}</div><br>'
        html += f'<span class="date"><strong>Published on:</strong> {entries[idx]["published"]}</span><br>'
        html += f'<div class="category"><strong>Category: </strong><span class="category-text">{entries[idx]["predicted_category"]}</span></div><br>'
        html += '<div class="similar">'
        html += '<span>For more reading on this topic:</span><br>'
        for count, similar_idx in enumerate(similar_idxs, start=1):
            html += f'{count}. <a href="{entries[similar_idx]["url"]}" target="_blank">{entries[similar_idx]["title"]}</a><br>'
        html += '</div>'
        html += "</div>"
        html += "<hr>"
        
    for idx, entry in enumerate(entries):
        if idx not in grouped_indices:
            html += "<div class='item'>"
            html += f'<h2><a href="{entry["url"]}" target="_blank">{entry["paraphrased_title"]}</a></h2>'
            html += f'<div class="description">{entry["summarized_description"]}</div><br>'
            html += f'<span class="date"><strong>Published on:</strong> {entry["published"]}</span><br>'
            html += f'<div class="category"><strong>Category: </strong><span class="category-text">{entry["predicted_category"]}</span></div><br>'
            html += "</div>"
            html += "<hr>"
    return html


def get_path_generated_folder():
    file_path = str(os.path.abspath(__file__)).split("/")
    generated_path = "files/"
    if len(file_path) == 1:
        file_path = str(os.path.abspath(__file__)).split("\\")
        generated_path = "files\\"

    return generated_path


def main():
    print('====== Start ======')

    feeds = get_feeds_from_excel('news_sites.xlsx')
    print(str(len(feeds) + 1) + ' news feeds loaded')

    entries = get_feed_entries(feeds)
    print(str(len(entries) + 1) + ' news articles loaded')

    entries = predict_category(entries)
    groups, grouped_indices = group_similar(entries)
    entries, groups = paraphrase_and_summarize_groups(entries, groups)
    entries = paraphrase_and_summarize_ungrouped(entries, grouped_indices)

    html_news_items = generate_html(entries, groups, grouped_indices)
    from template import php_template

    with open(f"{os.getcwd()}/{get_path_generated_folder()}{str(datetime.now()).split(':')[0]}.php", "w", encoding='utf-8') as f:
        f.write(php_template.replace("[news_items]", html_news_items))

    print('====== Finished ======')