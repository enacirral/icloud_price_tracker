import { useEffect, useState } from 'react'
import Head from 'next/head'

export default function Home() {
  const [priceData, setPriceData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    // 获取今天的日期
    const today = new Date().toISOString().split('T')[0].replace(/-/g, '')
    
    // 直接获取生成的HTML文件
    fetch(`/html/icloud_prices_sorted_${today}.html`)
      .then(res => {
        if (!res.ok) {
          throw new Error('数据加载失败')
        }
        return res.text()
      })
      .then(html => {
        // 提取需要的内容
        const container = html.match(/<div class="container">([\s\S]*?)<\/div>/)?.[1]
        if (container) {
          setPriceData(container)
        } else {
          throw new Error('数据格式错误')
        }
      })
      .catch(err => {
        console.error('Error:', err)
        setError(err.message)
      })
  }, [])

  return (
    <>
      <Head>
        <title>iCloud 全球价格比较</title>
        <meta name="description" content="实时追踪全球 iCloud 存储价格" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="page">
        {error ? (
          <div className="error">
            {error}
          </div>
        ) : priceData ? (
          <div dangerouslySetInnerHTML={{ __html: priceData }} />
        ) : (
          <div className="loading">加载中...</div>
        )}
        
        <style jsx global>{`
          .page {
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
          }
          .error {
            color: #ff3b30;
            text-align: center;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          }
          .loading {
            text-align: center;
            padding: 20px;
            color: #666;
          }
        `}</style>
      </div>
    </>
  )
}