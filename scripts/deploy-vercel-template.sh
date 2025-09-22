#!/bin/bash
# Vercel模板部署脚本

echo "🚀 开始部署Vercel AI模板..."

# 1. 检查必要工具
echo "🔍 检查必要工具..."
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI未安装，正在安装..."
    npm install -g vercel
fi

if ! command -v npx &> /dev/null; then
    echo "❌ npm未安装，请先安装Node.js"
    exit 1
fi

# 2. 创建前端项目目录
echo "📁 创建前端项目目录..."
mkdir -p frontend
cd frontend

# 3. 部署Pinecone模板
echo "🎯 部署Pinecone - Vercel AI SDK Starter模板..."
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm

# 4. 安装Pinecone相关依赖
echo "📦 安装Pinecone和AI SDK依赖..."
npm install @pinecone-database/pinecone @vercel/ai openai

# 5. 创建基础配置文件
echo "⚙️ 创建配置文件..."
cat > .env.local.example << 'EOF'
# Pinecone配置
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=firecrawl-data

# OpenAI配置
OPENAI_API_KEY=your_openai_api_key

# 后端API配置
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_KEY=your_api_key
EOF

# 6. 创建基础页面结构
echo "📄 创建基础页面结构..."
mkdir -p src/app/api/pinecone
mkdir -p src/components/data-collection
mkdir -p src/components/ai-chat
mkdir -p src/lib

# 7. 创建Pinecone API路由
cat > src/app/api/pinecone/route.ts << 'EOF'
import { NextRequest, NextResponse } from 'next/server';
import { Pinecone } from '@pinecone-database/pinecone';

const pc = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY!,
});

export async function POST(request: NextRequest) {
  try {
    const { query, topK = 5 } = await request.json();
    
    const index = pc.index(process.env.PINECONE_INDEX_NAME!);
    const queryResponse = await index.query({
      vector: query,
      topK,
      includeMetadata: true,
    });

    return NextResponse.json(queryResponse);
  } catch (error) {
    console.error('Pinecone query error:', error);
    return NextResponse.json({ error: 'Query failed' }, { status: 500 });
  }
}
EOF

# 8. 创建数据采集组件
cat > src/components/data-collection/DataCollectionDashboard.tsx << 'EOF'
'use client';

import { useState, useEffect } from 'react';

interface CollectionTask {
  id: string;
  url: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  result?: any;
}

export default function DataCollectionDashboard() {
  const [tasks, setTasks] = useState<CollectionTask[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const startCollection = async (url: string) => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/collect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      
      if (response.ok) {
        const newTask = await response.json();
        setTasks(prev => [...prev, newTask]);
      }
    } catch (error) {
      console.error('Collection failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">数据采集仪表板</h1>
      
      <div className="mb-6">
        <input
          type="url"
          placeholder="输入要采集的URL"
          className="w-full p-3 border rounded-lg mr-4"
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              startCollection(e.currentTarget.value);
            }
          }}
        />
        <button
          onClick={() => {
            const input = document.querySelector('input[type="url"]') as HTMLInputElement;
            if (input.value) startCollection(input.value);
          }}
          disabled={isLoading}
          className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
        >
          {isLoading ? '采集中...' : '开始采集'}
        </button>
      </div>

      <div className="grid gap-4">
        {tasks.map((task) => (
          <div key={task.id} className="p-4 border rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium">{task.url}</span>
              <span className={`px-2 py-1 rounded text-sm ${
                task.status === 'completed' ? 'bg-green-100 text-green-800' :
                task.status === 'failed' ? 'bg-red-100 text-red-800' :
                'bg-yellow-100 text-yellow-800'
              }`}>
                {task.status}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${task.progress}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
EOF

# 9. 创建AI聊天组件
cat > src/components/ai-chat/AIChat.tsx << 'EOF'
'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';

export default function AIChat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">AI数据助手</h2>
      
      <div className="border rounded-lg p-4 h-96 overflow-y-auto mb-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-2 p-2 rounded ${
              message.role === 'user'
                ? 'bg-blue-100 ml-8'
                : 'bg-gray-100 mr-8'
            }`}
          >
            <strong>{message.role === 'user' ? '你' : 'AI'}:</strong>
            <p className="mt-1">{message.content}</p>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="询问关于采集数据的问题..."
          className="flex-1 p-2 border rounded-lg"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          发送
        </button>
      </form>
    </div>
  );
}
EOF

# 10. 更新主页面
cat > src/app/page.tsx << 'EOF'
import DataCollectionDashboard from '@/components/data-collection/DataCollectionDashboard';
import AIChat from '@/components/ai-chat/AIChat';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <DataCollectionDashboard />
      <div className="mt-8">
        <AIChat />
      </div>
    </main>
  );
}
EOF

# 11. 创建README
cat > README.md << 'EOF'
# Firecrawl AI前端

基于Vercel AI SDK和Pinecone的现代化数据采集平台前端。

## 功能特性

- 🤖 AI驱动的数据查询
- 📊 实时数据可视化
- 🔍 语义搜索
- 💬 智能聊天助手
- 📱 响应式设计

## 快速开始

1. 安装依赖：
```bash
npm install
```

2. 配置环境变量：
```bash
cp .env.local.example .env.local
# 编辑.env.local文件，填入你的API密钥
```

3. 启动开发服务器：
```bash
npm run dev
```

4. 访问 http://localhost:3000

## 部署到Vercel

1. 安装Vercel CLI：
```bash
npm install -g vercel
```

2. 部署：
```bash
vercel
```

## 环境变量

- `PINECONE_API_KEY`: Pinecone API密钥
- `PINECONE_ENVIRONMENT`: Pinecone环境
- `PINECONE_INDEX_NAME`: Pinecone索引名称
- `OPENAI_API_KEY`: OpenAI API密钥
- `NEXT_PUBLIC_API_URL`: 后端API地址
- `NEXT_PUBLIC_API_KEY`: 后端API密钥
EOF

echo "✅ Vercel模板部署完成！"
echo ""
echo "📋 下一步操作："
echo "1. cd frontend"
echo "2. cp .env.local.example .env.local"
echo "3. 编辑.env.local文件，填入API密钥"
echo "4. npm run dev"
echo ""
echo "🌐 访问 http://localhost:3000 查看效果"
echo "🚀 运行 'vercel' 部署到生产环境"
