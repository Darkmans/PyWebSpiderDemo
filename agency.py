import requests
import re
import time

# 伪装浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

# 批量获取高匿代理ip
def get_agency_ip(max_page_number):
    for i in range(1, max_page_number + 1):
        page_number = i
        init_url = 'http://www.xicidaili.com/nn/' + str(i)
        req = requests.get(init_url, headers=headers)
        # 获取代理ip
        agency_ip_re = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b' ,re.S)
        agency_ip = agency_ip_re.findall(req.text)
        # 获取代理ip的端口号
        agency_port_re = re.compile('<td>([0-9]{2,5})</td>', re.S)
        agency_port = agency_port_re.findall(req.text)
        # 高匿代理ip页面中所列出的ip数量
        ip_number = len(agency_ip)
        print('正在获取第 %d 页代理中（请耐心等候）......' % page_number)
        for i in range(ip_number):
            total_ip = agency_ip[i] + ':' + agency_port[i]
            print(total_ip)
            time.sleep(1)
        print('第 %d 页代理获取完毕！' % page_number)
        print('------------------------------------')
        time.sleep(2)

if __name__ == '__main__':
    print('---------- 高匿代理ip获取 ----------')
    max_page_number = int(input('请输入您想获取的页数: '))
    get_agency_ip(max_page_number)
