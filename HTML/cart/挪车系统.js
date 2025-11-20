// 环境变量配置说明（需在Cloudflare Workers设置中添加）
/*
环境变量清单：
1. PHONE_NUMBER     [string]  必需 - 车主联系电话（示例：+8613812345678）
2. SITE_ICON_URL    [string]  可选 - 网站图标URL（建议尺寸：48x48px）
3. LICENSE_PLATE    [string]  可选 - 车牌号码（示例：京A12345）
4. PUSHPLUS_TOKEN   [string]  必需 - PushPlus推送服务的API令牌
*/

// IP频率限制存储（内存中，重启后清空）
const ipRateLimit = new Map();
const RATE_LIMIT_WINDOW = 60 * 1000; // 1分钟（毫秒）
const RATE_LIMIT_MAX_REQUESTS = 5; // 最多5次

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
  // 获取客户端IP地址
  const clientIP = getClientIP(request);
  console.log(`请求来自IP: ${clientIP}`);
  
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
          "Cache-Control": "max-age=300",
          ...corsHeaders(),
        },
      }
    );
  }

  // 处理 POST 请求 - 发送通知
  if (request.method === "POST") {
    try {
      // 环境变量验证
      if (!env.PUSHPLUS_TOKEN) {
        return jsonResponse({ success: false, message: "环境变量 PUSHPLUS_TOKEN 未配置" }, 500);
      }
      
      // IP频率限制检查
      const rateLimitResult = checkRateLimit(clientIP);
      if (!rateLimitResult.allowed) {
        console.log(`IP ${clientIP} 发送频率超限，剩余时间: ${Math.ceil(rateLimitResult.resetTime / 1000)}秒`);
        return jsonResponse({ 
          success: false, 
          message: `发送过于频繁，请等待 ${Math.ceil(rateLimitResult.resetTime / 1000)} 秒后重试（1分钟内最多5次）` 
        }, 429);
      }
      
      const { type, message } = await request.json();
      
      if (type === "message") {
        // 输入验证
        if (!message || message.trim().length === 0) {
          return jsonResponse({ success: false, message: "消息内容不能为空" }, 400);
        }
        
        if (message.length > 500) {
          return jsonResponse({ success: false, message: "消息长度不能超过500字符" }, 400);
        }
        
        // 发送通知（优化消息布局）
        const notificationContent = `
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333;">
  <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
    <h3 style="margin: 0 0 10px; color: #1a1a1a; font-size: 18px;">🚗 挪车通知</h3>
    <div style="font-size: 16px; color: #333; background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #3b82f6;">
      ${message.replace(/\n/g, '<br>')}
    </div>
  </div>
  
  <div style="font-size: 11px; color: #999; padding: 8px; background: #f8f9fa; border-radius: 4px; border-top: 1px solid #e0e0e0; margin-top: 10px;">
    <div style="opacity: 0.7;">📍 发送方IP: ${clientIP}</div>
    <div style="opacity: 0.7;">🕐 发送时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}</div>
  </div>
</div>`;
        
        await sendPushPlusNotification(
          env.PUSHPLUS_TOKEN,
          "挪车通知",
          notificationContent
        );
        
        // 记录成功发送
        recordRequest(clientIP);
        console.log(`消息发送成功，IP: ${clientIP}`);
        
        return jsonResponse({ success: true, message: "消息已发送" });
      }

      return jsonResponse({ success: false, message: "无效的请求类型" }, 400);
    } catch (error) {
      console.error(`发送失败，IP: ${clientIP}, 错误: ${error.message}`);
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

// 获取客户端IP地址
function getClientIP(request) {
  // 优先从 Cloudflare 头部获取真实IP
  const cfConnectingIP = request.headers.get('CF-Connecting-IP');
  if (cfConnectingIP) return cfConnectingIP;
  
  // 其他常见的IP头部
  const xForwardedFor = request.headers.get('X-Forwarded-For');
  if (xForwardedFor) return xForwardedFor.split(',')[0].trim();
  
  const xRealIP = request.headers.get('X-Real-IP');
  if (xRealIP) return xRealIP;
  
  // fallback到默认值
  return 'unknown';
}

// 检查IP频率限制
function checkRateLimit(ip) {
  const now = Date.now();
  const ipData = ipRateLimit.get(ip) || { requests: [], firstRequest: now };
  
  // 清理过期的请求记录（超过1分钟）
  ipData.requests = ipData.requests.filter(timestamp => now - timestamp < RATE_LIMIT_WINDOW);
  
  // 检查是否超过限制
  if (ipData.requests.length >= RATE_LIMIT_MAX_REQUESTS) {
    const oldestRequest = Math.min(...ipData.requests);
    const resetTime = oldestRequest + RATE_LIMIT_WINDOW - now;
    return { allowed: false, resetTime };
  }
  
  return { allowed: true };
}

// 记录请求
function recordRequest(ip) {
  const now = Date.now();
  const ipData = ipRateLimit.get(ip) || { requests: [], firstRequest: now };
  
  // 添加当前请求时间戳
  ipData.requests.push(now);
  
  // 清理过期记录
  ipData.requests = ipData.requests.filter(timestamp => now - timestamp < RATE_LIMIT_WINDOW);
  
  // 更新存储
  ipRateLimit.set(ip, ipData);
  
  // 定期清理Map以防内存泄漏（保留最近活跃的IP）
  if (ipRateLimit.size > 1000) {
    const cutoff = now - RATE_LIMIT_WINDOW * 2; // 保留2分钟内的记录
    for (const [ipKey, data] of ipRateLimit.entries()) {
      if (data.requests.length === 0 || Math.max(...data.requests) < cutoff) {
        ipRateLimit.delete(ipKey);
      }
    }
  }
}

// 推送通知功能
async function sendPushPlusNotification(token, title, content) {
  const response = await fetch("https://www.pushplus.plus/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      token,
      title,
      content,
      template: "html", // 使用HTML模板以支持样式
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
  // 环境变量验证
  if (!phoneNumber) {
    throw new Error('环境变量 PHONE_NUMBER 未配置');
  }
  
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
    
    .char-counter {
      text-align: right;
      margin-bottom: 16px;
      font-size: 14px;
      color: var(--secondary-color);
    }
    
    .char-counter.warning {
      color: var(--danger-color);
    }
    
    .loading {
      opacity: 0.6;
      pointer-events: none;
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
      <textarea id="messageInput" placeholder="请输入您要发送的信息..." maxlength="500"></textarea>
      <div class="char-counter">
        <span id="charCount">0</span>/500
      </div>
      <div class="template-buttons">
        <button onclick="useTemplate('default')">默认通知</button>
        <button onclick="useTemplate('polite')">礼貌通知</button>
        <button onclick="useTemplate('urgent')">紧急通知</button>
      </div>
      <div class="action-buttons">
        <button onclick="makeCall('${phoneNumber}')" class="call-button">拨打电话</button>
        <button id="sendBtn" onclick="sendMessage()" class="send-button">发送消息</button>
      </div>
      <div id="status"></div>
    </div>
  </div>
  <div class="footer">
    <p>由 Cloudflare Worker 提供技术支持</p>
  </div>
  <script>
    // 环境变量验证
    if (!('${phoneNumber}')) {
      throw new Error('环境变量验证失败：PHONE_NUMBER未配置');
    }
    
    // 优化后的 JavaScript 逻辑
    const templates = {
      default: "🔔 您好，有人需要您挪车，请及时处理。",
      polite: "🙏 您好，很抱歉打扰您。您的爱车可能影响到他人通行，请问方便移动一下吗？",
      urgent: "⚠️ 紧急！！！ 您的车辆需要立即移动，请尽快处理！"
    };
    
    let isLoading = false;

    function useTemplate(type) {
      const input = document.getElementById('messageInput');
      input.value = templates[type] || "";
      updateCharCount();
    }
    
    function updateCharCount() {
      const input = document.getElementById('messageInput');
      const counter = document.getElementById('charCount');
      const charCountContainer = document.querySelector('.char-counter');
      const count = input.value.length;
      
      counter.textContent = count;
      
      if (count > 450) {
        charCountContainer.classList.add('warning');
      } else {
        charCountContainer.classList.remove('warning');
      }
    }
    
    function makeCall(phoneNumber) {
      if (confirm('确定要拨打电话给车主吗？')) {
        window.location.href = 'tel:' + phoneNumber;
      }
    }
    
    function showStatus(message, isSuccess = true) {
      const status = document.getElementById('status');
      status.innerHTML = (isSuccess ? '✅' : '⚠️') + ' ' + message;
      status.style.color = isSuccess ? 'var(--success-color)' : 'var(--danger-color)';
      
      setTimeout(() => {
        status.innerHTML = '';
      }, 3000);
    }

    async function sendMessage() {
      if (isLoading) return;
      
      const message = document.getElementById('messageInput').value.trim();
      const sendBtn = document.getElementById('sendBtn');
      
      // 输入验证
      if (!message) {
        showStatus('请输入要发送的信息', false);
        return;
      }
      
      if (message.length > 500) {
        showStatus('消息长度不能超过500字符', false);
        return;
      }
      
      isLoading = true;
      sendBtn.classList.add('loading');
      sendBtn.textContent = '发送中...';
      
      try {
        const response = await fetch('', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ type: 'message', message })
        });
        
        const result = await response.json();
        showStatus(result.success ? '消息发送成功' : result.message, result.success);
        
        if (result.success) {
          document.getElementById('messageInput').value = '';
          updateCharCount();
        }
      } catch (e) {
        showStatus('发送失败，请重试', false);
      } finally {
        isLoading = false;
        sendBtn.classList.remove('loading');
        sendBtn.textContent = '发送消息';
      }
    }
    
    // 初始化
    document.addEventListener('DOMContentLoaded', function() {
      const input = document.getElementById('messageInput');
      
      // 实时字符计数
      input.addEventListener('input', updateCharCount);
      
      // 键盘快捷键：Ctrl+Enter 发送
      input.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
          e.preventDefault();
          sendMessage();
        }
      });
      
      // 初始化字符计数（输入框为空）
      updateCharCount();
    });
  </script>
</body>
</html>`;
}