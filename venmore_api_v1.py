#!/bin/python3

import requests,json,time,string,random,os
from urllib import parse


before_id = 2605676841557557260 #most recent transaction ID to work backwards (in time) from 
after_id = 2605676841557500000 #final transaction ID (stopping point)
results_limit = 50

if not os.path.exists("thenmo_results"):
    os.makedirs("thenmo_results")

session = requests.Session()

#Disposable account creation to get api token:
def new_account():
        global session
        tel_interchange = random.randint(100,999)
        tel_line = random.randint(1000,9999)
        username = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(20))
        password = random.randint(10000000000,99999999999999)
        username = f'{username}@email.com'
        client_id = 10 #unsure what this does, but it's necessary. 1, 10 and 2899 are valid values. New account seems to always get 10. 
        account_creation_url = 'https://venmo.com/api/v5/users'
        
        account_payload = {
                'email' :username,
                'first_name' :'gregory',
                'last_name' :'evans',
                'password' :password, 
                'phone' :f'(708) {tel_interchange}-{tel_line}',
                'client_id' :client_id
        }

        r = session.post(account_creation_url, data = account_payload)
 
        if r.status_code == 200: #all good
            response = json.loads(r.content)
            result = response['access_token']
            print("Got Access Token")
        else: #Probably a bad/used phone number. Try a new one. 
            print(r.content)
            tel_line += 1
            time.sleep(1)
            result = 0
        return(result)

#Generates a random user-agent:
def randUA(): 
    with open('user-agents.txt', 'r') as uaFile:
        allUserAgents = uaFile.read().splitlines()
        userAgent = random.choice(allUserAgents)
    return(userAgent)

#Create new account, get token
api_token = new_account()
while api_token == 0:
    api_token = new_account() 

feed_url = 'https://api.venmo.com/v1/stories'
next_page = feed_url

#these headers are not necessary, but. . .JIC
feed_headers = { 
        'DNT' :'1',
        'Cache-Control' :'max-age=0',
        'User-Agent' :randUA
}

#reeead tha feeeed:
while before_id >= after_id:
    feed_params = (
	('before_id', before_id),
	('limit', results_limit)
    )

    print("Trying to get feed. . .")
    print(feed_params)
    feed = session.get(next_page, params=feed_params) #get feed
    print("Success")

    if feed.status_code != 429:
        results = json.loads(feed.content)
        next_page = results['pagination']['next']
        feed_data = results['data']
        f= open("thenmo_results/{}".format(before_id),"w+") 
        json.dump(results, f)
        f.close()  
        before_id = parse.parse_qs(parse.urlparse(next_page).query)['before_id'][0]
        print(feed_data)
        print(before_id)
        time.sleep(3)
    else:
        print("Too Many Requests")
        print(next_page)
        time.sleep(600)
        api_token = new_account() # get fresh token
print("Job Complete!")