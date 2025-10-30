"""
Flask 백엔드 애플리케이션
- PDF 업로드 및 처리
- RAG 기반 질의응답 API
- 페이지 이미지 제공
"""
import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from pdf_processor import PDFProcessor
from rag_engine import RAGEngine

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB 제한
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# 전역 변수
rag_engine = None
current_pdf_path = None
pdf_processor = None


def allowed_file(filename):
    """업로드 파일 확장자 검증"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """메인 페이지"""
    # 기존 PDF 파일 목록 가져오기
    pdf_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        pdf_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
                    if f.endswith('.pdf')]
    
    return render_template('index.html', pdf_files=pdf_files)


@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    """PDF 파일 업로드 및 처리"""
    global rag_engine, current_pdf_path, pdf_processor
    
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
    if file and allowed_file(file.filename):
        # 파일 저장
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # PDF 처리 및 RAG 엔진 초기화
            current_pdf_path = filepath
            return process_pdf(filepath)
            
        except Exception as e:
            return jsonify({'error': f'PDF 처리 중 오류 발생: {str(e)}'}), 500
    
    return jsonify({'error': '허용되지 않는 파일 형식입니다.'}), 400


@app.route('/api/load-pdf', methods=['POST'])
def load_existing_pdf():
    """기존 업로드된 PDF 로드"""
    global current_pdf_path
    
    try:
        data = request.json
        filename = data.get('filename')
        
        logger.info(f"\n{'='*50}")
        logger.info(f"PDF 로드 요청: {filename}")
        logger.info(f"{'='*50}")
        
        if not filename:
            logger.error("파일명이 없습니다.")
            return jsonify({'error': '파일명이 제공되지 않았습니다.'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.info(f"파일 경로: {filepath}")
        
        if not os.path.exists(filepath):
            logger.error(f"파일이 존재하지 않습니다: {filepath}")
            return jsonify({'error': '파일을 찾을 수 없습니다.'}), 404
        
        logger.info(f"파일 확인 완료, 처리 시작...")
        current_pdf_path = filepath
        return process_pdf(filepath)
        
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.error(f"\nPDF 로드 중 예외 발생:")
        logger.error(error_msg)
        return jsonify({
            'error': f'PDF 로드 중 오류: {str(e)}',
            'details': error_msg
        }), 500


def process_pdf(filepath):
    """PDF 파일 처리 및 벡터 스토어 구축"""
    global rag_engine, pdf_processor
    
    try:
        # OpenAI API 키 확인
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY가 설정되지 않았습니다.")
            return jsonify({'error': 'OPENAI_API_KEY가 설정되지 않았습니다.'}), 500
        
        logger.info(f"PDF 처리 시작: {filepath}")
        
        # PDF 처리
        pdf_processor = PDFProcessor(filepath)
        logger.info(f"PDF 로드 완료 - 총 {pdf_processor.total_pages}페이지")
        
        chunks = pdf_processor.create_chunks_with_metadata(
            chunk_size=1000,
            chunk_overlap=200
        )
        logger.info(f"청크 생성 완료 - 총 {len(chunks)}개")
        
        # RAG 엔진 초기화 및 벡터 스토어 구축
        logger.info("RAG 엔진 초기화 중...")
        rag_engine = RAGEngine(api_key)
        
        logger.info("벡터 스토어 구축 중... (시간이 걸릴 수 있습니다)")
        rag_engine.build_vector_store(chunks)
        
        # 벡터 스토어 저장 (선택적)
        logger.info("벡터 스토어 저장 중...")
        rag_engine.save_vector_store()
        
        logger.info("모든 처리가 완료되었습니다!")
        
        return jsonify({
            'message': 'PDF 처리가 완료되었습니다.',
            'filename': os.path.basename(filepath),
            'total_pages': pdf_processor.total_pages,
            'total_chunks': len(chunks)
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"PDF 처리 중 오류 발생:")
        logger.error(error_details)
        return jsonify({
            'error': f'PDF 처리 중 오류 발생: {str(e)}',
            'details': error_details
        }), 500


@app.route('/api/query', methods=['POST'])
def query():
    """사용자 질문에 대한 답변 생성"""
    global rag_engine, pdf_processor
    
    if rag_engine is None:
        return jsonify({'error': 'PDF를 먼저 업로드해주세요.'}), 400
    
    data = request.json
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': '질문을 입력해주세요.'}), 400
    
    try:
        # RAG 파이프라인 실행
        result = rag_engine.query(
            question=question,
            k=3  # 상위 3개 청크 검색
        )
        
        # 참조 페이지 이미지 생성
        page_images = []
        for page_num in result['referenced_pages']:
            try:
                image_path = pdf_processor.render_page_as_image(page_num)
                # 웹 경로로 변환
                web_path = image_path.replace('\\', '/')
                page_images.append({
                    'page_number': page_num,
                    'image_url': f'/{web_path}'
                })
            except Exception as e:
                print(f"페이지 {page_num} 이미지 생성 실패: {e}")
        
        # 응답 구성 (카테고리별 분리)
        response = {
            'question': question,
            'answer': result['answer'],
            'categories': {
                'overview': extract_section(result['answer'], '개요'),
                'steps': extract_section(result['answer'], '단계별 설명'),
                'notes': extract_section(result['answer'], '참고사항')
            },
            'references': {
                'pages': result['referenced_pages'],
                'page_images': page_images,
                'source_chunks': [
                    {
                        'text': chunk['text'][:200] + '...' if len(chunk['text']) > 200 else chunk['text'],
                        'page_number': chunk['page_number'],
                        'similarity_score': chunk['similarity_score']
                    }
                    for chunk in result['source_chunks']
                ]
            },
            'metadata': {
                'model': result['model'],
                'total_tokens': result['total_tokens']
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'질의 처리 중 오류 발생: {str(e)}'}), 500


def extract_section(text, section_name):
    """답변에서 특정 섹션 추출"""
    lines = text.split('\n')
    section_lines = []
    in_section = False
    
    for line in lines:
        if section_name in line and ('**' in line or '#' in line):
            in_section = True
            continue
        elif in_section and (line.startswith('##') or line.startswith('**')):
            break
        elif in_section:
            section_lines.append(line)
    
    return '\n'.join(section_lines).strip() if section_lines else None


@app.route('/api/pdf-info', methods=['GET'])
def pdf_info():
    """현재 로드된 PDF 정보 반환"""
    global current_pdf_path, pdf_processor
    
    if not current_pdf_path or not pdf_processor:
        return jsonify({'error': 'PDF가 로드되지 않았습니다.'}), 400
    
    return jsonify({
        'filename': os.path.basename(current_pdf_path),
        'total_pages': pdf_processor.total_pages,
        'path': current_pdf_path
    })


@app.route('/static/<path:filename>')
def serve_static(filename):
    """정적 파일 제공"""
    return send_from_directory('static', filename)


@app.errorhandler(413)
def request_entity_too_large(error):
    """파일 크기 초과 에러"""
    return jsonify({'error': '파일 크기가 너무 큽니다. 최대 50MB까지 가능합니다.'}), 413


if __name__ == '__main__':
    # 필요한 디렉토리 생성
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static/page_images', exist_ok=True)
    os.makedirs('vector_store', exist_ok=True)
    
    # 포트 설정 (Render는 PORT 환경변수 사용)
    port = int(os.environ.get('PORT', 5000))
    
    # 프로덕션 환경 체크
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if is_production:
        logger.info(f"프로덕션 모드로 실행 중 (포트: {port})")
    
    # Flask 앱 실행
    app.run(
        debug=not is_production,
        host='0.0.0.0',
        port=port
    )

