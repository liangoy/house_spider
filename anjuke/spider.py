import requests
from lxml.etree import HTML as leh

HEADERS={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'accept-encoding': 'gzip, deflate, br',
 'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
 'cache-control': 'max-age=0',
 'cookie': 'aQQ_ajkguid=FE3305E2-2CEF-1B1F-7EC5-FDA5064E3AD1; 58tj_uuid=898f861a-e5dc-4917-82cd-d5c8491742d8; als=0; ctid=13; lps=http%3A%2F%2Fwww.anjuke.com%2Fsale%2F%3Fpi%3DPZ-baidu-pc-all-esf%7Chttp%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%26rsv_spt%3D1%26rsv_iqid%3D0xdd680f46000082cf%26issp%3D1%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D2%26ie%3Dutf-8%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26rsv_sug3%3D18%26rsv_sug1%3D3%26rsv_sug7%3D100%26rsv_sug2%3D0%26inputT%3D5947%26rsv_sug4%3D5947; twe=2; sessid=88C965A1-A49B-D3B4-4265-C3BCD2D81F97; _ga=GA1.2.899633620.1531274840; _gid=GA1.2.590944624.1531274840; init_refer=http%253A%252F%252Fwww.baidu.com%252Fs%253Fwd%253D%2525E5%2525AE%252589%2525E5%2525B1%252585%2525E5%2525AE%2525A2%2526rsv_spt%253D1%2526rsv_iqid%253D0xdd680f46000082cf%2526issp%253D1%2526f%253D8%2526rsv_bp%253D0%2526rsv_idx%253D2%2526ie%253Dutf-8%2526tn%253Dbaiduhome_pg%2526rsv_enter%253D1%2526rsv_sug3%253D18%2526rsv_sug1%253D3%2526rsv_sug7%253D100%2526rsv_sug2%253D0%2526inputT%253D5947%2526rsv_sug4%253D5947; new_uv=7; new_session=0; ajk_member_captcha=a464cf231c7c9a0386656827c2df4757; browse_comm_ids=435104%7C204644%7C871456; propertys=lj7mg9-pbok2c_lqrdpx-pbok0v_lqrjs5-pbojsx_jekdhm-pbhnwh_; __xsptplus8=8.7.1531274845.1531275925.34%232%7Cwww.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23Dc7Ncuvoteq5AAJTiYjIgAxRrOlb2Zk1%23',
 'upgrade-insecure-requests': '1',
 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36'}


sz=['guangmingx','nanshan','futian','luohu','longgang','longhuaq','baoan','pingshanq','yantian']

'https://sz.zu.anjuke.com/fangyuan/nanshan/p50-px3-x1/'
'https://shenzhen.anjuke.com/sale/nanshan/o5-p8/'

url_list=[]
for i in sz:
    for j in range(1,51)[::-1]:
        url_list.append('https://shenzhen.anjuke.com/sale/'+str(i)+'/o5-p'+str(j))


class Page_downloader():
    try_times=0
    max_try_times=0
    def __init__(self,max_try_times=3):
        self.max_try_times=max_try_times
    def download_a_page(self,url):
        try:
            r = requests.get(url, headers=HEADERS)
            r.close()
            if '访问验证-安居客' in r.text:
                input('stop:')
                return self.download_a_page(url)
            else:
                self.try_times=0
                return r.text
        except Exception as e:
            if self.try_times>self.max_try_times-1:
                print(url,e)
                return url
            else:
                self.try_times+=1
                return self.download_a_page(url)

page_downloader=Page_downloader()

def download_pages(url_list):
    cnt_t=len(url_list)
    cnt=0
    text_list=[]
    for i in url_list:
        text_list.append(page_downloader.download_a_page(i))
        cnt+=1
        if cnt%100==0:
            print(cnt*100//cnt_t)
    return text_list


def anal_pages_rent(text):
    l=leh(text)
    d={
        'url':l.xpath('//div[@class="zu-itemmod  "]/div[@class="zu-info"]/h3/a/@href'),
        'detail':','.join(l.xpath('//div[@class="zu-itemmod  "]/div[@class="zu-info"]/p[@class="details-item tag"]/text()')).replace(' ','').split('\n')[1:],
        'address':''.join(l.xpath('//div[@class="zu-itemmod  "]/div[@class="zu-info"]/address[@class="details-item"]//text()')).replace(' ','').replace('\xa0\xa0\n','-').splitlines()[1:],
        'face':l.xpath('//div[@class="zu-itemmod  "]/div[@class="zu-info"]/p[@class="details-item bot-tag clearfix"]/span[@class="cls-2"]/text()'),
        'price':l.xpath('//div[@class="zu-itemmod  "]/div[@class="zu-side"]/p/strong/text()')
    }
    return d

def anal_pages_sale(text):
    l=leh(text)
    d = {
        'address':'--'.join((''.join(l.xpath('//div[@class="first-col detail-col"]/dl[2]/dd/p//text()')).replace('\t','').split('－\n')+l.xpath('//div[@class="first-col detail-col"]/dl[1]/dd/a/text()'))),
        'year':l.xpath('//div[@class="first-col detail-col"]/dl[3]/dd/text()')[0],
        'structure':l.xpath('//div[@class="second-col detail-col"]/dl[1]/dd/text()')[0].replace('\t','').replace('\n',''),
        'area':l.xpath('//div[@class="second-col detail-col"]/dl[2]/dd/text()')[0],
        'face':l.xpath('//div[@class="second-col detail-col"]/dl[3]/dd/text()')[0],
        'floor':l.xpath('//div[@class="second-col detail-col"]/dl[4]/dd/text()')[0].replace('\t',''),
        'price':l.xpath('//div[@class="third-col detail-col"]/dl[1]/dd/text()')[0],
        'Decoration':l.xpath('//div[@class="third-col detail-col"]/dl[4]/dd/text()')[0],
    }
    return d


