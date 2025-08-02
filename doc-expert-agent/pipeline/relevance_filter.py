"""
Sistema de filtros de relevância para RAG.
Filtra chunks baseado em critérios de relevância e qualidade.
"""

from langchain_core.documents import Document
from typing import List, Dict, Any, Callable
import re
from fuzzywuzzy import fuzz
from logger import get_logger

logger = get_logger(__name__)


class RelevanceFilter:
    """Sistema de filtros de relevância para chunks."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.filters = []
        self.setup_default_filters()
    
    def setup_default_filters(self):
        """Configura filtros padrão."""
        self.add_filter(self.filter_empty_content, "Filtro de conteúdo vazio")
        self.add_filter(self.filter_too_short, "Filtro de chunks muito pequenos")
        self.add_filter(self.filter_too_long, "Filtro de chunks muito grandes")
        self.add_filter(self.filter_noise, "Filtro de ruído")
        self.add_filter(self.filter_duplicates, "Filtro de duplicatas")
    
    def add_filter(self, filter_func: Callable, name: str):
        """
        Adiciona um filtro personalizado.
        
        Args:
            filter_func: Função de filtro
            name: Nome do filtro
        """
        self.filters.append({
            'function': filter_func,
            'name': name
        })
    
    def filter_empty_content(self, chunk: Document) -> bool:
        """
        Filtra chunks com conteúdo vazio ou apenas espaços.
        
        Args:
            chunk: Chunk para verificar
            
        Returns:
            True se o chunk deve ser mantido
        """
        content = chunk.page_content.strip()
        return len(content) > 0
    
    def filter_too_short(self, chunk: Document) -> bool:
        """
        Filtra chunks muito pequenos (menos de 50 caracteres).
        
        Args:
            chunk: Chunk para verificar
            
        Returns:
            True se o chunk deve ser mantido
        """
        return len(chunk.page_content.strip()) >= 50
    
    def filter_too_long(self, chunk: Document) -> bool:
        """
        Filtra chunks muito grandes (mais de 2000 caracteres).
        
        Args:
            chunk: Chunk para verificar
            
        Returns:
            True se o chunk deve ser mantido
        """
        return len(chunk.page_content.strip()) <= 2000
    
    def filter_noise(self, chunk: Document) -> bool:
        """
        Filtra chunks com muito ruído (muitos números, caracteres especiais).
        
        Args:
            chunk: Chunk para verificar
            
        Returns:
            True se o chunk deve ser mantido
        """
        content = chunk.page_content
        
        # Conta caracteres especiais e números
        special_chars = len(re.findall(r'[^a-zA-Z\s]', content))
        numbers = len(re.findall(r'\d', content))
        total_chars = len(content)
        
        # Se mais de 40% são caracteres especiais/números, considera ruído
        noise_ratio = (special_chars + numbers) / total_chars if total_chars > 0 else 0
        
        return noise_ratio < 0.4
    
    def filter_duplicates(self, chunk: Document) -> bool:
        """
        Filtra chunks duplicados (implementado no nível da lista).
        
        Args:
            chunk: Chunk para verificar
            
        Returns:
            True se o chunk deve ser mantido
        """
        # Este filtro é aplicado no nível da lista
        return True
    
    def filter_by_keywords(self, chunk: Document, keywords: List[str], min_matches: int = 1) -> bool:
        """
        Filtra chunks baseado em palavras-chave.
        
        Args:
            chunk: Chunk para verificar
            keywords: Lista de palavras-chave
            min_matches: Número mínimo de matches
            
        Returns:
            True se o chunk deve ser mantido
        """
        content = chunk.page_content.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in content)
        return matches >= min_matches
    
    def filter_by_similarity(self, chunk: Document, reference_text: str, threshold: float = 0.7) -> bool:
        """
        Filtra chunks baseado em similaridade com texto de referência.
        
        Args:
            chunk: Chunk para verificar
            reference_text: Texto de referência
            threshold: Limite de similaridade (0-1)
            
        Returns:
            True se o chunk deve ser mantido
        """
        similarity = fuzz.token_set_ratio(chunk.page_content, reference_text) / 100
        return similarity >= threshold
    
    def filter_by_content_type(self, chunk: Document, content_types: List[str]) -> bool:
        """
        Filtra chunks baseado no tipo de conteúdo.
        
        Args:
            chunk: Chunk para verificar
            content_types: Tipos de conteúdo aceitos
            
        Returns:
            True se o chunk deve ser mantido
        """
        content = chunk.page_content.lower()
        
        # Detecta tipo de conteúdo
        if any(word in content for word in ['tabela', 'table', 'gráfico', 'chart']):
            chunk_type = 'table'
        elif any(word in content for word in ['código', 'code', 'programa', 'script']):
            chunk_type = 'code'
        elif any(word in content for word in ['imagem', 'image', 'figura', 'figure']):
            chunk_type = 'image'
        else:
            chunk_type = 'text'
        
        return chunk_type in content_types
    
    def apply_filters(self, chunks: List[Document]) -> List[Document]:
        """
        Aplica todos os filtros configurados.
        
        Args:
            chunks: Lista de chunks
            
        Returns:
            Lista de chunks filtrados
        """
        self.logger.info(f"Aplicando filtros de relevância em {len(chunks)} chunks")
        
        filtered_chunks = []
        stats = {}
        
        for filter_info in self.filters:
            filter_name = filter_info['name']
            filter_func = filter_info['function']
            
            if filter_name == "Filtro de duplicatas":
                # Aplica filtro de duplicatas no nível da lista
                filtered_chunks = self.remove_duplicates(filtered_chunks)
                stats[filter_name] = len(filtered_chunks)
            else:
                # Aplica filtro individual
                before_count = len(filtered_chunks)
                filtered_chunks = [chunk for chunk in filtered_chunks if filter_func(chunk)]
                after_count = len(filtered_chunks)
                stats[filter_name] = after_count
                
                self.logger.info(f"{filter_name}: {before_count} -> {after_count} chunks")
        
        self.logger.info(f"Filtros aplicados. Resultado: {len(filtered_chunks)} chunks")
        self.logger.info(f"Estatísticas: {stats}")
        
        return filtered_chunks
    
    def remove_duplicates(self, chunks: List[Document]) -> List[Document]:
        """
        Remove chunks duplicados baseado em similaridade.
        
        Args:
            chunks: Lista de chunks
            
        Returns:
            Lista de chunks únicos
        """
        if not chunks:
            return []
        
        unique_chunks = [chunks[0]]
        
        for chunk in chunks[1:]:
            is_duplicate = False
            
            for unique_chunk in unique_chunks:
                similarity = fuzz.token_set_ratio(chunk.page_content, unique_chunk.page_content) / 100
                if similarity > 0.8:  # 80% de similaridade
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_chunks.append(chunk)
        
        return unique_chunks
    
    def get_filter_stats(self, original_chunks: List[Document], filtered_chunks: List[Document]) -> Dict[str, Any]:
        """
        Obtém estatísticas dos filtros aplicados.
        
        Args:
            original_chunks: Chunks originais
            filtered_chunks: Chunks filtrados
            
        Returns:
            Estatísticas dos filtros
        """
        return {
            'original_count': len(original_chunks),
            'filtered_count': len(filtered_chunks),
            'removed_count': len(original_chunks) - len(filtered_chunks),
            'retention_rate': len(filtered_chunks) / len(original_chunks) if original_chunks else 0
        } 