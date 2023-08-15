from xmltodict import parse as xml_parse
from requests import get
from sentence_transformers import SentenceTransformer, util
from cleantext import clean
import nltk
from transformers import *
logging.set_verbosity_error()
import heapq
from datetime import datetime
import os
import sites

from sites import urls, title_summarise
from sites import your_webite_Name, your_webite_url, use_paraphrase

nltk.download('punkt')
nltk.download('stopwords')

file_path = str(os.path.abspath(__file__)).split("/")
generated_path = "generated/"
if len(file_path) == 1:
    file_path = str(os.path.abspath(__file__)).split("\\")
    generated_path = "generated\\"
    
current_search_value = None
final_dict = {}
new_news_bank = []


def cleanup(word):
    word = word.replace("&rsquo;", "'")
    word = word.replace("&quot;", "'") 
    word = word.replace("&ldquo;", "") 
    word = word.replace(",&rdquo;", "")
    word = word.replace(r"\n", "")
    word = word.replace("\\", "")
    word = clean(word,
      fix_unicode=True,               # fix various unicode errors
      to_ascii=True,                  # transliterate to closest ASCII representation
      lower=False,                     # lowercase text
      no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
      no_urls=False,                  # replace all URLs with a special token
      no_emails=False,                # replace all email addresses with a special token
      no_phone_numbers=False,         # replace all phone numbers with a special token
      no_numbers=False,               # replace all numbers with a special token
      no_digits=False,                # replace all digits with a special token
      no_currency_symbols=False,      # replace all currency symbols with a special token
      no_punct=False,                 # remove punctuations
      lang="en"                       # set to 'de' for German special handling
    )
    return word

def get_news():
    news = []
    for url in urls:
        try:
            req = get(url)
            for list_data in xml_parse(req.text)["rss"]["channel"]["item"]:
                news.append(cleanup(list_data["title"]) + ". " + cleanup(list_data["description"]))
        except Exception as e:
            print(f"An error occurred with URL {url}: {str(e)}")
            continue
    return news

def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=5, num_beams=5):
    inputs = tokenizer([sentence], truncation=True, padding="do_not_pad", return_tensors="pt")
    outputs = model.generate(
      **inputs,
      num_beams=num_beams,
      num_return_sequences=num_return_sequences,
    )

    return tokenizer.batch_decode(outputs, skip_special_tokens=True)

def filter_func(letter):
  if float(util.pytorch_cos_sim(letter[1], current_search_value[1])[0][0]) >= 0.6 :
    try:
      final_dict[current_search_value[0]].append(letter)
    except:
      final_dict[current_search_value[0]] = [ ]
      final_dict[current_search_value[0]].append(letter)
    return False
  else:
    return True
  
def recursive_provider(mylist):
    if len(mylist) > 0 :
        global current_search_value
        current_search_value = mylist[0]
        my_list = list(filter(filter_func, mylist) )
        recursive_provider(my_list)

def dated_html_generator(list_data):

    with open(f"{os.getcwd()}/{generated_path}{str(datetime.now()).split(':')[0]}.php", "w") as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html>\n')
        file.write('<head>\n')
        file.write(f'<title>News feeds</title>\n')
        # file.write(f'<link rel="icon" href="https://s.abcnews.com/images/site/abcnews_google_rss_logo.png" />\n')
        file.write('<style>.item {max-width: 800px; margin: 0 auto; border-bottom: 1px solid; } .sidebar { position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; } .sidebar a {color: #000; text-decoration: none; } .sidebar {position: fixed; width: 200px; height: 100%; overflow: auto; padding: 0.5em; border-right: 1px solid #000; } body { padding: 0; margin: 0; } .sidebar p {margin: 0; padding: 15px 0; } body > div > a { max-width: 800px; margin: 0 auto; display: block; padding-top: 20px; }</style>')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('<?php\n')
        file.write('$php_files = glob("*.php");\n')
        file.write('?>\n')
        file.write('<div class="sidebar">\n')
        file.write('<h3>Dates</h3>\n')
        file.write('<?php\n')
        file.write('foreach ($php_files as $php_file) {\n')
        file.write('    $link_name = substr($php_file, 0, -4);\n')
        file.write('    echo "<p><a href=\'$php_file\'>$link_name</a></p>";\n')
        file.write('}\n')
        file.write('?>\n')
        file.write('</div>\n')  # Close sidebar div
        file.write('<div style="margin-left: 210px;">\n')  # Add margin to main content to prevent overlap with sidebar
        # file.write(f'<h1>{your_website_Name}</h1>\n')
        #file.write(f'<a href="{sites.your_website_url}">Visit our Website</a>\n')
        for data in list_data:
            file.write('<div class="item">\n')
            file.write(f'<h2>{data["title"]}</h2>\n')
            file.write(f'<p>{data["description"]}</p>\n')
            file.write(f'<small>Published on: {datetime.now().strftime("%a, %d %b %Y, %H:%M:%S-%f")}</small>\n')
            file.write(f'<p>Category: {"US"}</p>\n')
            file.write('</div>\n')
        file.write('</div>\n')  # Close main content div
        file.write('</body>\n')
        file.write('</html>')
    print(f"{str(datetime.now()).split('.')[0]}.php generated")



def main():
    news = get_news()
    print(f"{len(news)} news feed collected")

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    news_token = [ model.encode(single, convert_to_tensor=True) for single in news ]

    words_and_token = list(zip(news, news_token))


    if use_paraphrase:
        PARmodel = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
        PARtokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")

    PEGmodel = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    PEGtokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
    recursive_provider(words_and_token)
    for key in list(final_dict.keys()):
        doc = ""
        for text in final_dict[key]:
            doc += text[0]
        new_news_bank.append(doc)
    print(f"{len(new_news_bank)} unique news feed filtered")

    # 
    stopwords = nltk.corpus.stopwords.words("english")
    print('defined stopwords')
    final_data = []
    i = 0
    for newsfeed in new_news_bank :
    
        print('## Processing new feed #' + str(i) + " ##")
        i += 1
        
        word_frequencies = {}
        sentence_list = nltk.sent_tokenize(newsfeed)
        for word in nltk.word_tokenize(newsfeed):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else :
                    word_frequencies[word] += 1
        maximum_frequency = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/ maximum_frequency )
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(" ")) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else :
                            sentence_scores[sent] += word_frequencies[word]
        summary_sentences = heapq.nlargest(2, sentence_scores, key=sentence_scores.get)
        title = summary_sentences
        title_sentences = summary_sentences
      
        if len(summary_sentences) >  1:
            a1= model.encode(summary_sentences[0], convert_to_tensor=True)
            a2= model.encode(summary_sentences[1], convert_to_tensor=True)
            if float(util.pytorch_cos_sim(a1, a2)[0][0]) >= 0.85:
                if len(summary_sentences[0]) > len(summary_sentences[1]):
                    title_sentences = [summary_sentences[1]]
                    summary_sentences = [summary_sentences[0]]
                else:
                    title_sentences = [summary_sentences[0]]
                    summary_sentences = [summary_sentences[1]]
                
        summary = " ".join(list(summary_sentences))
        if use_paraphrase:
            summary = get_paraphrased_sentences(PARmodel, PARtokenizer, summary , num_beams=1, num_return_sequences=1)[0]
        if title_summarise:
            title = get_paraphrased_sentences(PEGmodel, PEGtokenizer,title_sentences[0]  , num_beams=1, num_return_sequences=1)  
        final_data.append({
            "title" : title[0],
            "description" : summary
        })
       


    print('Start generation of HTML file')
    dated_html_generator(final_data)
    print('HTML file generated')



if __name__ == "__main__":
    main()