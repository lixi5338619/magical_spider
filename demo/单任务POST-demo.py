from demo.runflow import magical_start,magical_request,magical_close
import json
# POST案例昨天忘记加了，感谢 [尘川] 的提醒  by:2022/08/10

project_name = 'chinadrugtrials'
base_url = 'http://www.chinadrugtrials.org.cn'

session_id,process_url = magical_start(project_name,base_url)

data = {
        "id": "",
        "ckm_index": "",
        "sort": "desc",
        "sort2": "",
        "rule": "CTR",
        "secondLevel": "0",
        "currentpage": "2",
        "keywords": "",
        "reg_no": "",
        "indication": "",
        "case_no": "",
        "drugs_name": "",
        "drugs_type": "",
        "appliers": "",
        "communities": "",
        "researchers": "",
        "agencies": "",
        "state": ""
    }
formdata = json.dumps(data)
print(magical_request(session_id=session_id, process_url=process_url,
                      request_url='http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml',
                      request_type='post',formdata=formdata
                      ))

magical_close(session_id,process_url,project_name)
