import requests

url = 'http://httpbin.org/post'
file = {'file':open('/Users/HelloWorld/Desktop/demo.txt','rb')}
r = requests.post("http://httpbin.org/post", files = file)
# print r.text


with open('/Users/HelloWorld/Desktop/demo.txt') as f:
   r1 = requests.post('http://httpbin.org/post', data=f)

# print  r1.text



requests.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = requests.get("http://httpbin.org/cookies")
# print(r.text)



s = requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")
# print(r.text)



s = requests.Session()
s.headers.update({'x-test': 'true'})
r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
# print r.text

r = s.get('http://httpbin.org/headers', headers={'x-test': 'true'})

# print r.text




r = requests.get('https://kyfw.12306.cn/otn/', verify=False)
# print r.text


proxies = {
  "https": "http://41.118.132.69:4433"
}
r = requests.post("http://httpbin.org/post", proxies=proxies)
# print r.text
