# To do:
# TF-iDF para solo una palabra (?).

import math

class Document:
    def __init__(self, doc, freq) -> None:
        self.doc = doc
        self.freq = freq

class PostingList:
    def __init__(self) -> None:
        self.docs = dict()

    def add_doc(self, doc, freq):
        self.docs[doc] = freq

    def __str__(self):
        str_to_print = " ".join(f"{key} {value}" for key, value in self.docs.items())
        return str_to_print
    
    def get_keys(self):
        return self.docs.keys()
    
    def get_freqs(self):
        return self.docs.values()
    
    def get_full_index_sorted(self):
        return sorted(self.docs.items(), key=lambda item: item[1], reverse=True)

class InvertedList:
    def __init__(self) -> None:
        self.index = dict()
        self.doclen = list()

    def load_index(self, path: str):
        try:
            with open(path, 'r') as f:
                line = f.readline()
                while line:
                    current_post = PostingList()
                    if len(line) > 2:
                        elems = line.split()
                        word = elems[0]
                        count_docs = elems[1]
                        print(f"Loading word {word} in {count_docs} documents.")
                        pares = list(zip(elems[2::2], elems[3::2]))
                        for par in pares:
                            current_post.add_doc(par[0], par[1])
                        self.index[word] = current_post
                    line = f.readline()
        except Exception as e:
            print(f"Error al leer el archivo {path}: {e}")


    def load_doclen(self, path: str):
        try:
            with open(path, 'r') as f:
                line = f.readline()
                while line:
                    self.doclen.append(int(line))
                    line = f.readline()
                print(self.doclen)
        except Exception as e:
            print(f"Error al leer el archivo {path}: {e}")

    def __str__(self):
        str_to_print = "\n".join(f"{key} {value}" for key, value in self.index.items())
        return str_to_print
    
    def find(self, word):
        try:
            return self.index[word] 
        except KeyError:
            print(f"The word '{word}' does not exist in the index.")
            return PostingList()        # Retorna lista vacia.
    
    def query_or(self, intersection_list: PostingList, word: str):
        try:
            if intersection_list is not None:
                if self.index.get(word) is not None:
                    return self.intersection(intersection_list, self.index[word])
                else:
                    return intersection_list
            else:
                if self.index.get(word) is not None:
                    return self.index[word]
                else:
                    return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def calculate_tfidf(self, freq1, freq2, N1, N2, dfreq1, dfreq2, Ndocs):
        if N1 == 0 or dfreq1 == 0:
            tfidf1 = 0.0
        else:
            tfidf1 = self.calculate_tfidf_single(freq1, N1, dfreq1, Ndocs)

        if N2 == 0 or dfreq2 == 0:
            tfidf2 = 0.0
        else:
            tfidf2 = self.calculate_tfidf_single(freq2, N2, dfreq2, Ndocs)

        return tfidf1 + tfidf2

    def intersection(self, list1: PostingList, list2: PostingList):
        keys1 = list(list1.get_keys())
        keys2 = list(list2.get_keys())

        freqs1 = list(list1.get_freqs())
        freqs2 = list(list2.get_freqs())

        idx1 = 0
        idx2 = 0

        final_list = list()
        final_freqs = list()

        while(idx1 < len(keys1) and idx2 < len(keys2)):
            if keys1[idx1] == keys2[idx2]:
                final_list.append(keys1[idx1])
                final_freqs.append(self.calculate_tfidf(int(freqs1[idx1]), int(freqs2[idx2]), self.doclen[int(keys1[idx1])], self.doclen[int(keys2[idx2])], len(keys1), len(keys2), len(self.doclen)))
                final_list.append(keys1[idx1])
                idx1 += 1
                idx2 += 1
            elif keys1[idx1] < keys2[idx2]:
                idx1 += 1
            elif keys1[idx1] > keys2[idx2]:
                idx2 += 1
            else:
                raise("the impossible happens")
            
        current_post = PostingList()
        for doc, freq in zip(final_list, final_freqs):
            current_post.add_doc(doc, freq)
            
        return current_post
    

    def calculate_tfidf_single(self, freq, N, dfreq, Ndocs):
        if N == 0 or dfreq == 0:
            return 0.0
        tfidf = (freq / N) * (math.log(Ndocs / dfreq))
        return tfidf
