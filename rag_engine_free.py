"""
RAG 엔진 - 무료 버전 (HuggingFace 임베딩 사용)
OpenAI API 크레딧이 없을 때 사용
"""
import os
import pickle
from typing import List, Dict
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from openai import OpenAI


class RAGEngineFree:
    """RAG 파이프라인 관리 클래스 (무료 임베딩 사용)"""
    
    def __init__(self, openai_api_key: str):
        """
        Args:
            openai_api_key: OpenAI API 키 (답변 생성용만 사용)
        """
        self.api_key = openai_api_key
        
        # HuggingFace 임베딩 사용 (무료, 로컬)
        print("📥 HuggingFace 임베딩 모델 로드 중... (최초 1회만 다운로드)")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        self.vector_store = None
        self.chunks_metadata = []
        self.client = OpenAI(api_key=openai_api_key)
        
    def build_vector_store(self, chunks: List[Dict]) -> None:
        """
        청크로부터 벡터 스토어 구축
        
        Args:
            chunks: PDF 처리로부터 얻은 청크 리스트
        """
        # 청크 메타데이터 저장
        self.chunks_metadata = chunks
        
        # LangChain Document 객체로 변환
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk['text'],
                metadata={
                    'chunk_id': chunk['chunk_id'],
                    'page_number': chunk['page_number'],
                    'source': chunk['source']
                }
            )
            documents.append(doc)
        
        # FAISS 벡터 스토어 생성
        print(f"📊 {len(documents)}개의 청크에 대한 임베딩 생성 중... (무료 모델 사용)")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        print("✅ 벡터 스토어 구축 완료!")
        
    def save_vector_store(self, path: str = "vector_store_free") -> None:
        """
        벡터 스토어를 디스크에 저장
        
        Args:
            path: 저장 경로
        """
        if self.vector_store is None:
            raise ValueError("저장할 벡터 스토어가 없습니다.")
        
        os.makedirs(path, exist_ok=True)
        
        # FAISS 인덱스 저장
        self.vector_store.save_local(path)
        
        # 메타데이터 저장
        metadata_path = os.path.join(path, "chunks_metadata.pkl")
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.chunks_metadata, f)
        
        print(f"💾 벡터 스토어가 {path}에 저장되었습니다.")
        
    def load_vector_store(self, path: str = "vector_store_free") -> None:
        """
        디스크로부터 벡터 스토어 로드
        
        Args:
            path: 로드 경로
        """
        if not os.path.exists(path):
            raise ValueError(f"{path} 경로가 존재하지 않습니다.")
        
        # FAISS 인덱스 로드
        self.vector_store = FAISS.load_local(
            path, 
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        # 메타데이터 로드
        metadata_path = os.path.join(path, "chunks_metadata.pkl")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'rb') as f:
                self.chunks_metadata = pickle.load(f)
        
        print(f"📂 벡터 스토어가 {path}로부터 로드되었습니다.")
        
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        질의에 대한 유사 청크 검색
        
        Args:
            query: 사용자 질문
            k: 반환할 결과 개수
            
        Returns:
            List[Dict]: 검색된 청크와 메타데이터
        """
        if self.vector_store is None:
            raise ValueError("벡터 스토어가 초기화되지 않았습니다.")
        
        # 유사도 검색 (점수 포함)
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        search_results = []
        for doc, score in results:
            result = {
                'text': doc.page_content,
                'page_number': doc.metadata['page_number'],
                'chunk_id': doc.metadata['chunk_id'],
                'source': doc.metadata['source'],
                'similarity_score': float(score)
            }
            search_results.append(result)
        
        return search_results
    
    def generate_answer(self, query: str, search_results: List[Dict], system_prompt: str = None) -> Dict:
        """
        검색 결과를 기반으로 LLM 답변 생성
        
        Args:
            query: 사용자 질문
            search_results: 검색된 청크들
            system_prompt: 시스템 프롬프트 (선택)
            
        Returns:
            Dict: 답변 및 참조 페이지 정보
        """
        # 컨텍스트 구성
        context_parts = []
        page_numbers = set()
        
        for i, result in enumerate(search_results, 1):
            context_parts.append(
                f"[문서 {i} - 페이지 {result['page_number']}]\n{result['text']}\n"
            )
            page_numbers.add(result['page_number'])
        
        context = "\n".join(context_parts)
        
        # 기본 시스템 프롬프트
        if system_prompt is None:
            system_prompt = """당신은 전문적인 설치 안내 전문가입니다. 
제공된 문서 내용을 바탕으로 사용자의 질문에 명확하고 단계적으로 답변해주세요.

답변 형식:
1. **개요**: 질문에 대한 간단한 요약
2. **단계별 설명**: 구체적인 단계를 번호로 나열
3. **참고사항**: 추가로 알아야 할 중요한 정보

답변은 한국어로 작성하며, 전문적이면서도 이해하기 쉽게 작성해주세요."""
        
        # OpenAI API 호출
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""다음 문서 내용을 참고하여 질문에 답변해주세요.

문서 내용:
{context}

질문: {query}"""}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        answer = response.choices[0].message.content
        
        return {
            'answer': answer,
            'referenced_pages': sorted(list(page_numbers)),
            'source_chunks': search_results,
            'model': response.model,
            'total_tokens': response.usage.total_tokens
        }
    
    def query(self, question: str, k: int = 3, system_prompt: str = None) -> Dict:
        """
        질의에 대한 완전한 RAG 파이프라인 실행
        
        Args:
            question: 사용자 질문
            k: 검색할 청크 개수
            system_prompt: 커스텀 시스템 프롬프트
            
        Returns:
            Dict: 답변, 참조 페이지, 검색 결과 등
        """
        # 1. 검색
        search_results = self.search(question, k=k)
        
        # 2. 답변 생성
        result = self.generate_answer(question, search_results, system_prompt)
        
        # 3. 질문 추가
        result['question'] = question
        
        return result

