import requests
import json
import flask

def getanswer(examQstId):
  url = "https://education.gkgzj.com/education-intf/api/taskV2/queryMyExamQstPaper"
  payload = "{\"data\":{\"taskId\":\"这里填任务id\",\"examQstId\":"+examQstId+"}}"#
  headers = {
    'authority': 'education.gkgzj.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://education.gkgzj.com',
    'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56',
    'x-domain': 'A0',
    'x-userkey': '......'#这里在你登录后获取下
  }

  response = requests.request("POST", url, headers=headers, data=payload, timeout=20)

  json_data = json.loads(response.text)
  alllist = []
  for i in json_data['data']:
      #print('题目:',i['qstName'],'\n答案:',i['rightQstOptSym'])
      for x in i['opts']:
        if x['qstOptSym']==i['rightQstOptSym']:
          alllist.append(f'题目:{i["qstName"]}\n答案:{i["rightQstOptSym"]}.{x["qstOptName"]}')
          break
        if x['qstOptSym'] in i['rightQstOptSym']:
          duoxuanlist=[]
          for y in range(len(i['opts'])):
            duoxuanlist.append(x["qstOptName"])
          
          alllist.append(f'题目:{i["qstName"]}\n答案:{i["rightQstOptSym"]}.{"、".join(duoxuanlist)}')
          break
  printstr = '<br />'.join(alllist)
  return printstr


app = flask.Flask(__name__)
@app.route('/getanswer', methods=['get'])
def main():
    examQstId = flask.request.args.get('id')
    return getanswer(examQstId)

    
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=9000, debug=True)

