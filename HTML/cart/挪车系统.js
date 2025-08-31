// 环境变量配置说明（需在Cloudflare Workers设置中添加）
/*
环境变量清单：
1. PHONE_NUMBER     [string]  必需 - 车主联系电话（示例：+8613812345678）
2. SITE_ICON_URL    [string]  可选 - 网站图标URL（建议尺寸：48x48px）
3. LICENSE_PLATE    [string]  可选 - 车牌号码（示例：京A12345）
4. PUSHPLUS_TOKEN   [string]  必需 - PushPlus推送服务的API令牌
*/

export default {
  async fetch(request, env) {
    try {
      return await handleRequest(request, env);
    } catch (e) {
      return new Response(`Error: ${e.message}`, { status: 500 });
    }
  }
};

async function handleRequest(request, env) {
  // 处理 CORS 预检请求
  if (request.method === "OPTIONS") {
    return corsResponse();
  }

  // 处理 GET 请求 - 返回 HTML 页面
  if (request.method === "GET") {
    return new Response(
      generateHTML(env.PHONE_NUMBER, env.SITE_ICON_URL, env.LICENSE_PLATE),
      {
        headers: {
          "Content-Type": "text/html;charset=UTF-8",
          ...corsHeaders(),
        },
      }
    );
  }

  // 处理 POST 请求 - 发送通知
  if (request.method === "POST") {
    try {
      const { type, message } = await request.json();
      
      if (type === "message") {
        await sendPushPlusNotification(
          env.PUSHPLUS_TOKEN,
          "挪车通知",
          message
        );
        return jsonResponse({ success: true, message: "消息已发送" });
      }

      return jsonResponse({ success: false, message: "无效的请求类型" }, 400);
    } catch (error) {
      return jsonResponse({ success: false, message: error.message }, 500);
    }
  }

  return new Response("Not Found", { status: 404 });
}

// 通用 CORS 头设置
function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

// CORS 预检响应
function corsResponse() {
  return new Response(null, { headers: corsHeaders() });
}

// 推送通知功能
async function sendPushPlusNotification(token, title, content) {
  const response = await fetch("http://www.pushplus.plus/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      token,
      title,
      content,
      template: "html",
    }),
  });

  if (!response.ok) throw new Error("推送通知失败");
  return response.json();
}

// JSON 响应生成器
function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(),
    },
  });
}

// HTML 页面生成
function generateHTML(phoneNumber, iconUrl, licensePlate) {
  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>通知车主挪车</title>
  <link rel="icon" href="${iconUrl}" type="image/x-icon">
  <style>
    :root {
      --primary-color: #1a1a1a;
      --secondary-color: #666;
      --border-color: #e0e0e0;
      --accent-color: #3b82f6;
      --danger-color: #ef4444;
      --success-color: #22c55e;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #ffffff;
      min-height: 100vh;
      margin: 0;
      padding: 40px 20px;
      color: var(--primary-color);
    }
    
    .container {
      max-width: 680px;
      margin: 0 auto;
      background: white;
      border-radius: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      border: 1px solid var(--border-color);
    }
    
    .header {
      padding: 32px 40px;
      border-bottom: 1px solid var(--border-color);
      text-align: center;
    }
    
    .header h1 {
      margin: 0 0 16px;
      font-size: 28px;
      font-weight: 600;
    }
    
    .header p {
      margin: 0;
      color: var(--secondary-color);
      font-size: 16px;
    }
    
    .content {
      padding: 32px 40px;
    }
    
    textarea#messageInput {
      width: 100%;
      padding: 16px;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      min-height: 120px;
      font-size: 16px;
      margin-bottom: 24px;
      box-sizing: border-box;
      resize: vertical;
      transition: border-color 0.2s;
    }
    
    textarea#messageInput:focus {
      outline: none;
      border-color: var(--accent-color);
    }
    
    .template-buttons, .action-buttons {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }
    
    button {
      padding: 12px 20px;
      border: none;
      border-radius: 8px;
      font-weight: 500;
      font-size: 15px;
      cursor: pointer;
      transition: all 0.2s;
    }
    
    .template-buttons button {
      background: #f3f4f6;
      color: var(--primary-color);
    }
    
    .template-buttons button:hover {
      background: #e5e7eb;
    }
    
    .call-button {
      background: var(--accent-color);
      color: white;
    }
    
    .call-button:hover {
      background: #2563eb;
    }
    
    .send-button {
      background: var(--success-color);
      color: white;
    }
    
    .send-button:hover {
      background: #16a34a;
    }
    
    .footer {
      padding: 24px;
      text-align: center;
      color: var(--secondary-color);
      font-size: 14px;
    }
    
    #status {
      margin-top: 16px;
      text-align: center;
      font-size: 14px;
    }
    
    @media (max-width: 640px) {
      .header, .content {
        padding: 24px;
      }
      
      .template-buttons, .action-buttons {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>通知车主挪车</h1>
      <p>车牌号：${licensePlate || '未提供'}</p>
    </div>
    <div class="content">
      <textarea id="messageInput" placeholder="请输入您要发送的信息..." maxlength="200"></textarea>
      <div class="template-buttons">
        <button onclick="useTemplate('default')">默认通知</button>
        <button onclick="useTemplate('polite')">礼貌通知</button>
        <button onclick="useTemplate('urgent')">紧急通知</button>
      </div>
      <div class="action-buttons">
        <button onclick="makeCall('${phoneNumber}')" class="call-button">拨打电话</button>
        <button onclick="sendMessage()" class="send-button">发送消息</button>
      </div>
      <div id="status"></div>
    </div>
  </div>
  <div class="footer">
    <p>由 Cloudflare Worker 提供技术支持</p>
  </div>
  <script>
    // 优化后的 JavaScript 逻辑
    const templates = {
      default: "您好，有人需要您挪车，请及时处理。",
      polite: "您好，很抱歉打扰您。您的爱车可能影响到他人通行，请问方便移动一下吗？",
      urgent: "紧急！！！ 您的车辆需要立即移动，请尽快处理！"
    };

    function useTemplate(type) {
      document.getElementById('messageInput').value = templates[type] || "";
    }

    async function sendMessage() {
      const message = document.getElementById('messageInput').value.trim();
      if (!message) return alert('请输入要发送的信息');
      
      try {
        const response = await fetch('', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ type: 'message', message })
        });
        
        const result = await response.json();
        alert(result.success ? '发送成功' : result.message);
      } catch (e) {
        alert('发送失败，请重试');
      }
    }

    useTemplate('default');
  </script>
</body>
</html>`;
}