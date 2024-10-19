你可以使用以下代码示例，其中包含注释，说明如何更换随机一言的 API：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alist 网站</title>
  <style>
    /* 这里可以加入您的样式，如果有需要的话 */
    #hitokoto {
      font-size: 16px;
      color: #007BFF; /* 超链接蓝色 */
      text-align: center;
      padding: 20px;
      cursor: pointer;
      text-decoration: none; /* 去掉下划线 */
    }
  </style>
</head>
<body>

<div id="hitokoto">
  正在加载随机一言...
</div>

<script>
  // 获取显示随机一言的 div 元素
  const hitokotoDiv = document.getElementById('hitokoto');
  
  // 点击事件：当用户点击一言时，跳转到 Bing 搜索结果
  hitokotoDiv.addEventListener('click', () => {
    window.location.href = 'https://www.bing.com/search?q=' + encodeURIComponent(hitokotoDiv.textContent);
  });

  // 这里是获取随机一言的 API
  // 当前使用的是 https://v1.hitokoto.cn，您可以替换为其他 API
  fetch('https://v1.hitokoto.cn') // 替换为新的 API 地址
    .then(response => response.json())
    .then(data => {
      // 更新 div 内容为随机一言，添加引号
      hitokotoDiv.innerHTML = `“${data.hitokoto}”`; 
    })
    .catch(error => {
      console.error("Error fetching hitokoto:", error);
      // 若发生错误，则显示提示信息
      hitokotoDiv.textContent = "无法加载随机一言。";
    });
</script>

</body>
</html>
```

### 如何更换 API：

1. 找到以下行：
   ```javascript
   fetch('https://v1.hitokoto.cn') // 替换为新的 API 地址
   ```

2. 将 `'https://v1.hitokoto.cn'` 替换为你想要使用的新的随机一言 API 地址。

3. 确保新 API 返回的数据格式与当前格式一致，特别是需要从 `data` 对象中提取的字段。

如果你有特定的 API 想要更换，请提供信息，我可以帮助你确认数据格式和更新代码！

===========================================================================

你可以将 API 地址替换为 `https://tenapi.cn/v2/yiyan`，并根据新的请求参数进行相应的修改。以下是更新后的代码示例，包含必要的注释：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alist 网站</title>
  <style>
    /* 这里可以加入您的样式，如果有需要的话 */
    #hitokoto {
      font-size: 16px;
      color: #007BFF; /* 超链接蓝色 */
      text-align: center;
      padding: 20px;
      cursor: pointer;
      text-decoration: none; /* 去掉下划线 */
    }
  </style>
</head>
<body>

<div id="hitokoto">
  正在加载随机一言...
</div>

<script>
  // 获取显示随机一言的 div 元素
  const hitokotoDiv = document.getElementById('hitokoto');
  
  // 点击事件：当用户点击一言时，跳转到 Bing 搜索结果
  hitokotoDiv.addEventListener('click', () => {
    window.location.href = 'https://www.bing.com/search?q=' + encodeURIComponent(hitokotoDiv.textContent);
  });

  // 使用新的 API 地址
  fetch('https://tenapi.cn/v2/yiyan', {
    method: 'POST', // 使用 POST 方法
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded' // 设置请求头
    },
    body: 'format=json' // 请求体，指定返回格式为 json
  })
    .then(response => response.json())
    .then(data => {
      // 检查返回的状态码
      if (data.code === 200) {
        // 更新 div 内容为随机一言
        hitokotoDiv.innerHTML = `“${data.data.hitokoto}”`; 
      } else {
        // 处理其他状态码
        hitokotoDiv.textContent = "无法加载随机一言。";
      }
    })
    .catch(error => {
      console.error("Error fetching hitokoto:", error);
      // 若发生错误，则显示提示信息
      hitokotoDiv.textContent = "无法加载随机一言。";
    });
</script>

</body>
</html>
```

### 关键更改：

1. **API 地址**：替换为 `https://tenapi.cn/v2/yiyan`。
2. **请求方法**：使用 `POST` 方法。
3. **请求体**：传递 `'format=json'` 作为请求体。
4. **返回数据处理**：检查 `data.code` 确认请求是否成功，并从 `data.data.hitokoto` 中提取一言内容。

这样，点击页面上的随机一言就能获取新的内容。如果有其他需求或问题，请随时告诉我！