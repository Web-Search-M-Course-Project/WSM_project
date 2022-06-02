import utlis
import numpy as np

class tfidf_base(object):
    def __init__(self) -> None:
        pass
    
    def __call__(self, func_config):
        raise NotImplementedError
    
class tfidf(tfidf_base):
    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, func_config):
        pass
        if func_config["tf"] <= 0:
            w_td = 0
        else:
            w_td = 1+np.log10( func_config["tf"])
        if func_config["df"] > 0 and func_config["N"]>0 :
            idf_t = np.log10(func_config["N"]/func_config["df"])
        else:
            idf_t = 0
        return idf_t*w_td
    
class cosine(tfidf_base):
    def __init__(self) -> None:
        super().__init__()
    
    def __call__(self, func_config):
        if func_config["q_2norm"] == 0: return 0
        if func_config["d_2norm"] == 0: return 0
        return func_config["tf"]/(func_config["q_2norm"]*func_config["d_2norm"])