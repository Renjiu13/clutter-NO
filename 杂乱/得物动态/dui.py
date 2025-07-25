import pyperclip
import requests
import time
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json
import sys

# 配置
DOWNLOAD_DIR = "downloaded_images"  # 你可以改成你想要的路径
CHECK_INTERVAL = 1  # 秒

# 获取默认下载目录
def get_default_download_dir():
    if os.name == 'nt':
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

LAST_LINK_FILE = 'last_link.txt'

def read_last_link():
    if os.path.exists(LAST_LINK_FILE):
        with open(LAST_LINK_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ''

def write_last_link(link):
    with open(LAST_LINK_FILE, 'w', encoding='utf-8') as f:
        f.write(link)

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def is_dewu_shortlink(text):
    # 检查是否为得物短链
    return text.startswith("https://dw4.co/")

def expand_shortlink(url):
    # 跟随重定向，获取真实页面URL
    try:
        resp = requests.get(url, allow_redirects=True, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
        return resp.url
    except Exception as e:
        print(f"短链跳转失败: {e}")
        return None

def fetch_page(url):
    try:
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
        resp.encoding = resp.apparent_encoding
        return resp.text
    except Exception as e:
        print(f"页面获取失败: {e}")
        return None

def extract_image_links(html):
    # 1. 优先查找 JSON 数据中的图片链接
    soup = BeautifulSoup(html, "html.parser")
    image_links = set()
    # 查找 __NEXT_DATA__ 脚本
    for script in soup.find_all("script", id="__NEXT_DATA__"):
        try:
            data = json.loads(script.string)
            # 递归查找所有图片链接
            def find_images(obj):
                if isinstance(obj, dict):
                    for v in obj.values():
                        find_images(v)
                elif isinstance(obj, list):
                    for item in obj:
                        find_images(item)
                elif isinstance(obj, str):
                    if re.match(r"^https?://.*\.(webp|jpg|jpeg|png)$", obj, re.IGNORECASE):
                        image_links.add(obj)
            find_images(data)
        except Exception as e:
            pass
    # 2. 兜底：查找 img 标签
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if re.match(r"^https?://.*\.(webp|jpg|jpeg|png)$", src, re.IGNORECASE):
            image_links.add(src)
    # 3. 兜底：查找所有 script 里的图片链接
    for script in soup.find_all("script"):
        if script.string:
            matches = re.findall(r'https?://[^\s"\']+\.(webp|jpg|jpeg|png)', script.string, re.IGNORECASE)
            for m in matches:
                image_links.add(m)
    return list(image_links)

def extract_image_links_from_metaOGInfo(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script", id="__NEXT_DATA__"):
        try:
            data = json.loads(script.string)
            # 定位到 metaOGInfo
            meta = data
            for key in ["props", "pageProps", "metaOGInfo", "data"]:
                meta = meta.get(key, {})
            if isinstance(meta, list):
                image_links = []
                for item in meta:
                    content = item.get("content", {})
                    # cover
                    cover_url = content.get("cover", {}).get("url")
                    if cover_url:
                        image_links.append(cover_url)
                    # media.list
                    media_list = content.get("media", {}).get("list", [])
                    for media in media_list:
                        url = media.get("url")
                        if url:
                            image_links.append(url)
                return image_links
        except Exception:
            continue
    return []

def get_public_ip():
    try:
        resp = requests.get("https://api.ipify.org", timeout=5)
        return resp.text.strip()
    except Exception:
        return "unknown_ip"

def download_images(links, download_dir):
    for link in links:
        try:
            filename = os.path.basename(urlparse(link).path)
            filepath = os.path.join(download_dir, filename)
            if os.path.exists(filepath):
                print(f"已存在: {filename}")
                continue
            resp = requests.get(link, stream=True, timeout=10)
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            print(f"下载完成: {filename}")
        except Exception as e:
            print(f"下载失败: {link} 错误: {e}")

def extract_dw4_link(text):
    # 只提取 dw4.co 的短链（不包含后面的汉字等）
    match = re.search(r'https://dw4\.co/[A-Za-z0-9/_\-]+', text)
    return match.group(0) if match else None

def main():
    # 解析命令行参数
    if len(sys.argv) > 1:
        download_dir = sys.argv[1]
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
    else:
        download_dir = get_default_download_dir()
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
    global DOWNLOAD_DIR
    DOWNLOAD_DIR = download_dir
    print(f"图片将保存到: {DOWNLOAD_DIR}")
    print("开始监听剪切板，复制得物动态短链自动下载图片...")
    last_clipboard = ""
    last_link = read_last_link()
    while True:
        try:
            clipboard = pyperclip.paste().strip()
            if clipboard != last_clipboard:
                dw4_link = extract_dw4_link(clipboard)
                if dw4_link:
                    if dw4_link == last_link:
                        print("该短链已处理过，跳过。")
                    else:
                        print(f"检测到得物短链: {dw4_link}")
                        real_url = expand_shortlink(dw4_link)
                        if real_url and "community-share" in real_url:
                            print(f"跳转到真实页面: {real_url}")
                            html = fetch_page(real_url)
                            if html:
                                image_links = extract_image_links_from_metaOGInfo(html)
                                if image_links:
                                    print(f"检测到 {len(image_links)} 个图片，开始下载...")
                                    download_images(image_links, DOWNLOAD_DIR)
                                    write_last_link(dw4_link)
                                    last_link = dw4_link
                                else:
                                    print("未检测到图片链接。")
                        else:
                            print("未检测到有效的得物动态页面。")
                last_clipboard = clipboard
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("退出监听。")
            break

if __name__ == "__main__":
    main()