from datetime import datetime
from operator import itemgetter

class ReportGenerator:
    """HTML报告生成器"""
    
    def generate_report(self, price_data: dict) -> str:
        """生成HTML报告"""
        sorted_prices = self._sort_prices(price_data)
        table_content = self._generate_table(sorted_prices)
        html_content = self._generate_html(
            table_content,
            price_data['fetch_time'],
            price_data.get('exchange_rates_time', '-')
        )
        return html_content
            
    def _sort_prices(self, price_data: dict) -> list:
        """对价格数据进行排序"""
        country_prices = []
        for country, prices in price_data['countries'].items():
            min_price = float('inf')
            for price in prices.values():
                try:
                    price_value = float(price.replace('¥', '').replace(',', ''))
                    min_price = min(min_price, price_value)
                except (ValueError, AttributeError):
                    continue
            
            if min_price != float('inf'):
                country_prices.append({
                    'country': country,
                    'prices': prices,
                    'min_price': min_price
                })
        
        return sorted(country_prices, key=itemgetter('min_price'))
            
    def _generate_table(self, sorted_prices: list) -> str:
        """生成价格表格HTML"""
        rows = []
        for item in sorted_prices:
            prices = item['prices']
            row = f"""
                <tr>
                    <td class="country-name">{item['country']}</td>
                    <td class="price">{prices.get('50GB', '-')}</td>
                    <td class="price">{prices.get('200GB', '-')}</td>
                    <td class="price">{prices.get('2TB', '-')}</td>
                    <td class="price">{prices.get('6TB', '-')}</td>
                    <td class="price">{prices.get('12TB', '-')}</td>
                </tr>"""
            rows.append(row)
        return '\n'.join(rows)
            
    def _generate_html(self, table_content: str, fetch_time: str, exchange_time: str) -> str:
        """生成完整的HTML内容"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iCloud 全球价格比较</title>
    <style>
        :root {{
            --primary-color: #0071e3;
            --background-color: #f5f5f7;
            --text-color: #1d1d1f;
            --secondary-text: #86868b;
            --border-color: #d2d2d7;
            --hover-color: #f5f5f7;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Icons", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 1200px;
            margin: 20px auto;
            padding: 0 20px;
        }}

        .card {{
            background: white;
            border-radius: 18px;
            box-shadow: var(--card-shadow);
            padding: 30px;
            margin-bottom: 20px;
            overflow: hidden;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 1rem;
            background: linear-gradient(120deg, var(--primary-color), #00a0dc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 20px 0;
        }}

        .update-info {{
            text-align: center;
            color: var(--secondary-text);
            margin-bottom: 2rem;
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        .table-container {{
            overflow-x: auto;
            margin: 0 -30px;
            padding: 0 30px;
        }}

        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 1rem;
        }}

        th, td {{
            padding: 1rem;
            text-align: right;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }}

        th {{
            background: white;
            color: var(--secondary-text);
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        .country-name {{
            text-align: left;
            font-weight: 500;
            position: sticky;
            left: 0;
            background: white;
            z-index: 5;
        }}

        .price {{
            font-family: "SF Mono", SFMono-Regular, ui-monospace, Menlo, Monaco, monospace;
            font-size: 0.95rem;
            color: var(--text-color);
        }}

        tr:hover {{
            background-color: var(--hover-color);
        }}

        tr:hover .country-name {{
            background-color: var(--hover-color);
        }}

        /* 响应式设计 */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
                margin: 10px;
            }}

            .card {{
                padding: 15px;
                border-radius: 12px;
            }}

            h1 {{
                font-size: 1.8rem;
                padding: 15px 0;
            }}

            .update-info {{
                font-size: 0.85rem;
                margin-bottom: 1.5rem;
            }}

            th, td {{
                padding: 0.8rem;
                font-size: 0.9rem;
            }}

            .price {{
                font-size: 0.85rem;
            }}
        }}

        @media (max-width: 480px) {{
            h1 {{
                font-size: 1.5rem;
            }}

            .card {{
                padding: 10px;
            }}

            th, td {{
                padding: 0.6rem;
                font-size: 0.8rem;
            }}

            .price {{
                font-size: 0.8rem;
            }}
        }}

        /* 暗色模式支持 */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --background-color: #000000;
                --text-color: #f5f5f7;
                --secondary-text: #86868b;
                --border-color: #38383d;
                --hover-color: #1c1c1e;
            }}

            .card {{
                background: #1c1c1e;
            }}

            th, .country-name {{
                background: #1c1c1e;
            }}

            tr:hover .country-name {{
                background-color: var(--hover-color);
            }}
        }}

        /* 添加排序相关样式 */
        th.sortable {{
            cursor: pointer;
            position: relative;
            padding-right: 1.5rem;
        }}

        th.sortable:hover {{
            background-color: var(--hover-color);
        }}

        th.sortable::after {{
            content: '⇅';
            position: absolute;
            right: 0.5rem;
            color: var(--secondary-text);
            opacity: 0.5;
        }}

        th.sortable.asc::after {{
            content: '↑';
            opacity: 1;
        }}

        th.sortable.desc::after {{
            content: '↓';
            opacity: 1;
        }}

        /* 添加动画效果 */
        tbody tr {{
            transition: background-color 0.2s ease;
        }}

        .highlight {{
            background-color: var(--hover-color);
            transition: background-color 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>iCloud 全球价格比较</h1>
            <div class="update-info">
                <div>数据更新时间：{fetch_time}</div>
                <div>汇率更新时间：{exchange_time}</div>
            </div>
            <div class="table-container">
                <table id="priceTable">
                    <thead>
                        <tr>
                            <th class="country-name">国家/地区</th>
                            <th class="sortable" data-column="50GB">50GB</th>
                            <th class="sortable" data-column="200GB">200GB</th>
                            <th class="sortable" data-column="2TB">2TB</th>
                            <th class="sortable" data-column="6TB">6TB</th>
                            <th class="sortable" data-column="12TB">12TB</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_content}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const table = document.getElementById('priceTable');
        const headers = table.querySelectorAll('th.sortable');
        let currentSort = {{
            column: null,
            direction: 'asc'
        }};

        // 价格转换函数
        function extractPrice(priceStr) {{
            return parseFloat(priceStr.replace('¥', '').replace(',', '')) || 0;
        }}

        // 排序函数
        function sortTable(column) {{
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const columnIndex = Array.from(headers).findIndex(h => h.dataset.column === column) + 1;
            
            // 重置所有表头的排序标记
            headers.forEach(header => {{
                if (header.dataset.column !== column) {{
                    header.classList.remove('asc', 'desc');
                }}
            }});

            // 确定排序方向
            let direction = 'asc';
            const header = table.querySelector(`th[data-column="${{column}}"]`);
            
            if (currentSort.column === column) {{
                direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            }}

            // 更新排序状态
            currentSort.column = column;
            currentSort.direction = direction;

            // 更新表头样式
            header.classList.remove('asc', 'desc');
            header.classList.add(direction);

            // 执行排序
            rows.sort((a, b) => {{
                const aValue = extractPrice(a.cells[columnIndex].textContent);
                const bValue = extractPrice(b.cells[columnIndex].textContent);
                
                if (isNaN(aValue)) return 1;  // 无效价格放到最后
                if (isNaN(bValue)) return -1;
                
                return direction === 'asc' 
                    ? aValue - bValue
                    : bValue - aValue;
            }});

            // 清空表格并重新填充排序后的行
            tbody.innerHTML = '';
            rows.forEach(row => {{
                row.classList.add('highlight');
                tbody.appendChild(row);
                // 移除高亮效果
                setTimeout(() => row.classList.remove('highlight'), 300);
            }});
        }}

        // 添加点击事件监听器
        headers.forEach(header => {{
            header.addEventListener('click', () => {{
                const column = header.dataset.column;
                sortTable(column);
            }});
        }});
    }});
    </script>
</body>
</html>"""