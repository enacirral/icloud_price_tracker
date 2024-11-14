import json
from datetime import datetime
from operator import itemgetter
from pathlib import Path
import logging

# 配置日志
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'price_sorter.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def load_price_data(filename):
    """加载价格数据"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def sort_prices(price_data):
    """对价格数据进行排序"""
    # 存储所有国家的价格信息
    country_prices = {}
    
    # 收集每个国家的最低价格（用于排序）
    for country, prices in price_data['countries'].items():
        min_price = float('inf')
        for price in prices.values():
            price_value = float(price.replace('¥', ''))
            min_price = min(min_price, price_value)
        
        country_prices[country] = {
            'country': country,
            'prices': prices,
            'min_price': min_price
        }
    
    # 按最低价格排序
    return sorted(country_prices.values(), key=lambda x: x['min_price'])

def generate_html(sorted_prices, price_data):
    """生成HTML报告"""
    html_template = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>iCloud 全球价格比较</title>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f7;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 20px;
            }}
            h1 {{
                color: #1d1d1f;
                text-align: center;
                margin-bottom: 30px;
            }}
            .update-info {{
                text-align: center;
                color: #666;
                margin-bottom: 20px;
                font-size: 0.9em;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: white;
            }}
            th, td {{
                padding: 12px;
                text-align: right;
                border-bottom: 1px solid #e6e6e6;
            }}
            th {{
                background: #f5f5f7;
                color: #1d1d1f;
                font-weight: 500;
            }}
            .country-name {{
                text-align: left;
            }}
            tr:hover {{
                background-color: #f5f5f7;
            }}
            .price {{
                font-family: monospace;
                font-size: 0.95em;
            }}
            @media (max-width: 768px) {{
                body {{
                    padding: 10px;
                }}
                .container {{
                    padding: 10px;
                }}
                th, td {{
                    padding: 8px;
                    font-size: 0.9em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>iCloud 全球价格比较</h1>
            <div class="update-info">
                数据更新时间：{fetch_time}<br>
                汇率更新时间：{exchange_time}
            </div>
            <table>
                <thead>
                    <tr>
                        <th class="country-name">国家/地区</th>
                        <th>50GB</th>
                        <th>200GB</th>
                        <th>2TB</th>
                        <th>6TB</th>
                        <th>12TB</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    # 生成表格内容
    table_content = ""
    for country_data in sorted_prices:
        prices = country_data['prices']
        table_content += f'''
            <tr>
                <td class="country-name">{country_data['country']}</td>
                <td class="price">{prices.get('50GB', '-')}</td>
                <td class="price">{prices.get('200GB', '-')}</td>
                <td class="price">{prices.get('2TB', '-')}</td>
                <td class="price">{prices.get('6TB', '-')}</td>
                <td class="price">{prices.get('12TB', '-')}</td>
            </tr>
        '''
    
    html_content = html_template.format(
        fetch_time=price_data['fetch_time'],
        exchange_time=price_data.get('exchange_rates_time', '-')
    )
    
    html_content += table_content + '''
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''
    
    return html_content

def main():
    base_dir = Path(__file__).parent.parent
    today = datetime.now().strftime("%Y%m%d")
    
    # 读取价格数据
    input_file = base_dir / 'public' / 'json' / f'icloud_prices_rmb_{today}.json'
    price_data = load_price_data(input_file)
    
    # 排序价格
    sorted_prices = sort_prices(price_data)
    
    # 生成HTML
    html_content = generate_html(sorted_prices, price_data)
    
    # 保存HTML文件
    output_file = base_dir / 'public' / 'html' / f'icloud_prices_sorted_{today}.html'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    main() 