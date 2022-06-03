import json
from light import dataset
from search.FussySearch import FussySearch


def path_changer(path):
    # from 2020-04-03/noncomm_use_subset/pmc_json/PMC6522884.xml.json
    #  -->"./data_all/comm_use_subset/pdf_json/000b7d1517ceebb34e1e3e817695b6de03e2fa78.json" 
    new_path = './data_all' + path[10:]
    return new_path


if __name__ == '__main__':
    fussy_search = FussySearch(fussy_method='stem')
    DataSorter = dataset()

    file_path = './data/meta_data.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        meta_data = json.load(f)

    searchText = 'Strain AND Identification OR network'
    results_all = fussy_search.search(searchText)[:20]
    
    paths = [path_changer(res['filename']) for res in results_all ]
    uids = [res['cord_uid'] for res in results_all]
    sorted_res = DataSorter.sort_uid(uids, paths, searchText)

    uids_sorted = [res[1] for res in sorted_res]
    results_all_sorted = [results_all[uid] for uid in uids_sorted]
    
    
    

    # uid-> fullpath paperid

    # res = {'cord_uid':uid, 'title': paper['title'], 
    #             'authors': authors, 
    #             'abstract': abstract, 'positions': positions}

