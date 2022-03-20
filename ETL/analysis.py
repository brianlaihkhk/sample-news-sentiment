from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.np_extractors import ConllExtractor
import itertools
import re

regex = '[^a-zA-Z \n\.]'

class Analysis:

    def __init__(self, text, category):
        self.blob = TextBlob(text, analyzer=NaiveBayesAnalyzer(), np_extractor=ConllExtractor())
        self.category = category

    def get_sentiment(self):
        sentiment = self.blob.sentiment
        if abs(sentiment.p_pos - sentiment.p_neg) <= 0.2:
            return "neu"
        else :
            return str(sentiment.classification)

    def get_topic(self):
        merged_topic = [ phrases.split(' ') for phrases in self.blob.noun_phrases ]
        filter_topic = self.filter_topic(list(itertools.chain(*merged_topic)))
        output_topic = [ re.sub(regex, '', topic.lower()) for topic in filter_topic ]
        return set(output_topic)
        
    def filter_topic (self, merged_topic):
        print(merged_topic)
        return sorted(set([i for i in merged_topic if merged_topic.count(i) > 3]))


    def get_category(self):
        return str(self.category).lower()

    def get_tags(self):
        filter_tags = [ str(tag).lower() for tag in list(itertools.starmap(self.filter_tag, self.blob.tags)) if tag is not None ]
        output_tags = [ re.sub(regex, '', tag) for tag in filter_tags if self.blob.words.count(tag) >= 3 ]
        return set(output_tags)

    def filter_tag(self, tag, type):
        if type == 'NNP' and len(tag) > 5:
            return tag
        elif type == 'NN' and len(tag) > 5:
            return tag
        else:
            return None