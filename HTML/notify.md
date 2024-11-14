# **通知车主挪车系统 使用说明**

## **概述**

此系统用于通过飞书（Feishu）Webhook 向车主发送挪车通知。用户可以在浏览器中输入自定义的通知内容，也可以使用预设的快捷模板。系统还支持拨打车主电话，帮助用户联系车主。此系统部署在 Cloudflare Workers 上，使用环境变量配置车主手机号、飞书 Webhook 地址及网站图标。

## **说明**
非原创，转载吾爱论坛`Aliman`
原文链接: [点击直达](https://www.52pojie.cn/thread-1979717-1-1.html)

## **功能**

1. **通知车主挪车**：
   - 用户可以输入通知内容，并通过飞书 Webhook 发送通知。
   - 支持限制最大字符数为200，防止通知过长。
   
2. **快捷模板**：
   - 系统提供3个预设的快捷模板，帮助用户快速生成常见的挪车通知。
   
3. **拨打车主电话**：
   - 如果用户在桌面设备上，可以点击显示车主的电话号码；如果是在移动设备上，点击后直接拨打车主电话。
   
4. **网站图标**：
   - 支持通过环境变量设置网站的图标，提升系统的用户体验。

## **环境变量**

在部署时，以下环境变量需要被设置：

- `PHONE_NUMBER`：车主的手机号码，用于拨打电话或显示在页面上。
- `FEISHU_WEBHOOK`：飞书的 Webhook URL，用于发送通知。
- `SITE_ICON_URL`：网站的图标 URL，用于设置浏览器标签页的图标。

点击[这里](https://img.roswe.top/file/1731160450823_image.png)可以查看图片示例
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

## 更新微信通知方式


#### 主要改进

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

#### 使用说明

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


脚本如下
```
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // 处理 POST 请求
  if (request.method === 'POST') {
    try {
      const { message } = await request.json();
      const pushPlusToken = PUSHPLUS_TOKEN;
      
      // 设置请求超时
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 30000); // 30秒超时

      try {
        // 发送请求到 PushPlus
        const response = await fetch('https://www.pushplus.plus/send', {
          method: 'POST',
          signal: controller.signal,
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            token: pushPlusToken,
            title: '挪车通知',
            content: message,
            template: 'html'
          })
        });

        clearTimeout(timeout);

        // 检查响应状态
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 尝试解析响应
        let result;
        const text = await response.text();
        try {
          result = JSON.parse(text);
        } catch (e) {
          throw new Error(`Invalid JSON response: ${text}`);
        }

        return new Response(JSON.stringify({
          code: 200,
          msg: 'success',
           result
        }), {
          headers: { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });

      } catch (error) {
        if (error.name === 'AbortError') {
          return new Response(JSON.stringify({
            code: 408,
            msg: '请求超时，请稍后重试'
          }), {
            headers: { 
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*'
            }
          });
        }
        throw error;
      } finally {
        clearTimeout(timeout);
      }

    } catch (error) {
      return new Response(JSON.stringify({
        code: 500,
        msg: `发送失败: ${error.message}`
      }), {
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
  }

  // 处理 OPTIONS 请求（用于CORS预检）
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  }

  const phone = PHONE_NUMBER;
  const siteIconUrl = SITE_ICON_URL;

  const htmlContent = `
    <!DOCTYPE html>
    <html lang="zh-CN">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>通知车主挪车</title>
        <link rel="icon" href="${siteIconUrl}" type="image/x-icon">
        <style>
          /* 样式保持不变 */
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
          const phoneNumber = '${phone}';

          function useTemplate(template) {
            const messageInput = document.getElementById('messageInput');
            messageInput.value = template;
            updateCharCount();
          }

          function updateCharCount() {
            const messageInput = document.getElementById('messageInput');
            const charCount = document.getElementById('charCount');
            const notifyBtn = document.getElementById('notifyBtn');
            const currentLength = messageInput.value.length;
            
            charCount.textContent = currentLength + '/200';
            notifyBtn.disabled = currentLength === 0 || currentLength > 200;
            
            if (currentLength > 200) {
              charCount.style.color = '#dc3545';
            } else {
              charCount.style.color = '#666';
            }
          }

          function formatPhoneNumber(phone) {
            return phone.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');
          }

          async function notifyOwner() {
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

            try {
              const controller = new AbortController();
              const timeoutId = setTimeout(() => controller.abort(), 30000);

              const response = await fetch(window.location.href, {
                method: 'POST',
                signal: controller.signal,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
              });

              clearTimeout(timeoutId);

              if (!response.ok) {
                throw new Error(\`HTTP error! status: \${response.status}\`);
              }

              const result = await response.json();
              
              if (result.code === 200) {
                notifyBtn.textContent = '发送成功';
                messageInput.value = '';
                updateCharCount();
              } else {
                throw new Error(result.msg || '发送失败');
              }
            } catch (error) {
              console.error("发送通知失败", error);
              notifyBtn.textContent = '发送失败';
              if (error.name === 'AbortError') {
                alert('发送超时，请稍后重试');
              } else {
                alert('发送失败：' + error.message);
              }
            } finally {
              setTimeout(() => { 
                notifyBtn.textContent = '发送通知'; 
                notifyBtn.disabled = false; 
              }, 2000);
            }
          }

          function showCallModal() {
            const formattedNumber = formatPhoneNumber(phoneNumber);
            document.getElementById('modalPhoneNumber').textContent = formattedNumber;
            document.getElementById('callModal').style.display = 'block';
          }

          function hideCallModal() {
            document.getElementById('callModal').style.display = 'none';
          }

          function callOwner() {
            window.location.href = \`tel:\${phoneNumber}\`;
            hideCallModal();
          }

          document.addEventListener('DOMContentLoaded', () => {
            useTemplate('您好，有人需要您挪车，请及时处理。');
          });

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