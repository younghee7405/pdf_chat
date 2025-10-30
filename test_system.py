"""
시스템 테스트 스크립트
- 필수 라이브러리 설치 확인
- OpenAI API 키 확인
- PDF 처리 및 RAG 엔진 테스트
"""
import os
import sys


def print_header(text):
    """헤더 출력"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)


def check_libraries():
    """필수 라이브러리 확인"""
    print_header("1. 필수 라이브러리 확인")
    
    required_libraries = {
        'flask': 'Flask',
        'openai': 'OpenAI',
        'langchain': 'LangChain',
        'fitz': 'PyMuPDF',
        'faiss': 'FAISS',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    
    for module, name in required_libraries.items():
        try:
            __import__(module)
            print(f"✅ {name} - 설치됨")
        except ImportError:
            print(f"❌ {name} - 설치 필요")
            all_installed = False
    
    return all_installed


def check_env_file():
    """환경 변수 파일 확인"""
    print_header("2. 환경 변수 확인")
    
    if not os.path.exists('.env'):
        print("❌ .env 파일이 존재하지 않습니다.")
        return False
    
    print("✅ .env 파일 존재")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key.strip() == '':
        print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 OpenAI API 키를 입력하세요.")
        return False
    
    print(f"✅ OPENAI_API_KEY 설정됨 (앞 10자: {api_key[:10]}...)")
    return True


def check_openai_connection():
    """OpenAI API 연결 테스트"""
    print_header("3. OpenAI API 연결 테스트")
    
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 간단한 테스트 요청
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✅ OpenAI API 연결 성공")
        print(f"   모델: {response.model}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API 연결 실패: {str(e)}")
        return False


def check_pdf_file():
    """PDF 파일 확인"""
    print_header("4. PDF 파일 확인")
    
    upload_dir = 'uploads'
    
    if not os.path.exists(upload_dir):
        print(f"⚠️  '{upload_dir}' 디렉토리가 없습니다.")
        os.makedirs(upload_dir)
        print(f"✅ '{upload_dir}' 디렉토리 생성됨")
        return False
    
    pdf_files = [f for f in os.listdir(upload_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"⚠️  '{upload_dir}' 디렉토리에 PDF 파일이 없습니다.")
        print("   웹 인터페이스를 통해 PDF를 업로드하세요.")
        return False
    
    print(f"✅ {len(pdf_files)}개의 PDF 파일 발견:")
    for pdf in pdf_files:
        print(f"   - {pdf}")
    
    return True


def test_pdf_processing():
    """PDF 처리 테스트"""
    print_header("5. PDF 처리 테스트")
    
    upload_dir = 'uploads'
    pdf_files = [f for f in os.listdir(upload_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("⚠️  테스트할 PDF 파일이 없습니다. 이 테스트를 건너뜁니다.")
        return True
    
    try:
        from pdf_processor import PDFProcessor
        
        test_pdf = os.path.join(upload_dir, pdf_files[0])
        print(f"테스트 PDF: {pdf_files[0]}")
        
        with PDFProcessor(test_pdf) as processor:
            print(f"✅ PDF 로드 성공")
            print(f"   총 페이지: {processor.total_pages}")
            
            chunks = processor.create_chunks_with_metadata()
            print(f"✅ 청크 생성 성공")
            print(f"   총 청크 수: {len(chunks)}")
            
            if chunks:
                print(f"   첫 청크 미리보기: {chunks[0]['text'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF 처리 실패: {str(e)}")
        return False


def test_rag_engine():
    """RAG 엔진 테스트"""
    print_header("6. RAG 엔진 테스트")
    
    upload_dir = 'uploads'
    pdf_files = [f for f in os.listdir(upload_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("⚠️  테스트할 PDF 파일이 없습니다. 이 테스트를 건너뜁니다.")
        return True
    
    try:
        from pdf_processor import PDFProcessor
        from rag_engine import RAGEngine
        from dotenv import load_dotenv
        
        load_dotenv()
        
        test_pdf = os.path.join(upload_dir, pdf_files[0])
        
        # PDF 처리
        with PDFProcessor(test_pdf) as processor:
            chunks = processor.create_chunks_with_metadata()
        
        # RAG 엔진 초기화
        engine = RAGEngine(os.getenv('OPENAI_API_KEY'))
        print("✅ RAG 엔진 초기화 성공")
        
        # 벡터 스토어 구축 (간단한 테스트)
        print("   벡터 스토어 구축 중... (시간이 걸릴 수 있습니다)")
        engine.build_vector_store(chunks[:5])  # 처음 5개 청크만 테스트
        print("✅ 벡터 스토어 구축 성공")
        
        # 검색 테스트
        search_results = engine.search("test", k=1)
        print(f"✅ 검색 기능 작동")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG 엔진 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_directories():
    """필요한 디렉토리 확인 및 생성"""
    print_header("7. 디렉토리 구조 확인")
    
    required_dirs = [
        'uploads',
        'static/page_images',
        'static/css',
        'static/js',
        'templates'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} - 존재")
        else:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ {dir_path} - 생성됨")
    
    return True


def main():
    """메인 테스트 실행"""
    print("\n" + "🔍 PDF 챗봇 시스템 테스트 시작".center(50))
    
    results = []
    
    # 1. 라이브러리 확인
    results.append(("라이브러리", check_libraries()))
    
    # 2. 환경 변수 확인
    results.append(("환경 변수", check_env_file()))
    
    # 3. OpenAI 연결 테스트 (환경 변수가 있을 때만)
    if results[-1][1]:
        results.append(("OpenAI API", check_openai_connection()))
    
    # 4. 디렉토리 확인
    results.append(("디렉토리", check_directories()))
    
    # 5. PDF 파일 확인
    results.append(("PDF 파일", check_pdf_file()))
    
    # 6. PDF 처리 테스트 (라이브러리와 PDF가 있을 때만)
    if results[0][1] and results[-1][1]:
        results.append(("PDF 처리", test_pdf_processing()))
    
    # 7. RAG 엔진 테스트 (모든 것이 준비되었을 때만)
    if all(r[1] for r in results) and results[0][1]:
        results.append(("RAG 엔진", test_rag_engine()))
    
    # 결과 요약
    print_header("테스트 결과 요약")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{name}: {status}")
    
    print(f"\n총 {total}개 중 {passed}개 통과")
    
    if passed == total:
        print("\n🎉 모든 테스트를 통과했습니다!")
        print("   run.bat (Windows) 또는 run.sh (Linux/Mac)를 실행하여 서버를 시작하세요.")
        return 0
    else:
        print("\n⚠️  일부 테스트가 실패했습니다.")
        print("   위의 오류 메시지를 확인하고 문제를 해결하세요.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

