# **通知车主挪车系统 使用说明**

## 微信版本


### 主要改进

1. **请求超时控制**
   - 添加了请求超时控制，默认设置为 30 秒。

2. **错误处理增强**
   - 添加了对非 JSON 响应的处理，确保能够正确处理不同类型的响应。
   - 处理了网络错误和超时错误，提供更好的用户体验。
   - 添加了更详细的错误信息，便于调试和排查问题。

3. **CORS 处理改进**
   - 添加了 OPTIONS 请求处理，确保跨域请求的顺利进行。
   - 添加了必要的 CORS 头，确保客户端能够正确访问 API。

4. **fetch 请求配置修改**
   - 添加了 Accept 头，以指定期望的响应格式。
   - 添加了错误状态检查，确保能够捕获并处理 HTTP 错误状态。

5. **前端代码改进**
   - 前端代码也添加了超时控制，确保用户在请求过程中不会长时间等待。
   - 增强了错误处理，提供更友好的错误提示。

### 使用说明

要使用更新后的代码，请按照以下步骤操作：

1. **环境变量设置**
   - 确保以下环境变量已正确设置：
     - `PUSHPLUS_TOKEN`：用于推送通知的令牌。
     - `PHONE_NUMBER`：接收通知的电话号码。
     - `SITE_ICON_URL`：网站图标的 URL。

2. **部署代码**
   - 在 Cloudflare Workers 中部署更新后的代码。

3. **测试**
   - 部署完成后，进行测试以确保所有功能正常运行，特别是请求超时和错误处理部分。

 ### 代码查看
脚本如下
```
// index.js
export default {
    async fetch(request, env, ctx) {
      try {
        return await handleRequest(request, env);
      } catch (e) {
        return new Response(`Error: ${e.message}`, { status: 500 });
      }
    }
  };
  
  async function handleRequest(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }
  
    if (request.method === "GET") {
      return new Response(generateHTML(env.PHONE_NUMBER, env.SITE_ICON_URL), {
        headers: {
          "Content-Type": "text/html;charset=UTF-8",
          "Access-Control-Allow-Origin": "*",
        },
      });
    }
  
    if (request.method === "POST") {
      try {
        const data = await request.json();
        const { type, message } = data;
  
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
  
  async function sendPushPlusNotification(token, title, content) {
    const response = await fetch("http://www.pushplus.plus/send", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token: token,
        title: title,
        content: content,
        template: "html",
      }),
    });
  
    if (!response.ok) {
      throw new Error('推送通知失败');
    }
  
    return response.json();
  }
  
  function jsonResponse(data, status = 200) {
    return new Response(JSON.stringify(data), {
      status,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }

  function generateHTML(phoneNumber, iconUrl) {
    return `
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="theme-color" content="#1e88e5">
      <title>通知车主挪车</title>
      <link rel="icon" href="${iconUrl}" type="image/x-icon">
      <style>
          :root {
              --primary-color: #1e88e5;
              --success-color: #43a047;
              --border-color: #e0e0e0;
              --bg-color: #f5f5f5;
              --text-color: #212121;
              --button-bg: #f8f9fa;
              --button-active-bg: #e0e0e0;
          }
          
          * {
              box-sizing: border-box;
              margin: 0;
              padding: 0;
          }
          
          body {
              font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
              line-height: 1.5;
              color: var(--text-color);
              background-color: var(--bg-color);
              padding: 24px;
              min-height: 100vh;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
          }
          
          .container {
              width: 100%;
              max-width: 600px;
              background: white;
              border-radius: 12px;
              box-shadow: 0 4px 16px rgba(0,0,0,0.1);
              overflow: hidden;
          }
          
          .header {
              background: var(--primary-color);
              padding: 24px;
              text-align: center;
              border-bottom: 1px solid var(--border-color);
          }
          
          .header h1 {
              color: white;
              font-size: 24px;
              font-weight: 600;
              margin: 0;
          }
          
          .content {
              padding: 24px;
          }
          
          .message-area {
              margin-bottom: 24px;
          }
          
          .textarea {
              width: 100%;
              padding: 16px;
              border: 1px solid var(--border-color);
              border-radius: 8px;
              resize: vertical;
              min-height: 150px;
              font-size: 16px;
              transition: border-color 0.2s ease;
              margin-bottom: 8px;
          }
          
          .textarea:focus {
              outline: none;
              border-color: var(--primary-color);
          }
          
          .char-count {
              text-align: right;
              color: #666;
              font-size: 14px;
          }
          
          .template-buttons {
              display: grid;
              grid-template-columns: repeat(3, 1fr);
              gap: 16px;
              margin: 24px 0;
          }
          
          .template-button {
              padding: 12px;
              border: 1px solid var(--border-color);
              border-radius: 8px;
              background: var(--button-bg);
              cursor: pointer;
              font-size: 14px;
              transition: background-color 0.2s ease;
          }
          
          .template-button:hover {
              background: var(--button-active-bg);
          }
          
          .action-buttons {
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 16px;
              margin-top: 24px;
          }
          
          .button {
              padding: 16px 24px;
              border: none;
              border-radius: 8px;
              cursor: pointer;
              font-size: 16px;
              font-weight: 600;
              color: var(--text-color);
              background: var(--button-bg);
              transition: background-color 0.2s ease;
              text-align: center;
              text-decoration: none;
              display: flex;
              align-items: center;
              justify-content: center;
              line-height: 1.4;
          }
          
          .button:active {
              background: var(--button-active-bg);
          }
          
          .button:disabled {
              opacity: 0.7;
              cursor: not-allowed;
          }
          
          .call-button:active {
              background: var(--success-color);
              color: white;
          }
          
          .send-button:active {
              background: var(--primary-color);
              color: white;
          }
          
          .status {
              margin-top: 24px;
              padding: 12px 16px;
              border-radius: 8px;
              text-align: center;
              display: none;
              font-size: 15px;
          }
          
          .status.success {
              background: #e8f5e9;
              color: #2e7d32;
              display: block;
          }
          
          .status.error {
              background: #ffebee;
              color: #c62828;
              display: block;
          }
  
          @media (max-width: 480px) {
              body {
                  padding: 16px;
              }
              
              .template-buttons {
                  grid-template-columns: 1fr;
              }
              
              .action-buttons {
                  grid-template-columns: 1fr;
              }
              
              .button {
                  width: 100%;
              }
              
              .header {
                  padding: 16px;
              }
              
              .content {
                  padding: 16px;
              }
          }
      </style>
  </head>
  <body>
      <div class="container">
          <div class="header">
              <h1>通知车主挪车</h1>
          </div>
          
          <div class="content">
              <div class="message-area">
                  <textarea id="messageInput" class="textarea" 
                      placeholder=""
                      maxlength="200"></textarea>
                  <div class="char-count">
                      <span id="charCount">0</span>/200
                  </div>
              </div>
  
              <div class="template-buttons">
                  <button class="template-button" onclick="useTemplate('default')">
                      默认通知
                  </button>
                  <button class="template-button" onclick="useTemplate('polite')">
                      礼貌通知
                  </button>
                  <button class="template-button" onclick="useTemplate('urgent')">
                      紧急通知
                  </button>
              </div>
  
              <div class="action-buttons">
                  <button onclick="makeCall('${phoneNumber}')" class="button call-button">
                      拨打电话
                  </button>
                  <button id="sendButton" class="button send-button" onclick="sendMessage()">
                      发送消息
                  </button>
              </div>
              
              <div id="status" class="status"></div>
          </div>
      </div>
  
      <script>
          const messageInput = document.getElementById('messageInput');
          const charCountEl = document.getElementById('charCount');
          const sendButton = document.getElementById('sendButton');
          const status = document.getElementById('status');
  
          const templates = {
              default: "您好，有人需要您挪车，请及时处理。",
              polite: "您好，很抱歉打扰您。您的爱车可能影响到他人通行，请问方便移动一下吗？",
              urgent: "紧急！！！ 您的车辆需要立即移动，请尽快处理！"
          };
  
          messageInput.addEventListener('input', () => {
              charCountEl.textContent = messageInput.value.length;
          });
  
          function useTemplate(type) {
              messageInput.value = templates[type] || "";
              charCountEl.textContent = messageInput.value.length;
          }
  
          function makeCall(phoneNumber) {
              window.location.href = 'tel:' + phoneNumber;
          }
  
          function showStatus(message, isError = false) {
              status.textContent = message;
              status.className = 'status ' + (isError ? 'error' : 'success');
              setTimeout(() => {
                  status.className = 'status';
              }, 3000);
          }
  
          async function sendMessage() {
              const message = messageInput.value.trim();
              if (!message) {
                  showStatus('请输入要发送的信息', true);
                  return;
              }
  
              sendButton.disabled = true;
              try {
                  const response = await fetch('', {
                      method: 'POST',
                      headers: {
                          'Content-Type': 'application/json',
                      },
                      body: JSON.stringify({
                          type: 'message',
                          message: message
                      })
                  });
                  
                  const data = await response.json();
                  if (response.ok) {
                      showStatus('消息已发送');
                      messageInput.value = '';
                      charCountEl.textContent = '0';
                  } else {
                      throw new Error(data.message || '发送失败');
                  }
              } catch (error) {
                  showStatus(error.message || '发送失败，请重试', true);
              } finally {
                  sendButton.disabled = false;
              }
          }
  
          // 初始化
          useTemplate('default');
      </script>
  </body>
  </html>
    `;
}
```

## 飞书版本
### **概述**

此系统用于通过飞书（Feishu）Webhook 向车主发送挪车通知。用户可以在浏览器中输入自定义的通知内容，也可以使用预设的快捷模板。系统还支持拨打车主电话，帮助用户联系车主。此系统部署在 Cloudflare Workers 上，使用环境变量配置车主手机号、飞书 Webhook 地址及网站图标。

### **说明**
非原创，转载吾爱论坛`Aliman`
原文链接: [点击直达](https://www.52pojie.cn/thread-1979717-1-1.html)

### **功能**

1. **通知车主挪车**：
   - 用户可以输入通知内容，并通过飞书 Webhook 发送通知。
   - 支持限制最大字符数为200，防止通知过长。
   
2. **快捷模板**：
   - 系统提供3个预设的快捷模板，帮助用户快速生成常见的挪车通知。
   
3. **拨打车主电话**：
   - 如果用户在桌面设备上，可以点击显示车主的电话号码；如果是在移动设备上，点击后直接拨打车主电话。
   
4. **网站图标**：
   - 支持通过环境变量设置网站的图标，提升系统的用户体验。

### **环境变量**

在部署时，以下环境变量需要被设置：

- `PHONE_NUMBER`：车主的手机号码，用于拨打电话或显示在页面上。
- `FEISHU_WEBHOOK`：飞书的 Webhook URL，用于发送通知。
- `SITE_ICON_URL`：网站的图标 URL，用于设置浏览器标签页的图标。
### 图片示例

点击这个[这里](https://img.confused.us.kg/file/1731160450823_image.png)查看

---


```
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const phone = PHONE_NUMBER // 从环境变量获取车主手机号
  const feishuWebhook = FEISHU_WEBHOOK // 从环境变量获取飞书 Webhook URL
  const siteIconUrl = SITE_ICON_URL // 从环境变量获取网站图标 URL

  const htmlContent = `
    <!DOCTYPE html>
    <html lang="zh-CN">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>通知车主挪车</title>
        <link rel="icon" href="${siteIconUrl}" type="image/x-icon">
        <style>
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }
          
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            background-color: #f8f9fa;
            color: #333;
          }
          
          .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          }
          
          h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 24px;
          }
          
          .message-area {
            margin-bottom: 20px;
          }
          
          textarea {
            width: 100%;
            height: 120px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            resize: none;
            font-size: 16px;
            margin-bottom: 5px;
          }
          
          .char-count {
            text-align: right;
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
          }
          
          .templates {
            margin-bottom: 20px;
          }
          
          .template-btn {
            background: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 8px 15px;
            margin: 0 5px 5px 0;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
          }
          
          .template-btn:hover {
            background: #e9ecef;
          }
          
          .action-buttons {
            display: flex;
            gap: 10px;
          }
          
          .btn {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
          }
          
          .notify-btn {
            background: #007bff;
            color: white;
          }
          
          .notify-btn:hover {
            background: #0056b3;
          }
          
          .notify-btn:disabled {
            background: #cccccc;
            cursor: not-allowed;
          }
          
          .call-btn {
            background: #28a745;
            color: white;
          }
          
          .call-btn:hover {
            background: #218838;
          }
          
          /* 模态框样式 */
          .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 1000;
          }
          
          .modal-content {
            position: relative;
            background-color: white;
            margin: 20% auto;
            padding: 20px;
            width: 90%;
            max-width: 400px;
            border-radius: 10px;
            text-align: center;
          }
          
          .modal-title {
            margin-bottom: 15px;
            font-size: 18px;
            color: #2c3e50;
          }
          
          .modal-phone {
            font-size: 24px;
            color: #007bff;
            margin-bottom: 20px;
          }
          
          .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
          }
          
          .modal-btn {
            padding: 8px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
          }
          
          .confirm-btn {
            background: #28a745;
            color: white;
          }
          
          .confirm-btn:hover {
            background: #218838;
          }
          
          .cancel-btn {
            background: #dc3545;
            color: white;
          }
          
          .cancel-btn:hover {
            background: #c82333;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>通知车主挪车</h1>
          
          <div class="message-area">
            <textarea id="messageInput" placeholder="请输入通知内容" oninput="updateCharCount()"></textarea>
            <div id="charCount" class="char-count">0/200</div>
          </div>
          
          <div class="templates">
            <button class="template-btn" onclick="useTemplate('您好，有人需要您挪车，请及时处理。')">默认模板</button>
            <button class="template-btn" onclick="useTemplate('您好，您的车辆阻碍他人通行，请尽快挪车，谢谢配合。')">礼貌模板</button>
            <button class="template-btn" onclick="useTemplate('紧急情况！您的车辆阻碍消防通道，请立即挪车！')">紧急模板</button>
          </div>
          
          <div class="action-buttons">
            <button id="notifyBtn" class="btn notify-btn" onclick="notifyOwner()">发送通知</button>
            <button class="btn call-btn" onclick="showCallModal()">拨打电话</button>
          </div>
        </div>

        <!-- 拨打电话确认模态框 -->
        <div id="callModal" class="modal">
          <div class="modal-content">
            <h2 class="modal-title">确认拨打车主电话？</h2>
            <div id="modalPhoneNumber" class="modal-phone"></div>
            <div class="modal-buttons">
              <button class="modal-btn confirm-btn" onclick="callOwner()">确认拨打</button>
              <button class="modal-btn cancel-btn" onclick="hideCallModal()">取消</button>
            </div>
          </div>
        </div>

        <script>
          // 在脚本开始处定义全局变量
          const phoneNumber = '${phone}';
          const webhookUrl = '${feishuWebhook}';

          // 使用模板消息
          function useTemplate(template) {
            const messageInput = document.getElementById('messageInput');
            messageInput.value = template;
            updateCharCount();
          }

          // 更新字符计数
          function updateCharCount() {
            const messageInput = document.getElementById('messageInput');
            const charCount = document.getElementById('charCount');
            const notifyBtn = document.getElementById('notifyBtn');
            const currentLength = messageInput.value.length;
            
            charCount.textContent = currentLength + '/200';
            
            // 启用/禁用发送按钮
            notifyBtn.disabled = currentLength === 0 || currentLength > 200;
            
            // 改变字符计数颜色
            if (currentLength > 200) {
              charCount.style.color = '#dc3545';
            } else {
              charCount.style.color = '#666';
            }
          }

          // 格式化电话号码显示
          function formatPhoneNumber(phone) {
            return phone.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');
          }

          // 调用飞书 Webhook 发送通知
          function notifyOwner() {
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message) {
              alert('请输入通知内容');
              return;
            }
            
            if (message.length > 200) {
              alert('通知内容不能超过200字');
              return;
            }

            const notifyBtn = document.getElementById('notifyBtn');
            notifyBtn.disabled = true;
            notifyBtn.textContent = '发送中...';

            fetch(webhookUrl, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                "msg_type": "text",
                "content": {
                  "text": message
                }
              })
            })
            .then(response => response.json())
            .then(data => {
              console.log("通知发送成功", data);
              notifyBtn.textContent = '发送成功';
              messageInput.value = ''; // 清空输入框
              updateCharCount(); // 更新字符计数
              setTimeout(() => { 
                notifyBtn.textContent = '发送通知'; 
                notifyBtn.disabled = false; 
              }, 2000);
            })
            .catch(error => {
              console.error("发送通知失败", error);
              notifyBtn.textContent = '发送失败';
              setTimeout(() => { 
                notifyBtn.textContent = '发送通知'; 
                notifyBtn.disabled = false; 
              }, 2000);
            });
          }

          // 显示拨打电话的确认框
          function showCallModal() {
            const formattedNumber = formatPhoneNumber(phoneNumber);
            document.getElementById('modalPhoneNumber').textContent = formattedNumber;
            document.getElementById('callModal').style.display = 'block';
          }

          // 隐藏拨打电话的确认框
          function hideCallModal() {
            document.getElementById('callModal').style.display = 'none';
          }

          // 拨打车主电话
          function callOwner() {
            window.location.href = \`tel:\${phoneNumber}\`;
            hideCallModal();
          }

          // 页面加载完成后初始化
          document.addEventListener('DOMContentLoaded', () => {
            useTemplate('您好，有人需要您挪车，请及时处理。');
          });

          // 点击模态框外部关闭模态框
          window.onclick = function(event) {
            const modal = document.getElementById('callModal');
            if (event.target === modal) {
              hideCallModal();
            }
          }
        </script>
      </body>
    </html>
  `;

  return new Response(htmlContent, {
    headers: { 
      'Content-Type': 'text/html;charset=UTF-8'
    }
  });
}
```

