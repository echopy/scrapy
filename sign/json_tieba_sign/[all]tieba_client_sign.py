# -*- coding: utf-8 -*-  
import requests,hashlib,json,base64,time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
Header = {
    'User-Agent': 'BaiduTieba for Android 6.0.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'c.tieba.baidu.com',
}   

def decodeURI_post(postData):
    SIGN_KEY =  "tiebaclient!!!"
    s = ""
    keys = postData.keys() 
    keys.sort() 
    for i in keys:
            s += i + '=' + postData[i]
    sign = hashlib.md5((s + SIGN_KEY).encode("utf-8")).hexdigest().upper()
    postData.update({'sign':str(sign)})
    return postData

def tiebaClientLogin(name,password):
        loginUrl = "http://c.tieba.baidu.com/c/s/login"
        loginData = {
		"_client_id":"wappc_1386816224047_167",
                "_client_type":'1',
                "_client_version":"6.0.1",
                "_phone_imei":"a6ca20a897260bb1a1529d1276ee8176",
                "cuid":"JC6737884997EF9AFE247470B6E960E4|165384710041368|com.baidu.tieba6.0.1",
                "model":"M1",
                "un":name,
                "passwd":base64.encodestring(password),
                "isphone":"0",
                'stErrorNums' : '0',
                'stMethod' : '1',
                'stMode' : '3',
                'stSize' : '91',
                'stTime' : '356',
                'stTimesNum' : '0',
                'from':'baidu_appstore',
                "timestamp" : str(time.time()).replace('.',''),                
                }
        
        loginData = decodeURI_post(loginData)
        
        login_Response=requests.post(loginUrl,data=loginData,headers=Header)
        return login_Response.content

def tiebaLogin(username,password):
    #登录后并获得BDUSS、tbs等数据
    respjson=tiebaClientLogin(username,password)
    respj=json.loads(respjson)
    #取出BDUSS/tbs
    BDUSS=respj['user']['BDUSS']
    tbs=respj['anti']['tbs']
    return BDUSS,tbs

def postData_Struct(kw,fid,BDUSS,tbs):
    #计算sign所需参数
    #post字典
    postdict={
    "BDUSS":BDUSS,
    "fid":fid,
    "kw":kw,
    "tbs":tbs,
    }
    #生成postdata
    postdata=decodeURI_post(postdict)
    return postdata

def readFromJson():
    f=open('tieba.json','r')
    data=json.loads(f.read())
    f.close()
    return data

if __name__ == '__main__':
    #签到url
    sign_url="http://c.tieba.baidu.com/c/c/forum/sign"
    _username=""
    _password=""
    
    _BDUSS,_tbs=tiebaLogin(_username, _password)

    tieba_list=readFromJson()
    for i in range(len(tieba_list)):
        _kw=tieba_list[i]['kw']
        _fid=tieba_list[i]['fid']
        print "Sign for %s:%s"%(_kw,_fid)
        postdata=postData_Struct(_kw, _fid, _BDUSS, _tbs)
        #post数据到签到url
        sign_response=requests.post(sign_url,data=postdata,headers=Header)
        #返回签到结果
        print sign_response.content

    #fid='155829'
    #kw='python'
    #fid="8142"
    #kw="深圳".decode('utf-8')