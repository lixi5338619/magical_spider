import requests

host = 'http://127.0.0.1:5000'

def magical_start(project_name,base_url = 'http://www.lxspider.com'):
    # 1、create browser and select session_id
    result = requests.post(f'{host}/create',data={'name':project_name,'url':base_url}).json()
    session_id,process_url = result['session_id'],result['process_url']
    return session_id,process_url


def magical_request(session_id,process_url,request_url):
    # 2、request browser_xhr
    data = {'session_id':session_id,'process_url':process_url,
            'request_url':request_url,'request_type':'get'}
    result = requests.post(f'{host}/xhr',data=data).json()
    return result['result']


def magical_close(session_id,process_url,process_name):
    # 4、close browser
    close_data = {'session_id':session_id,'process_url':process_url,'process_name':process_name}
    requests.post(f'{host}/close',data=close_data).json()