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
        req = get(url)
        try :
            for list_data in xml_parse(req.text)["rss"]["channel"]["item"] :
                news.append( cleanup(list_data["title"]) + ". " + cleanup(list_data["description"]))
        except Exception as e :
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


def dated_xml_generator(list_data):
    with open(f"{os.getcwd()}\\{generated_path}{str(datetime.now()).split(':')[0]}.xml" , "w") as file:
        file.write('<rss xmlns:media="http://search.yahoo.com/mrss/" xmlns:abcnews="http://abcnews.com/content/" version="2.0">\n')
        file.write('<channel>\n')
        file.write(f"""<title>{your_webite_Name}</title>\n<link>{your_webite_url}</link>\n<description/>\n""")
        file.write(f"""<image>\n<title>{your_webite_Name}</title>\n<url>https://s.abcnews.com/images/site/abcnews_google_rss_logo.png</url>\n<link>{your_webite_url}</link>\n</image>""")
        for data in list_data:
            file.write('<item>\n')
            file.write(f'<title><![CDATA[{data["title"]}]]></title>\n')
            file.write(f'<description><![CDATA[{data["description"]}]]></description>\n')
            file.write(f'<pubDate>{datetime.now().strftime("%a, %d %b %Y, %H:%M:%S-%f")}</pubDate>\n')
            file.write(f'<category>{"US"}</category>\n')
            file.write('</item>\n')
        file.write('</channel>\n')
        file.write('</rss>')
    print(f"{str(datetime.now()).split('.')[0]}.xml  generated")

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
    
    stopwords = nltk.corpus.stopwords.words("english")
    final_data = []
    for newsfeed in new_news_bank :
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
    dated_xml_generator(final_data)



if __name__ == "__main__":
    main()