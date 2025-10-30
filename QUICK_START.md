# ⚡ 빠른 시작 가이드

## 🎯 목표
PDF 챗봇을 GitHub에 올리고 Render에 배포하기

---

## 📋 체크리스트

### ✅ 준비물
- [ ] GitHub 계정 (https://github.com)
- [ ] Render 계정 (https://render.com)
- [ ] OpenAI API 키 (https://platform.openai.com/api-keys)
- [ ] Git 설치 확인 (`git --version` 실행)

---

## 🚀 단계별 가이드

### 1단계: Git 사용자 정보 설정 (⏱️ 1분)

```powershell
# PowerShell에서 실행
git config --global user.name "본인이름"
git config --global user.email "본인이메일@example.com"
```

### 2단계: 첫 커밋 (⏱️ 1분)

```powershell
cd C:\Users\able0\Desktop\PDF_CHAT
git commit -m "Initial commit: PDF Chatbot with RAG"
```

### 3단계: GitHub 저장소 생성 (⏱️ 2분)

1. https://github.com → 로그인
2. 오른쪽 상단 **"+"** → **"New repository"**
3. 정보 입력:
   - **Repository name**: `pdf-chatbot`
   - **Public** 선택
   - **"Create repository"** 클릭

### 4단계: GitHub에 푸시 (⏱️ 2분)

GitHub 저장소 페이지에 표시된 URL 복사 후:

```powershell
# origin 연결
git remote add origin https://github.com/본인username/pdf-chatbot.git

# 브랜치 이름 변경
git branch -M main

# 푸시
git push -u origin main
```

**인증**:
- Username: GitHub 사용자명
- Password: Personal Access Token (아래 참고)

#### Personal Access Token 생성:
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token → **repo** 체크 → Generate
4. **토큰 복사** (ghp_로 시작)

### 5단계: Render 배포 (⏱️ 5분)

1. **Render 로그인**: https://dashboard.render.com
2. **New +** → **Web Service**
3. **Connect GitHub** → `pdf-chatbot` 저장소 선택
4. 설정 입력:
   - **Name**: `pdf-chatbot`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app --timeout 300 --workers 2`
   - **Instance Type**: `Free`

5. **환경 변수 추가**:
   ```
   OPENAI_API_KEY = sk-xxxxxxx (본인의 API 키)
   FLASK_ENV = production
   PYTHON_VERSION = 3.11.9
   ```

6. **Create Web Service** 클릭

### 6단계: 배포 완료 대기 (⏱️ 5-10분)

- 로그에서 진행 상황 확인
- `Your service is live 🎉` 메시지 확인
- 제공된 URL로 접속

---

## 🎉 완료!

배포된 URL로 접속하여 PDF 챗봇 사용!

**총 소요 시간**: 약 15-20분

---

## 📚 상세 가이드

더 자세한 내용은 다음 문서를 참고하세요:

- **GitHub 올리기**: `GITHUB_SETUP.md`
- **Render 배포**: `DEPLOY.md`
- **로컬 실행**: `README.md`

---

## 💬 문제 발생 시

### GitHub 푸시 실패
→ `GITHUB_SETUP.md` 파일의 "문제 해결" 섹션 참고

### Render 빌드 실패
→ `DEPLOY.md` 파일의 "문제 해결" 섹션 참고

### OpenAI API 오류
→ API 키 확인 및 크레딧 충전

---

## 🎯 다음 단계

- [ ] 커스텀 도메인 연결
- [ ] PDF 추가 업로드
- [ ] 기능 개선 및 커스터마이징

**행운을 빕니다!** 🚀

