# 使用腾讯云函数定时推送天气信息

- 准备材料
	- `钉钉机器人Webhook地址`
	- `钉钉机器人的加签`
	- `高德开放平台API Key`
	- `城市编码(默认330109_萧山区)`

- 必须设置以下环境变量：
	- `CITY_CODE`: 城市编码（默认值：330109）
	- `AMAP_API_KEY`: 高德开放平台 API Key
	- `DINGTALK_WEBHOOK`: 钉钉机器人 Webhook 地址
	- `DINGTALK_SECRET`: 钉钉机器人的加签秘钥

- 部署步骤
	- - 将`index.py`上传到腾讯云函数
	- - 设置环境变量
	- - 定时触发每天上午 8 点 45 分执行一次
	- -示例：`45 8 * * *`

- 特点
	- `使用标准库，无额外依赖` 
	- `这就是最大的优点！！！`


```
# 部署图片示例下载
https://wwmd.lanzouv.com/i8qCo2hz5y1a  密码:52pj
```

代码如下

``` python
import os
import json
import time
import hmac
import hashlib
import base64
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

def get_weather_forecast(city_code, api_key):
    """获取3天天气预报信息"""
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city={city_code}&extensions=all"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data['status'] == '1' and data['count'] == '1':
                forecast = data['forecasts'][0]
                return {
                    'city': forecast['city'],
                    'forecast': forecast['casts']
                }
            else:
                return None
    except Exception as e:
        print(f"获取天气预报失败: {e}")
        return None

def dingtalk_sign(secret):
    """钉钉机器人签名"""
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = f'{timestamp}\n{secret}'
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

def send_dingtalk_message(webhook, secret, message):
    """发送钉钉机器人消息"""
    timestamp, sign = dingtalk_sign(secret)
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # 仅传递消息内容部分，确保是纯文本
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    
    req = urllib.request.Request(
        url=f"{webhook}&timestamp={timestamp}&sign={sign}", 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"发送消息失败: {e}")
        return None

def main_handler(event, context):
    """主处理函数"""
    # 从环境变量读取配置
    city_code = os.environ.get('CITY_CODE', '330109')  # 默认萧山区
    amap_key = os.environ.get('AMAP_API_KEY')
    dingtalk_webhook = os.environ.get('DINGTALK_WEBHOOK')
    dingtalk_secret = os.environ.get('DINGTALK_SECRET')
    
    if not all([amap_key, dingtalk_webhook, dingtalk_secret]):
        print("环境变量配置不完整")
        return
    
    # 获取当前时间
    now = datetime.now() + timedelta(hours=8)  # 转换为北京时间
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M")
    
    # 获取天气预报信息
    weather_forecast = get_weather_forecast(city_code, amap_key)
    
    if weather_forecast:
        # 构建消息
        message = f"天气预报通知\n" \
                  f"城市：{weather_forecast['city']}\n" \
                  f"当前时间：{date_str} {time_str}\n\n" \
                  f"未来三天天气预报：\n"
        
        # 添加3天天气预报
        for day in weather_forecast['forecast'][:3]:
            message += f"{day['date']}\n" \
                       f"  白天：{day['dayweather']}  |  夜间：{day['nightweather']}\n" \
                       f"  温度：{day['daytemp']}°C / {day['nighttemp']}°C\n" \
                       f"  风向：{day['daywind']} {day['daypower']} 级\n\n"
        
        # 去除最后的换行
        message = message.rstrip()
        
        # 发送钉钉消息
        send_dingtalk_message(dingtalk_webhook, dingtalk_secret, message)
    
    return {"statusCode": 200, "body": "Weather forecast sent"}

```