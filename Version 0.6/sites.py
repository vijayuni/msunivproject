import pandas as pd

def get_sites_urls():
    excel_file = 'news_sites.xlsx'
    df = pd.read_excel(excel_file, header=None)

    urls = df.iloc[:, 0].dropna().tolist()

    return urls



urls = get_sites_urls()


your_webite_url = ""
your_webite_Name = ""


use_paraphrase = False

title_summarise = True