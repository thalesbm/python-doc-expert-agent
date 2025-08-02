"""
Sistema de chunking adaptativo para RAG.
Ajusta o tamanho dos chunks baseado no conteúdo e contexto.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict, Any
import re
from logger import get_logger

logger = get_logger(__name__)


class AdaptiveChunker:
    """Sistema de chunking que se adapta ao conteúdo."""
    
    def __init__(self, base_chunk_size: int = 512, base_overlap: int = 100):
        self.base_chunk_size = base_chunk_size
        self.base_overlap = base_overlap
        self.logger = get_logger(__name__)
    
    def analyze_content(self, text: str) -> Dict[str, Any]:
        """
        Analisa o conteúdo para determinar a estratégia de chunking.
        
        Args:
            text: Texto para análise
            
        Returns:
            Dicionário com métricas do conteúdo
        """
        metrics = {
            'length': len(text),
            'sentences': len(re.split(r'[.!?]+', text)),
            'paragraphs': len(text.split('\n\n')),
            'avg_sentence_length': 0,
            'complexity_score': 0,
            'technical_terms': 0
        }
        
        # Calcula comprimento médio das frases
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            metrics['avg_sentence_length'] = sum(len(s) for s in sentences) / len(sentences)
        
        # Calcula complexidade (palavras longas, termos técnicos)
        words = text.split()
        long_words = sum(1 for word in words if len(word) > 8)
        metrics['complexity_score'] = long_words / len(words) if words else 0
        
        # Conta termos técnicos (palavras com mais de 10 caracteres)
        metrics['technical_terms'] = sum(1 for word in words if len(word) > 10)
        
        return metrics
    
    def determine_chunk_strategy(self, metrics: Dict[str, Any]) -> Dict[str, int]:
        """
        Determina a estratégia de chunking baseada nas métricas.
        
        Args:
            metrics: Métricas do conteúdo
            
        Returns:
            Estratégia de chunking (tamanho e overlap)
        """
        base_size = self.base_chunk_size
        base_overlap = self.base_overlap
        
        # Ajusta baseado no comprimento médio das frases
        if metrics['avg_sentence_length'] > 200:
            # Frases longas - chunks menores
            chunk_size = int(base_size * 0.7)
            overlap = int(base_overlap * 0.8)
        elif metrics['avg_sentence_length'] < 50:
            # Frases curtas - chunks maiores
            chunk_size = int(base_size * 1.3)
            overlap = int(base_overlap * 1.2)
        else:
            chunk_size = base_size
            overlap = base_overlap
        
        # Ajusta baseado na complexidade
        if metrics['complexity_score'] > 0.3:
            # Texto complexo - chunks menores para melhor compreensão
            chunk_size = int(chunk_size * 0.8)
            overlap = int(overlap * 1.1)
        
        # Ajusta baseado no número de parágrafos
        if metrics['paragraphs'] > 10:
            # Muitos parágrafos - chunks menores para preservar estrutura
            chunk_size = int(chunk_size * 0.9)
        
        return {
            'chunk_size': max(200, chunk_size),  # Mínimo de 200 caracteres
            'overlap': max(50, overlap)          # Mínimo de 50 caracteres
        }
    
    def chunk_document(self, document: Document) -> List[Document]:
        """
        Chunk um documento usando estratégia adaptativa.
        
        Args:
            document: Documento para chunking
            
        Returns:
            Lista de chunks
        """
        self.logger.info(f"Iniciando chunking adaptativo para documento: {document.metadata}")
        
        # Analisa o conteúdo
        metrics = self.analyze_content(document.page_content)
        strategy = self.determine_chunk_strategy(metrics)
        
        self.logger.info(f"Métricas: {metrics}")
        self.logger.info(f"Estratégia: {strategy}")
        
        # Cria o splitter com a estratégia determinada
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=strategy['chunk_size'],
            chunk_overlap=strategy['overlap'],
            separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", " "]
        )
        
        # Faz o chunking
        chunks = splitter.split_documents([document])
        
        # Remove chunks duplicados
        unique_chunks = self.remove_duplicates(chunks)
        
        self.logger.info(f"Chunks gerados: {len(chunks)}, Únicos: {len(unique_chunks)}")
        
        return unique_chunks
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Chunk múltiplos documentos usando estratégia adaptativa.
        
        Args:
            documents: Lista de documentos
            
        Returns:
            Lista de chunks
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        # Remove duplicados globais
        final_chunks = self.remove_duplicates(all_chunks)
        
        self.logger.info(f"Total de chunks únicos: {len(final_chunks)}")
        
        return final_chunks
    
    def remove_duplicates(self, chunks: List[Document]) -> List[Document]:
        """
        Remove chunks duplicados baseado no conteúdo.
        
        Args:
            chunks: Lista de chunks
            
        Returns:
            Lista de chunks únicos
        """
        unique_chunks = []
        seen_contents = set()
        
        for chunk in chunks:
            # Normaliza o conteúdo para comparação
            normalized_content = re.sub(r'\s+', ' ', chunk.page_content.strip())
            
            if normalized_content not in seen_contents:
                unique_chunks.append(chunk)
                seen_contents.add(normalized_content)
        
        return unique_chunks
    
    def get_chunk_stats(self, chunks: List[Document]) -> Dict[str, Any]:
        """
        Obtém estatísticas dos chunks gerados.
        
        Args:
            chunks: Lista de chunks
            
        Returns:
            Estatísticas dos chunks
        """
        if not chunks:
            return {}
        
        lengths = [len(chunk.page_content) for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_length': sum(lengths) / len(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'total_content_length': sum(lengths)
        } 