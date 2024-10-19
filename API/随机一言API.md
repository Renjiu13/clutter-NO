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