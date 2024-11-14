import json
from datetime import datetime
import requests
import logging
from pathlib import Path

# 配置日志
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'currency_converter.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def get_exchange_rates():
    """获取最新汇率"""
    try:
        # 使用免费的汇率API
        url = "https://api.exchangerate-api.com/v4/latest/CNY"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        rates = response.json()['rates']
        logging.info("成功获取最新汇率")
        return rates
    except Exception as e:
        logging.error(f"获取汇率失败: {str(e)}")
        raise

def get_currency_code(currency):
    """获取标准货币代码"""
    currency_map = {
        '美元': 'USD', '欧元': 'EUR', '日元': 'JPY', '港元': 'HKD',
        '英镑': 'GBP', '澳元': 'AUD', '加元': 'CAD', '新西兰元': 'NZD',
        '新加坡元': 'SGD', '瑞士法郎': 'CHF', '瑞典克朗': 'SEK',
        '丹麦克朗': 'DKK', '挪威克朗': 'NOK', '韩元': 'KRW',
        '新台币': 'TWD', '泰铢': 'THB', '马来西亚林吉特': 'MYR',
        '巴西雷亚尔': 'BRL', '智利比索': 'CLP', '哥伦比亚比索': 'COP',
        '墨西哥比索': 'MXN', '秘鲁索尔': 'PEN', '保加利亚列弗': 'BGN',
        '捷克克朗': 'CZK', '匈牙利福林': 'HUF', '波兰兹罗提': 'PLN',
        '罗马尼亚列伊': 'RON', '俄罗斯卢布': 'RUB', '以色列新谢克尔': 'ILS',
        '沙特里亚尔': 'SAR', '南非兰特': 'ZAR', '土耳其里拉': 'TRY',
        '阿联酋迪拉姆': 'AED', '人民币': 'CNY', '印度卢比': 'INR',
        '印尼卢比': 'IDR', '菲律宾比索': 'PHP', '越南盾': 'VND',
        '埃及镑': 'EGP', '尼日利亚奈拉': 'NGN', '巴基斯坦卢比': 'PKR',
        '哈萨克斯坦坚戈': 'KZT', '坦桑尼亚先令': 'TZS',
        '卡塔尔里亚尔': 'QAR',  # 卡塔尔
        '新土耳其里拉': 'TRY',  # 土耳其
        '秘鲁索尔': 'PEN',    # 秘鲁
        '巴西雷亚尔': 'BRL',  # 巴西
        '智利比索': 'CLP',    # 智利
        '哥伦比亚比索': 'COP', # 哥伦比亚
        '墨西哥比索': 'MXN',  # 墨西哥
        '菲律宾比索': 'PHP',  # 菲律宾
        '越南盾': 'VND',      # 越南
        '印尼卢比': 'IDR',    # 印尼
        '印度卢比': 'INR',    # 印度
        '哈萨克斯坦坚戈': 'KZT', # 哈萨克斯坦
        '坦桑尼亚先令': 'TZS', # 坦桑尼亚
        '南非兰特': 'ZAR',    # 南非
        '沙特里亚尔': 'SAR',  # 沙特阿拉伯
        '俄罗斯卢布': 'RUB',  # 俄罗斯
        '罗马尼亚列伊': 'RON' # 罗马尼亚
    }
    return currency_map.get(currency)

def clean_price(price_str):
    """清理价格字符串"""
    # 移除所有空格
    price_str = ''.join(price_str.split())
    
    # 处理特殊格式的价格
    special_formats = {
        'S/.': '',     # 秘鲁索尔
        'R$': '',      # 巴西雷亚尔
        'Rs.': '',     # 印度卢比
        'Rs': '',      # 印度卢比
        'Rp': '',      # 印尼卢比
        'NT$': '',     # 新台币
        'HK$': '',     # 港币
        'S$': '',      # 新加坡元
        'RM': '',      # 马来西亚林吉特
        'CHF': '',     # 瑞士法郎
        'AED': '',     # 阿联酋迪拉姆
        'zł': '',      # 波兰兹罗提
        'lei': '',     # 罗马尼亚列伊
        'p.': '',      # 俄罗斯卢布
        'TL': '',      # 土耳其里拉
        'TSh': '',     # 坦桑尼亚先令
    }
    
    # 移除货币符号
    symbols = ['$', '€', '£', '¥', '₪', 'лв', 'Kč', 'kr', 'Ft', '₱', '฿', '₫', 
               '₦', '₸', '﷼', 'R', '₩']
    
    # 先处理特殊格式
    for format_str, replace_str in special_formats.items():
        if format_str in price_str:
            price_str = price_str.replace(format_str, replace_str)
    
    # 再移除货币符号
    for symbol in symbols:
        price_str = price_str.replace(symbol, '')
    
    # 移除千位分隔符
    price_str = price_str.replace(',', '')
    
    # 确保小数点格式正确
    if '.' in price_str:
        # 如果有多个小数点，只保留最后一个
        parts = price_str.split('.')
        price_str = ''.join(parts[:-1]) + '.' + parts[-1]
    
    # 移除所有非数字和小数点的字符
    price_str = ''.join(c for c in price_str if c.isdigit() or c == '.')
    
    return price_str.strip()

def convert_price_to_rmb(price_str, currency, rates):
    """将价格转换为人民币"""
    try:
        # 清理价格字符串
        clean_price_str = clean_price(price_str)
        price = float(clean_price_str)
        
        # 获取货币代码
        currency_code = get_currency_code(currency)
        if not currency_code:
            logging.warning(f"未知货币类型: {currency}")
            return None
            
        # 获取汇率并转换
        if currency_code in rates:
            rate = rates[currency_code]
            rmb_price = price / rate
            return round(rmb_price, 2)
        else:
            logging.warning(f"未找到汇率: {currency_code}")
            return None
            
    except ValueError as e:
        logging.error(f"价格格式错误: {price_str} - {str(e)}")
        return None
    except Exception as e:
        logging.error(f"价格转换失败: {str(e)}")
        return None

def convert_prices():
    """转换所有价格为人民币"""
    try:
        base_dir = Path(__file__).parent.parent
        today = datetime.now().strftime("%Y%m%d")
        
        # 修改输入文件路径
        input_file = base_dir / 'public' / 'json' / f'icloud_prices_{today}.json'
        with open(input_file, 'r', encoding='utf-8') as f:
            price_data = json.load(f)
        
        # 获取汇率
        rates = get_exchange_rates()
        
        # 创建新的价格数据结构
        rmb_prices = {
            'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'exchange_rates_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'countries': {}
        }
        
        # 转换每个国家的价格
        for country, prices in price_data['countries'].items():
            currency = country.split('(')[1].split(')')[0].strip()
            rmb_prices['countries'][country] = {}
            
            for plan, price in prices.items():
                rmb_price = convert_price_to_rmb(price, currency, rates)
                if rmb_price:
                    rmb_prices['countries'][country][plan] = f"¥{rmb_price}"
        
        # 修改输出文件路径
        output_file = base_dir / 'public' / 'json' / f'icloud_prices_rmb_{today}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(rmb_prices, f, ensure_ascii=False, indent=2)
            
        logging.info(f"价格转换完成，已保存到 {output_file}")
        
    except Exception as e:
        logging.error(f"价格转换过程失败: {str(e)}")
        raise

if __name__ == '__main__':
    convert_prices()