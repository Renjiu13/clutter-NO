#  彩云天气API 获取实时及当日天气等内容

转载[吾爱破解](https://www.52pojie.cn/thread-1972591-1-1.html)

![图片示例](https://attach.52pojie.cn/forum/202410/15/120347wr1ubir8pa7p4snu.png)


```
import requests
 # 用户输入的秘钥和经纬度（以逗号分隔）
api_key = ""  # 这里输入用户自己的秘钥
location = ""  # 输入用户的经纬度
 
# 抓取天气信息的函数
def get_weather_info(api_key, location):
    try:
        # 实时天气API
        realtime_url = f"https://api.caiyunapp.com/v2.6/{api_key}/{location}/realtime"
        # 当日天气API
        daily_url = f"https://api.caiyunapp.com/v2.6/{api_key}/{location}/daily?dailysteps=1"
 
        # 获取实时天气数据
        realtime_response = requests.get(realtime_url)
        # 获取当日天气数据
        daily_response = requests.get(daily_url)
 
        if realtime_response.status_code == 200 and daily_response.status_code == 200:
            realtime_data = realtime_response.json().get('result', {}).get('realtime', {})
            daily_data = daily_response.json().get('result', {}).get('daily', {})
 
            # 提取实时天气数据
            temperature = realtime_data.get('temperature')
            humidity = realtime_data.get('humidity')
            skycon = realtime_data.get('skycon')
            wind = realtime_data.get('wind', {})
            apparent_temperature = realtime_data.get('apparent_temperature')
            precipitation = realtime_data.get('precipitation', {})
            local_precip = precipitation.get('local', {})
            nearest_precip = precipitation.get('nearest', {})
 
            # 提取当日天气数据
            daily_temp = daily_data.get('temperature', [{}])[0]
            daily_humidity = daily_data.get('humidity', [{}])[0]
            daily_skycon = daily_data.get('skycon', [{}])[0].get('value', '未知')
 
            # 天气状况翻译
            skycon_translation = {
                "CLEAR_DAY": "晴天",
                "CLEAR_NIGHT": "晴夜",
                "PARTLY_CLOUDY_DAY": "多云",
                "PARTLY_CLOUDY_NIGHT": "多云夜晚",
                "CLOUDY": "阴天",
                "LIGHT_HAZE": "轻度雾霾",
                "MODERATE_HAZE": "中度雾霾",
                "HEAVY_HAZE": "重度雾霾",
                "LIGHT_RAIN": "小雨",
                "MODERATE_RAIN": "中雨",
                "HEAVY_RAIN": "大雨",
                "STORM_RAIN": "暴雨",
                "FOG": "雾",
                "LIGHT_SNOW": "小雪",
                "MODERATE_SNOW": "中雪",
                "HEAVY_SNOW": "大雪",
                "STORM_SNOW": "暴雪",
                "DUST": "浮尘",
                "SAND": "沙尘",
                "WIND": "大风"
            }
 
            # 翻译天气状况
            skycon_desc = skycon_translation.get(skycon, "未知天气状况")
 
            # 构建输出字符串
            weather_info = (
                f"实时天气情况: {skycon_desc}\n"
                f"实时温度: {round(temperature)}°C (体感: {round(apparent_temperature)}°C)\n"
                f"每秒风速: {wind.get('speed')}米\n"
            )
 
            # 判断降水状况
            if local_precip.get('intensity', 0) == 0 and nearest_precip.get('distance', 0) > 10000:
                weather_info += "降水监测: 目前无降水（雷达显示最近降水距离超过10公里）"
            else:
                weather_info += "降水监测: 雷达显示10公里区域内存在降水"
 
            # 加入当日天气信息（只显示温度、湿度和天气状况）
            weather_info += (
                f"\n当日天气情况: {skycon_translation.get(daily_skycon, '未知')}\n"
                f"当日温度: {round(daily_temp.get('min'))}°C ～ {round(daily_temp.get('max'))}°C\n"
                f"当日湿度: {round(int(daily_humidity.get('min') * 100))} % ～ {round(int(daily_humidity.get('max') * 100))} %\n"
            )
 
            return weather_info
        else:
            return "无法获取天气数据。"
 
    except requests.exceptions.RequestException as e:
        print(f"抓取天气信息失败: {e}")
        return None
 
# 主程序入口
if __name__ == "__main__":
 
    # 调用天气信息函数
    weather_result = get_weather_info(api_key, location)
 
    if weather_result:
        print("公司总部天气信息：\n",weather_result)
    else:
        print("未能提取到天气信息。")
```