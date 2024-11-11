document.addEventListener('DOMContentLoaded', () => {
  loadBookmarks();
});

async function loadBookmarks() {
  const bookmarks = await chrome.bookmarks.getTree();
  const container = document.getElementById('bookmarkContainer');
  container.innerHTML = '';

  // 获取所有顶级文件夹
  const topFolders = bookmarks[0].children;
  
  // 为每个顶级文件夹创建一个列
  topFolders.forEach(folder => {
    const column = document.createElement('div');
    column.className = 'bookmark-folder';
    
    const folderTitle = document.createElement('h3');
    folderTitle.className = 'folder-title';
    folderTitle.textContent = folder.title || 'Bookmarks Bar';
    column.appendChild(folderTitle);
    
    // 递归处理所有书签和子文件夹
    processBookmarkNode(folder, column);
    
    container.appendChild(column);
  });
}

function processBookmarkNode(node, parentElement) {
  // 处理当前节点的所有子节点
  node.children?.forEach(child => {
    if (child.url) {
      // 如果是书签
      const bookmarkElement = createBookmarkElement(child);
      parentElement.appendChild(bookmarkElement);
    } else {
      // 如果是文件夹
      const folderDiv = document.createElement('div');
      folderDiv.className = 'subfolder';
      
      const folderTitle = document.createElement('h4');
      folderTitle.className = 'folder-title';
      folderTitle.textContent = child.title;
      folderDiv.appendChild(folderTitle);
      
      // 递归处理子文件夹
      processBookmarkNode(child, folderDiv);
      
      parentElement.appendChild(folderDiv);
    }
  });
}

function createBookmarkElement(bookmark) {
  const element = document.createElement('div');
  element.className = 'bookmark-item';
  
  try {
    const favicon = document.createElement('img');
    favicon.src = `https://www.google.com/s2/favicons?domain=${new URL(bookmark.url).hostname}`;
    favicon.width = 16;
    favicon.height = 16;
    favicon.onerror = () => {
      favicon.src = 'image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgZmlsbD0iI2NjYyIgdmlld0JveD0iMCAwIDE2IDE2Ij48cmVjdCB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHJ4PSIyIi8+PC9zdmc+';
    };
    element.appendChild(favicon);
  } catch (e) {
    // 如果URL无效，使用默认图标
    const defaultIcon = document.createElement('div');
    defaultIcon.style.width = '16px';
    defaultIcon.style.height = '16px';
    defaultIcon.style.backgroundColor = '#ccc';
    defaultIcon.style.borderRadius = '2px';
    element.appendChild(defaultIcon);
  }
  
  const title = document.createElement('span');
  title.className = 'bookmark-title';
  title.textContent = bookmark.title || bookmark.url;
  element.appendChild(title);
  
  const actions = document.createElement('div');
  actions.className = 'bookmark-actions';
  
  // Edit button
  const editButton = document.createElement('button');
  editButton.className = 'action-button';
  editButton.innerHTML = '✏️';
  editButton.onclick = (e) => {
    e.stopPropagation();
    editBookmark(bookmark, title);
  };
  actions.appendChild(editButton);
  
  // Delete button
  const deleteButton = document.createElement('button');
  deleteButton.className = 'action-button';
  deleteButton.innerHTML = '🗑️';
  deleteButton.onclick = (e) => {
    e.stopPropagation();
    deleteBookmark(bookmark.id);
  };
  actions.appendChild(deleteButton);
  
  element.appendChild(actions);
  
  // Click to open bookmark
  element.onclick = () => {
    chrome.tabs.create({ url: bookmark.url });
  };
  
  return element;
}

function editBookmark(bookmark, titleElement) {
  const newTitle = prompt('Edit bookmark title:', bookmark.title);
  if (newTitle !== null) {
    chrome.bookmarks.update(bookmark.id, {
      title: newTitle
    }, () => {
      titleElement.textContent = newTitle;
    });
  }
}

async function deleteBookmark(id) {
  if (confirm('Are you sure you want to delete this bookmark?')) {
    await chrome.bookmarks.remove(id);
    loadBookmarks(); // Reload the bookmark list
  }
}