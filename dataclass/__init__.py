import pickle
import utlis
import json


def str_to_tuple(title_str: str, fussy_method:str = None, ) ->tuple:
    if title_str is None:
        return None
    title = tuple(utlis.preprocess(title_str, fussy_method=fussy_method))
    return title

class dataclass:
    def __init__(self, fussy_method=None) -> None:
        """
        Dataset
        """
        self.fussy_method = fussy_method
        with open("data/data.pkl","rb") as f:
            data = pickle.load(f)
            f.close()
        self.data = data
        
        self.d_title_to_paperid = {}
        """title: tuple -> paperid: str
        """
        
        self.d_paperid_to_paper = {}
        """paperid: str -> tilte: tuple
        """
        
        self.d_cites = {}
        """paper id: str -> cited paper id: str
        """
        
        self.d_cited_by = {}
        """cited paper id: str -> paper id: str
        """
        
        for paper in data:
            paper_id = paper["paper_id"]
            self.d_paperid_to_paper[paper_id] = paper
            self.d_cited_by[paper_id] = []
        
        for paper in data:
            title = paper["metadata"]["title"]
            title = str_to_tuple(title, fussy_method=self.fussy_method)
            self.d_title_to_paperid[title] = paper["paper_id"]
            
        for paper in data:
            paper_id = paper["paper_id"]
            bib = paper["bib_entries"]
            cite_list = []
            for bib_key in bib:
                cited_paper = bib[bib_key]
                cited_title = str_to_tuple(cited_paper["title"], self.fussy_method)
                cited_id = self.title_to_id(cited_title)
                if cited_id is None:
                    # print(cited_title," not found")
                    continue
                cite_list.append(cited_id)
                self.d_cited_by[cited_id].append(paper_id)
            self.d_cites[paper_id] = cite_list
        
    def id_to_title(self, p_id:str) -> tuple:
        if p_id is None:
            return None
        paper = self.d_paperid_to_paper.get(p_id)
        if paper is None:
            return None
        return str_to_tuple(paper["metadata"]["title"], self.fussy_method)
    
    def title_to_id(self, title: tuple) -> str:
        if title is None:
            return None
        ret = self.d_title_to_paperid.get(title)
        return ret
    
    
        
