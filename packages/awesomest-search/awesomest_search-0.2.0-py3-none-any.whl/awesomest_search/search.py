import os
os.environ["OMP_NUM_THREADS"] = "1"
import time
import multiprocessing 
from mpire import WorkerPool
from pprint import pprint
import itertools


def fuzzy_search_perm(text):
    data = list(text)
    arr =  []
    for r in range(1, len(data) + 1):  # Generate combinations of all lengths
        comb = itertools.combinations(data, r)
        string = ""
        for c in comb:
            string="".join(c)
        arr.append(string)
    return arr
def kmp_search(text, pattern):
    # Helper function to preprocess the pattern and create the LPS array
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0  # length of the previous longest prefix suffix
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    # Preprocess the pattern
    lps = compute_lps(pattern)
    result_indices = []

    i = 0  # index for text
    j = 0  # index for pattern

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):  # Found a match
            result_indices.append(i - j)
            j = lps[j - 1]  # Reset j using the LPS array
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return result_indices

def fuzzy_search_level(search,search_term,level):

    tmp_searches = [search]
    full_matches = []
    for l in range(level):
        matches = [kmp_search(search,search_term) for search in tmp_searches]
        tmp = []
        for match in matches:
            for m in match:
                tmp.append(search[m:])
        tmp_searches=tmp
        full_matches+=tmp_searches 

    return full_matches


def fuzzy_search(search,search_terms,level):
    num_cores = multiprocessing.cpu_count() - 1
    results = [{"search":search,"search_term":search_term,"level":level} for search_term in search_terms]
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(fuzzy_search_level, results, progress_bar=True, chunk_size=1)
    return results

  
def kmp_searches(search,search_term):
    results = ""
    for s in kmp_search(search,search_term):
        results+=search[s]
    return {"full_matches":results,"search":search,"search_term":search_term}

def text_search(text,search_term):

    results = [{"search":text,"search_term":search_term[i]} for i in range(len(search_term))]
    num_cores = multiprocessing.cpu_count() - 1
    
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(kmp_searches, results, progress_bar=True, chunk_size=1)
    
    
    return results

def flatten_list(nested_list):
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened
def awesome_search(text,search_term,level=2):
    text_chunks =  []
    
    for i in range(0,len(text),8):
        text_chunks.append({"text":text[i:min(i+8,len(text))]})
    # print(text_chunks)
    num_cores = multiprocessing.cpu_count() - 1
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(fuzzy_search_perm, text_chunks, progress_bar=True, chunk_size=1)
    results = [{"search":text,"search_terms":results[i],"level":level} for i in range(len(results))]

    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(fuzzy_search, results, progress_bar=True, chunk_size=1)
        
    results = flatten_list(results)
    # pprint(results)

    results = [{"text":text,"search_term":search_term} for text in results]
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(text_search, results, progress_bar=True, chunk_size=1)
    
    
    return results


# if __name__ == "__main__":
    
#     para = "Hi my name is Prakhar!"
#     search_term = "Prakhar!"
#     level = 1 # for faster execution
#     # level = 2 # for slower execution
#     results = awesome_search(para,search_term,level)
#     pprint(results)
    