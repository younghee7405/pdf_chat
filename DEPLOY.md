# 🚀 Render 배포 가이드

이 가이드는 PDF 챗봇을 Render에 배포하는 방법을 설명합니다.

## 📋 사전 준비

1. **GitHub 계정** - https://github.com
2. **Render 계정** - https://render.com (GitHub로 가입 가능)
3. **OpenAI API 키** - https://platform.openai.com/api-keys

---

## 🔧 1단계: GitHub 저장소 생성

### 방법 A: GitHub 웹사이트에서 생성

1. **GitHub 접속**: https://github.com
2. **New repository** 클릭
3. **저장소 정보 입력**:
   - Repository name: `pdf-chatbot` (원하는 이름)
   - Description: `RAG 기반 PDF 질의응답 챗봇`
   - Public 또는 Private 선택
   - **Initialize this repository with a README** 체크 안 함
4. **Create repository** 클릭
5. **저장소 URL 복사** (예: `https://github.com/username/pdf-chatbot.git`)

### 방법 B: 명령어로 생성

아래 명령어를 따라하세요:

```bash
# 1. Git 초기화
cd C:\Users\able0\Desktop\PDF_CHAT
git init

# 2. 파일 추가
git add .

# 3. 첫 커밋
git config user.name "Your Name"
git config user.email "your.email@example.com"
git commit -m "Initial commit: PDF Chatbot with RAG"

# 4. GitHub 저장소에 푸시
git branch -M main
git remote add origin https://github.com/username/pdf-chatbot.git
git push -u origin main
```

**주의**: `username`을 본인의 GitHub 사용자명으로 변경하세요!

---

## 🌐 2단계: Render에 배포

### 1. Render 대시보드 접속

1. **Render 로그인**: https://dashboard.render.com
2. **New +** 버튼 클릭
3. **Web Service** 선택

### 2. 저장소 연결

1. **Connect GitHub** 선택
2. GitHub 계정 연동 (최초 1회)
3. 방금 만든 `pdf-chatbot` 저장소 선택
4. **Connect** 클릭

### 3. 서비스 설정

다음 정보를 입력하세요:

| 설정 | 값 |
|------|-----|
| **Name** | `pdf-chatbot` (또는 원하는 이름) |
| **Region** | `Singapore` (가장 가까운 지역) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT app:app --timeout 300 --workers 2` |
| **Instance Type** | `Free` (무료) 또는 원하는 플랜 |

### 4. 환경 변수 설정

**Environment Variables** 섹션에서 **Add Environment Variable** 클릭:

```
Key: OPENAI_API_KEY
Value: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (본인의 API 키)
```

```
Key: FLASK_ENV
Value: production
```

```
Key: PYTHON_VERSION
Value: 3.11.9
```

### 5. 디스크 추가 (선택사항)

PDF 파일과 벡터 스토어를 영구 저장하려면:

1. **Advanced** 섹션 확장
2. **Add Disk** 클릭
3. **Name**: `pdf-storage`
4. **Mount Path**: `/opt/render/project/src/uploads`
5. **Size**: `10 GB` (무료 플랜: 1GB 제한)

### 6. 배포 시작

1. **Create Web Service** 클릭
2. 자동 빌드 및 배포 시작 (5-10분 소요)
3. 로그에서 진행 상황 확인

---

## ✅ 3단계: 배포 확인

### 배포 완료 확인

1. 로그에 다음 메시지가 표시되면 성공:
   ```
   [INFO] Booting worker with pid: xxx
   Your service is live 🎉
   ```

2. **제공된 URL 클릭** (예: `https://pdf-chatbot-xxxx.onrender.com`)

### 테스트

1. 브라우저에서 URL 접속
2. PDF 업로드 또는 기존 PDF 선택
3. 질문 입력 및 답변 확인

---

## 🔧 문제 해결

### 1. 빌드 실패

**증상**: `Build failed` 메시지

**해결**:
```bash
# requirements.txt 확인
pip install -r requirements.txt

# 로컬에서 테스트
python app.py
```

### 2. OpenAI API 오류

**증상**: `insufficient_quota` 또는 `invalid_api_key`

**해결**:
1. Render 대시보드 → Environment 탭
2. `OPENAI_API_KEY` 확인 및 업데이트
3. **Manual Deploy** → **Deploy latest commit** 클릭

### 3. 메모리 부족

**증상**: 서버가 자주 재시작됨

**해결**:
1. Instance Type을 유료 플랜으로 업그레이드
2. 또는 `chunk_size`를 줄임 (app.py 수정)

### 4. 타임아웃 오류

**증상**: PDF 처리 중 504 Gateway Timeout

**해결**:
- Procfile에서 `--timeout 300`을 `--timeout 600`으로 증가

---

## 💰 비용 안내

### Render 무료 플랜
- ✅ 750시간/월 무료
- ✅ 자동 슬립 (15분 비활성화 시)
- ✅ 512MB RAM
- ⚠️ 콜드 스타트 (첫 요청 시 느림)

### OpenAI API 비용
- **임베딩 (text-embedding-ada-002)**: $0.0001 / 1K 토큰
- **GPT-4o-mini**: $0.00015 / 1K 토큰 (입력), $0.0006 / 1K 토큰 (출력)
- **예상 비용**: 137페이지 PDF 처리 약 $0.10-0.20

---

## 🔄 업데이트 방법

코드를 수정한 후:

```bash
# 1. 변경사항 커밋
git add .
git commit -m "Update: 설명"

# 2. GitHub에 푸시
git push origin main

# 3. Render가 자동으로 재배포 (Auto-Deploy 활성화 시)
```

수동 배포:
1. Render 대시보드
2. **Manual Deploy** → **Deploy latest commit**

---

## 📊 모니터링

### 로그 확인
1. Render 대시보드 → 서비스 선택
2. **Logs** 탭
3. 실시간 로그 확인

### 메트릭 확인
- **Metrics** 탭에서 CPU, 메모리, 네트워크 사용량 확인

---

## 🎯 프로덕션 최적화 팁

### 1. 환경 변수로 설정 관리
```python
# app.py에서
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
MAX_CHUNKS = int(os.environ.get('MAX_CHUNKS', 1000))
```

### 2. 캐싱 활성화
```python
# 벡터 스토어 캐싱
if os.path.exists('vector_store'):
    rag_engine.load_vector_store()
else:
    rag_engine.build_vector_store(chunks)
    rag_engine.save_vector_store()
```

### 3. 로깅 레벨 조정
```python
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)
```

---

## 🔒 보안 주의사항

1. **.env 파일은 절대 Git에 커밋하지 마세요!**
2. API 키는 Render 환경 변수에만 저장
3. 파일 업로드 크기 제한 유지 (50MB)
4. CORS 설정 (필요시)

---

## 📞 지원

문제가 발생하면:
1. **Render 문서**: https://render.com/docs
2. **OpenAI 문서**: https://platform.openai.com/docs
3. **GitHub Issues**: 저장소에 이슈 등록

---

## 🎉 완료!

축하합니다! PDF 챗봇이 성공적으로 배포되었습니다!

**배포된 앱 공유**: 
- URL을 친구들과 공유하세요!
- 무료 플랜은 공개 URL로 접근 가능합니다.

**다음 단계**:
- [ ] 커스텀 도메인 연결
- [ ] HTTPS 인증서 (자동 제공)
- [ ] 사용량 모니터링
- [ ] 기능 추가 및 개선

