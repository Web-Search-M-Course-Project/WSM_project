import pandas as pd
# data = dataclass.dataclass("stem")
# print(data.id_to_title("daf32e013d325a6feb80e83d15aabc64a48fae33"))
# title = dataclass.str_to_tuple("Spatial epidemiology of networked metapopulation: An overview","stem")
# print(title)
# print(data.title_to_id(title))
# num_with_citation = 0
# num_sited = 0
# for i in data.d_cites:
#     if len(data.d_cites[i])>0:
#         num_with_citation += 1
#     if len(data.d_cited_by[i])>0:
#         num_sited += 1

# print(num_with_citation,"/",len(data.d_cites))
# print(num_sited,"/",len(data.d_cited_by))



metadata = pd.read_csv("./2020-04-03/metadata_with_mag_mapping_04_03.csv", encoding="utf-8")
metadata.head()

paper_id = ['bcn6tpnx','4k1k02r8','jof3mnnk','n8n1folf']
for uid in paper_id:
    # find by paper id
    res = metadata.query(f"cord_uid == '{uid}'")
    print(f'----------{uid}-----------')
    print(res)



