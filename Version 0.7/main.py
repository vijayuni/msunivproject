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
            published = entry.published if hasattr(entry, 'published') else ''  # Get the publishing date
            if description:  # Only append if there's a description
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


def paraphrase_text(input_text):
    model = BartForConditionalGeneration.from_pretrained('eugenesiow/bart-paraphrase')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    tokenizer = BartTokenizer.from_pretrained('eugenesiow/bart-paraphrase')
    batch = tokenizer(input_text, return_tensors='pt')
    generated_ids = model.generate(batch['input_ids'])
    paraphrased_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    return paraphrased_text


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
        description_summary = summarizer(all_descriptions, do_sample=False)

        entries[idx]['title'] = title_paraphrased[0]
        entries[idx]['description'] = re.sub(r'\s+\.', '.', description_summary[0]['summary_text'])


    return entries, groups





def paraphrase_and_summarize_ungrouped(entries, grouped_indices):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    for idx, entry in enumerate(entries):
        if idx not in grouped_indices:
            print('=== Working on: ' + entry['title'] + ' ===')

            title_paraphrased = paraphrase_text(entry['title'])
            description_summary = summarizer(entry['description'], do_sample=False)

            entry['title'] = title_paraphrased[0]
            entry['description'] = re.sub(r'\s+\.', '.', description_summary[0]['summary_text'])
    return entries



def generate_html(entries, groups, grouped_indices):
    html = ""
    for idx, similar_idxs in groups.items():
        html += "<div class='item'>"
        html += f'<h2><a href="{entries[idx]["url"]}" target="_blank">{entries[idx]["title"]}</a></h2>'
        html += f'<div class="description">{entries[idx]["description"]}</div><br>'
        html += f'<span class="date"><strong>Published on:</strong> {entries[idx]["published"]}</span><br>'
        html += '<div class="similar">'
        html += '<span>For more reading on this topic:</span><br>'
        for similar_idx in similar_idxs:
            html += f'<a href="{entries[similar_idx]["url"]}" target="_blank">{entries[similar_idx]["title"]}</a><br>'
        html += '</div>'
        html += "</div>"
        html += "<hr>"
        
    for idx, entry in enumerate(entries):
        if idx not in grouped_indices:
            html += "<div class='item'>"
            html += f'<h2><a href="{entry["url"]}" target="_blank">{entry["title"]}</a></h2>'
            html += f'<div class="description">{entry["description"]}</div><br>'
            html += f'<span class="date"><strong>Published on:</strong> {entry["published"]}</span><br>'
            html += "</div>"
            html += "<hr>"
    return html

def get_path_generated_folder():
    file_path = str(os.path.abspath(__file__)).split("/")
    generated_path = "generated/"
    if len(file_path) == 1:
        file_path = str(os.path.abspath(__file__)).split("\\")
        generated_path = "generated\\"

    return generated_path

def main():
    feeds = get_feeds_from_excel('news_sites.xlsx')
    entries = get_feed_entries(feeds)
    groups, grouped_indices = group_similar(entries)
    entries, groups = paraphrase_and_summarize_groups(entries, groups)
    entries = paraphrase_and_summarize_ungrouped(entries, grouped_indices)
    html_news_items = generate_html(entries, groups, grouped_indices)
    from template import php_template

    with open(f"{os.getcwd()}/{get_path_generated_folder()}{str(datetime.now()).split(':')[0]}.php", "w") as f:
        f.write(php_template.replace("[news_items]", html_news_items))

def scheduled_job():
    if __name__ == '__main__':
        main()

schedule.every(24).hours.do(scheduled_job)

while True:
    schedule.run_pending()
    time.sleep(1)