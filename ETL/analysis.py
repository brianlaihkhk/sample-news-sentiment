from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.np_extractors import ConllExtractor
import itertools

class Analysis:

    def __init__(self, text, category):
        self.blob = TextBlob(text, analyzer=NaiveBayesAnalyzer(), np_extractor=ConllExtractor())
        self.category = category

    def get_sentiment(self):
        sentiment = self.blob.sentiment
        if abs(sentiment.p_pos - sentiment.p_neg) <= 0.2:
            return "neu"
        else :
            return sentiment.classification

    def get_topic(self):
        output_topic = [ topic for topic in self.blob.noun_phrases if self.filter_topic(topic) is not None ]
        return output_topic
        
    def filter_topic (self, topic):
        noun_phrase = ' '.join(topic)
        if ' ' in noun_phrase and len(noun_phrase) > 8:
            return noun_phrase
        else:
            return None

    def get_category(self):
        return self.category

    def get_tags(self):
        filter_tags = [ tag for tag in list(itertools.starmap(self.filter_tag, self.blob.tags)) if tag is not None ]
        output_tags = [ tag for tag in filter_tags if self.blob.words.count(tag) >= 3 ]
        return output_tags

    def filter_tag(self, tag, type):
        if type == 'NNP' and len(tag) > 5:
            return tag
        elif type == 'NN' and len(tag) > 5:
            return tag
        else:
            return None