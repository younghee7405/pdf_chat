// 전역 변수
let currentPDF = null;

// DOM 로드 완료 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 앱 초기화
function initializeApp() {
    // 이벤트 리스너 설정
    setupEventListeners();
    
    // 기존 PDF가 있는지 확인
    checkExistingPDFs();
}

// 이벤트 리스너 설정
function setupEventListeners() {
    // PDF 업로드
    const uploadInput = document.getElementById('pdf-upload');
    if (uploadInput) {
        uploadInput.addEventListener('change', handlePDFUpload);
    }
    
    // PDF 목록 아이템 클릭
    const pdfItems = document.querySelectorAll('.pdf-item');
    pdfItems.forEach(item => {
        item.addEventListener('click', () => handlePDFSelect(item));
    });
    
    // 채팅 폼 제출
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        chatForm.addEventListener('submit', handleChatSubmit);
    }
    
    // 엔터 키로 전송 (Shift+Enter는 줄바꿈)
    const questionInput = document.getElementById('question-input');
    if (questionInput) {
        questionInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    }
}

// 기존 PDF 확인
function checkExistingPDFs() {
    const pdfItems = document.querySelectorAll('.pdf-item');
    if (pdfItems.length > 0) {
        console.log(`${pdfItems.length}개의 기존 PDF 발견`);
    }
}

// PDF 업로드 처리
async function handlePDFUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // 파일 크기 확인 (50MB)
    if (file.size > 50 * 1024 * 1024) {
        alert('파일 크기가 너무 큽니다. 최대 50MB까지 가능합니다.');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading('PDF 업로드 및 처리 중...');
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentPDF = data;
            displayPDFInfo(data);
            enableChat();
            showNotification('PDF가 성공적으로 처리되었습니다!', 'success');
            
            // PDF 목록 새로고침
            addPDFToList(data.filename);
        } else {
            showNotification(data.error || 'PDF 처리 중 오류가 발생했습니다.', 'error');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showNotification('서버 연결 오류가 발생했습니다.', 'error');
    } finally {
        hideLoading();
        event.target.value = ''; // 입력 초기화
    }
}

// PDF 선택 처리
async function handlePDFSelect(item) {
    const filename = item.dataset.filename;
    
    showLoading('PDF 로드 중...');
    
    try {
        const response = await fetch('/api/load-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentPDF = data;
            displayPDFInfo(data);
            enableChat();
            showNotification(`${filename}이(가) 로드되었습니다.`, 'success');
            
            // 활성 상태 표시
            document.querySelectorAll('.pdf-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        } else {
            showNotification(data.error || 'PDF 로드 중 오류가 발생했습니다.', 'error');
        }
    } catch (error) {
        console.error('Load error:', error);
        showNotification('서버 연결 오류가 발생했습니다.', 'error');
    } finally {
        hideLoading();
    }
}

// PDF 정보 표시
function displayPDFInfo(data) {
    const pdfInfo = document.getElementById('current-pdf-info');
    document.getElementById('pdf-filename').textContent = data.filename;
    document.getElementById('pdf-pages').textContent = data.total_pages;
    document.getElementById('pdf-chunks').textContent = data.total_chunks;
    
    pdfInfo.style.display = 'block';
}

// PDF를 목록에 추가
function addPDFToList(filename) {
    const listContainer = document.getElementById('pdf-list-items');
    
    // 이미 있는지 확인
    const existing = Array.from(listContainer.children).find(
        item => item.dataset.filename === filename
    );
    
    if (!existing) {
        const li = document.createElement('li');
        li.className = 'pdf-item';
        li.dataset.filename = filename;
        li.innerHTML = `
            <i class="fas fa-file-pdf"></i>
            <span>${filename}</span>
        `;
        li.addEventListener('click', () => handlePDFSelect(li));
        listContainer.appendChild(li);
    }
}

// 채팅 활성화
function enableChat() {
    const questionInput = document.getElementById('question-input');
    const sendBtn = document.getElementById('send-btn');
    
    questionInput.disabled = false;
    sendBtn.disabled = false;
    questionInput.placeholder = '질문을 입력하세요...';
    questionInput.focus();
    
    // 환영 메시지 제거
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.style.display = 'none';
    }
}

// 채팅 제출 처리
async function handleChatSubmit(event) {
    event.preventDefault();
    
    const questionInput = document.getElementById('question-input');
    const question = questionInput.value.trim();
    
    if (!question) return;
    
    // 사용자 메시지 표시
    addMessage('user', question);
    questionInput.value = '';
    
    // 입력 비활성화
    questionInput.disabled = true;
    document.getElementById('send-btn').disabled = true;
    
    showLoading('답변 생성 중...');
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addBotMessage(data);
            displayReferences(data.references);
        } else {
            addMessage('bot', `오류: ${data.error}`);
        }
    } catch (error) {
        console.error('Query error:', error);
        addMessage('bot', '서버 연결 오류가 발생했습니다.');
    } finally {
        hideLoading();
        questionInput.disabled = false;
        document.getElementById('send-btn').disabled = false;
        questionInput.focus();
    }
}

// 사용자 메시지 추가
function addMessage(sender, content) {
    const messagesContainer = document.getElementById('chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const icon = sender === 'user' ? 'fa-user' : 'fa-robot';
    const senderName = sender === 'user' ? '사용자' : 'AI 어시스턴트';
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-icon">
                <i class="fas ${icon}"></i>
            </div>
            <span class="message-sender">${senderName}</span>
        </div>
        <div class="message-content">${content}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 봇 메시지 추가 (카테고리별)
function addBotMessage(data) {
    const messagesContainer = document.getElementById('chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    let contentHTML = '';
    
    // 카테고리별로 표시
    if (data.categories) {
        if (data.categories.overview) {
            contentHTML += `
                <div class="answer-category">
                    <div class="category-title">
                        <i class="fas fa-lightbulb"></i>
                        개요
                    </div>
                    <div class="category-content">${formatText(data.categories.overview)}</div>
                </div>
            `;
        }
        
        if (data.categories.steps) {
            contentHTML += `
                <div class="answer-category">
                    <div class="category-title">
                        <i class="fas fa-list-ol"></i>
                        단계별 설명
                    </div>
                    <div class="category-content">${formatText(data.categories.steps)}</div>
                </div>
            `;
        }
        
        if (data.categories.notes) {
            contentHTML += `
                <div class="answer-category">
                    <div class="category-title">
                        <i class="fas fa-exclamation-circle"></i>
                        참고사항
                    </div>
                    <div class="category-content">${formatText(data.categories.notes)}</div>
                </div>
            `;
        }
    }
    
    // 전체 답변이 카테고리로 나누어지지 않은 경우
    if (!contentHTML) {
        contentHTML = `<div class="category-content">${formatText(data.answer)}</div>`;
    }
    
    // 참조 페이지 이미지 표시
    if (data.references && data.references.page_images && data.references.page_images.length > 0) {
        contentHTML += '<div class="answer-category"><div class="category-title"><i class="fas fa-image"></i> 참조 페이지</div><div>';
        data.references.page_images.forEach(img => {
            contentHTML += `
                <div class="page-preview" onclick="openImageModal('${img.image_url}')">
                    <img src="${img.image_url}" alt="Page ${img.page_number}">
                    <span class="page-number-badge">페이지 ${img.page_number}</span>
                </div>
            `;
        });
        contentHTML += '</div></div>';
    }
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-icon">
                <i class="fas fa-robot"></i>
            </div>
            <span class="message-sender">AI 어시스턴트</span>
        </div>
        <div class="message-content">${contentHTML}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// 텍스트 포맷팅 (마크다운 스타일)
function formatText(text) {
    if (!text) return '';
    
    // 줄바꿈을 <br>로 변환
    text = text.replace(/\n/g, '<br>');
    
    // 번호 목록 감지 및 포맷팅
    text = text.replace(/(\d+)\.\s/g, '<br><strong>$1.</strong> ');
    
    // 볼드 처리
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    return text;
}

// 참조 정보 표시
function displayReferences(references) {
    if (!references) return;
    
    const referencePanel = document.getElementById('reference-panel');
    referencePanel.style.display = 'block';
    
    // 참조 페이지
    if (references.page_images && references.page_images.length > 0) {
        const pagesContainer = document.getElementById('reference-pages');
        pagesContainer.innerHTML = '';
        
        references.page_images.forEach(img => {
            const card = document.createElement('div');
            card.className = 'page-card';
            card.onclick = () => openImageModal(img.image_url);
            card.innerHTML = `
                <img src="${img.image_url}" alt="Page ${img.page_number}">
                <div class="page-card-info">페이지 ${img.page_number}</div>
            `;
            pagesContainer.appendChild(card);
        });
    }
    
    // 검색된 청크
    if (references.source_chunks && references.source_chunks.length > 0) {
        const chunksContainer = document.getElementById('source-chunks');
        chunksContainer.innerHTML = '';
        
        references.source_chunks.forEach((chunk, index) => {
            const card = document.createElement('div');
            card.className = 'chunk-card';
            card.innerHTML = `
                <div class="chunk-header">
                    <span class="chunk-page">페이지 ${chunk.page_number}</span>
                    <span class="chunk-score">관련도: ${(1 - chunk.similarity_score).toFixed(2)}</span>
                </div>
                <div class="chunk-text">${chunk.text}</div>
            `;
            chunksContainer.appendChild(card);
        });
    }
}

// 이미지 모달 열기
function openImageModal(imageUrl) {
    // 간단한 구현: 새 탭에서 열기
    window.open(imageUrl, '_blank');
}

// 채팅 영역을 맨 아래로 스크롤
function scrollToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 로딩 표시
function showLoading(text = '처리 중...') {
    const overlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    loadingText.textContent = text;
    overlay.style.display = 'flex';
}

// 로딩 숨기기
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    overlay.style.display = 'none';
}

// 알림 표시
function showNotification(message, type = 'info') {
    // 간단한 알림 (나중에 토스트 알림으로 개선 가능)
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // 브라우저 알림을 사용할 수도 있음
    if (type === 'error') {
        alert(message);
    }
}

