import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import json
import logging
import re
from pathlib import Path

# 配置日志
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'icloud_price_fetcher.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def clean_text(text):
    """清理文本,移除多余的空白字符"""
    return ' '.join(text.strip().split())

def is_country_line(text):
    """判断是否为国家/地区行"""
    # 排除不需要的行
    if any(x in text for x in ['注：', '*', '进一步了解', '了解中国大陆']):
        return False
    # 通常国家行以货币结尾
    return '（' in text and '）' in text and not '：' in text

def is_price_line(text):
    """判断是否为价格行"""
    return '：' in text and any(size in text for size in ['50GB', '200GB', '2TB', '6TB', '12TB'])

def extract_country_info(text):
    """提取国家和货币信息"""
    country = text.split('（')[0].strip()
    currency = text.split('（')[1].split('）')[0].strip()
    # 移除国家名称中的注释标记
    country = re.sub(r'[0-9,]+$', '', country).strip()
    return f"{country} ({currency})"

def extract_price_info(text):
    """提取容量和价格信息"""
    capacity = text.split('：')[0].replace('*', '').strip()
    price = text.split('：')[1].strip()
    return capacity, price

def fetch_icloud_prices():
    """抓取 iCloud 价格数据"""
    url = 'https://support.apple.com/zh-cn/108047'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 发送请求获取页面内容
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 创建存储数据的字典
        price_data = {
            'fetch_time': datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
            'countries': {}
        }
        
        # 查找所有段落元素
        paragraphs = soup.find_all('p', class_='gb-paragraph')
        
        current_country = None
        
        for p in paragraphs:
            text = clean_text(p.get_text())
            
            # 跳过空行
            if not text:
                continue
            
            # 处理国家行
            if is_country_line(text):
                current_country = extract_country_info(text)
                price_data['countries'][current_country] = {}
                logging.info(f"处理国家/地区: {current_country}")
                continue
            
            # 处理价格行
            if current_country and is_price_line(text):
                capacity, price = extract_price_info(text)
                price_data['countries'][current_country][capacity] = price
                logging.debug(f"添加价格: {capacity} = {price}")
        
        # 修改保存路径
        base_dir = Path(__file__).parent.parent
        filename = base_dir / 'public' / 'json' / f'icloud_prices_{datetime.now().strftime("%Y%m%d")}.json'
        
        # 确保目录存在
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(price_data, f, ensure_ascii=False, indent=2)
            
        logging.info(f'数据已成功抓取并保存到 {filename}')
        
    except Exception as e:
        logging.error(f'抓取数据时发生错误: {str(e)}', exc_info=True)
        raise

if __name__ == '__main__':
    fetch_icloud_prices()