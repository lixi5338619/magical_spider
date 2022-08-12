from demo.runflow import magical_start,magical_request,magical_close

project_name = 'cnipa'
base_url = 'https://www.cnipa.gov.cn'

session_id,process_url = magical_start(project_name,base_url)

for i in range(200):
    print(len(magical_request(session_id, process_url,'https://www.cnipa.gov.cn/col/col2486/index.html')))


magical_close(session_id,process_url,project_name)
