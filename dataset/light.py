from curses import newwin
from time import time
import numpy as np
import os
import utlis
import json
import pickle
from . import tfidf_score
import collections

def normalize(title, fussy_method="stem"):
    title = list(utlis.preprocess(title, fussy_method=fussy_method))
    return " ".join(title)

def cal_2_norm(s: list):
    term_count = collections.Counter(s)
    ans = np.linalg.norm(np.array(list(term_count.values()),dtype = np.float64))
    return ans
    
class dataset:
    def __init__(self) -> None:
        pass
    
    def init(
        self,
        data_path = "./data_all",
        fussy_method = "stem",
    ):
        datasubsets = [
            "comm_use_subset/pdf_json",
            "comm_use_subset/pmc_json",
            "biorxiv_medrxiv/pdf_json",
            "custom_license/pdf_json",
            "custom_license/pmc_json",
            "noncomm_use_subset/pdf_json",
            "noncomm_use_subset/pmc_json",
        ]
        self.data_path = data_path
        self.fussy_method = fussy_method
        self.datasubsets = datasubsets

        title_to_id = {}
        id_to_info = {}
        short_id_to_id = {}
        
        term_to_id = {}
        
        # self.invert_index
        for datasubset in datasubsets:        
            datasubset_path = os.path.join(data_path,datasubset)
            jsonfiles = os.listdir(datasubset_path)
            for jsonfilename in jsonfiles:
                with open(os.path.join(datasubset_path, jsonfilename),"r") as file:
                    jsondata = json.load(file)
                    jsondata["subset"] = datasubset
                    
                    # data
                    short_id = jsondata["paper_id"]
                    title = (normalize(jsondata["metadata"]["title"], fussy_method=fussy_method))
                    paper_id = os.path.join(datasubset_path, jsonfilename)

                    # short_id_to_id
                    if short_id not in short_id_to_id:
                        short_id_to_id[short_id] = []
                    short_id_to_id[short_id].append(paper_id)
                    
                    # title_to_id
                    if title not in title_to_id:
                        title_to_id[title] = []
                    title_to_id[title].append(paper_id)
                    
                    # term_to_id
                    terms = list(utlis.preprocess(jsondata["metadata"]["title"], fussy_method=fussy_method))
                    if "abstract" in jsondata:
                        for abstract_text in jsondata["abstract"]:
                            terms += list(utlis.preprocess(abstract_text["text"], fussy_method=fussy_method))
                    for term in terms:
                        if term not in term_to_id:
                            term_to_id[term] = {}
                        tmp = term_to_id[term]
                        if paper_id not in tmp:
                            term_to_id[term][paper_id] = 0
                        tmp[paper_id] += 1

                    # id_to_info
                    info = {}
                    info["paper_id"] = (short_id, paper_id)
                    info["title"] = title
                    info["authors"] = [(people["first"], people["last"]) for people in jsondata["metadata"]["authors"]]
                    info["abstract"] = " ".join(terms)
                    info["abstract_len"] = len(terms)
                    info["abstract_2norm"] = cal_2_norm(terms)
                    id_to_info[paper_id] = info
                    


                        
                    
                # break

        self.save_pickle("light/title_to_id",title_to_id)
        self.save_pickle("light/short_id_to_id",short_id_to_id)
        self.save_pickle("light/id_to_info",id_to_info)
            
        
        self.save_json("light/title_to_id",title_to_id)
        self.save_json("light/short_id_to_id",short_id_to_id)
        self.save_json("light/id_to_info",id_to_info)

        
        if False:
            term_to_id_lower = {}
            for term in term_to_id:
                term_lower = self.shortcut(term)
                if term_lower not in term_to_id_lower:
                    term_to_id_lower[term_lower] = {}
                term_to_id_lower[term_lower][term] = term_to_id[term]
            
            for term_lower in term_to_id_lower:
                self.save_json(os.path.join("light/term_to_id_lower",term_lower),term_to_id_lower[term_lower])
                self.save_pickle(os.path.join("light/term_to_id_lower",term_lower),term_to_id_lower[term_lower])

        self.save_pickle("light/term_to_id_whole",term_to_id)
        self.save_json("light/term_to_id_whole",term_to_id)

        pass
        
    def citation_init(
        self,
        data_path = "./data_all",
        fussy_method = "stem",
        
    ):
        datasubsets = [
            "comm_use_subset/pdf_json",
            "comm_use_subset/pmc_json",
            "biorxiv_medrxiv/pdf_json",
            "custom_license/pdf_json",
            "custom_license/pmc_json",
            "noncomm_use_subset/pdf_json",
            "noncomm_use_subset/pmc_json",
        ]
        self.data_path = data_path
        self.fussy_method = fussy_method
        self.datasubsets = datasubsets

        term_to_id = self.load_pickle("light/term_to_id_whole")

        title_to_id = self.load_pickle("light/title_to_id")
        short_id_to_id = self.load_pickle("light/short_id_to_id")
        id_to_info = self.load_pickle("light/id_to_info")

        cited_by = {}
        to_cite = {}
        
        for datasubset in datasubsets:        
            datasubset_path = os.path.join(data_path,datasubset)
            jsonfiles = os.listdir(datasubset_path)
            for jsonfilename in jsonfiles:
                with open(os.path.join(datasubset_path, jsonfilename),"r") as file:
                    jsondata = json.load(file)
                    jsondata["subset"] = datasubset

                    # data
                    short_id = jsondata["paper_id"]
                    title = (normalize(jsondata["metadata"]["title"], fussy_method=fussy_method))
                    paper_id = os.path.join(datasubset_path, jsonfilename)

                    # citation
                    if "bib_entries" in jsondata:
                        for bib_info in jsondata["bib_entries"]:
                            __bib_title = jsondata["bib_entries"][bib_info]["title"]
                            bib_title = normalize(__bib_title, fussy_method=fussy_method)

                            if bib_title in title_to_id and title in title_to_id:
                                if len(title_to_id[bib_title])<10 and len(title_to_id[title])<10:
                                    pass
                                    if bib_title not in cited_by:
                                        cited_by[bib_title] = []
                                    cited_by[bib_title].append(title)
                                    if title not in to_cite:
                                        to_cite[title] = []
                                    to_cite[title].append(bib_title)
                    # if title not in to_cite:
                    #     print(title,paper_id)
                # break
        
        for title in cited_by:
            cited_by[title] = list(set(cited_by[title]))
        
        for title in to_cite:
            to_cite[title] = list(set(to_cite[title]))
        
        self.save_pickle("light/cited_by",cited_by)        
        self.save_json("light/cited_by",cited_by)        
        self.save_pickle("light/to_cite",to_cite)        
        self.save_json("light/to_cite",to_cite)        
        
    def pagerank_init(
        self,
        data_path = "./data_all",
    ):
        self.data_path = data_path
        self.cited_by = self.load_pickle("light/cited_by")
        self.to_cite = self.load_pickle("light/to_cite")
        self.title_to_id = self.load_pickle("light/title_to_id")
        
        weights = {title:1. for title in self.title_to_id}
        
        prob = .25
        for i in range(100):
            new_weights = {title:0. for title in weights}
            gift = 0.
            for title in weights:
                if title in self.to_cite:
                    for cit in self.to_cite[title]:
                        new_weights[cit] += weights[title]*prob / len(self.to_cite[title])
                else:
                    gift += weights[title]*prob
                
                new_weights[title] += weights[title]*(1-prob)
                
                pass
            for title in new_weights:
                new_weights[title] += gift / len(new_weights)
            w_old = np.array(list(weights.values()))
            w_new = np.array(list(new_weights.values()))
            print(w_new.sum(), end=",\t")
            print(np.linalg.norm(w_new-w_old))
            weights = new_weights
        
        self.save_json("light/pagerank",weights)
        self.save_pickle("light/pagerank",weights)
        
        pass
    
    def load_dataset(
        self,
        data_path = "./data_all",
        fussy_method = "stem",
    ):
        datasubsets = [
            "comm_use_subset/pdf_json",
            "comm_use_subset/pmc_json",
            "biorxiv_medrxiv/pdf_json",
            "custom_license/pdf_json",
            "custom_license/pmc_json",
            "noncomm_use_subset/pdf_json",
            "noncomm_use_subset/pmc_json",
        ]
        self.data_path = data_path
        self.fussy_method = fussy_method
        self.datasubsets = datasubsets
        
        self.term_to_id = self.load_pickle("light/term_to_id_whole")

        self.title_to_id = self.load_pickle("light/title_to_id")
        self.short_id_to_id = self.load_pickle("light/short_id_to_id")
        self.id_to_info = self.load_pickle("light/id_to_info")

        self.cited_by = self.load_pickle("light/cited_by")
        self.to_cite = self.load_pickle("light/to_cite")
        
        self.pagerank = self.load_pickle("light/pagerank")
        pass  
    
    def query_to_list(self, q_str):
        ans = []
        terms = utlis.preprocess(q_str, self.fussy_method)
        for term in terms:
            if term in self.term_to_id:
                ans += self.term_to_id[term]
        ans = list(set(ans))
        return ans, terms
    
    def list_of_tf_idf(self, l_id:list, query:list, scorer: tfidf_score.tfidf_base = tfidf_score.tfidf()) -> list:
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
        ans = np.matmul( (doc_tfidf/doc_norm), (query_tfidf/query_norm) )
        # print((doc_tfidf/doc_norm))
        # print((query_tfidf/query_norm))
        return list(ans)

    
    def list_of_cosine(self, l_id:list, query:list, scorer: tfidf_score.tfidf_base = tfidf_score.cosine()) -> list:
        score = []
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
        pass
    
    def zipper2(self, l_paper_id:list, l_title:list, l_score:list):
        all = list(zip(l_score, l_paper_id, l_title))
        tmp1 = {}
        for score,paper_id,title in all:
            if title not in tmp1 or tmp1[title] < (score, paper_id):
                tmp1[title] = (score, paper_id)
        tmp2 = [(tmp1[title][0],tmp1[title][1],title) for title in tmp1]
        return list(reversed(sorted(tmp2)))
        pass

    
    
    
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

    def load_pickle(self, file_path):
        with open(os.path.join(self.data_path,file_path+".pkl"),"rb") as file:
            return pickle.load(file)

    def load_json(self, file_path):
        with open(os.path.join(self.data_path,file_path+".json"),"r") as file:
            return json.load(file)
    
    def shortcut(self, s):
        return s.lower()[:2]