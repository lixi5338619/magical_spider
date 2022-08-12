import requests
sess = requests.session()
host = 'http://127.0.0.1:5000'

def magical_start(project_name,base_url = 'http://www.lxspider.com'):
    # 1、create browser and select session_id
    result = sess.post(f'{host}/create',data={'name':project_name,'url':base_url}).json()
    session_id,process_url = result['session_id'],result['process_url']
    return session_id,process_url


def magical_request(session_id,process_url,request_url,request_type='get',formdata=''):
    # 2、request browser_xhr
    data = {'session_id': session_id, 'process_url': process_url,
            'request_url': request_url, 'request_type': request_type}

    if request_type.lower()=='post':
        data.update({'request_type':'post','formdata':formdata})

    result = sess.post(f'{host}/xhr',data=data).json()
    return result['result']


def magical_close(session_id,process_url,process_name):
    # 4、close browser
    close_data = {'session_id':session_id,'process_url':process_url,'process_name':process_name}
    sess.post(f'{host}/close',data=close_data).json()
