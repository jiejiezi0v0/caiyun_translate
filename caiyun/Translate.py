import requests
import execjs
import os
import time


def get_T():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,zh-TW;q=0.6,en-US;q=0.5',
        'app-name': 'xy',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'device-id': '35f1d20dd4b100b15ce5be9453a84454',
        'origin': 'https://fanyi.caiyunapp.com',
        'os-type': 'web',
        'os-version': '',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://fanyi.caiyunapp.com/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-authorization': 'token:qgemv4jr1y38jyq6vhvi',
    }

    json_data = {
        'browser_id': '35f1d20dd4b100b15ce5be9453a84454',
    }
    response = requests.post('https://api.interpreter.caiyunai.com/v1/user/jwt/generate', headers=headers,
                             json=json_data)
    if response.status_code == 200:
        result = response.json()
        return result['jwt']
    else:
        return None


def translate(text):
    T = get_T()
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,zh-TW;q=0.6,en-US;q=0.5',
        'app-name': 'xy',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'device-id': '35f1d20dd4b100b15ce5be9453a84454',
        'origin': 'https://fanyi.caiyunapp.com',
        'os-type': 'web',
        'os-version': '',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://fanyi.caiyunapp.com/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-authorization': 'token:qgemv4jr1y38jyq6vhvi',
        'T-Authorization': T
    }

    json_data = {
        'source': text,
        'trans_type': 'auto2zh',
        'request_id': 'web_fanyi',
        'media': 'text',
        'os_type': 'web',
        'dict': True,
        'cached': True,
        'replaced': True,
        'style': 'formal',
        'model': '',
        'detect': True,
        'browser_id': '35f1d20dd4b100b15ce5be9453a84454',
    }
    response = requests.post('https://api.interpreter.caiyunai.com/v1/translator', headers=headers,
                             json=json_data).json()
    if "isdict" not in response:
        for i in range(5):
            time.sleep(1)
            response = requests.post('https://api.interpreter.caiyunai.com/v1/translator', headers=headers,
                                     json=json_data).json()
            if "isdict" in response:
                break
            else:
                print("retrying..." + str(i))
    if response["isdict"] == 0:
        result = response
        return (execjs.compile(open('./decode1.js', 'r', encoding='utf-8').read()).call("decode1", result['target']))
    else:
        by_dict(text)


def by_dict(text):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,zh-TW;q=0.6,en-US;q=0.5',
        'app-name': 'xy',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'device-id': '35f1d20dd4b100b15ce5be9453a84454',
        'origin': 'https://fanyi.caiyunapp.com',
        'os-type': 'web',
        'os-version': '',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://fanyi.caiyunapp.com/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-authorization': 'token:qgemv4jr1y38jyq6vhvi',
    }

    json_data = {
        'trans_type': 'en2zh',
        'source': text,
    }

    response = requests.post('https://api.interpreter.caiyunai.com/v1/dict', headers=headers, json=json_data).json()
    for meaning in response["dictionary"]["explanations"]:
        print(meaning)


if __name__ == '__main__':
    file_name = r".txt"
    with open(translate(os.path.basename(file_name).split('.')[0]) + ".txt", 'w', encoding='utf-8') as f:
        with open(file_name, 'r', encoding='utf-8') as f1:
            for line in f1:
                text = line.strip()
                if not text == '':
                    f.write(translate(text))
                    f.write('\n')
