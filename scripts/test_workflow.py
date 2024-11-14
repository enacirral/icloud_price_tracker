import os
import sys
import logging
from datetime import datetime
from pathlib import Path

def setup_directories():
    """创建必要的目录结构"""
    try:
        base_dir = Path(__file__).parent.parent
        directories = [
            base_dir / 'public' / 'json',
            base_dir / 'public' / 'json' / 'archive',
            base_dir / 'public' / 'html',
            base_dir / 'public' / 'html' / 'archive',
            base_dir / 'logs'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {directory}")
            
        return base_dir / 'logs' / 'workflow_test.log'
            
    except Exception as e:
        print(f"创建目录失败: {str(e)}")
        raise

def setup_logging(log_file):
    """配置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def run_workflow():
    """运行完整的工作流程"""
    try:
        # 记录开始时间
        start_time = datetime.now()
        logging.info("开始执行工作流程")
        
        # 获取基础路径
        base_dir = Path(__file__).parent.parent
        today = datetime.now().strftime("%Y%m%d")
        
        # 1. 抓取价格数据
        logging.info("步骤 1: 抓取 iCloud 价格数据")
        import icloud_price_fetcher
        icloud_price_fetcher.fetch_icloud_prices()
        
        # 2. 转换货币
        logging.info("步骤 2: 转换货币到人民币")
        import currency_converter
        currency_converter.convert_prices()
        
        # 3. 生成HTML报告
        logging.info("步骤 3: 生成HTML报告")
        import price_sorter
        price_sorter.main()
        
        # 4. 检查文件是否生成
        files_to_check = [
            base_dir / 'public' / 'json' / f'icloud_prices_{today}.json',
            base_dir / 'public' / 'json' / f'icloud_prices_rmb_{today}.json',
            base_dir / 'public' / 'html' / f'icloud_prices_sorted_{today}.html'
        ]
        
        for file_path in files_to_check:
            if file_path.exists():
                file_size = file_path.stat().st_size
                logging.info(f"文件已生成: {file_path} (大小: {file_size/1024:.2f}KB)")
            else:
                logging.error(f"文件未生成: {file_path}")
        
        # 记录完成时间和总耗时
        end_time = datetime.now()
        duration = end_time - start_time
        logging.info(f"工作流程执行完成，总耗时: {duration}")
        
    except Exception as e:
        logging.error(f"工作流程执行失败: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    try:
        # 1. 设置目录结构
        log_file = setup_directories()
        
        # 2. 配置日志
        setup_logging(log_file)
        
        # 3. 运行工作流程
        run_workflow()
        
        logging.info("本地测试完成")
        sys.exit(0)
    except Exception as e:
        print(f"测试失败: {str(e)}")
        sys.exit(1)