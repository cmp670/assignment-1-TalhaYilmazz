import re

class Ngram:

    def __init__(self):
        print("hello")

    def generate_ngrams(self, s, n):
        tokens = [token for token in s.split(" ") if token != ""]

        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [" ".join(ngram) for ngram in ngrams]

    def count_in_corpus(self, text, corpus):
        total=0
        for line in corpus:
            total += line.count(text)
        return total

    def count_corpus_word_size(self,corpus):
        length = 0
        for line in corpus:
            length += len(line.split(" "))
        return length

    def count_corpus_unique_word_size(self,corpus):
        unique_list = []
        for line in corpus:
            word_list = line.split(" ")
            for word in word_list:
                if word not in unique_list:
                    unique_list.append(word)
        return len(unique_list)

    def prob(self, sentence, corpus, n):

        if(n == 1):
            prob = 1
            sentence_unigrams = self.generate_ngrams(sentence, n=1)
            for unigram in sentence_unigrams:
                if(unigram != '\n'):
                    count = self.count_in_corpus(unigram, corpus)
                    prob_unigram = count/self.count_corpus_word_size(corpus)
                    prob *= prob_unigram
            return prob

        if (n == 2):
            prob = 1
            sentence_bigrams = self.generate_ngrams(sentence, n=2)
            for bigram_str in sentence_bigrams:
                bigram = bigram_str.split(" ")
                if ((bigram[0] != '\n') & (bigram[1] != '\n')):
                    count_bigram = self.count_in_corpus(bigram[0] + " " + bigram[1], corpus)
                    count_unigram = self.count_in_corpus(bigram[0], corpus)
                    prob_bigram = count_bigram / count_unigram
                    prob *= prob_bigram
            return prob

        if (n == 3):
            prob = 1
            sentence_trigrams = self.generate_ngrams(sentence, n=3)
            for trigram_str in sentence_trigrams:
                trigram = trigram_str.split(" ")
                if ((trigram[0] != '\n') & (trigram[1] != '\n') & (trigram[2] != '\n')):
                    count_trigram = self.count_in_corpus(trigram[0] + " " + trigram[1] + " " + trigram[2], corpus)
                    count_bigram = self.count_in_corpus(trigram[0] + " " + trigram[1], corpus)
                    prob_trigram = count_trigram / count_bigram
                    prob *= prob_trigram
            return prob

    def sprob(self, sentence, corpus, n):

        #laplace smoothing
        if (n == 1):
            prob = 1
            sentence_unigrams = self.generate_ngrams(sentence, n=1)
            for unigram in sentence_unigrams:
                if (unigram != '\n'):
                    count = self.count_in_corpus(unigram, corpus)
                    prob_unigram = (count + 1) / (self.count_corpus_word_size(corpus) + self.count_corpus_unique_word_size(corpus))
                    prob *= prob_unigram
            return prob

        # good turing smoothing


    def ppl(self, corpus, n):
        perplexity = 1
        for x in corpus:
            perplexity *= (1/(self.prob(x, corpus, n)))

        corpus_word_size = self.count_corpus_word_size(corpus)
        return perplexity**(1/corpus_word_size)

    def next(self):
        print()

    def linear_interpolation(self, corpus, n):
        if (n == 2):
            prob = 1

            for sentence in corpus:
                mle_prob_bigram = self.prob(sentence, corpus, 2)
                mle_prob_unigram = self.prob(sentence, corpus, 1)

                prob *= 0.5*mle_prob_bigram + 0.5*mle_prob_unigram

            return prob

        if (n == 3):
            prob = 1

            for sentence in corpus:
                mle_prob_trigram = self.prob(sentence, corpus, 3)
                mle_prob_bigram = self.prob(sentence, corpus, 2)
                mle_prob_unigram = self.prob(sentence, corpus, 1)

                prob *= mle_prob_trigram/3 + mle_prob_bigram/3 + mle_prob_unigram/3

            return prob

    def clean_prepare_file(self, corpus):
        clean_file = []
        for x in corpus:
            x = x.lower()
            x = re.sub(r'[^a-zA-Z0-9\s]', ' ', x)
            tokens = [token for token in x.split(" ") if token != ""]
            tokens = ' '.join(tokens)
            clean_file.append(tokens)
        return clean_file

def main():
    gr = Ngram()

    #read from file
    #read train
    file_train = open("C:\\Users\\Talha\\Desktop\\assignment1\\brown_train.txt", "r")
    corpus_train = file_train.readlines()
    file_train.close()

    #read dev
    file_dev = open("C:\\Users\\Talha\\Desktop\\assignment1\\brown_dev.txt", "r")
    corpus_dev = file_dev.readlines()
    file_dev.close()

    #read test
    file_test = open("C:\\Users\\Talha\\Desktop\\assignment1\\brown_test.txt", "r")
    corpus_test = file_test.readlines()
    file_test.close()

    file_simple = open("C:\\Users\\Talha\\Desktop\\assignment1\\simple.txt", "r")
    corpus_simple = file_simple.readlines()
    file_simple.close()

    clean_file = gr.clean_prepare_file(corpus_test)
    print(gr.ppl(clean_file, 1))

if __name__ == "__main__":
    main()
