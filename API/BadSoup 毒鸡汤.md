# Bad Soup 毒鸡汤 API

将这碗毒鸡汤引用至您的网站，时时刻刻体现您的精神。

## 1. 使用方式

将以下代码引用至您的网页中即可。

```html
<!-- Body -->
<p id="badsoup">有人一笑就很好看，你是一看就挺好笑。</p>

<!-- Footer -->
<script>
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'https://api.7ed.net/soup/api');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var data = JSON.parse(xhr.responseText);
      var badsoup = document.getElementById('badsoup');
      badsoup.innerText = data.badsoup;
    }
  };
  xhr.send();
</script>
```

提示
本服务托管于 Vercel，目前大陆到 Vercel 的路由间歇性不可用。
可使用托管于 Deno 并使用 Google Cloud 线路的 `https://api.7ed.net/soup/api` 代替。

## 2. 效果

刷新页面即可看到新的毒鸡汤。

## 3. 更多

收集于 [7ED](https://www.7ed.net/) 。
在使用过程中出现任何问题均可至 [后花园](https://www.7ed.net/garden) 进行反馈。