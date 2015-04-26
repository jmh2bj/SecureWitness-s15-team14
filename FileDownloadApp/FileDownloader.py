import requests

client = requests.session()
base_url = 'http://127.0.0.1:8000'
url_login = base_url + '/registration/login'

r0 = requests.get(url_login)

#print(r0.status_code)

csrftoken = r0.cookies['csrftoken']

#print(csrftoken)

userid = 'admin'
password = 'admin1'

login_data = {'username':userid,'password':password, 'csrfmiddlewaretoken':csrftoken}


resp = requests.post(url_login, data=login_data, cookies=r0.cookies)

#print(resp.status_code)


#print(resp.cookies['sessionid'])

cookies = dict(sessionid=resp.cookies['sessionid'])


#display all reports you have
r1 = requests.get(base_url + '/reports/', cookies=cookies)
text = str(r1.text.encode("utf-8"))
x = text.find('<p>Your Reports: </p>')
text = text[x:]
text = text[text.find('<a href='):]
index = 0
reports = {}
while('<a href=' in text):
	start = text.find('"', 8)
	stop = text.find('"', 10)
	url = text[start+1:stop]
	start = text.find('>')
	stop = text.find('</a>')
	reports[text[start+1:stop]] = url
	print(url)
	print(text[start+1:stop])
	index = text.find('<a href=', index+8)
	text = text[index:]
print(reports)

#display chosen report
r2 = requests.get(base_url + '/reports/3', cookies=cookies, stream=True)

text = str(r2.text.encode("utf-8"))

#download the file, wont work until we fix downloads on actual website
r3 = requests.get(base_url + '/reports/reports/Self_Reflection.docx', cookies=cookies, stream=True)

with open('hello.txt', 'wb') as f:
        for chunk in r3.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

print(text)