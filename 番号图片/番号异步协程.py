import requests
import os
import asyncio
import aiohttp
import aiofiles
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

if not os.path.exists('番号'):
    os.mkdir('番号')

async def aiodownload(href):
    async with aiohttp.ClientSession() as session:
        async with session.get(href, headers=headers) as resp1:
            resp1 = await resp1.content.read()
            html = etree.HTML(resp1)
            srcs = html.xpath('//ul[@class="fhlist clearfix loadimg"]/li/a/img/@src')
            names = html.xpath("//ul[@class='fhlist clearfix loadimg']/li/a/p/text()")
            file_name = html.xpath('//div[@class="infosay fr pos-r"]/h1/text()')[0]
            # print(srcs, names)
            if not os.path.exists('./番号/{}'.format(file_name)):
                os.mkdir('./番号/{}'.format(file_name))
            print('正在下载 {}'.format(file_name))
            n = 0
            for name, src in zip(names, srcs):
                name = name + '.jpg'
                # print(name, src)
                async with session.get(src, headers=headers) as resp2:
                    async with aiofiles.open('./番号/{}/{}'.format(file_name, name), 'wb') as f:
                        await f.write(await resp2.content.read())
                        print('{} 下载完成'.format(name))
                        n += 1
            print(f'============={file_name} Over！ 共下载了{n}张图片===========')

async def get_url_list(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp0:
            resp0 = await resp0.content.read()
            html0 = etree.HTML(resp0)
            hrefs = html0.xpath('//ul[@class="nylist clearfix loadimg"]/li/a/@href')
            # file_names = html0.xpath('//ul[@class="nylist clearfix loadimg"]/li/a/p/text()')
            url_list = []
            for href in hrefs:
                href = 'https://www.66fhz.com' + href
                #print(href)
                url_list.append(aiodownload(href))
            await asyncio.wait(url_list)

async def main():
    page_url = []
    for page in range(1, 3):
        if page < 2:
                url = 'https://www.66fhz.com/you/'
        else:
            url = f'https://www.66fhz.com/you/index_{page}.html'
        page_url.append(get_url_list(url))
    await asyncio.wait(page_url)

if __name__ == '__main__':
    # url = 'https://www.66fhz.com/you/'
    asyncio.run(main())
    print('================全部over==============')
