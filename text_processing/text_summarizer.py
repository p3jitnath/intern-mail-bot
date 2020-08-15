import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

class AbstractiveTextSummarizer():
    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained('t5-large')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-large')
        self.device = torch.device('cpu')

    def _tokenize(self, text):
        preprocess_text = text.strip().replace("\n","")
        t5_prepared_Text = "summarize: " + preprocess_text
        tokenized_text = self.tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(self.device)

        return tokenized_text
    
    def generate_summary(self, text):
        tokenized_text = self._tokenize(text)

        summary_ids = self.model.generate(tokenized_text,
                                        num_beams=8,
                                        no_repeat_ngram_size=10,
                                        min_length=75,
                                        max_length=100,
                                        early_stopping=True)

        output = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        output_sentences = output.split('. ')    
        result = []
        for sentence in output_sentences:
            sentence = sentence.capitalize()
            result.append(sentence)        
        
        return ". ".join(result)

class ExtractiveTextSummarizer():

    def __init__(self):
        self.stop_words = stopwords.words('english')
    
    def _get_sentences(self, text):
        raw_sentences = text.split('. ')
        cleaned_sentences = []
        for raw_sentence in raw_sentences:
            cleaned_sentences.append(raw_sentence.replace("[^a-zA-Z]", " ").split(" "))
        return cleaned_sentences

    def _sentence_similarity(self, sentence_1, sentence_2):
        sentence_1_lower = [w.lower() for w in sentence_1]
        sentence_2_lower = [w.lower() for w in sentence_2]
        
        all_words = list(set(sentence_1_lower + sentence_2_lower))
        
        vector_1 = [0] * len(all_words)
        vector_2 = [0] * len(all_words)
        
        for word in sentence_1_lower:
            if word in self.stop_words:
                continue
            vector_1[all_words.index(word)] += 1
        
        for word in sentence_2_lower:
            if word in self.stop_words:
                continue
            vector_2[all_words.index(word)] += 1
        
        return 1 - cosine_distance(vector_1, vector_2)
    
    def _build_similarity_matrix(self, sentences):
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:
                    continue 
                similarity_matrix[idx1][idx2] = self._sentence_similarity(sentences[idx1], sentences[idx2])
        return similarity_matrix

    def generate_summary(self, text):
        summarize_text = []
        sentences = self._get_sentences(text)
        
        top_n = int(len(sentences) * 0.5)
        
        sentence_similarity_matrix = self._build_similarity_matrix(sentences)
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        
        scores = nx.pagerank(sentence_similarity_graph)
        ranked_sentence = sorted(((scores[i], s) for i,s in enumerate(sentences)), reverse=True)    
        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        return ". ".join(summarize_text) + "."