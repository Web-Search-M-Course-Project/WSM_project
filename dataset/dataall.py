import numpy as np
import json
import os
import utlis
import pickle

def normalize(title, fussy_method="stem"):
    title = list(utlis.preprocess(title, fussy_method=fussy_method))
    return "+".join(title)

def str_to_tuple(title_str: str, fussy_method:str = None, ) ->tuple:
    if title_str is None:
        return None
    title = tuple(utlis.preprocess(title_str, fussy_method=fussy_method))
    return title

class data_all(object):
    def __init__(
        self,
        data_path = "./data_all",
        fussy_method = "stem",
        
    ) -> None:
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
        
        lenN = 0
        id_to_paper = {}
        paper_list = []
        title_to_id = {}
        for datasubset in datasubsets:        
            datasubset_path = os.path.join(data_path,datasubset)
            jsonfiles = os.listdir(datasubset_path)
            lenN += len(jsonfiles)
            for jsonfilename in jsonfiles:
                with open(os.path.join(datasubset_path, jsonfilename),"r") as file:
                    jsondata = json.load(file)
                    jsondata["subset"] = datasubset
                    title = (normalize(jsondata["metadata"]["title"], fussy_method=fussy_method))
                    title_to_id[title] = (jsondata["paper_id"])
                    paper_list.append(jsondata)
                    id_to_paper[jsondata["paper_id"]] = jsondata
                    
                    # break
        
        print(lenN)
        self.save_json("paper_list",paper_list)
        self.save_json("title_to_id",title_to_id)
        self.save_json("id_to_paper",id_to_paper)
        self.save_pickle("paper_list",paper_list)
        self.save_pickle("title_to_id",title_to_id)
        self.save_pickle("id_to_paper",id_to_paper)
        # assert(str(self.load_json("id_to_paper"))==str(self.load_pickle("id_to_paper")))

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
    
    def __getitem__(
        self,
    ) -> None:
        pass

class data_cached:
    def __init__(
        self,
        data_path = "./data_all",
        fussy_method = "stem",
    ) -> None:
        """_summary_

        Args:
            data_path (str, optional): _description_. Defaults to "./data_all".
            fussy_method (str, optional): _description_. Defaults to "stem".
        """
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
        
        lenN = 0
        id_to_paper = {}
        paper_list = []
        title_to_id = {}
        # id_to_paper = self.load_pickle("id_to_paper")
        title_to_id = self.load_pickle("title_to_id")
        # paper_list = self.load_pickle("paper_list")
        
        # self.id_to_paper = id_to_paper
        self.title_to_id = title_to_id
        # self.paper_list = paper_list
        # print(len(paper_list))
        # print(len(id_to_paper))
        print(len(title_to_id))

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
    
    def __getitem__(
        self,
    ) -> None:
        pass
