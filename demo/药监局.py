from demo.runflow import magical_start,magical_request,magical_close

project_name = '药监局1'
base_url = 'https://www.nmpa.gov.cn'
request_list = [
    'https://www.nmpa.gov.cn/yaopin/ypjgdt/index.html',
    'https://www.nmpa.gov.cn/yaopin/ypjgdt/20220705190551125.html'
]

session_id,process_url = magical_start(project_name,base_url)

for request_url in request_list:
    print(magical_request(session_id, process_url, request_url))

magical_close(session_id,process_url,project_name)