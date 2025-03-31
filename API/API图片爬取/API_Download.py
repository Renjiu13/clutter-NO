import argparse
import os
import uuid
import requests
import mimetypes
import threading
import json
import hashlib
import time
import queue
from concurrent.futures import ThreadPoolExecutor
from tkinter import *
from tkinter import ttk, messagebox
from requests.exceptions import RequestException

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("API图片下载器")
        self.running = False
        self.total_downloads = 0
        self.max_downloads = 0
        self.saved_apis = []    # 有效API列表
        self.invalid_apis = []  # 无效API列表
        self.download_queue = queue.Queue()
        self.max_workers = 10   # 最大并发线程数
        self.retry_count = 3    # 最大重试次数
        self.failed_apis = set() # 本次运行失败的API
        
        # 加载保存的API和无效API
        self.load_saved_apis()
        self.create_widgets()

    def load_saved_apis(self):
        """加载保存的API记录和无效API记录"""
        try:
            # 使用绝对路径保存历史记录
            history_path = os.path.join(os.path.dirname(__file__), 'api_history.json')
            with open(history_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.saved_apis = data.get('apis', [])
                self.invalid_apis = data.get('invalid_apis', [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.saved_apis = []
            self.invalid_apis = []

    def save_apis(self, new_apis=[]):
        """保存API记录，避免重复"""
        # 将新API添加到历史记录中，避免重复
        for api in new_apis:
            if api not in self.saved_apis and api not in self.invalid_apis:
                self.saved_apis.append(api)
        
        # 限制历史记录数量，最多保留100条
        if len(self.saved_apis) > 100:
            self.saved_apis = self.saved_apis[-100:]
            
        # 使用绝对路径保存历史记录
        history_path = os.path.join(os.path.dirname(__file__), 'api_history.json')
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump({
                'apis': self.saved_apis,
                'invalid_apis': self.invalid_apis
            }, f, ensure_ascii=False, indent=2)
        
        # 如果历史列表已存在，则更新它
        if hasattr(self, 'history_listbox'):
            self.update_history_listbox()

    def update_history_listbox(self):
        """更新历史API列表显示"""
        if hasattr(self, 'history_listbox'):
            self.history_listbox.delete(0, END)
            # 先显示有效API
            for api in self.saved_apis:
                self.history_listbox.insert(END, api)
            # 再显示无效API，带标记
            for api in self.invalid_apis:
                self.history_listbox.insert(END, f"[无效] {api}")

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
        
        # 添加第二行按钮
        btn_frame2 = Frame(main_frame, bg=bg_color)
        btn_frame2.pack(pady=(0, 10), fill=X)
        
        # 添加清理空文件夹按钮
        self.clean_empty_btn = Button(btn_frame2, text="清理空文件夹", command=self.clean_empty_folders,
                                    bg="#f39c12", fg="white", font=normal_font, width=15)
        self.clean_empty_btn.pack(side=LEFT, padx=5)
        
        # 添加测试API按钮
        self.test_api_btn = Button(btn_frame2, text="测试API有效性", command=self.test_and_clean_apis,
                                 bg="#3498db", fg="white", font=normal_font, width=15)
        self.test_api_btn.pack(side=LEFT, padx=5)
        
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
            selected_apis = []
            for i in selection:
                api_text = self.history_listbox.get(i)
                # 如果是无效API（带[无效]前缀），则去掉前缀
                if api_text.startswith("[无效] "):
                    api_text = api_text[6:]  # 去掉"[无效] "前缀
                selected_apis.append(api_text)
            
            self.api_text.delete("1.0", END)
            self.api_text.insert(END, "\n".join(selected_apis))
            self.log_message(f"已加载 {len(selected_apis)} 个API")
    
    def log_message(self, message):
        """向日志文本框添加消息"""
        if hasattr(self, 'log_text'):
            self.log_text.config(state=NORMAL)
            self.log_text.insert(END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
            self.log_text.see(END)  # 自动滚动到最新消息
            self.log_text.config(state=DISABLED)
            # 确保UI更新
            self.root.update_idletasks()
    
    def get_folder_name_from_url(self, url):
        """从URL生成文件夹名称"""
        # 移除协议前缀
        url_no_protocol = url.split('://')[-1]
        
        # 提取域名部分
        domain = url_no_protocol.split('/')[0]
        
        # 使用域名作为基础，但避免特殊字符
        folder_name = ''.join(c if c.isalnum() or c in '.-' else '_' for c in domain)
        
        # 添加URL的哈希值后缀以确保唯一性
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        return f"{folder_name}_{url_hash}"
    
    def update_stats(self, count):
        """更新统计信息"""
        if hasattr(self, 'stats_label'):
            self.stats_label.config(text=f"总共下载: {count}")
            # 确保UI更新
            self.root.update_idletasks()
    
    def start_download(self):
        """开始下载任务"""
        api_urls = [url.strip() for url in self.api_text.get("1.0", END).split("\n") if url.strip()]
        
        if not api_urls:
            messagebox.showerror("错误", "请输入至少一个API地址")
            return

        # 保存API记录
        self.save_apis(api_urls)
            
        # 获取下载数量
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
        
        # 重置下载队列
        while not self.download_queue.empty():
            self.download_queue.get()
        
        # 重置失败API集合
        self.failed_apis = set()
        
        # 将所有API添加到队列
        for url in api_urls:
            # 跳过已知的无效API
            if url in self.invalid_apis:
                self.log_message(f"跳过已知无效API: {url}")
                continue
            self.download_queue.put(url)
        
        # 创建统计标签
        self.stats_label.config(text=f"总共下载: 0")
        self.total_downloads = 0
        
        # 使用线程池管理下载线程
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.download_manager_thread = threading.Thread(target=self.manage_downloads)
        self.download_manager_thread.daemon = True
        self.download_manager_thread.start()
        
        self.log_message(f"已启动下载管理器，最大并发线程数: {self.max_workers}")
    
    def manage_downloads(self):
        """管理下载线程池"""
        active_tasks = {}  # 跟踪活动任务
        api_folders = {}   # 记录API对应的文件夹
        api_download_counts = {}  # 记录每个API的下载数量
        
        try:
            while self.running:
                # 检查是否有完成的任务
                completed = [url for url, future in active_tasks.items() if future.done()]
                for url in completed:
                    future = active_tasks.pop(url)
                    try:
                        # 获取下载结果
                        success, download_count = future.result()
                        if not success and url not in self.failed_apis:
                            self.failed_apis.add(url)
                            self.log_message(f"⚠ API无法访问: {url}")
                    except Exception as e:
                        self.log_message(f"获取下载结果时出错: {str(e)}")
                        if url not in self.failed_apis:
                            self.failed_apis.add(url)
                
                # 如果队列不为空且活动任务数小于最大工作线程数，添加新任务
                while not self.download_queue.empty() and len(active_tasks) < self.max_workers:
                    url = self.download_queue.get()
                    
                    # 为每个API创建独立文件夹
                    if url not in api_folders:
                        api_folder_name = self.get_folder_name_from_url(url)
                        api_download_dir = os.path.join(self.download_dir, api_folder_name)
                        os.makedirs(api_download_dir, exist_ok=True)
                        api_folders[url] = (api_folder_name, api_download_dir)
                        api_download_counts[url] = 0
                    
                    # 提交下载任务到线程池
                    future = self.executor.submit(
                        self.download_single_file, url, *api_folders[url], api_download_counts[url])
                    active_tasks[url] = future
                
                # 如果所有任务都完成且队列为空，结束循环
                if not active_tasks and self.download_queue.empty():
                    if self.running:  # 确保不是因为用户停止而结束
                        self.root.after(0, self.download_completed)
                    break
                
                time.sleep(0.1)  # 避免CPU占用过高
                
        except Exception as e:
            self.log_message(f"下载管理器发生错误: {str(e)}")
            self.root.after(0, lambda: self.stop_download())
    
    def download_completed(self):
        """下载完成后的处理"""
        self.running = False
        self.start_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        
        # 处理失败的API
        if self.failed_apis:
            self.log_message(f"有 {len(self.failed_apis)} 个API无法访问，已标记为无效")
            
            # 将失败的API添加到无效API列表
            for api in self.failed_apis:
                if api not in self.invalid_apis:
                    self.invalid_apis.append(api)
                # 如果在有效API列表中，则移除
                if api in self.saved_apis:
                    self.saved_apis.remove(api)
            
            # 保存API记录
            self.save_apis()
            
            # 提示用户是否要清理无效API创建的文件夹
            if messagebox.askyesno("清理提示", "是否要清理无效API创建的文件夹？"):
                self.clean_invalid_api_folders()
        
        self.log_message("所有API下载任务已完成!")
    
    def load_existing_hashes(self, folder_path, hash_dict):
        """加载文件夹中已有文件的哈希值"""
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            for file in files:
                file_path = os.path.join(folder_path, file)
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    hash_dict[file_hash] = file
                except Exception:
                    # 忽略无法读取的文件
                    pass
        except Exception:
            # 如果文件夹不存在或无法访问，则忽略
            pass
    
    def stop_download(self):
        """停止下载任务"""
        if self.running:
            self.running = False
            self.log_message("正在停止下载任务...")
            # 关闭线程池
            if hasattr(self, 'executor'):
                self.executor.shutdown(wait=False)
            self.start_btn.config(state=NORMAL)
            self.stop_btn.config(state=DISABLED)
    
    def deduplicate_files(self):
        """清理重复文件"""
        download_dir = os.path.join(os.path.dirname(__file__), 'Download')
        if not os.path.exists(download_dir):
            messagebox.showinfo("提示", "下载文件夹不存在")
            return
            
        # 获取所有子文件夹
        subfolders = [f for f in os.listdir(download_dir) 
                     if os.path.isdir(os.path.join(download_dir, f))]
        
        if not subfolders:
            messagebox.showinfo("提示", "没有找到子文件夹")
            return
            
        # 询问用户是清理所有文件夹还是选择特定文件夹
        result = messagebox.askyesnocancel("选择", "是否清理所有子文件夹的重复文件?\n是 - 清理所有\n否 - 选择特定文件夹\n取消 - 取消操作")
        
        if result is None:  # 用户取消
            return
            
        folders_to_clean = []
        
        if result:  # 清理所有文件夹
            folders_to_clean = subfolders
        else:  # 选择特定文件夹
            # 创建文件夹选择对话框
            folder_window = Toplevel(self.root)
            folder_window.title("选择要清理的文件夹")
            folder_window.geometry("300x400")
            folder_window.resizable(False, False)
            
            Label(folder_window, text="选择要清理的文件夹:").pack(pady=10)
            
            # 创建子文件夹列表 - 支持多选
            folder_frame = Frame(folder_window)
            folder_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
            
            scrollbar = Scrollbar(folder_frame)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            folder_list = Listbox(folder_frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED)
            for folder in sorted(subfolders):
                folder_list.insert(END, folder)
            folder_list.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.config(command=folder_list.yview)
            
            # 选择按钮
            def confirm_selection():
                nonlocal folders_to_clean
                selection = folder_list.curselection()
                if selection:
                    folders_to_clean = [folder_list.get(i) for i in selection]
                    folder_window.destroy()
                    self._perform_deduplication(folders_to_clean)
                else:
                    messagebox.showwarning("警告", "请至少选择一个文件夹")
            
            Button(folder_window, text="确认选择", 
                  command=confirm_selection).pack(pady=10, fill=X, padx=10)
            
            # 等待窗口关闭
            folder_window.transient(self.root)
            folder_window.grab_set()
            self.root.wait_window(folder_window)
            return
        
        # 执行去重操作
        if folders_to_clean:
            self._perform_deduplication(folders_to_clean)
    
    def _perform_deduplication(self, folder_names):
        """执行文件去重操作"""
        download_dir = os.path.join(os.path.dirname(__file__), 'Download')
        
        # 创建进度窗口
        progress_window = Toplevel(self.root)
        progress_window.title("去重进度")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        
        Label(progress_window, text="正在清理重复文件...").pack(pady=10)
        
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress_bar.pack(fill=X, padx=20, pady=10)
        
        status_label = Label(progress_window, text="准备中...")
        status_label.pack(pady=5)
        
        # 使用线程执行去重操作
        def run_deduplication():
            total_folders = len(folder_names)
            total_files = 0
            removed_files = 0
            
            # 第一遍扫描，计算文件总数
            for i, folder_name in enumerate(folder_names):
                folder_path = os.path.join(download_dir, folder_name)
                try:
                    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                    total_files += len(files)
                except Exception:
                    pass
                progress_var.set((i + 1) / total_folders * 50)  # 前50%进度用于扫描
                status_label.config(text=f"扫描中: {i+1}/{total_folders} 文件夹")
                progress_window.update()
            
            # 第二遍扫描，执行去重
            all_hashes = {}
            processed_files = 0
            
            for i, folder_name in enumerate(folder_names):
                folder_path = os.path.join(download_dir, folder_name)
                status_label.config(text=f"处理中: {folder_name}")
                progress_window.update()
                
                try:
                    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                    for file in files:
                        file_path = os.path.join(folder_path, file)
                        try:
                            with open(file_path, 'rb') as f:
                                file_hash = hashlib.md5(f.read()).hexdigest()
                            
                            processed_files += 1
                            progress_var.set(50 + (processed_files / total_files * 50))
                            
                            if file_hash in all_hashes:
                                # 文件是重复的，删除它
                                os.remove(file_path)
                                removed_files += 1
                                status_label.config(text=f"删除重复文件: {file}")
                            else:
                                all_hashes[file_hash] = file_path
                        except Exception as e:
                            pass
                        
                        progress_window.update()
                except Exception:
                    pass
            
            # 完成
            progress_var.set(100)
            status_label.config(text=f"完成! 共处理 {total_files} 个文件，删除 {removed_files} 个重复文件")
            
            # 添加关闭按钮
            Button(progress_window, text="关闭", command=progress_window.destroy).pack(pady=10)
            
            # 记录日志
            self.log_message(f"去重完成: 共处理 {total_files} 个文件，删除 {removed_files} 个重复文件")
        
        # 启动线程
        threading.Thread(target=run_deduplication, daemon=True).start()
    
    def delete_selected_api(self):
        """删除选中的历史API"""
        selection = self.history_listbox.curselection()
        if not selection:
            messagebox.showinfo("提示", "请先选择要删除的API")
            return
            
        # 确认删除
        if not messagebox.askyesno("确认", "确定要删除选中的API吗?"):
            return
            
        # 获取选中的API
        selected_apis = []
        for i in reversed(selection):  # 从后向前删除，避免索引变化
            api_text = self.history_listbox.get(i)
            
            # 判断是有效API还是无效API
            if api_text.startswith("[无效] "):
                api = api_text[6:]  # 去掉"[无效] "前缀
                if api in self.invalid_apis:
                    self.invalid_apis.remove(api)
            else:
                if api_text in self.saved_apis:
                    self.saved_apis.remove(api_text)
        
        # 保存更改
        self.save_apis()
        self.log_message(f"已删除 {len(selection)} 个API")
    
    def clear_history(self):
        """清空历史记录"""
        if not messagebox.askyesno("确认", "确定要清空所有历史记录吗?"):
            return
            
        self.saved_apis = []
        self.invalid_apis = []
        self.save_apis()
        self.log_message("已清空所有历史记录")
    
    def clean_invalid_api_folders(self):
        """清理无效API创建的文件夹"""
        download_dir = os.path.join(os.path.dirname(__file__), 'Download')
        if not os.path.exists(download_dir):
            return
            
        # 获取所有无效API的文件夹名称
        invalid_folders = []
        for api in self.invalid_apis:
            folder_name = self.get_folder_name_from_url(api)
            folder_path = os.path.join(download_dir, folder_name)
            if os.path.exists(folder_path):
                invalid_folders.append((folder_name, folder_path))
        
        if not invalid_folders:
            self.log_message("没有找到无效API创建的文件夹")
            return
            
        # 创建进度窗口
        progress_window = Toplevel(self.root)
        progress_window.title("清理进度")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        
        Label(progress_window, text=f"正在清理 {len(invalid_folders)} 个无效API文件夹...").pack(pady=10)
        
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress_bar.pack(fill=X, padx=20, pady=10)
        
        status_label = Label(progress_window, text="准备中...")
        status_label.pack(pady=5)
        
        # 使用线程执行清理操作
        def run_cleanup():
            import shutil
            
            total_folders = len(invalid_folders)
            removed_folders = 0
            
            for i, (folder_name, folder_path) in enumerate(invalid_folders):
                try:
                    status_label.config(text=f"正在删除: {folder_name}")
                    progress_var.set((i / total_folders) * 100)
                    progress_window.update()
                    
                    shutil.rmtree(folder_path)
                    removed_folders += 1
                except Exception as e:
                    self.log_message(f"删除文件夹 {folder_name} 失败: {str(e)}")
            
            # 完成
            progress_var.set(100)
            status_label.config(text=f"完成! 已删除 {removed_folders}/{total_folders} 个文件夹")
            
            # 添加关闭按钮
            Button(progress_window, text="关闭", command=progress_window.destroy).pack(pady=10)
            
            # 记录日志
            self.log_message(f"清理完成: 已删除 {removed_folders}/{total_folders} 个无效API文件夹")
        
        # 启动线程
        threading.Thread(target=run_cleanup, daemon=True).start()
    
    def download_single_file(self, api_url, folder_name, download_dir, current_count):
        """从API下载单个文件"""
        # 检查是否达到最大下载数量
        if self.max_downloads > 0 and self.total_downloads >= self.max_downloads:
            return True, 0
        
        # 检查是否已停止
        if not self.running:
            return False, 0
        
        # 创建文件哈希字典，用于避免重复下载
        file_hashes = {}
        self.load_existing_hashes(download_dir, file_hashes)
        
        # 下载计数
        download_count = 0
        retry_attempts = 0
        
        while self.running and (self.max_downloads == 0 or self.total_downloads < self.max_downloads):
            try:
                # 请求API获取图片
                response = requests.get(api_url, timeout=10)
                
                # 检查响应状态
                if response.status_code != 200:
                    retry_attempts += 1
                    if retry_attempts >= self.retry_count:
                        self.log_message(f"API响应错误 ({response.status_code}): {api_url}")
                        return False, download_count
                    time.sleep(1)  # 等待一秒后重试
                    continue
                
                # 重置重试计数
                retry_attempts = 0
                
                # 获取内容类型
                content_type = response.headers.get('Content-Type', '')
                
                # 检查是否为图片
                if not content_type.startswith('image/'):
                    self.log_message(f"API返回非图片内容: {content_type}")
                    return False, download_count
                
                # 计算文件哈希以避免重复
                content_hash = hashlib.md5(response.content).hexdigest()
                
                # 检查是否已存在相同文件
                if content_hash in file_hashes:
                    self.log_message(f"跳过重复图片: {file_hashes[content_hash]}")
                    continue
                
                # 确定文件扩展名
                extension = mimetypes.guess_extension(content_type)
                if not extension:
                    # 如果无法确定扩展名，使用默认扩展名
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        extension = '.jpg'
                    elif 'png' in content_type:
                        extension = '.png'
                    elif 'gif' in content_type:
                        extension = '.gif'
                    elif 'webp' in content_type:
                        extension = '.webp'
                    else:
                        extension = '.jpg'  # 默认使用jpg
                
                # 生成唯一文件名
                filename = f"{uuid.uuid4().hex}{extension}"
                file_path = os.path.join(download_dir, filename)
                
                # 保存文件
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                # 更新哈希字典
                file_hashes[content_hash] = filename
                
                # 更新下载计数
                download_count += 1
                self.total_downloads += 1
                
                # 更新统计信息
                self.root.after(0, lambda: self.update_stats(self.total_downloads))
                
                # 记录日志
                if download_count % 5 == 0 or download_count == 1:
                    self.log_message(f"已从 {folder_name} 下载 {download_count} 张图片")
                
            except RequestException as e:
                retry_attempts += 1
                if retry_attempts >= self.retry_count:
                    self.log_message(f"API请求失败: {str(e)}")
                    return False, download_count
                time.sleep(1)  # 等待一秒后重试
                
            except Exception as e:
                self.log_message(f"下载出错: {str(e)}")
                return False, download_count
        
        return True, download_count

    def test_and_clean_apis(self):
        """测试并清理无效的API"""
        if not self.saved_apis:
            messagebox.showinfo("提示", "没有保存的API")
            return
        
        # 创建进度窗口
        progress_window = Toplevel(self.root)
        progress_window.title("API测试")
        progress_window.geometry("500x300")
        progress_window.resizable(False, False)
        
        Label(progress_window, text="正在测试API有效性...").pack(pady=10)
        
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress_bar.pack(fill=X, padx=20, pady=10)
        
        status_label = Label(progress_window, text="准备中...")
        status_label.pack(pady=5)
        
        result_text = Text(progress_window, height=10, width=60)
        result_text.pack(fill=BOTH, expand=True, padx=20, pady=5)
        
        result_scrollbar = Scrollbar(result_text)
        result_text.config(yscrollcommand=result_scrollbar.set)
        result_scrollbar.config(command=result_text.yview)
        result_scrollbar.pack(side=RIGHT, fill=Y)
        
        # 使用线程执行测试
        def run_test():
            total_apis = len(self.saved_apis)
            invalid_apis = []
            
            for i, api in enumerate(self.saved_apis):
                try:
                    status_label.config(text=f"测试API: {api}")
                    progress_var.set((i / total_apis) * 100)
                    progress_window.update()
                    
                    # 尝试请求API
                    response = requests.get(api, timeout=5)
                    
                    # 检查响应状态
                    if response.status_code != 200:
                        invalid_apis.append(api)
                        result_text.insert(END, f"[无效] {api} - 状态码: {response.status_code}\n")
                    else:
                        # 检查内容类型
                        content_type = response.headers.get('Content-Type', '')
                        if not content_type.startswith('image/'):
                            invalid_apis.append(api)
                            result_text.insert(END, f"[无效] {api} - 非图片内容: {content_type}\n")
                        else:
                            result_text.insert(END, f"[有效] {api}\n")
                    
                    result_text.see(END)
                    
                except Exception as e:
                    invalid_apis.append(api)
                    result_text.insert(END, f"[无效] {api} - 错误: {str(e)}\n")
                    result_text.see(END)
            
            # 完成测试
            progress_var.set(100)
            status_label.config(text=f"测试完成! 发现 {len(invalid_apis)}/{total_apis} 个无效API")
            
            # 如果有无效API，直接删除
            if invalid_apis:
                # 将无效API从有效列表移除
                for api in invalid_apis:
                    if api in self.saved_apis:
                        self.saved_apis.remove(api)
                    if api not in self.invalid_apis:
                        self.invalid_apis.append(api)
                
                # 保存更改
                self.save_apis()
                self.log_message(f"已删除 {len(invalid_apis)} 个无效API")
                
                # 询问是否要清理无效API创建的文件夹
                if messagebox.askyesno("清理确认", "是否要清理无效API创建的文件夹?"):
                    progress_window.destroy()
                    self.clean_invalid_api_folders()
                    return
            
            # 添加关闭按钮
            Button(progress_window, text="关闭", command=progress_window.destroy).pack(pady=10)
        
        # 启动线程
        threading.Thread(target=run_test, daemon=True).start()
    
    def clean_empty_folders(self):
        """清理空文件夹"""
        download_dir = os.path.join(os.path.dirname(__file__), 'Download')
        if not os.path.exists(download_dir):
            messagebox.showinfo("提示", "下载文件夹不存在")
            return
        
        # 获取所有子文件夹
        subfolders = [f for f in os.listdir(download_dir) 
                     if os.path.isdir(os.path.join(download_dir, f))]
        
        if not subfolders:
            messagebox.showinfo("提示", "没有找到子文件夹")
            return
        
        # 创建进度窗口
        progress_window = Toplevel(self.root)
        progress_window.title("清理空文件夹")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        
        Label(progress_window, text="正在扫描空文件夹...").pack(pady=10)
        
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=100)
        progress_bar.pack(fill=X, padx=20, pady=10)
        
        status_label = Label(progress_window, text="准备中...")
        status_label.pack(pady=5)
        
        # 使用线程执行清理操作
        def run_cleanup():
            total_folders = len(subfolders)
            empty_folders = []
            
            # 扫描空文件夹
            for i, folder_name in enumerate(subfolders):
                folder_path = os.path.join(download_dir, folder_name)
                status_label.config(text=f"扫描中: {folder_name}")
                progress_var.set((i / total_folders) * 50)
                progress_window.update()
                
                # 检查文件夹是否为空
                try:
                    if not os.listdir(folder_path):
                        empty_folders.append((folder_name, folder_path))
                except Exception:
                    pass
            
            # 删除空文件夹
            total_empty = len(empty_folders)
            if total_empty == 0:
                progress_var.set(100)
                status_label.config(text="没有找到空文件夹")
                Button(progress_window, text="关闭", command=progress_window.destroy).pack(pady=10)
                self.log_message("没有找到空文件夹")
                return
            
            removed_count = 0
            for i, (folder_name, folder_path) in enumerate(empty_folders):
                try:
                    status_label.config(text=f"删除空文件夹: {folder_name}")
                    progress_var.set(50 + (i / total_empty) * 50)
                    progress_window.update()
                    
                    os.rmdir(folder_path)
                    removed_count += 1
                except Exception as e:
                    self.log_message(f"删除文件夹 {folder_name} 失败: {str(e)}")
            
            # 完成
            progress_var.set(100)
            status_label.config(text=f"完成! 已删除 {removed_count}/{total_empty} 个空文件夹")
            Button(progress_window, text="关闭", command=progress_window.destroy).pack(pady=10)
            self.log_message(f"清理完成: 已删除 {removed_count}/{total_empty} 个空文件夹")
        
        # 启动线程
        threading.Thread(target=run_cleanup, daemon=True).start()

# 主程序入口
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='API图片下载器')
    parser.add_argument('--api', help='API地址，多个地址用逗号分隔')
    parser.add_argument('--count', type=int, default=0, help='下载数量，0表示无限')
    args = parser.parse_args()
    
    root = Tk()
    app = DownloaderApp(root)
    
    # 如果命令行提供了API，则自动填充
    if args.api:
        apis = args.api.split(',')
        app.api_text.delete("1.0", END)
        app.api_text.insert(END, "\n".join(apis))
    
    # 如果命令行提供了下载数量，则自动填充
    if args.count > 0:
        app.count_entry.delete(0, END)
        app.count_entry.insert(0, str(args.count))
    
    root.mainloop()