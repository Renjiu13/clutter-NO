import argparse
import os
import uuid
import requests
import mimetypes
import threading
import json
import hashlib  # 添加hashlib模块导入
from tkinter import *
from tkinter import ttk, messagebox
from requests.exceptions import RequestException

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("API图片下载器")
        self.running = False
        self.total_downloads = 0
        self.max_downloads = 0  # 新增：最大下载数量
        self.saved_apis = []    # 新增：存储的API列表
        
        # 加载保存的API
        self.load_saved_apis()
        self.create_widgets()

    def load_saved_apis(self):
        """加载保存的API记录"""
        try:
            # 使用绝对路径保存历史记录
            history_path = os.path.join(os.path.dirname(__file__), 'api_history.json')
            with open(history_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.saved_apis = data.get('apis', [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.saved_apis = []

    def save_apis(self, apis):
        """保存API记录，避免重复"""
        # 将新API添加到历史记录中，避免重复
        for api in apis:
            if api not in self.saved_apis:
                self.saved_apis.append(api)
        
        # 限制历史记录数量，最多保留10条
        if len(self.saved_apis) > 10:
            self.saved_apis = self.saved_apis[-10:]
            
        # 使用绝对路径保存历史记录
        history_path = os.path.join(os.path.dirname(__file__), 'api_history.json')
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump({'apis': self.saved_apis}, f, ensure_ascii=False, indent=2)
        
        # 如果历史列表已存在，则更新它
        if hasattr(self, 'history_listbox'):
            self.update_history_listbox()

    def update_history_listbox(self):
        """更新历史API列表显示"""
        if hasattr(self, 'history_listbox'):
            self.history_listbox.delete(0, END)
            for api in self.saved_apis:
                self.history_listbox.insert(END, api)

    def create_widgets(self):
        # 设置主题颜色和字体
        bg_color = "#f0f0f0"
        button_color = "#4a86e8"
        text_color = "#333333"
        header_font = ("Arial", 10, "bold")
        normal_font = ("Arial", 9)
        
        self.root.configure(bg=bg_color)
        
        # 创建主框架
        main_frame = Frame(self.root, bg=bg_color)
        main_frame.pack(padx=15, pady=10, fill=BOTH, expand=True)
        
        # API输入框
        api_frame = LabelFrame(main_frame, text="API接口设置", font=header_font, bg=bg_color)
        api_frame.pack(pady=5, fill=X)
        
        Label(api_frame, text="输入API接口(每行一个):", bg=bg_color, font=normal_font).pack(pady=(5,0), anchor=W)
        
        # API文本框和滚动条
        api_text_frame = Frame(api_frame, bg=bg_color)
        api_text_frame.pack(fill=X, pady=5)
        
        api_scrollbar = Scrollbar(api_text_frame)
        api_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.api_text = Text(api_text_frame, height=5, width=50, font=normal_font, yscrollcommand=api_scrollbar.set)
        self.api_text.pack(side=LEFT, fill=BOTH, expand=True)
        api_scrollbar.config(command=self.api_text.yview)
        
        # 下载设置框架
        settings_frame = Frame(api_frame, bg=bg_color)
        settings_frame.pack(fill=X, pady=5)
        
        Label(settings_frame, text="下载数量(0表示无限):", bg=bg_color, font=normal_font).pack(side=LEFT, padx=(0,5))
        self.count_entry = Entry(settings_frame, width=10, font=normal_font)
        self.count_entry.insert(0, "0")
        self.count_entry.pack(side=LEFT)
        
        # 控制按钮
        btn_frame = Frame(main_frame, bg=bg_color)
        btn_frame.pack(pady=10, fill=X)
        
        self.start_btn = Button(btn_frame, text="开始下载", command=self.start_download, 
                               bg=button_color, fg="white", font=normal_font, width=15)
        self.start_btn.pack(side=LEFT, padx=5)
        
        self.stop_btn = Button(btn_frame, text="停止", command=self.stop_download, 
                              bg="#e74c3c", fg="white", font=normal_font, width=15, state=DISABLED)
        self.stop_btn.pack(side=LEFT, padx=5)
        
        self.open_folder_btn = Button(btn_frame, text="打开下载文件夹", command=self.open_download_folder,
                                    bg="#27ae60", fg="white", font=normal_font, width=15)
        self.open_folder_btn.pack(side=LEFT, padx=5)
        
        # 添加去重按钮
        self.dedup_btn = Button(btn_frame, text="清理重复文件", command=self.deduplicate_files,
                              bg="#9b59b6", fg="white", font=normal_font, width=15)
        self.dedup_btn.pack(side=LEFT, padx=5)
        
        # 历史API框架
        history_frame = LabelFrame(main_frame, text="历史API记录", font=header_font, bg=bg_color)
        history_frame.pack(pady=5, fill=X)
        
        # 创建带滚动条的历史列表 - 支持多选
        history_list_frame = Frame(history_frame, bg=bg_color)
        history_list_frame.pack(fill=BOTH, expand=True, pady=5)
        
        history_scrollbar = Scrollbar(history_list_frame)
        history_scrollbar.pack(side=RIGHT, fill=Y)
        
        # 修改为支持Ctrl和Shift多选的列表框
        self.history_listbox = Listbox(history_list_frame, height=5, font=normal_font,
                                      selectmode=EXTENDED, yscrollcommand=history_scrollbar.set)
        self.history_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        history_scrollbar.config(command=self.history_listbox.yview)
        
        # 更新历史列表
        self.update_history_listbox()
        
        # 历史API操作按钮
        history_btn_frame = Frame(history_frame, bg=bg_color)
        history_btn_frame.pack(pady=5, fill=X)
        
        Button(history_btn_frame, text="使用选中API", command=self.use_selected_api,
              bg=button_color, fg="white", font=normal_font).pack(side=LEFT, padx=5)
        Button(history_btn_frame, text="删除选中API", command=self.delete_selected_api,
              bg="#e67e22", fg="white", font=normal_font).pack(side=LEFT, padx=5)
        Button(history_btn_frame, text="清空历史记录", command=self.clear_history,
              bg="#e74c3c", fg="white", font=normal_font).pack(side=LEFT, padx=5)
        
        # 下载日志框架
        log_frame = LabelFrame(main_frame, text="下载日志", font=header_font, bg=bg_color)
        log_frame.pack(pady=5, fill=BOTH, expand=True)
        
        # 日志文本框和滚动条
        log_text_frame = Frame(log_frame, bg=bg_color)
        log_text_frame.pack(fill=BOTH, expand=True, pady=5)
        
        log_scrollbar = Scrollbar(log_text_frame)
        log_scrollbar.pack(side=RIGHT, fill=Y)
        
        self.log_text = Text(log_text_frame, height=10, font=normal_font, state=DISABLED, yscrollcommand=log_scrollbar.set)
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)
        log_scrollbar.config(command=self.log_text.yview)
        
        # 统计信息
        self.stats_label = Label(main_frame, text="总共下载: 0", font=header_font, bg=bg_color)
        self.stats_label.pack(pady=5)

    def open_download_folder(self):
        """打开下载文件夹"""
        download_dir = os.path.join(os.path.dirname(__file__), 'Download')
        os.makedirs(download_dir, exist_ok=True)
        
        # 检查是否有子文件夹
        subfolders = [f for f in os.listdir(download_dir) 
                     if os.path.isdir(os.path.join(download_dir, f))]
        
        if not subfolders:
            # 没有子文件夹，直接打开主文件夹
            try:
                os.startfile(download_dir)
                self.log_message("已打开下载文件夹")
            except:
                self.log_message("无法打开下载文件夹")
            return
            
        # 创建选择对话框
        folder_window = Toplevel(self.root)
        folder_window.title("选择要打开的文件夹")
        folder_window.geometry("300x400")
        folder_window.resizable(False, False)
        
        Label(folder_window, text="选择要打开的文件夹:").pack(pady=10)
        
        # 添加"打开主文件夹"选项
        Button(folder_window, text="打开主下载文件夹", 
              command=lambda: self._open_folder(download_dir, folder_window)).pack(pady=5, fill=X, padx=10)
        
        # 创建子文件夹列表
        folder_frame = Frame(folder_window)
        folder_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = Scrollbar(folder_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        folder_list = Listbox(folder_frame, yscrollcommand=scrollbar.set)
        for folder in sorted(subfolders):
            folder_list.insert(END, folder)
        folder_list.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=folder_list.yview)
        
        # 双击打开文件夹
        folder_list.bind('<Double-Button-1>', lambda e: self._open_selected_folder(
            folder_list, download_dir, folder_window))
        
        # 打开选中文件夹按钮
        Button(folder_window, text="打开选中文件夹", 
              command=lambda: self._open_selected_folder(
                  folder_list, download_dir, folder_window)).pack(pady=10, fill=X, padx=10)
    
    def _open_selected_folder(self, listbox, base_dir, window):
        """打开选中的文件夹"""
        selection = listbox.curselection()
        if selection:
            folder_name = listbox.get(selection[0])
            folder_path = os.path.join(base_dir, folder_name)
            self._open_folder(folder_path, window)
    
    def _open_folder(self, path, window=None):
        """打开指定路径的文件夹"""
        try:
            os.startfile(path)
            self.log_message(f"已打开文件夹: {os.path.basename(path)}")
            if window:
                window.destroy()
        except Exception as e:
            self.log_message(f"无法打开文件夹: {str(e)}")

    def use_selected_api(self):
        """使用选中的历史API(支持多选)"""
        selection = self.history_listbox.curselection()
        if selection:
            selected_apis = [self.history_listbox.get(i) for i in selection]
            self.api_text.delete("1.0", END)
            self.api_text.insert(END, "\n".join(selected_apis))
            self.log_message(f"已加载 {len(selected_apis)} 个API")

    def delete_selected_api(self):
        """删除选中的历史API(支持多选)"""
        selection = self.history_listbox.curselection()
        if selection:
            # 从后往前删除，避免索引变化问题
            selected_apis = [self.history_listbox.get(i) for i in sorted(selection, reverse=True)]
            for api in selected_apis:
                if api in self.saved_apis:
                    self.saved_apis.remove(api)
            
            self.update_history_listbox()
            self.save_apis([])  # 触发保存，但不添加新API
            self.log_message(f"已删除 {len(selected_apis)} 个API")

    def clear_history(self):
        """清空历史API记录"""
        if messagebox.askyesno("确认", "确定要清空所有历史API记录吗？"):
            self.saved_apis = []
            self.update_history_listbox()
            self.save_apis([])  # 触发保存，但不添加新API
            self.log_message("已清空所有历史API记录")

    def start_download(self):
        api_urls = [url.strip() for url in self.api_text.get("1.0", END).split("\n") if url.strip()]
        
        if not api_urls:
            messagebox.showerror("错误", "请输入至少一个API地址")
            return

        # 新增：保存API记录
        self.save_apis(api_urls)
            
        # 新增：获取下载数量
        try:
            self.max_downloads = int(self.count_entry.get())
        except ValueError:
            self.max_downloads = 0

        self.running = True
        self.start_btn.config(state=DISABLED)
        self.stop_btn.config(state=NORMAL)
        
        # 创建下载目录
        self.download_dir = os.path.join(os.path.dirname(__file__), 'Download')
        os.makedirs(self.download_dir, exist_ok=True)
        
        # 为每个API创建独立线程
        self.threads = []
        for url in api_urls:
            thread = threading.Thread(target=self.download_single, args=(url,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def stop_download(self):
        """停止所有下载线程"""
        self.running = False
        self.start_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        self.log_message("正在停止所有下载线程...")
        
        # 等待所有线程结束
        for thread in self.threads:
            thread.join(timeout=1)  # 等待1秒让线程正常结束
            
        self.log_message("所有下载线程已停止")
        self.threads = []  # 清空线程列表

    def download_single(self, url):
        """单个URL的下载线程"""
        download_count = 0
        file_hashes = {}  # 用于存储已下载文件的哈希值
        
        # 为每个API创建独立文件夹
        api_folder_name = self.get_folder_name_from_url(url)
        api_download_dir = os.path.join(self.download_dir, api_folder_name)
        os.makedirs(api_download_dir, exist_ok=True)
        
        # 加载已有文件的哈希值
        self.load_existing_hashes(api_download_dir, file_hashes)
        
        while self.running and (self.max_downloads == 0 or download_count < self.max_downloads):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                
                # 计算内容的哈希值
                content_hash = hashlib.md5(response.content).hexdigest()
                
                # 检查是否已存在相同内容的文件
                if content_hash in file_hashes:
                    self.log_message(f"⚠ 跳过重复内容: 与 {file_hashes[content_hash]} 相同")
                    continue
                
                content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
                ext = mimetypes.guess_extension(content_type)
                
                if not ext:
                    if 'jpeg' in content_type:
                        ext = '.jpg'
                    elif 'png' in content_type:
                        ext = '.png'
                    else:
                        ext = '.jpg'
                
                # 优化文件命名规则：时间戳_序号
                timestamp = uuid.uuid4().hex[:8]
                filename = f"{timestamp}_{download_count+1}{ext}"
                filepath = os.path.join(api_download_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # 保存文件哈希值
                file_hashes[content_hash] = filename
                
                download_count += 1
                self.total_downloads += 1
                message = f"✓ 成功下载 [{api_folder_name}]: {filename}"
                self.log_message(message)
                self.update_stats(self.total_downloads)
                
            except RequestException as e:
                self.log_message(f"✗ 下载失败 [{api_folder_name}]：{str(e)}")
            except Exception as e:
                self.log_message(f"✗ 处理 [{api_folder_name}] 时发生意外错误：{str(e)}")
    
    def load_existing_hashes(self, folder_path, hash_dict):
        """加载文件夹中已有文件的哈希值"""
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    hash_dict[file_hash] = filename
            self.log_message(f"已加载 {len(hash_dict)} 个已存在文件的哈希值")
        except Exception as e:
            self.log_message(f"加载已有文件哈希值时出错: {str(e)}")

    def get_folder_name_from_url(self, url):
        """从URL生成合适的文件夹名称"""
        try:
            # 尝试从URL中提取域名作为文件夹名
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # 如果域名为空，使用路径的一部分
            if not domain:
                path_parts = parsed_url.path.strip('/').split('/')
                if path_parts:
                    domain = path_parts[0]
            
            # 如果仍然为空，使用URL的哈希值
            if not domain:
                domain = f"api_{hash(url) % 10000:04d}"
                
            # 添加URL的部分哈希值作为后缀，确保唯一性
            url_hash = hash(url) % 1000
            domain = f"{domain}_{url_hash:03d}"
                
            # 清理文件夹名中的非法字符
            import re
            domain = re.sub(r'[\\/*?:"<>|]', '_', domain)
            
            # 记录URL到文件夹的映射
            self.log_message(f"API URL: {url} -> 文件夹: {domain}")
            
            return domain
        except Exception as e:
            # 出错时使用哈希值，并记录错误
            folder_name = f"api_{hash(url) % 10000:04d}"
            self.log_message(f"生成文件夹名称时出错: {str(e)}, 使用备用名称: {folder_name}")
            return folder_name
    def log_message(self, message):
        """线程安全的日志记录方法"""
        self.root.after(0, self._log_message, message)
    
    def _log_message(self, message):
        """实际执行日志记录的方法"""
        self.log_text.config(state=NORMAL)
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)
        self.log_text.config(state=DISABLED)

    def update_stats(self, count):
        """线程安全的统计信息更新"""
        self.root.after(0, self._update_stats, count)
    
    def _update_stats(self, count):
        """实际更新统计信息的方法"""
        self.stats_label.config(text=f"总共下载: {count}")

    def deduplicate_files(self):
        """清理所有下载文件夹中的重复文件"""
        if not messagebox.askyesno("确认", "此操作将扫描并删除所有重复内容的图片文件，是否继续？"):
            return
            
        download_dir = os.path.join(os.path.dirname(__file__), 'Download')
        if not os.path.exists(download_dir):
            self.log_message("下载文件夹不存在")
            return
            
        # 获取所有子文件夹
        subfolders = [f for f in os.listdir(download_dir) 
                     if os.path.isdir(os.path.join(download_dir, f))]
                     
        if not subfolders:
            self.log_message("没有找到API下载文件夹")
            return
            
        # 创建进度窗口
        progress_window = Toplevel(self.root)
        progress_window.title("清理重复文件")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        
        Label(progress_window, text="正在扫描文件...").pack(pady=10)
        
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress_bar.pack(fill=X, padx=20, pady=10)
        
        status_label = Label(progress_window, text="准备中...")
        status_label.pack(pady=10)
        
        # 启动去重线程
        threading.Thread(target=self._deduplicate_thread, 
                        args=(download_dir, subfolders, progress_var, status_label, progress_window),
                        daemon=True).start()
    
    def _deduplicate_thread(self, download_dir, subfolders, progress_var, status_label, window):
        """执行去重操作的线程"""
        try:
            total_folders = len(subfolders)
            total_files = 0
            deleted_files = 0
            saved_space = 0
            
            # 全局哈希表
            global_hashes = {}
            
            # 第一步：扫描所有文件
            for i, folder in enumerate(subfolders):
                folder_path = os.path.join(download_dir, folder)
                status_label.config(text=f"扫描文件夹: {folder} ({i+1}/{total_folders})")
                progress_var.set((i / total_folders) * 50)  # 前50%进度用于扫描
                
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                total_files += len(files)
                
                for file in files:
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        
                        file_size = os.path.getsize(file_path)
                        
                        if file_hash in global_hashes:
                            # 已存在相同内容的文件
                            global_hashes[file_hash].append((file_path, file_size))
                        else:
                            global_hashes[file_hash] = [(file_path, file_size)]
                    except Exception as e:
                        self.log_message(f"处理文件 {file} 时出错: {str(e)}")
            
            # 第二步：删除重复文件
            duplicates = {h: files for h, files in global_hashes.items() if len(files) > 1}
            total_duplicates = sum(len(files) - 1 for files in duplicates.values())
            
            status_label.config(text=f"发现 {total_duplicates} 个重复文件，正在清理...")
            
            processed = 0
            for hash_val, files in duplicates.items():
                # 保留第一个文件，删除其余文件
                for file_path, file_size in files[1:]:
                    try:
                        os.remove(file_path)
                        deleted_files += 1
                        saved_space += file_size
                        self.log_message(f"删除重复文件: {os.path.basename(file_path)}")
                    except Exception as e:
                        self.log_message(f"删除文件 {file_path} 时出错: {str(e)}")
                
                processed += len(files) - 1
                progress_var.set(50 + (processed / total_duplicates) * 50)  # 后50%进度用于删除
            
            # 完成
            saved_mb = saved_space / (1024 * 1024)
            status_label.config(text=f"完成! 删除了 {deleted_files} 个重复文件，节省了 {saved_mb:.2f} MB 空间")
            progress_var.set(100)
            
            self.log_message(f"清理完成! 共扫描 {total_files} 个文件，删除了 {deleted_files} 个重复文件，节省了 {saved_mb:.2f} MB 空间")
            
            # 3秒后关闭窗口
            window.after(3000, window.destroy)
            
        except Exception as e:
            self.log_message(f"清理重复文件时发生错误: {str(e)}")
            status_label.config(text=f"发生错误: {str(e)}")
            window.after(3000, window.destroy)

def main():
    root = Tk()
    app = DownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()