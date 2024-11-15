from scripts.config import Config
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import re

class ICloudPriceFetcher:
    """iCloud价格数据获取器"""
    
    def fetch(self) -> dict:
        """获取价格数据的主方法"""
        response = self._get_page_content()
        return self._parse_data(response.text)
    
    def _get_page_content(self) -> requests.Response:
        """获取页面内容"""
        try:
            response = requests.get(
                Config.ICLOUD_URL,
                headers=Config.HEADERS,
                timeout=10
            )
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response
        except requests.RequestException as e:
            raise
            
    def _parse_data(self, html: str) -> dict:
        """解析页面数据"""
        soup = BeautifulSoup(html, 'html.parser')
        price_data = {
            'fetch_time': datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
            'countries': {}
        }
        
        # 查找所有段落元素
        paragraphs = soup.find_all('p', class_='gb-paragraph')
        current_country = None
        
        for p in paragraphs:
            text = self._clean_text(p.get_text())
            
            # 跳过空行
            if not text:
                continue
                
            # 处理国家行
            if self._is_country_line(text):
                current_country = self._extract_country_info(text)
                price_data['countries'][current_country] = {}
                continue
                
            # 处理价格行
            if current_country and self._is_price_line(text):
                capacity, price = self._extract_price_info(text)
                price_data['countries'][current_country][capacity] = price
                
        return price_data
    
    def _clean_text(self, text: str) -> str:
        """清理文本，移除多余的空白字符"""
        return ' '.join(text.strip().split())
    
    def _is_country_line(self, text: str) -> bool:
        """判断是否为国家/地区行"""
        # 排除不需要的行
        if any(x in text for x in ['注：', '*', '进一步了解', '了解中国大陆']):
            return False
        # 通常国家行以货币结尾
        return '（' in text and '）' in text and not '：' in text
    
    def _is_price_line(self, text: str) -> bool:
        """判断是否为价格行"""
        return '：' in text and any(
            size in text for size in ['50GB', '200GB', '2TB', '6TB', '12TB']
        )
    
    def _extract_country_info(self, text: str) -> str:
        """提取国家和货币信息"""
        try:
            country = text.split('（')[0].strip()
            currency = text.split('（')[1].split('）')[0].strip()
            # 移除国家名称中的注释标记
            country = re.sub(r'[0-9,]+$', '', country).strip()
            return f"{country} ({currency})"
        except Exception as e:
            raise
    
    def _extract_price_info(self, text: str) -> tuple:
        """提取容量和价格信息"""
        try:
            capacity = text.split('：')[0].replace('*', '').strip()
            price = text.split('：')[1].strip()
            return capacity, price
        except Exception as e:
            raise
