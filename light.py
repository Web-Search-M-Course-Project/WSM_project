from curses import newwin
from time import time
import numpy as np
import os, sys, json, pickle
import tfidf_score
import collections

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
from utils import preprocess

def normalize(title, fussy_method="stem"):
    title = list(preprocess(title, fussy_method=fussy_method))
    return " ".join(title)

def cal_2_norm(s: list):
    term_count = collections.Counter(s)
    ans = np.linalg.norm(np.array(list(term_count.values()),dtype = np.float64))
    return ans
    
class dataset:
    def __init__(self, fussy_method='stem'):
        self.fussy_method = fussy_method    

        self.term_to_id = self.load_pickle(f"./data/light/term_to_id_whole_{self.fussy_method}")
        self.title_to_id = self.load_pickle(f"./data/light/title_to_id_{self.fussy_method}")
        self.short_id_to_id = self.load_pickle(f"./data/light/short_id_to_id_{self.fussy_method}")
        self.id_to_info = self.load_pickle(f"./data/light/id_to_info_{self.fussy_method}")

        self.cited_by = self.load_pickle(f"./data/light/cited_by_{self.fussy_method}")
        self.to_cite = self.load_pickle(f"./data/light/to_cite_{self.fussy_method}")
        self.pagerank = self.load_pickle(f"./data/light/pagerank_{self.fussy_method}")
        

    def query_to_list(self, q_str):
        ans = []
        terms = preprocess(q_str, self.fussy_method)
        for term in terms:
            if term in self.term_to_id:
                ans += self.term_to_id[term]
        ans = list(set(ans))
        return ans, terms
    
    def __path_changer(self, path):
        new_path = './data_all' + path[10:]
        return new_path


    # def sort_uid(self, uids, list_filepath, query, method='mix'):
    def cal_score(self, results_all, query, method='mix'):

        list_filepath = [self.__path_changer(res['filename']) for res in results_all ]
        query = preprocess(query, self.fussy_method)

        if method == 'tfidf':
            scores = self.list_of_tf_idf(list_filepath, query, scorer=tfidf_score.tfidf())
        elif method =='cos-tf':
            scores = self.list_of_cosine_tf_idf(list_filepath, query, scorer=tfidf_score.tfidf())
        elif method == 'norm1':
            scores = self.list_of_cosine_norm1(list_filepath, query, scorer=tfidf_score.cosine())
        elif method == 'citation':
            scores = self.list_of_citations(list_filepath)
        elif method == 'pagerank':
            scores = self.list_of_pagerank(list_filepath)
        else: # mix
            pg_rank = self.list_of_pagerank(list_filepath)
            citation = self.list_of_citations(list_filepath)
            tf_idf = self.list_of_tf_idf(list_filepath, query, scorer=tfidf_score.tfidf())
            cos_tf = self.list_of_cosine_tf_idf(list_filepath, query, scorer=tfidf_score.tfidf())

            scores = np.array([cos_tf,citation,pg_rank,tf_idf],
                dtype = np.float64)
            scores = scores - np.mean(scores, axis = 1, keepdims = True)
            scores = scores / np.sqrt(np.var(scores, axis = 1, keepdims = True)) * np.array([10.0, 1.0, 1.0, 1.0]).reshape((-1,1))
            scores = list(scores.mean(axis = 0))
        
        for idx in range(len(results_all)):
            results_all[idx]['score'] = scores[idx]
       
        sorted_results = list(reversed(sorted(results_all, key=lambda x: x['score'])))
        
        # res_with_score = {} # uid: score
        # for uid, score in zip(uids, scores):
        #     if uid not in res_with_score or res_with_score[uid] < score :
        #         res_with_score[uid] = score
        # res = [(score, uid) for uid, score in res_with_score.items()]

        # return list(reversed(sorted(res)))
        return sorted_results
    

    def list_of_tf_idf(self, l_id:list, query: list, scorer: tfidf_score.tfidf_base = tfidf_score.tfidf()) -> list:
        """
        Args:
            l_id (list): _description_ \n
            query (list): _description_ \n
            scorer (tfidf_score.tfidf_base, optional): _description_. Defaults to tfidf_score.tfidf(). \n

        Returns:
            list: list of scores \n
            `dict( zip (list_of_paper_id, list_of_scores) )` might be helpful \n
        """
        query = list(set(query))
        score = []
        for paper_id in l_id:
            if paper_id not in self.id_to_info: 
                # score.append(0)
                assert False
                continue
            # title = self.id_to_info[paper_id][]
            q_score = 0.
            # print("title:["+self.id_to_info[paper_id]["title"]+"]: "+self.id_to_info[paper_id]["paper_id"][1])
            for __q_word__ in query:
                if __q_word__ not in self.term_to_id:
                    continue
                inv_ind = self.term_to_id[__q_word__]
                doc_freq = len(inv_ind)
                term_freq = 0
                num_paper = len(self.id_to_info)
                if paper_id not in inv_ind:
                    term_freq = 0
                else:
                    term_freq = inv_ind[paper_id]
                param = {
                        "tf" : term_freq,
                        "df" : doc_freq,
                        "N"  : num_paper,
                }
                w_score = scorer(param)
                # if paper_id=="./data_all/comm_use_subset/pdf_json/53889c98bb5e342ae879f4e67c3b4c6368389716.json": 
                #     print(json.dumps(param,indent=4))
                #     print(w_score)
                q_score = q_score + w_score
            score.append(q_score)    
        return score


    def list_of_cosine_tf_idf(self, l_id:list, query:list, scorer: tfidf_score.tfidf_base = tfidf_score.tfidf()) -> list:
        """
        Args:
            l_id (list): _description_ \n
            query (list): _description_ \n
            scorer (tfidf_score.tfidf_base, optional): _description_. Defaults to tfidf_score.tfidf(). \n

        Returns:
            list: list of scores \n
            `dict( zip (list_of_paper_id, list_of_scores) )` might be helpful \n
        """
        term_count = collections.Counter(query)
        query_tfidf = []
        sorted_term_count = list(sorted(term_count))
        for term in sorted_term_count:
            if term not in self.term_to_id:
                continue
            param = {
                "tf" : term_count[term],            # term freq
                "N" : len(self.id_to_info),         # num paper
                "df" : len(self.term_to_id[term]),  # doc freq
            }
            tmp = scorer(param)
            query_tfidf.append(tmp)

        # print(time())
        doc_tfidf = []
        score = []
        for paper_id in l_id:
            if paper_id not in self.id_to_info: 
                assert False
                continue
            q_score = 0.
            paper_tfidf = []
            for __q_word__ in sorted_term_count:
                if __q_word__ not in self.term_to_id:
                    continue
                inv_ind = self.term_to_id[__q_word__]
                doc_freq = len(inv_ind)
                term_freq = 0
                num_paper = len(self.id_to_info)
                if paper_id not in inv_ind:
                    term_freq = 0
                else:
                    term_freq = inv_ind[paper_id]
                param = {
                        "tf" : term_freq,
                        "df" : doc_freq,
                        "N"  : num_paper,
                }
                # print(json.dumps(param,indent=4))
                w_score = scorer(param)
                paper_tfidf.append(w_score)
                q_score = q_score + w_score
            # if paper_id in [
            #     "./data_all/noncomm_use_subset/pdf_json/5a0937374802cad6f72576fb6c511715aa884b18.json",
            #     "./data_all/noncomm_use_subset/pdf_json/11f3cdbb678b326042e1d0c38887a34a2177ddfe.json",
                
            # ]:
            #     print(paper_tfidf)
            doc_tfidf.append(paper_tfidf)
            score.append(q_score)
        # print(time())
        
        doc_tfidf = np.array(doc_tfidf, dtype = np.float64)
        doc_norm = np.linalg.norm(doc_tfidf,axis=1,keepdims=True)
        query_tfidf = np.array(query_tfidf, dtype = np.float64)
        query_norm = np.linalg.norm(query_tfidf)
        # print(query_norm, query_tfidf)
        ans = np.matmul( (doc_tfidf/ (doc_norm+1e-10) ), (query_tfidf/(query_norm +1e-10) ) )
        # print((doc_tfidf/doc_norm))
        # print((query_tfidf/query_norm))
        return list(ans)

    
    def list_of_cosine(self, l_id:list, query:list, scorer: tfidf_score.tfidf_base = tfidf_score.cosine()) -> list:
        score = []
        query = preprocess(query, self.fussy_method)
        len_q = cal_2_norm(query)
        for paper_id in l_id:
            if paper_id not in self.id_to_info: 
                assert False
                continue

            q_score = 0.
            # print("title:["+self.id_to_info[paper_id]["title"]+"]: "+self.id_to_info[paper_id]["paper_id"][1])
            for __q_word__ in query:
                if __q_word__ not in self.term_to_id:
                    continue
                inv_ind = self.term_to_id[__q_word__]
                doc_freq = len(inv_ind)
                term_freq = 0
                num_paper = len(self.id_to_info)
                
                
                if paper_id not in inv_ind:
                    term_freq = 0
                else:
                    term_freq = inv_ind[paper_id]
                param = {
                    "tf" : term_freq,
                    # "d_1norm" : self.id_to_info[paper_id]["abstract_len"],
                    # "q_1norm" : len(l_id),
                    "d_2norm" : self.id_to_info[paper_id]["abstract_2norm"],
                    "q_2norm" : len_q,
                }
                # print(json.dumps(param,indent=4))
                w_score = scorer(param)
                q_score = q_score + w_score
            score.append(q_score)    
        return score


    def list_of_cosine_norm1(self, l_id:list, query:list, scorer: tfidf_score.tfidf_base = tfidf_score.cosine()) -> list:
        score = []
        for paper_id in l_id:
            if paper_id not in self.id_to_info: 
                assert False
                continue

            q_score = 0.
            # len_q = cal_2_norm(self.id_to_info[paper_id]["abstract"].split(" "))
            # len_d = cal_2_norm(l_id)
            # print("title:["+self.id_to_info[paper_id]["title"]+"]: "+self.id_to_info[paper_id]["paper_id"][1])
            for __q_word__ in query:
                if __q_word__ not in self.term_to_id:
                    continue
                inv_ind = self.term_to_id[__q_word__]
                doc_freq = len(inv_ind)
                term_freq = 0
                num_paper = len(self.id_to_info)
                
                
                if paper_id not in inv_ind:
                    term_freq = 0
                else:
                    term_freq = inv_ind[paper_id]
                param = {
                    "tf" : term_freq,
                    "d_2norm" : self.id_to_info[paper_id]["abstract_len"],
                    "q_2norm" : len(query),
                    # "q_2norm" : len_q,
                    # "d_2norm" : len_d,
                }
                # print(json.dumps(param,indent=4))
                w_score = scorer(param)
                q_score = q_score + w_score
            score.append(q_score)    
        return score
    

    def zipper(self, l_paper_id:list, l_title:list, l_score:list):
        all = list(zip(l_score, l_paper_id, l_title))
        return list(reversed(sorted(all)))

    
    def zipper2(self, l_paper_id:list, l_title:list, l_score:list):
        all = list(zip(l_score, l_paper_id, l_title))
        tmp1 = {}
        for score,paper_id,title in all:
            if title not in tmp1 or tmp1[title] < (score, paper_id):
                tmp1[title] = (score, paper_id)
        tmp2 = [(tmp1[title][0],tmp1[title][1],title) for title in tmp1]
        return list(reversed(sorted(tmp2)))


    
    def list_of_id_to_name(self, l_id:list):
        return [self.id_to_info[paper_id]["title"]  for paper_id in l_id if paper_id in self.id_to_info]
    

    def list_of_citations(self, l_id:list) -> list:
        """_summary_

        Args:
            l_id (list): _description_

        Returns:
            list: _description_
        """
        ans = []
        for paper_id in l_id:
            assert paper_id in self.id_to_info
            title = self.id_to_info[paper_id]["title"]
            
            if title not in self.cited_by:
                ans.append(0)
                continue
            ans.append(len(self.cited_by[title]))
        return ans    


    def list_of_pagerank(self, l_id:list) -> list:
        """_summary_

        Args:
            l_id (list): _description_

        Returns:
            list: _description_
        """
        ans = []
        for paper_id in l_id:
            assert paper_id in self.id_to_info
            title = self.id_to_info[paper_id]["title"]
            
            if title not in self.pagerank:
                ans.append(0)
                assert False
                continue
            ans.append(self.pagerank[title])
        return ans    

    
    def __call__(self, *args, **kwds):
        pass
        
    
    def save_json(self, file_path, jsondata):
        with open(os.path.join(self.data_path,file_path+".json"),"w") as file:
            json.dump(jsondata, file, indent=4)

    def save_pickle(self, file_path, pklfile):
        with open(os.path.join(self.data_path,file_path+".pkl"),"wb") as file:
            pickle.dump(pklfile, file)

    def __load_pickle(self, file_path):
        with open(os.path.join(self.data_path,file_path+".pkl"),"rb") as file:
            return pickle.load(file)

    def load_pickle(self, file_path):
        with open(file_path+".pkl","rb") as file:
            return pickle.load(file)

    def load_json(self, file_path):
        with open(os.path.join(self.data_path,file_path+".json"),"r") as file:
            return json.load(file)
    
    
    def shortcut(self, s):
        return s.lower()[:2]