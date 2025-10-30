# 📦 GitHub에 코드 올리기

## 🔧 Git 사용자 정보 설정 (최초 1회만)

**PowerShell에서 다음 명령어를 실행하세요:**

```powershell
# Git 사용자 이름 설정 (GitHub 사용자명)
git config --global user.name "본인의 이름"

# Git 이메일 설정 (GitHub 이메일)
git config --global user.email "본인이메일@example.com"

# 설정 확인
git config --list
```

---

## 📤 GitHub에 올리기

### 1단계: 첫 커밋 만들기

```powershell
cd C:\Users\able0\Desktop\PDF_CHAT

# 첫 커밋
git commit -m "Initial commit: PDF Chatbot with RAG"
```

### 2단계: GitHub 저장소 생성

1. **GitHub 웹사이트 접속**: https://github.com
2. **로그인**
3. **오른쪽 상단 "+" 클릭** → **"New repository"**
4. **저장소 정보 입력**:
   - Repository name: `pdf-chatbot` (원하는 이름)
   - Description: `RAG 기반 PDF 질의응답 챗봇`
   - Public 선택 (또는 Private)
   - **"Initialize this repository with a README"는 체크 안 함!**
5. **"Create repository"** 클릭

### 3단계: 로컬 코드를 GitHub에 푸시

GitHub에서 저장소를 만든 후 표시되는 URL을 복사하세요.  
예: `https://github.com/username/pdf-chatbot.git`

```powershell
cd C:\Users\able0\Desktop\PDF_CHAT

# GitHub 저장소 연결
git remote add origin https://github.com/본인username/pdf-chatbot.git

# 브랜치 이름을 main으로 변경
git branch -M main

# GitHub에 푸시
git push -u origin main
```

**주의**: `본인username`을 실제 GitHub 사용자명으로 변경하세요!

---

## 🔐 인증 문제 해결

### GitHub Personal Access Token 필요

GitHub는 비밀번호 대신 **Personal Access Token (PAT)**을 사용합니다.

#### PAT 생성 방법:

1. GitHub 로그인
2. 오른쪽 상단 프로필 → **Settings**
3. 왼쪽 메뉴 맨 아래 **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**
6. 정보 입력:
   - Note: `PDF Chatbot Deploy`
   - Expiration: `90 days` (또는 원하는 기간)
   - 권한 선택: ✅ **repo** (전체 체크)
7. **Generate token** 클릭
8. **토큰 복사** (다시 볼 수 없으니 안전한 곳에 저장!)

#### 토큰으로 푸시:

```powershell
git push -u origin main

# Username: 본인의 GitHub 사용자명
# Password: 위에서 복사한 토큰 (ghp_로 시작)
```

---

## ✅ 푸시 성공 확인

1. GitHub 저장소 페이지 새로고침
2. 파일들이 보이면 성공! 🎉

---

## 🚨 문제 해결

### 에러: "remote origin already exists"

```powershell
git remote remove origin
git remote add origin https://github.com/본인username/pdf-chatbot.git
```

### 에러: "fatal: unable to access"

- 인터넷 연결 확인
- GitHub URL이 정확한지 확인
- Personal Access Token 재생성

### 에러: "Permission denied"

- Personal Access Token 권한 확인 (repo 체크 필요)
- Token이 만료되지 않았는지 확인

---

## 🔄 이후 업데이트 방법

코드를 수정한 후:

```powershell
cd C:\Users\able0\Desktop\PDF_CHAT

# 변경사항 확인
git status

# 변경된 파일 추가
git add .

# 커밋
git commit -m "Update: 설명"

# GitHub에 푸시
git push origin main
```

---

## 📝 참고사항

### .gitignore로 제외되는 파일들:

✅ Git에 올라가지 **않는** 파일들:
- `.env` (API 키 보호)
- `venv/` (가상환경)
- `__pycache__/` (Python 캐시)
- `*.log` (로그 파일)
- `vector_store/` (벡터 데이터베이스 - 용량 큼)
- `static/page_images/` (생성된 이미지 - 용량 큼)

✅ Git에 올라가는 파일들:
- 모든 `.py` 파일 (소스 코드)
- `requirements.txt` (의존성)
- `templates/`, `static/css/`, `static/js/` (웹 파일)
- `README.md`, `DEPLOY.md` (문서)
- `render.yaml`, `Procfile` (배포 설정)
- `uploads/*.pdf` (샘플 PDF)

---

## 🎯 다음 단계

GitHub에 코드를 올린 후:

1. ✅ **DEPLOY.md** 파일을 읽고 Render 배포 진행
2. ✅ Render에서 GitHub 저장소 연결
3. ✅ 환경 변수 설정 (OPENAI_API_KEY)
4. ✅ 배포 시작!

**행운을 빕니다!** 🚀

