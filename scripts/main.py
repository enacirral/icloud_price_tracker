import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scripts.config import Config
from scripts.fetcher import ICloudPriceFetcher
from scripts.converter import PriceConverter
from scripts.generator import ReportGenerator

class PriceManager:
    """iCloud价格管理器"""
    
    def __init__(self):
        """初始化各个模块"""
        self.fetcher = ICloudPriceFetcher()
        self.converter = PriceConverter()
        self.generator = ReportGenerator()
        
    def run(self):
        """执行完整的数据处理流程"""
        try:
            # 确保必要的目录存在
            Config.ensure_dirs()
            today = Config.get_today_str()
            
            # 1. 获取原始数据
            raw_data = self.fetcher.fetch()
            self._save_json(raw_data, f'icloud_prices_{today}.json')
            
            # 2. 转换价格
            converted_data = self.converter.convert_prices(raw_data)
            self._save_json(converted_data, f'icloud_prices_rmb_{today}.json')
            
            # 3. 生成报告
            html_content = self.generator.generate_report(converted_data)
            self._save_html(html_content, f'icloud_prices_sorted_{today}.html')
            
        except Exception as e:
            print(f"处理失败: {str(e)}")
            raise
            
    def _save_json(self, data: dict, filename: str):
        """保存JSON数据"""
        try:
            filepath = Config.JSON_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"JSON数据已保存到: {filepath}")
        except Exception as e:
            print(f"保存JSON数据失败: {str(e)}")
            raise
            
    def _save_html(self, content: str, filename: str):
        """保存HTML报告"""
        try:
            # 保存日期版本
            filepath = Config.HTML_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"HTML报告已保存到: {filepath}")
            
            # 同时保存 latest 版本
            latest_path = Config.HTML_DIR / 'icloud_prices_sorted_latest.html'
            with open(latest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"最新HTML报告已保存到: {latest_path}")
        except Exception as e:
            print(f"保存HTML报告失败: {str(e)}")
            raise

def main():
    """主程序入口"""
    lock_file = Path(Config.BASE_DIR) / '.running'
    if lock_file.exists():
        print("另一个实例正在运行")
        return
    
    try:
        lock_file.touch()
        manager = PriceManager()
        manager.run()
    except Exception as e:
        print(f"程序执行失败: {str(e)}")
        exit(1)
    finally:
        lock_file.unlink(missing_ok=True)

if __name__ == '__main__':
    main()