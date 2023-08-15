from transformers import pipeline
from rouge_score import rouge_scorer

# Load the summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Example input texts
input_texts = [
    "Rail workers’ union says 20,000 members from 14 firms will strike on 26 August and 2 September Members of the biggest rail workers’ union are to stage fresh strikes in a long-running dispute over pay, jobs and conditions.The Rail, Maritime and Transport workers’ union (RMT) said 20,000 of its members from 14 train operators would walk out on 26 August and 2 September, both Saturdays.",
    "Another British police force has experienced a huge breach of the data of all its officers and staff, the Guardian has learned.Cumbria police has admitted accidentally publishing the names and salaries of every one of its more than 2,000 employees and has apologised.One officer told the Guardian of dismay in the force at the leak.",
    "Chancellor’s younger brother was diagnosed with sarcoma three years ago The younger brother of the chancellor, Jeremy Hunt, has died aged 53 after being diagnosed with cancer three years ago. Charlie Hunt discovered he had sarcoma, an aggressive and rare type of cancer that typically begins in the bones or soft tissue, in 2020.",
    "Detectives say people sought over suspected murder of 10-year-old girl in Surrey have probably left UK An international search has been launched after detectives said they believed three people sought over the suspected murder of a 10-year-old girl in Surrey had left the UK. A murder investigation, led by the Surrey and Sussex major crime team, was opened on Thursday after the child’s body was found at a house in the village of Horsell, near Woking.",
    "Hollywood star had come to see an exhibition featuring 17 images of his face, but found the door locked The owner of an art gallery featuring an exhibition dedicated to Hollywood star Pedro Pascal said she was “mortified” the gallery was closed when the actor turned up for a visit. Jessica Rhodes Robb, who owns and runs the venue with her partner, Gavin Blake, was bemused to discover Pascal, 48, had turned up to the Rhodes Gallery in Margate on Sunday to find the door closed."
    "The owner of X Corp and the chief executive of Facebook-owner Meta first raised the idea of a one-on-one scrap in a series of social media posts back in June. The challenge came as Zuckerberg prepared to launch Threads, a rival microblogging site to Musk’s now rebranded Twitter platform.",
    "Ukrainian president describes taking of cash from people who want to avoid conscription as form of treachery Volodymyr Zelenskiy has announced the dismissal of all the heads of Ukraine’s regional military recruitment centres in the latest drive to root out corruption after officials were accused of taking bribes from those seeking to avoid the frontlines. At a time when the country’s army is in need of new recruits, Ukraine’s president described the taking of cash from people who wanted to avoid conscription while others suffered as a form of treachery.",
    "The $369bn Inflation Reduction Act has boosted clean energy and EV cars, but the politics remain difficult The US’ first serious legislative attempt to tackle the climate crisis, the Inflation Reduction Act, is hitting its first anniversary both lauded for turbocharging a seismic shift to clean energy while also weathering serious attack from Republicans.Joe Biden hailed the bill, which despite its name is at heart a major shove towards a future dominated by renewable energy and electric vehicles, as “one of the most significant laws in our history” when signing it on 16 August last year.",
    "In this episode from March 2023, Ian Sample hears from Scotland’s Astronomer Royal, Prof Catherine Heymans, about her experience of long Covid and how it has affected her life. He also speaks to Prof Danny Altmann, an immunologist at Imperial College London, about the scientific understanding of the condition, and whether we’re any closer to a treatment",
    "A huge fire has reportedly broken out at a warehouse just four miles away from Vladimir Putin’s official residence.",
    "The fire that tore across Lahaina in Maui caught many by surprise, claiming dozens of lives and burning more than 1,000 buildings. Aerial photographs reveal the extent of the damage."
    # Add more input texts
]

# Example reference summaries
reference_summaries = [
    "The Rail, Maritime and Transport workers’ union (RMT) said 20,000 of its members from 14 train operators would walk out on 26 August and 2 September, both Saturdays. The strike is part of a long-running dispute over pay, jobs and conditions.",
    "Cumbria police has admitted accidentally publishing names and salaries of every one of its more than 2,000 employees. It follows scandal over leak of data of all officers and staff, Guardian has learned.",
    "Charlie Hunt discovered he had sarcoma, an aggressive and rare type of cancer that typically begins in the bones or soft tissue, in 2020. Chancellor’s younger brother was diagnosed with the cancer three years ago. Charlie Hunt, 53, has died aged 53 after being diagnosed with cancer.",
    "Detectives say people sought over suspected murder of 10-year-old girl in Surrey have probably left UK. Child’s body was found at a house in the village of Horsell, near Woking, Surrey. Detectives said they believed three people sought have left the UK.",
    "Hollywood star had come to see exhibition featuring 17 images of his face. Jessica Rhodes Robb said she was the gallery was closed when the actor turned up for a visit. She was bemused to discover Pascal, 48, had turned up to the Rhodes Gallery in Margate.",
    "X owner in talks with government over historic site for event – though Colosseum and Rome ruled out. The owner of X Corp and the chief executive of Facebook-owner Meta first raised the idea of a one-on-one scrap in June. The challenge came as Zuckerberg prepared to launch Threads, a rival microblogging site to Musk’s now rebranded Twitter platform.",
    "An open letter signed by more than 50 authors calls for Baillie Gifford to be dropped as main sponsor for 2024. Authors include Zadie Smith, Ali Smith and Katherine Rundell. Company has up to £5bn invested in corporations that profit from fossil fuels.",
    "Ukrainian president describes taking of cash from people who want to avoid conscription as form of treachery. Volodymyr Zelenskiy has announced the dismissal of all the heads of Ukraine’s regional military recruitment centres. Officials were accused of taking bribes from those seeking to avoid the frontlines.",
    "The $369bn Inflation Reduction Act has boosted clean energy and EV cars. Joe Biden hailed the bill as ‘one of the most significant laws in our history’ when signing it on 16 August last year. The bill is both lauded for turbocharging a seismic shift to clean energy while also weathering attack from Republicans.",
    "Ian Sample hears from Scotland’s Astronomer Royal, Prof Catherine Heymans, about her experience of long Covid and how it has affected her life. He also speaks to Prof Danny Altmann, an immunologist at Imperial College London, about the scientific understanding of the condition.",
    "A huge fire has reportedly broken out at a warehouse just four miles away from Vladimir Putin’s official residence. The warehouse is located four miles from the Russian president''s official residence in Moscow. The fire is believed to have started in a warehouse in the warehouse just outside the Kremlin compound.",  
    "Aerial photographs reveal the extent of the fire that tore across Lahaina in Maui. The fire claimed dozens of lives and burned more than 1,000 buildings in Lahaina. Aerial photos reveal the damage caused by the fire, which left dozens dead and injured more than 100 people."
    # Add more reference summaries
]

# Generate model summaries
model_summaries = []
for input_text in input_texts:
    summary = summarizer(input_text, max_length=150, min_length=50, do_sample=False)
    model_summaries.append(summary[0]['summary_text'])

# Calculate ROUGE scores
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
average_rouge1 = 0
average_rouge2 = 0
average_rougeL = 0

for model_summary, reference_summary in zip(model_summaries, reference_summaries):
    scores = scorer.score(reference_summary, model_summary)
    average_rouge1 += scores['rouge1'].fmeasure
    average_rouge2 += scores['rouge2'].fmeasure
    average_rougeL += scores['rougeL'].fmeasure

num_samples = len(input_texts)
average_rouge1 /= num_samples
average_rouge2 /= num_samples
average_rougeL /= num_samples

# Print average ROUGE scores
print("Average ROUGE-1:", average_rouge1)
print("Average ROUGE-2:", average_rouge2)
print("Average ROUGE-L:", average_rougeL)
