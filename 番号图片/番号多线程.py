import requests
import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}
if not os.path.exists('番号'):
    os.mkdir('番号')


def get_url_list():
    resp0 = requests.get(url, headers=headers).content.decode('utf-8')
    # print(resp0)
    html0 = etree.HTML(resp0)
    hrefs = html0.xpath('//ul[@class="nylist clearfix loadimg"]/li/a/@href')
    # file_names = html0.xpath('//ul[@class="nylist clearfix loadimg"]/li/a/p/text()')
    url_list = [] 
    for href in hrefs:
        href = 'https://www.66fhz.com' + href
        # print(file_name,href)
        url_list.append(href)      
    return url_list


def download(href):
    resp1 = requests.get(href, headers=headers).content.decode('utf-8')
    html = etree.HTML(resp1)
    srcs = html.xpath('//ul[@class="fhlist clearfix loadimg"]/li/a/img/@src')
    names = html.xpath("//ul[@class='fhlist clearfix loadimg']/li/a/p/text()")
    file_name = html.xpath('//div[@class="infosay fr pos-r"]/h1/text()')[0]
    #print(srcs, names)
    if not os.path.exists('./番号/{}'.format(file_name)):
        os.mkdir('./番号/{}'.format(file_name))
    print('正在下载 {}'.format(file_name))
    n = 0
    for name, src in zip(names, srcs):
        name = name+'.jpg'
        #print(name, src)
        with open('./番号/{}/{}'.format(file_name, name), 'wb') as f:
            f.write(requests.get(src).content)
            f.close()
            print('{} 下载完成'.format(name))
            n += 1
    print(f'============={file_name} Over！ 共下载了{n}张图片===========')


if __name__ == '__main__':
    with ThreadPoolExecutor(48) as t:
        for page in range(1, 3):
            if page < 2:
                url = 'https://www.66fhz.com/you/'
            else:
                url = f'https://www.66fhz.com/you/index_{page}.html'
            for href in get_url_list():       
                t.submit(download, href)    
    print('========下载完成==========')

