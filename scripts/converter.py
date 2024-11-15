import requests
from datetime import datetime
import re
import json
from scripts.config import Config
class PriceConverter:
    """价格转换处理器"""
    
    def __init__(self):
        self.rates = {}
        
    def convert_prices(self, price_data: dict) -> dict:
        """转换所有价格为人民币"""
        try:
            # 获取汇率
            self.rates = self._get_exchange_rates()
            
            # 创建新的价格数据结构
            converted_data = {
                'fetch_time': price_data['fetch_time'],
                'exchange_rates_time': Config.get_datetime_str(),
                'countries': {}
            }
            
            # 转换每个国家的价格
            for country, prices in price_data['countries'].items():
                currency = self._extract_currency(country)
                converted_data['countries'][country] = {}
                
                for plan, price in prices.items():
                    rmb_price = self._convert_to_rmb(price, currency)
                    if rmb_price:
                        converted_data['countries'][country][plan] = f"¥{rmb_price}"
            
            return converted_data
            
        except Exception as e:
            raise
            
    def _get_exchange_rates(self) -> dict:
        """获取最新汇率"""
        try:
            response = requests.get(Config.EXCHANGE_RATE_API, timeout=10)
            response.raise_for_status()
            rates = response.json()['rates']
            return rates
        except Exception as e:
            # 如果 API 失败，使用备用 API 或返回上次保存的汇率
            backup_file = Config.JSON_DIR / 'latest_rates.json'
            if backup_file.exists():
                with open(backup_file, 'r') as f:
                    return json.load(f)
            raise
            
    def _extract_currency(self, country: str) -> str:
        """从国家信息中提取货币代码"""
        try:
            # 从括号中提取货币名称
            currency = country.split('(')[1].split(')')[0].strip()
            return currency
        except Exception as e:
            raise
            
    def _convert_to_rmb(self, price_str: str, currency: str) -> float:
        """将价格转换为人民币"""
        try:
            # 清理价格字符串
            clean_price = self._clean_price(price_str)
            if not clean_price:
                return None
                
            price = float(clean_price)
            
            # 如果已经是人民币，直接返回
            if currency == 'CNY':
                return round(price, 2)
                
            # 获取货币代码
            currency_code = Config.CURRENCY_MAP.get(currency)
            if not currency_code:
                return None
                
            # 获取汇率并转换
            if currency_code in self.rates:
                rate = self.rates[currency_code]
                rmb_price = price / rate
                return round(rmb_price, 2)
            else:
                return None
                
        except ValueError as e:
            return None
        except Exception as e:
            return None
            
    def _clean_price(self, price_str: str) -> str:
        """清理价格字符串"""
        try:
            # 移除所有空格
            price_str = ''.join(price_str.split())
            
            # 处理特殊格式的价格符号
            special_formats = {
                'S/.': '', 'R$': '', 'Rs.': '', 'Rs': '', 'Rp': '',
                'NT$': '', 'HK$': '', 'S$': '', 'RM': '', 'CHF': '',
                'AED': '', 'zł': '', 'lei': '', 'p.': '', 'TL': '',
                'TSh': ''
            }
            
            # 通用货币符号
            symbols = ['$', '€', '£', '¥', '₪', 'лв', 'Kč', 'kr', 'Ft', 
                      '₱', '฿', '₫', '₦', '₸', '﷼', 'R', '₩']
            
            # 处理特殊格式
            for format_str in special_formats:
                if format_str in price_str:
                    price_str = price_str.replace(format_str, '')
            
            # 移除货币符号
            for symbol in symbols:
                price_str = price_str.replace(symbol, '')
            
            # 移除千位分隔符和其他非数字字符
            price_str = re.sub(r'[^0-9.]', '', price_str)
            
            # 处理多个小数点的情况
            if price_str.count('.') > 1:
                parts = price_str.split('.')
                price_str = ''.join(parts[:-1]) + '.' + parts[-1]
            
            return price_str.strip()
            
        except Exception as e:
            return None
