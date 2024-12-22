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