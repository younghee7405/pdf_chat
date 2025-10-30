# 📚 PDF 챗봇 - RAG 기반 질의응답 시스템

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)

RAG(Retrieval-Augmented Generation) 아키텍처를 기반으로 한 전문적인 PDF 문서 질의응답 시스템입니다.

## ✨ 주요 기능

### 🎯 핵심 기능
- **RAG 기반 검색**: FAISS 벡터 데이터베이스를 사용한 고속 유사도 검색
- **페이지 이미지 제공**: 관련 내용이 포함된 페이지를 이미지로 렌더링하여 제공
- **단계별 설명**: OpenAI GPT 모델을 활용한 체계적이고 명확한 답변 생성
- **카테고리별 응답**: 개요, 단계별 설명, 참고사항으로 구분된 구조화된 답변
- **인터랙티브 UI**: 현대적이고 사용하기 쉬운 웹 인터페이스

### 🔧 기술적 특징
- **PDF 처리**: PyMuPDF를 사용한 텍스트 및 이미지 추출
- **텍스트 청킹**: LangChain의 RecursiveCharacterTextSplitter로 최적화된 청크 생성
- **벡터 임베딩**: OpenAI Embeddings를 사용한 고품질 벡터 생성
- **벡터 검색**: FAISS를 활용한 초고속 유사도 검색
- **답변 생성**: GPT-4o-mini를 사용한 정확하고 맥락적인 답변

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐
│   사용자 (Web)   │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Flask  │ ◄──── 웹 서버 & API
    └────┬────┘
         │
    ┌────▼────────────────────┐
    │  RAG Engine             │
    │  ┌──────────────────┐   │
    │  │  Vector Search   │   │ ◄──── FAISS 벡터 검색
    │  └──────────────────┘   │
    │  ┌──────────────────┐   │
    │  │  OpenAI API      │   │ ◄──── GPT-4 답변 생성
    │  └──────────────────┘   │
    └─────────────────────────┘
         │
    ┌────▼──────────┐
    │ PDF Processor  │ ◄──── PyMuPDF로 PDF 처리
    └────────────────┘
```

## 📋 요구사항

### 시스템 요구사항
- Python 3.8 이상
- OpenAI API 키
- 최소 4GB RAM (대용량 PDF 처리 시 더 많이 필요)

### 주요 라이브러리
- `flask`: 웹 프레임워크
- `openai`: OpenAI API 연동
- `langchain`: RAG 파이프라인 구성
- `PyMuPDF`: PDF 처리 및 렌더링
- `faiss-cpu`: 벡터 데이터베이스
- `python-dotenv`: 환경 변수 관리

## 🚀 설치 및 실행

### 1. 저장소 클론 및 이동
```bash
cd PDF_CHAT
```

### 2. 가상 환경 생성 (권장)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일을 프로젝트 루트에 생성하고 다음 내용을 입력:
```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=1
```

**OpenAI API 키 발급 방법:**
1. [OpenAI Platform](https://platform.openai.com/)에 접속
2. 계정 생성 또는 로그인
3. API Keys 메뉴에서 새 키 생성
4. 생성된 키를 `.env` 파일에 입력

### 5. 애플리케이션 실행
```bash
python app.py
```

서버가 시작되면 브라우저에서 `http://localhost:5000` 접속

## 📖 사용 방법

### 1단계: PDF 업로드
1. 왼쪽 사이드바의 "PDF 업로드" 버튼 클릭
2. PDF 파일 선택 (최대 50MB)
3. 자동으로 텍스트 추출 및 벡터화 진행

### 2단계: 질문하기
1. PDF 처리가 완료되면 하단 입력창 활성화
2. 질문을 입력하고 전송 버튼 클릭 또는 Enter 키 입력
3. AI가 답변 생성 (평균 5-10초 소요)

### 3단계: 답변 확인
- **카테고리별 답변**: 개요, 단계별 설명, 참고사항으로 구분
- **참조 페이지 이미지**: 관련 페이지의 실제 이미지 제공
- **검색된 문서 조각**: 오른쪽 패널에서 상세 정보 확인

## 🗂️ 프로젝트 구조

```
PDF_CHAT/
│
├── app.py                      # Flask 메인 애플리케이션
├── pdf_processor.py            # PDF 처리 모듈
├── rag_engine.py               # RAG 엔진 (검색 & 생성)
├── requirements.txt            # Python 의존성
├── .env                        # 환경 변수 (직접 생성)
├── .gitignore                  # Git 제외 파일
│
├── templates/                  # HTML 템플릿
│   └── index.html              # 메인 페이지
│
├── static/                     # 정적 파일
│   ├── css/
│   │   └── style.css           # 스타일시트
│   ├── js/
│   │   └── app.js              # 프론트엔드 JavaScript
│   └── page_images/            # 렌더링된 페이지 이미지 (자동 생성)
│
├── uploads/                    # 업로드된 PDF 파일
│   └── network.pdf
│
└── vector_store/               # FAISS 벡터 데이터베이스 (자동 생성)
```

## 🎨 UI 특징

### 현대적인 디자인
- **그라데이션 배경**: 보라색-파란색 그라데이션
- **카드 기반 레이아웃**: 깔끔하고 직관적인 구성
- **반응형 디자인**: 다양한 화면 크기 지원

### 인터랙티브 요소
- **클릭 가능한 PDF 목록**: 이전에 업로드한 PDF 빠른 로드
- **실시간 로딩 표시**: 처리 상태를 명확하게 표시
- **페이지 이미지 확대**: 참조 페이지 클릭 시 확대 보기
- **청크 카드**: 검색된 문서 조각을 카드 형태로 표시

## 🔍 RAG 파이프라인 상세

### 1. 문서 처리 단계
```python
1. PDF 로드 (PyMuPDF)
2. 페이지별 텍스트 추출
3. 텍스트 청킹 (1000자, 200자 겹침)
4. 메타데이터 추가 (페이지 번호, 출처)
```

### 2. 벡터화 단계
```python
1. OpenAI Embeddings로 벡터 생성
2. FAISS 인덱스 구축
3. 로컬 저장 (재사용 가능)
```

### 3. 검색 단계
```python
1. 질문을 벡터로 변환
2. FAISS 유사도 검색 (상위 3개)
3. 관련 청크 반환
```

### 4. 생성 단계
```python
1. 검색된 청크를 컨텍스트로 구성
2. 시스템 프롬프트와 함께 GPT-4에 전달
3. 구조화된 답변 생성 (개요/단계/참고)
```

## ⚙️ 커스터마이징

### 청크 크기 조정
`app.py`의 `process_pdf()` 함수에서:
```python
chunks = pdf_processor.create_chunks_with_metadata(
    chunk_size=1000,      # 더 큰 청크 → 더 많은 컨텍스트
    chunk_overlap=200     # 더 큰 겹침 → 경계 정보 손실 감소
)
```

### 검색 결과 개수 조정
`app.py`의 `query()` 엔드포인트에서:
```python
result = rag_engine.query(
    question=question,
    k=3  # 3 → 5로 변경하면 더 많은 문서 검색
)
```

### LLM 모델 변경
`rag_engine.py`의 `generate_answer()` 함수에서:
```python
response = self.client.chat.completions.create(
    model="gpt-4o-mini",  # gpt-4, gpt-3.5-turbo 등으로 변경 가능
    messages=messages,
    temperature=0.7,      # 0.0-2.0 (낮을수록 일관적)
    max_tokens=1500       # 답변 최대 길이
)
```

### 시스템 프롬프트 커스터마이징
`rag_engine.py`의 `generate_answer()` 함수에서 `system_prompt` 수정

## 🐛 문제 해결

### 1. OpenAI API 오류
```
오류: OPENAI_API_KEY가 설정되지 않았습니다.
해결: .env 파일에 유효한 API 키 입력
```

### 2. PDF 처리 실패
```
오류: PDF 처리 중 오류 발생
해결: 
- PDF가 손상되지 않았는지 확인
- 파일 크기가 50MB 이하인지 확인
- 텍스트가 추출 가능한 PDF인지 확인 (스캔 이미지 PDF는 불가)
```

### 3. 메모리 부족
```
오류: 대용량 PDF 처리 시 메모리 부족
해결:
- chunk_size를 줄임 (1000 → 500)
- k 값을 줄임 (3 → 2)
- PDF를 분할하여 처리
```

### 4. FAISS 설치 오류
```
오류: faiss-cpu 설치 실패
해결:
# Windows에서는 먼저 Visual C++ 재배포 가능 패키지 설치
# 또는 conda 사용
conda install -c conda-forge faiss-cpu
```

## 📊 성능 최적화 팁

1. **벡터 스토어 재사용**: 같은 PDF는 한 번만 처리하고 저장된 벡터 스토어 재사용
2. **청크 크기 최적화**: 문서 특성에 따라 청크 크기 조정
3. **캐싱**: 자주 묻는 질문은 캐싱하여 API 비용 절감
4. **배치 처리**: 여러 PDF를 한 번에 처리할 경우 배치 임베딩 사용

## 🔒 보안 고려사항

1. **API 키 보호**: `.env` 파일을 절대 Git에 커밋하지 마세요
2. **파일 검증**: 업로드된 파일의 MIME 타입 검증
3. **크기 제한**: 대용량 파일 업로드 방지 (현재 50MB 제한)
4. **입력 검증**: 사용자 입력에 대한 적절한 검증 및 새니타이징

## 🤝 기여

이슈 제보 및 풀 리퀘스트를 환영합니다!

## 📄 라이선스

MIT License

## 👨‍💻 개발자

20년차 CTO 경험을 바탕으로 설계된 엔터프라이즈급 PDF 챗봇 시스템

## 🔗 참고 자료

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [FAISS Documentation](https://faiss.ai/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**문의사항이나 지원이 필요하신 경우 Issues 탭을 이용해주세요!**

