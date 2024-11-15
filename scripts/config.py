from pathlib import Path
from datetime import datetime

class Config:
    """配置管理类"""
    # 基础路径配置
    BASE_DIR = Path(__file__).parent.parent
    PUBLIC_DIR = BASE_DIR / 'public'
    JSON_DIR = PUBLIC_DIR / 'json'
    HTML_DIR = PUBLIC_DIR / 'html'
    
    # API配置
    ICLOUD_URL = 'https://support.apple.com/zh-cn/108047'
    EXCHANGE_RATE_API = 'https://api.exchangerate-api.com/v4/latest/CNY'
    
    # 请求头
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 货币代码映射
    CURRENCY_MAP = {
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
        '埃及镑': 'EGP', '尼日利亚奈拉': 'NGN',
        '巴基斯坦卢比': 'PKR', '卡塔尔里亚尔': 'QAR', '坦桑尼亚先令': 'TZS',
        '哈萨克斯坦坚戈': 'KZT'
    }
    
    @staticmethod
    def ensure_dirs():
        """确保必要的目录存在"""
        for dir_path in [Config.JSON_DIR, Config.HTML_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_today_str() -> str:
        """获取今天的日期字符串"""
        return datetime.now().strftime("%Y%m%d")
    
    @staticmethod
    def get_datetime_str() -> str:
        """获取当前时间字符串"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
