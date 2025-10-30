"""
PDF 처리 모듈
- PDF에서 텍스트 추출 및 청킹
- 페이지별 이미지 렌더링
- 메타데이터 관리 (페이지 번호 등)
"""
import fitz  # PyMuPDF
import os
from typing import List, Dict, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFProcessor:
    """PDF 파일 처리 클래스"""
    
    def __init__(self, pdf_path: str):
        """
        Args:
            pdf_path: PDF 파일 경로
        """
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.total_pages = len(self.doc)
        
    def extract_text_with_pages(self) -> List[Dict]:
        """
        PDF에서 페이지별로 텍스트 추출
        
        Returns:
            List[Dict]: 각 페이지의 텍스트와 페이지 번호를 포함한 딕셔너리 리스트
        """
        pages_data = []
        
        for page_num in range(self.total_pages):
            page = self.doc[page_num]
            text = page.get_text()
            
            pages_data.append({
                'page_number': page_num + 1,  # 1부터 시작
                'text': text,
                'char_count': len(text)
            })
            
        return pages_data
    
    def create_chunks_with_metadata(
        self, 
        chunk_size: int = 1000, 
        chunk_overlap: int = 200
    ) -> List[Dict]:
        """
        텍스트를 청크로 분할하고 메타데이터(페이지 번호) 포함
        
        Args:
            chunk_size: 각 청크의 최대 크기
            chunk_overlap: 청크 간 겹치는 부분의 크기
            
        Returns:
            List[Dict]: 청크 텍스트와 메타데이터를 포함한 딕셔너리 리스트
        """
        pages_data = self.extract_text_with_pages()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = []
        chunk_id = 0
        
        for page_data in pages_data:
            page_num = page_data['page_number']
            text = page_data['text']
            
            if not text.strip():
                continue
            
            # 각 페이지의 텍스트를 청크로 분할
            page_chunks = text_splitter.split_text(text)
            
            for chunk_text in page_chunks:
                chunks.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'page_number': page_num,
                    'source': os.path.basename(self.pdf_path)
                })
                chunk_id += 1
                
        return chunks
    
    def render_page_as_image(
        self, 
        page_number: int, 
        output_dir: str = 'static/page_images',
        dpi: int = 150
    ) -> str:
        """
        특정 페이지를 이미지로 렌더링
        
        Args:
            page_number: 페이지 번호 (1부터 시작)
            output_dir: 이미지 저장 디렉토리
            dpi: 이미지 해상도
            
        Returns:
            str: 저장된 이미지 파일 경로
        """
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 페이지 번호 유효성 검사
        if page_number < 1 or page_number > self.total_pages:
            raise ValueError(f"페이지 번호는 1부터 {self.total_pages} 사이여야 합니다.")
        
        # 페이지 렌더링 (0부터 시작하는 인덱스)
        page = self.doc[page_number - 1]
        
        # 고해상도로 렌더링
        zoom = dpi / 72  # 기본 DPI는 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # 파일명 생성
        pdf_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
        image_filename = f"{pdf_name}_page_{page_number}.png"
        image_path = os.path.join(output_dir, image_filename)
        
        # 이미지 저장
        pix.save(image_path)
        
        return image_path
    
    def get_page_info(self, page_number: int) -> Dict:
        """
        특정 페이지의 정보 추출
        
        Args:
            page_number: 페이지 번호 (1부터 시작)
            
        Returns:
            Dict: 페이지 정보 (텍스트, 이미지 개수 등)
        """
        if page_number < 1 or page_number > self.total_pages:
            raise ValueError(f"페이지 번호는 1부터 {self.total_pages} 사이여야 합니다.")
        
        page = self.doc[page_number - 1]
        text = page.get_text()
        images = page.get_images()
        
        return {
            'page_number': page_number,
            'text': text,
            'text_length': len(text),
            'image_count': len(images),
            'has_images': len(images) > 0
        }
    
    def close(self):
        """PDF 문서 닫기"""
        if self.doc:
            self.doc.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

