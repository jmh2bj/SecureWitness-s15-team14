import requests

client = requests.session()
base_url = 'http://127.0.0.1:8000'
url_login = base_url + '/registration/login'

r0 = requests.get(url_login)

#print(r0.status_code)

csrftoken = r0.cookies['csrftoken']

#print(csrftoken)
respcontent = ''


while(not respcontent == 'logged in'):

	userid = input("Username: ")
	password = input("Password: ")

	login_data = {'username':userid,'password':password, 'csrfmiddlewaretoken':csrftoken}


	resp = requests.post(url_login, data=login_data, cookies=r0.cookies)

	respcontent = resp.text

	if(not respcontent == 'logged in'):
		print("Username and password do not match. Please try again.")

cookies = dict(sessionid=resp.cookies['sessionid'])

print("Log in successful")

#display all reports you have
r1 = requests.get(base_url + '/visiblereports', cookies=cookies)
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
	index = text.find('<a href=', index+8)
	text = text[index:]

print("Reports:")
for key in reports:
	print(key)

while(True):
	selrep = input("Please select a report: ")
	if(selrep in reports):
		break
	print("That report does not exist.")

#display chosen report
r2 = requests.get(base_url + reports[selrep], cookies=cookies, stream=True)

text = str(r2.text.encode("utf-8"))
text = text[text.find("<form method="):text.find("</form>")+7]

while(not text.find('<label') == -1):
	field = text[text.find('>', text.find('<label'))+1:text.find("</label>")]
	if(field == "Public Report?"):
		break
	if(field == "Rep file:"):
		if(text.find("<a href=") == -1):
			fileexists = False
		else:
			fileexists = True
			value = text[text.find("<a href=")+9:text.find('>', text.find("<a href="))-1]
			file_path = value
		text = text[text.find("<input id="):]
	else:
		text = text[text.find("<input id="):]
		if(text.find("<p/>") > text.find('value=')):
			value = text[text.find('value=')+7:text.find('"', text.find('value=')+8)]
		else:
			value = ''
	text = text[text.find('<p/>'):]
	print(field + " " + value)

dlfile = ""
while(fileexists):
	dlfile = input("Would you like to download the file? (y or n): ")
	if(dlfile == 'y' or dlfile == 'n'):
		break
	print("Please put y for yes or n for no.")

if(dlfile == 'y'):
	r3 = requests.get(base_url + '/reports/' + file_path, cookies=cookies, stream=True)

	with open(file_path[file_path.find('/')+1:], 'wb') as f:
		for chunk in r2.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				f.flush()
