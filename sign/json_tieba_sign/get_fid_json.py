#coding="utf-8"
import re,requests,json
BDUSS=""
headers={
"Host":"tieba.baidu.com",
"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER",
"Cookie": "BDUSS=%s"%BDUSS
}
headers2={
	"Host":"tieba.baidu.com",
	"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329 Q"
}
def _fetch_like_tieba_list():
    print u'Fetch your like_tieba_kw...'
    page_count = 1
    find_like_tieba = []
    while True:
        like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count
        resp = requests.get(like_tieba_url,headers=headers)
        resp = resp.content.decode('gbk').encode('utf8')
        re_like_tieba = '<a href="\/f\?kw=.*?" title="(.*?)">.+?<\/a><\/td><td><a class="cur_exp" target="_blank".*?'
        temp_like_tieba = re.findall(re_like_tieba, resp)
        if not temp_like_tieba:
            break
        if not find_like_tieba:
            find_like_tieba = temp_like_tieba
        else:
            find_like_tieba += temp_like_tieba
        page_count += 1
    return find_like_tieba

def _fetch_tieba_fid(tieba):
    tieba_wap_url = "http://tieba.baidu.com/mo/m?kw=" + tieba
    print tieba_wap_url
    wap_resp = requests.get(tieba_wap_url,headers=headers2)
    wap_resp=wap_resp.content
    fid=re.compile(r'"fid".*?:.*?"(.*?)"',re.S).findall(wap_resp)[0]
    return fid

if __name__ == '__main__':
	#fetch kw
	L_kw=_fetch_like_tieba_list()

	#[{'kw':'','fid':}]
	print "Fetch fid from like_tieba_kw:"
	L_Temp=[]
	L_Failed=[]
	L_Failed_Sec=[]
	D_Temp={}
	for i in range(len(L_kw)):
		D_Temp['kw']=L_kw[i]
		D_Temp['fid']=_fetch_tieba_fid(D_Temp['kw'])
		if (D_Temp['fid']).isdigit():
			L_Temp.append(D_Temp)
		else:
			L_Failed.append(L_kw[i])
		D_Temp={}
	
	print "\nFailed list:\n",L_Failed
	print "\nFetch fid from Failed_list:"
	for i in range(len(L_Failed)):
		D_Temp['kw']=L_Failed[i]
		D_Temp['fid']=_fetch_tieba_fid(D_Temp['kw'])
		if (D_Temp['fid']).isdigit():
			L_Temp.append(D_Temp)
		else:
			L_Failed_Sec.append(L_kw[i])
			D_Temp['fid']=''
			L_Temp.append(D_Temp)
		D_Temp={}
	print "\nSecond Failed list(Please fetch fid by hand):\n",L_Failed_Sec

	print "\nTotal:",len(L_Temp)

	#json file
	f=open("tieba.json","w")
	f.write(json.dumps(L_Temp,indent=4))
	f.close()

	