import citation
import dataclass
import utlis
data = dataclass.dataclass()
print(data.id_to_title("daf32e013d325a6feb80e83d15aabc64a48fae33"))
title = dataclass.str_to_tuple("Spatial epidemiology of networked metapopulation: An overview")
print(title)
print(data.title_to_id(title))
num_with_citation = 0
num_sited = 0
for i in data.d_cites:
    if len(data.d_cites[i])>0:
        num_with_citation += 1
    if len(data.d_cited_by[i])>0:
        num_sited += 1

print(num_with_citation,"/",len(data.d_cites))
print(num_sited,"/",len(data.d_cited_by))
