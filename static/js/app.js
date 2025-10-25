// DeepSeek OCR 前端應用程式

// 全域變數
let selectedFile = null;
let outputFilename = null;

// DOM 元素
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const selectFileBtn = document.getElementById('selectFileBtn');
const fileSelected = document.getElementById('fileSelected');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const changeFileBtn = document.getElementById('changeFileBtn');
const processBtn = document.getElementById('processBtn');
const progressSection = document.getElementById('progressSection');
const progressText = document.getElementById('progressText');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const downloadBtn = document.getElementById('downloadBtn');
const newProcessBtn = document.getElementById('newProcessBtn');
const retryBtn = document.getElementById('retryBtn');
const markdownPreview = document.getElementById('markdownPreview');
const markdownRaw = document.getElementById('markdownRaw');
const metadata = document.getElementById('metadata');

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

// 設定事件監聽器
function setupEventListeners() {
    // 檔案選擇
    selectFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });
    changeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });
    fileInput.addEventListener('change', handleFileSelect);

    // 拖放
    uploadBox.addEventListener('click', (e) => {
        // 只有點擊背景區域才觸發，避免與按鈕衝突
        if (e.target === uploadBox || e.target.classList.contains('upload-icon') ||
            e.target.tagName === 'H2' || e.target.tagName === 'P') {
            fileInput.click();
        }
    });
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleDrop);

    // 處理按鈕
    processBtn.addEventListener('click', handleProcess);
    downloadBtn.addEventListener('click', handleDownload);
    newProcessBtn.addEventListener('click', resetApp);
    retryBtn.addEventListener('click', handleProcess);

    // 標籤頁切換
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
}

// 處理檔案選擇
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        setSelectedFile(file);
    }
}

// 處理拖放
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadBox.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];

        // 檢查檔案類型
        if (file.type === 'application/pdf') {
            setSelectedFile(file);
        } else {
            showError('請上傳 PDF 檔案');
        }
    }
}

// 設定選中的檔案
function setSelectedFile(file) {
    selectedFile = file;

    // 更新 UI
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);

    uploadBox.style.display = 'none';
    fileSelected.style.display = 'block';
    hideError();
}

// 格式化檔案大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// 處理 OCR
async function handleProcess() {
    if (!selectedFile) {
        showError('請先選擇檔案');
        return;
    }

    // 檢查檔案大小
    const maxSize = 16 * 1024 * 1024; // 16 MB
    if (selectedFile.size > maxSize) {
        showError('檔案過大，請上傳小於 16 MB 的檔案');
        return;
    }

    // 顯示進度
    showProgress();

    // 建立 FormData
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // 發送請求
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            // 顯示結果
            displayResult(result);
        } else {
            showError(result.error || '處理失敗，請重試');
        }

    } catch (error) {
        console.error('Error:', error);
        showError('網路錯誤，請檢查連線後重試');
    }
}

// 顯示結果
function displayResult(result) {
    outputFilename = result.output_file;

    // 渲染 Markdown
    if (result.markdown_content) {
        // 使用 marked.js 轉換 Markdown 為 HTML
        markdownPreview.innerHTML = marked.parse(result.markdown_content);
        markdownRaw.textContent = result.markdown_content;
    }

    // 顯示元資料
    if (result.metadata) {
        const meta = result.metadata;
        let metaHTML = '<h4>處理資訊</h4>';

        if (meta.input_file) {
            metaHTML += `<p><strong>輸入檔案:</strong> ${meta.input_file}</p>`;
        }
        if (meta.output_file) {
            metaHTML += `<p><strong>輸出檔案:</strong> ${meta.output_file}</p>`;
        }
        if (meta.processed_at) {
            metaHTML += `<p><strong>處理時間:</strong> ${formatDateTime(meta.processed_at)}</p>`;
        }
        if (meta.content_length) {
            metaHTML += `<p><strong>內容長度:</strong> ${meta.content_length.toLocaleString()} 字元</p>`;
        }

        metadata.innerHTML = metaHTML;
    }

    // 切換顯示
    hideProgress();
    hideError();
    fileSelected.style.display = 'none';
    resultSection.style.display = 'block';
}

// 下載檔案
function handleDownload() {
    if (outputFilename) {
        window.location.href = `/download/${outputFilename}`;
    }
}

// 切換標籤頁
function switchTab(tabName) {
    // 更新按鈕狀態
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });

    // 更新內容顯示
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    if (tabName === 'preview') {
        document.getElementById('previewTab').classList.add('active');
    } else if (tabName === 'markdown') {
        document.getElementById('markdownTab').classList.add('active');
    }
}

// 顯示進度
function showProgress() {
    fileSelected.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    progressSection.style.display = 'block';
}

// 隱藏進度
function hideProgress() {
    progressSection.style.display = 'none';
}

// 顯示錯誤
function showError(message) {
    errorMessage.textContent = message;
    fileSelected.style.display = 'none';
    resultSection.style.display = 'none';
    progressSection.style.display = 'none';
    errorSection.style.display = 'block';
}

// 隱藏錯誤
function hideError() {
    errorSection.style.display = 'none';
}

// 重置應用程式
function resetApp() {
    selectedFile = null;
    outputFilename = null;
    fileInput.value = '';

    uploadBox.style.display = 'block';
    fileSelected.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    progressSection.style.display = 'none';
}

// 格式化日期時間
function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}
