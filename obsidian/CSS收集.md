# obsidian收集CSS片段

## 代码块

### 代码块显示行号

```
.HyperMD-codeblock-begin {
  counter-reset: line-numbers;
}

.HyperMD-codeblock.cm-line:not(.HyperMD-codeblock-begin):not(.HyperMD-codeblock-end) {
  padding-left: 3em;
  position: relative;
}

.HyperMD-codeblock.cm-line:not(.HyperMD-codeblock-begin):not(.HyperMD-codeblock-end)::after {
  align-items: flex-start;
  color: var(--text-faint);
  content: counter(line-numbers);
  counter-increment: line-numbers;
  display: flex;
  font-size: 0.8em;
  height: 100%;
  justify-content: flex-end;
  left: 0;
  position: absolute;
  text-align: right;
  width: 2em;
  padding-right: 0.5em;
  bottom: -2px;
  border-right: 1px solid var(--scrollbar-thumb-bg);
 white-space: nowrap;
}

.HyperMD-codeblock.cm-line.cm-active:not(.HyperMD-codeblock-begin):not(.HyperMD-codeblock-end)::after {
  color: var(--color-accent);
}

.HyperMD-codeblock .cm-foldPlaceholder::before {
  display: none;
}

```


### 圆角代码块


```
/* !代码块显示长度 */
/* https://forum-zh.obsidian.md/t/topic/27088 */
pre code {
  display: block;
  max-height: 500px;
  overflow-x: hidden;
  /* 添加自动换行 */
  white-space: pre-wrap;
}

/* 隐藏滚动条只在代码块内生效 */
pre code::-webkit-scrollbar {
  display:inherit !important;
}

/*! 以下CSS片段参考PinkTopaz主题的代码块样式 */

/* !代码块按钮设置*/
/*===========================*/
/*copy button for code blocks*/
/*===========================*/
.copy-code-button {
  writing-mode: vertical-rl;
  width: 1.2rem;
  font-size: large !important;
  color: transparent !important;
  border-radius: 0px 5px 5px 0px !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  margin-bottom: 0 !important;
  padding: 0px 1px !important;
  position: absolute;
  top: 0 !important;
  bottom: 0px !important;
}

.copy-code-button:hover {
  background-color: #696c6e7c !important;
  color: aliceblue !important;
}

/* Code */
:not(pre)>code[class*="language-"],
pre[class*="language-"] {
  background-color: var(--background-primary-alt);
  /* 代码块 圆角 阴影 */
  border-left: 0.5rem solid slateblue !important;
  border-radius: 6px;
  margin-top: 10px;
  margin-bottom: 10px;
  box-shadow: rgb(0 0 0/15%) 0px 2px 10px;
}

pre {
  position: relative;
  color: slateblue !important;
  line-height: 20px !important;
}

/* 每个语言单独写 C语言 要写在前面 否则出现覆盖C# C++的问题 */
pre::before{
  position: absolute;
  right: 20px !important;
}

pre[class='language-c']:before {
  content: "C";
}

pre[class='language-py']:before {
  content: "Python";
}

pre[class='language-python']:before {
  content: "Python";
}

pre[class='language-nginx']:before {
  content: "Nginx";
}

pre[class='language-css']:before {
  content: "CSS";
}

pre[class='language-javascript']:before {
  content: "JS";
}

pre[class='language-js']:before {
  content: "JS";
}


pre[class='language-php']:before {
  content: "Php";
}

pre[class='language-shell']:before {
  content: "Shell";
}

pre[class='language-flow']:before {
  content: "Flow";
}

pre[class='language-sequence']:before {
  content: "Sequence";
}

pre[class='language-sql']:before {
  content: "Sql";
}

pre[class='language-yaml']:before {
  content: "Yaml";
}

pre[class='language-ini']:before {  
  content: "ini";  
}  

pre[class='language-xml']:before {  
  content: "Xml";  
}  

pre[class='language-git']:before {  
  content: "Git";  
}  

pre[class='language-cs']:before {  
  content: "C#";  
}  

pre[class='language-cpp']:before {  
  content: "C++";  
}  

pre[class='language-java']:before {  
  content: "Java";  
}  

pre[class='language-html']:before {  
  content: "Html";  
}  

pre[class='language-txt']:before {  
  content: "txt";  
}  
```


## 链接美化

### 链接美化

![示例图|475](https://tc-cdn.flowus.cn/oss/d6715e35-82a4-4050-b0e9-03fd93a61de9/%25E9%2593%25BE%25E6%258E%25A5.gif?time=1734777000&token=d84403e49394a2d9a011ca7d9ac10819ec103ea5ebb2a1b9dca6566e1fa9358f&role=sharePaid)


```
body {  
  
  /* 内部链接颜色 */
  --link-color: #5291e5;  
  
  /* 鼠标经过当前行内部链接文字颜色 */
  --link-color-hover: var(--text-accent);  
  
  /* 外部链接颜色 */
  --link-external-color: #ff9f31;  
  
  /* 鼠标经过当前行外部链接文字颜色 */
  --link-external-color-hover: var(--text-accent);  
  
  /* 脚注颜色 */
  --link-footnote: var(--color-purple);  
  
  --link-decoration-hover: none;  
  --link-external-decoration-hover: none;  
  --animation: var(--anim-duration-fast) var(--anim-motion-smooth);  
}  

@property --link-offset {  
  syntax: "<length>";  
  inherits: false;  
  initial-value: 4px;  
}  
@property --link-thickness {  
  syntax: "<length>";  
  inherits: false;  
  initial-value: 2px;  
}  
:is(a.external-link, .cm-link .cm-underline) {  
  font-size: var(--font-text-size);
  text-underline-offset: var(--link-offset);
  color: var(--link-external-color) !important;
  -webkit-text-decoration-line: underline !important;
          text-decoration-line: underline !important;
  -webkit-text-decoration-skip-ink: none;
          text-decoration-skip-ink: none;
  -webkit-text-decoration-color: var(--link-external-color) !important;
          text-decoration-color: var(--link-external-color) !important;
  text-decoration-thickness: var(--link-thickness) !important;
  transition: --link-offset var(--animation), --link-thickness var(--animation), color var(--animation);
}
:is(a.external-link, .cm-link .cm-underline):hover, :is(a.external-link, .cm-link .cm-underline):focus {
  color: var(--text-on-accent) !important;
  --link-offset: calc(var(--font-text-size) * -1 - var(--size-4-4));
  --link-thickness: calc(var(--font-text-size) + 10px);
}

.cm-hmd-footnote .cm-underline {
  color: var(--link-footnote) !important;
  font-size: var(--footnote-size);
  -webkit-text-decoration-color: var(--link-footnote) !important;
          text-decoration-color: var(--link-footnote) !important;
  pointer-events: none;
}

body:not(.click-to-edit-link-in-live-preview) :is(:is(.markdown-source-view, .markdown-preview-view) a.external-link, :is(.cm-link:not(.cm-hmd-footnote, .cm-escape), .cm-url) .cm-underline):not(.cm-escape+.cm-link .cm-underline)::before {
  content: "";
  display: inline-block;
  transform: translateY(var(--size-2-1));
  width: calc(var(--font-text-size) - var(--size-4-1));
  height: calc(var(--font-text-size) - var(--size-4-1));
  margin-right: var(--size-4-1);
  background-color: var(--link-external-color);
  -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon lucide-link"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>');
}

:is(a.internal-link, .cm-hmd-internal-link .cm-underline) {
  font-size: var(--font-text-size);
  text-underline-offset: var(--link-offset);
  color: var(--link-color) !important;
  -webkit-text-decoration-line: underline !important;
          text-decoration-line: underline !important;
  -webkit-text-decoration-skip-ink: none;
          text-decoration-skip-ink: none;
  -webkit-text-decoration-color: var(--link-color) !important;
          text-decoration-color: var(--link-color) !important;
  text-decoration-thickness: var(--link-thickness) !important;
  transition: --link-offset var(--animation), --link-thickness var(--animation), color var(--animation);
}
:is(a.internal-link, .cm-hmd-internal-link .cm-underline):hover, :is(a.internal-link, .cm-hmd-internal-link .cm-underline):focus {
  color: var(--text-on-accent) !important;
  --link-offset: calc(var(--font-text-size) * -1 - var(--size-4-4));
  --link-thickness: calc(var(--font-text-size) + 10px);
}

:is(.markdown-preview-view a.internal-link, .cm-hmd-internal-link .cm-underline)::before {
  content: "";
  display: inline-block;
  transform: translateY(var(--size-2-1));
  width: calc(var(--font-text-size) - var(--size-2-1));
  height: calc(var(--font-text-size) - var(--size-2-1));
  margin-right: var(--size-2-1);
  background-color: var(--link-color);
  -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill=""><path d="M0 0h24v24H0V0z" fill="none"/><path d="M8 16h8v2H8zm0-4h8v2H8zm6-10H6c-1.1 0-2 .9-2 2v16c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm4 18H6V4h7v5h5v11z"/></svg>');
}

:is(.cm-hmd-internal-link, .cm-link) {
  transition: color var(--animation);
}

.cm-url {
  color: var(--link-color) !important;
}

span.cm-formatting-link {
  color: var(--accent-active) !important;
}

body:not(.click-to-edit-link-in-live-preview) a.external-link {
  background-image: none;
  background-size: unset;
  padding-right: 0;
}
body:not(.click-to-edit-link-in-live-preview) span.external-link {
  display: none;
}

body.click-to-edit-link-in-live-preview :is(.cm-link .cm-underline, .cm-hmd-internal-link .cm-underline) {
  pointer-events: none;
}

/* @settings

name: theme-subframe7536
id: theme-subframe7536
settings:
    -
        id: click-to-edit-link-in-live-preview
        title: click to edit link in live preview
        description.zh: live preview 模式时点击链接进行编辑而不是跳转
        type: class-toggle
*/
```


### 编辑优化

```
/* Moy Link Optimize.css */

/* 点击链接的时候不跳转 */
/* Style Settings 开关 */
/* @settings

name: Moy Link Mods
id: moy-link-mods
settings:
    - 
        id: link-editing-mode
        title: Link Editing Mode
        title.zh: 链接编辑模式
        description: Cancel the link left mouse button click event
        description.zh: 是否取消链接的左键点击功能
        type: class-toggle
        default: true
        addCommand: true
    - 
        id: link-shorten
        title: Link Shorten
        title.zh: 缩短链接
        description: Shorten the link, unless mouse hover
        description.zh: 将链接缩短为 emoji，鼠标经过才完整显示
        type: class-toggle
        default: true
        addCommand: true

*/


.link-editing-mode .cm-link .cm-underline,
.link-editing-mode .cm-hmd-internal-link .cm-underline {
  pointer-events: none;
}


/* 隐藏过长的链接网址部分 */
/* Src: https://forum.obsidian.md/t/how-to-hide-url-link-in-edit-mode-until-hovered-on/82827 */
/* Hide the URL text and show the symbol */
.link-shorten div.cm-line .cm-string.cm-url:not(.cm-formatting) {
    font-size: 0;
}

/* Display a symbol after the URL */
.link-shorten div.cm-line .cm-string.cm-url:not(.cm-formatting)::after {
    content: '🔗'; /* Replace with your desired symbol */
    font-size: 1rem; /* Adjust font size as needed */
    color: inherit; /* Inherit color from the parent element */
}

/* Ensure the URL text is visible when the cursor is over it */
.link-shorten div.cm-line .cm-string.cm-url:not(.cm-formatting):hover {
    font-size: inherit;
}

/* Hide the symbol when the cursor is over the URL */
.link-shorten div.cm-line .cm-string.cm-url:not(.cm-formatting):hover::after {
    content: '';
}


/* 修改 wikilink 格式的 */
/* Modified by Moy */
.link-shorten .cm-hmd-internal-link.cm-link-has-alias {
    font-size: 0;
}

.link-shorten .cm-hmd-internal-link.cm-link-has-alias:hover {
    font-size: inherit;
}

.link-shorten .cm-hmd-internal-link.cm-link-has-alias:not(.cm-formatting)::after {
    content: '📜'; /* Replace with your desired symbol 📄 */
    font-size: 1rem; /* Adjust font size as needed */
    color: inherit; /* Inherit color from the parent element */
}
```

### 下划线与图标

```
/*---------------------------外部链接样式优化---------------------------------------------*/
/* 外部链接取消右上角的链接图标和下划线 */
.external-link {
    background-image: none !important; /* 取消右上角的链接图标 */
    text-decoration: none; /* 取消下划线 */
  }
  
```




## 代办事项

### 清除任务的删除线

```
/* 
@Author   : 咖啡豆
@contact  : https://obsidian.vip/
@File     : coffeebean-去除删除线-任务回顾专用.css
@Software : vscode
@Date     : 2022-10-17
@upDate   : 2022-10-17
@Desc     : CSS提供给系统yaml调用，调用格式如下
            ---
            cssclass: coffeebean-del-checklist-done-decoration
            ---
@Source    :[CSS片段-清除任务的删除线 | obsidian文档咖啡豆版](https://obsidian.vip/zh/css-snippets/coffeebean-del-checklist-done-decoration.html)
*/

/* 去除删除线效果 */
.coffeebean-del-checklist-done-decoration ul > li.task-list-item[data-task="x"], ul > li.task-list-item[data-task="X"]{
    text-decoration: none !important;
}

```


## 表格优化


### 优化一

```
/* 来源地址 */
/* https://forum-zh.obsidian.md/t/topic/27878/18 */

body {
    /* 表格圆角大小 */
    --table-radius: var(--size-2-3);
    /* 表格按钮颜色 */
    --table-btn-color: #fff;
    /* 表格按钮背景色 */
    --table-btn-bg: #ddd;
    /* 表格头背景色 */
    --table-header-bg: #f4f4f4;
    /* 表格隔行背景色 */
    --table-alt-line-bg: #fff;
    /* 动画时间 */
    --animation: 200ms var(--anim-motion-smooth);
  }
  
  .markdown-rendered table {
    border-collapse: initial;
    border-spacing: 0;
  }
  
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) {
    --table-white-space: break-all;
    width: 100%;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) .table-editor {
    width: 100%;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) .table-col-btn {
    border-top-right-radius: var(--table-radius);
    border-bottom-right-radius: var(--table-radius);
    color: var(--table-btn-color);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) .table-row-btn {
    border-bottom-left-radius: var(--table-radius);
    border-bottom-right-radius: var(--table-radius);
    color: var(--table-btn-color);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) :is(.table-col-btn, .table-row-btn, .table-col-drag-handle:hover, .table-row-drag-handle:hover) {
    transition: var(--animation);
    background-color: var(--table-btn-bg);
    --table-drag-handle-color: var(--table-btn-color);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) :is(tr:hover .table-row-drag-handle, th:hover .table-col-drag-handle) {
    opacity: 1;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) th:first-child:not(:has(:is(.table-row-drag-handle, .table-col-drag-handle):hover)) {
    border-top-left-radius: var(--table-radius);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) th:last-child:not(:has(.table-col-drag-handle:hover)) {
    border-top-right-radius: var(--table-radius);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table):has(.table-col-btn:hover) th:last-child {
    border-top-right-radius: 0;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) tr:last-child td:first-child {
    border-bottom-left-radius: var(--table-radius);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table):has(.table-row-btn:hover) tr:last-child td:first-child {
    border-bottom-left-radius: 0;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) tr:last-child td:last-child {
    border-bottom-right-radius: var(--table-radius);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table):has(:is(.table-col-btn, .table-row-btn):hover) tr:last-child td:last-child {
    border-bottom-right-radius: 0;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) :is(th, td):not(:first-child) {
    border-left: 0;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) tbody td {
    border-top: 0;
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) thead tr {
    background-color: var(--table-header-bg);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) tbody tr:nth-of-type(2n) {
    background-color: var(--table-alt-line-bg);
  }
  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) tbody tr:nth-of-type(2n+1) {
    background-color: var(--background-primary);
  }

  :is(.markdown-source-view.mod-cm6 .cm-table-widget .table-wrapper, .markdown-rendered table) :is(th, td) {
    /* 通过 padding 调整单元格大小 */
    padding: 8px 0px;  /* 上下12px，左右8px */
}
```

## 待定