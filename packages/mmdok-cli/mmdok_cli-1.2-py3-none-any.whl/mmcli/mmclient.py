import mimetypes
import pprint
import requests
import time
import urllib
import webbrowser

class MMClient:
    def __init__(self, server, login_server):
        self.server = server
        self.login_server = login_server
        self.refresh_token = 'No token'
        self.access_token = 'No token'

    def set_server(self, server):
        self.server = server

    def set_login_server(self, login_server):
        self.login_server = login_server
        
    def _login(self, response):
        #headers = response.headers
        if response.status_code == 200:
            j = response.json()
            self.access_token = j['tokens']['access_token']
            self.refresh_token = j['tokens']['refresh_token']
            print("AccessToken:" + self.access_token)
            print("RefreshToken:" + self.refresh_token) 
            if 'company' in j: 
                self.company = j['company']
            return True
        else:
            print(response.text)
            return False
        
    def _refresh(self):
        response = requests.post(self.login_server + '/refresh', 
                          headers={'Authorization': 'Bearer ' + self.refresh_token})
        if response.status_code == 200:
            j = response.json()
            self.access_token = j['tokens']['access_token']
            self.refresh_token = j['tokens']['refresh_token']
        else:
            print("Could not refresh" + str(response.status_code))
        
    def _send_get(self, url, resend=True):
        response = requests.get(url, headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code==401 and resend:
            self._refresh()
            return self._send_get(url, False)
        else:
            return response

    def _send_post(self, url, data={}, resend=True):
        response = requests.post(url, data=data, 
                                 headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code==401 and resend:
            self._refresh()
            return self._send_post(url, data, False)
        else:
            return response
        
    def _send_put(self, url, data={}, resend=True):
        response = requests.put(url, json=data, 
                                headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code==401 and resend:
            self._refresh()
            return self._send_post(url, data, False)
        else:
            return response
        
    def _send_delete(self, url, resend=True):
        response = requests.delete(url,
                                   headers={'Authorization': 'Bearer ' + self.access_token})
        if response.status_code==401 and resend:
            self._refresh()
            return self._send_delete(url, False)
        else:
            return response
        
    def register(self):
        webbrowser.open(self.login_server + '/register')
            
    def login_bankid(self, ssn):
        response = requests.post(self.login_server + '/login', json={"ssn": ssn, "type":"bankid"})
        return self._login(response)

    def login_freja(self, ssn):
        response = requests.post(self.login_server + '/login', json={"email": ssn, "type":"freja"})
        j = response.json()
        if response.status_code == 202:
            return self._poll(ssn, "freja", j['token'])
        else:
            return False
        
    def _poll(self, email, type, token):
        url = self.login_server + '/poll'
        time.sleep(1)
        print(url)
        response = requests.post(url, json={"email": email, "type": type}, 
                                 headers={"Authorization": "Bearer " + token})
        j = response.json()
        if response.status_code == 202:
            new_token = j['token']
            return self._poll(email, type, new_token)
        elif response.status_code == 200:
            return self._login(response)
        else:
            return False
          
    def login_usrpwd(self, email, password, code):
        response = requests.post(self.login_server + '/login', json={"email": email, 
                                                               "password": password, 
                                                               "code": code,
                                                               "type": "password"})
        return self._login(response)
    
    def login_apikey(self, email, apikey):
        response = requests.post(self.login_server + '/login', json={"type": "apikey", 
                                                                     "email": email, 
                                                                     "apikey": apikey})
        return self._login(response)
    
    def logout(self):
        url = self.login_server + '/logout'
        response = requests.post(url,  
                                 headers={'Authorization': 'Bearer ' + self.refresh_token})
        return response.status_code == 200
        
        
    def test_auth(self):
        r = self._send_get(self.login_server + '/private')
        if r.status_code==200:
            j = r.json()
            if 'email' in j:
                email = j['email']
                return True, email
            else:
                return False, "Could not identify user"
        else:
            return False, "Not permitted"

    def types(self):
        return self._send_get(self.server + '/types')

    """
    Example:
        filter={"doctype":"kunddokument", "kundnummer":"AAA"}
        sort: {"kundnummer": 1}
        range: {"from":100, "to:200"}
    """
    def search(self, filter=None, sort=None, range=None):
        if not filter:
            filter = {}
        if not sort:
            sort = {} 
        if not range:
            range = {}
        params = urllib.parse.urlencode({'filter': filter, 'sort': sort, 'range': range}) # json(), status_code
        print(params)
        return self._send_get(self.server + '/documents?' + params)                

    def upload(self, data, path, id):
        url = self.server + '/document'
        if id: url += '/' + id
        response = self._send_post(url, data=data)
        response = response.json()
        if 'url' not in response: 
            return False, response
        url = response['url']
        fields = response['fields']
        id = response['id']
        mimetype = mimetypes.guess_type(path)
        if len(mimetype)<0: mimetype='application/octet-stream' 
        with open(path, 'rb') as f:
            files = {'file': (path, f, mimetype),
                 'Content-Disposition': 'form-data; name="files"',
                 'Content-Type': mimetype}
            response = requests.post(url, files=files, data=fields)
            if not response.ok:
                return False, ('Failed upload to Minio. Reason: ' +
                  response.reason + '. Text:' + response.text)

            return True, id

    def download(self, id, path, pdf):
        url = self.server + '/document/' + id + '?isAttachment=true'
        if (pdf): url += '&pdf=true'
        response = self._send_get(url)
        if not response.ok:
            return False, ('Get document failed. Reason: ' +
                  response.reason + '. Text:' + response.text)
        response = requests.get(response.json()['url'])
        open(path, "wb").write(response.content)
        return True, "OK"

    def view(self, id, version=None):
        url = self.server + '/document/' + id
        if version: 
            url += '?version=' + version
        response = self._send_get(url)
        if not response.ok:
            return False, ('Get document failed. Reason: ' +
                  response.reason + '. Text:' + response.text)
        webbrowser.open(response.json()['url'])
        return True, "OK"

    def metadata(self, id):
        url = self.server + '/document/' + id + '?type=metadata'
        response = self._send_get(url)
        if not response.ok:
            return False, ('Get metadata failed. Reason: ' +
                  response.reason + '. Text:' + response.text)
        pprint.pprint(response.json()['metadata'])
        return True, "OK"

    def audit(self, id):
        url = self.server + '/document/' + id + '?type=audit'
        response = self._send_get(url)
        if not response.ok:
            return False, ('Get audits failed. Reason: ' +
                  response.reason + '. Text:' + response.text)
        pprint.pprint(response.json()['audit'])
        return True, "OK"

    def update(self, id, metadata):
        data = {}
        data['metadata'] = metadata
        rsp = self._send_put(self.server + "/document/" + id, json=data)
        return rsp

    def delete(self, id, isFullDelete):
        url = self.server
        if isFullDelete: url += "/document/"
        else: url += "/version/"
        url += id
        print(url) 
        rsp = self._send_delete(url)
        return rsp

    def count(self):
        url = self.server + '/count'
        return self._send_get(url)

    def dump(self, response):
        print(response.request.method)
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)

