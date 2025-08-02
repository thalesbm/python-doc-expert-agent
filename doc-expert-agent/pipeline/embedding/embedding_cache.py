"""
Sistema de cache de embeddings para RAG.
Armazena embeddings em cache para melhorar performance.
"""

import hashlib
import json
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
from logger import get_logger

logger = get_logger(__name__)

class EmbeddingCache:
    """Sistema de cache para embeddings."""
    
    def __init__(self, cache_dir: str = "cache/embeddings", max_size_mb: int = 1000):
        self.cache_dir = Path(cache_dir)
        self.max_size_mb = max_size_mb
        self.logger = get_logger(__name__)
        self.cache_metadata_file = self.cache_dir / "metadata.json"
        
        # Cria diretório de cache se não existir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Carrega metadados do cache
        self.metadata = self.load_metadata()
    
    def generate_cache_key(self, text: str, model: str) -> str:
        """
        Gera chave única para o cache baseada no texto e modelo.
        
        Args:
            text: Texto para embedding
            model: Modelo de embedding
            
        Returns:
            Chave única do cache
        """
        # Combina texto e modelo
        content = f"{text}:{model}"
        
        # Gera hash SHA-256
        hash_object = hashlib.sha256(content.encode('utf-8'))
        return hash_object.hexdigest()
    
    def get_cache_path(self, cache_key: str) -> Path:
        """
        Obtém caminho do arquivo de cache.
        
        Args:
            cache_key: Chave do cache
            
        Returns:
            Caminho do arquivo
        """
        return self.cache_dir / f"{cache_key}.pkl"
    
    def is_cached(self, text: str, model: str) -> bool:
        """
        Verifica se o embedding está em cache.
        
        Args:
            text: Texto para verificar
            model: Modelo de embedding
            
        Returns:
            True se está em cache
        """
        cache_key = self.generate_cache_key(text, model)
        cache_path = self.get_cache_path(cache_key)
        
        if not cache_path.exists():
            return False
        
        # Verifica se o cache não expirou
        if cache_key in self.metadata:
            created_time = datetime.fromisoformat(self.metadata[cache_key]['created'])
            max_age = timedelta(days=30)  # Cache expira em 30 dias
            
            if datetime.now() - created_time > max_age:
                self.logger.info(f"Cache expirado para chave: {cache_key}")
                self.remove_from_cache(cache_key)
                return False
        
        return True
    
    def get_from_cache(self, text: str, model: str) -> Optional[List[float]]:
        """
        Obtém embedding do cache.
        
        Args:
            text: Texto para obter embedding
            model: Modelo de embedding
            
        Returns:
            Embedding se encontrado, None caso contrário
        """
        cache_key = self.generate_cache_key(text, model)
        cache_path = self.get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                embedding = pickle.load(f)
            
            self.logger.info(f"Embedding carregado do cache: {cache_key}")
            return embedding
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar cache: {e}")
            return None
    
    def save_to_cache(self, text: str, model: str, embedding: List[float]):
        """
        Salva embedding no cache.
        
        Args:
            text: Texto do embedding
            model: Modelo de embedding
            embedding: Embedding para salvar
        """
        cache_key = self.generate_cache_key(text, model)
        cache_path = self.get_cache_path(cache_key)
        
        try:
            # Salva embedding
            with open(cache_path, 'wb') as f:
                pickle.dump(embedding, f)
            
            # Atualiza metadados
            self.metadata[cache_key] = {
                'created': datetime.now().isoformat(),
                'model': model,
                'text_length': len(text),
                'embedding_dim': len(embedding),
                'file_size': cache_path.stat().st_size
            }
            
            self.save_metadata()
            
            self.logger.info(f"Embedding salvo no cache: {cache_key}")
            
            # Verifica se precisa limpar cache
            self.check_cache_size()
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar cache: {e}")
    
    def remove_from_cache(self, cache_key: str):
        """
        Remove item do cache.
        
        Args:
            cache_key: Chave do cache
        """
        cache_path = self.get_cache_path(cache_key)
        
        if cache_path.exists():
            cache_path.unlink()
        
        if cache_key in self.metadata:
            del self.metadata[cache_key]
            self.save_metadata()
    
    def clear_cache(self):
        """Limpa todo o cache."""
        try:
            # Remove arquivos de cache
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
            
            # Limpa metadados
            self.metadata = {}
            self.save_metadata()
            
            self.logger.info("Cache limpo com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro ao limpar cache: {e}")
    
    def check_cache_size(self):
        """Verifica e limpa cache se necessário."""
        total_size = 0
        cache_files = []
        
        # Calcula tamanho total do cache
        for cache_file in self.cache_dir.glob("*.pkl"):
            size = cache_file.stat().st_size
            total_size += size
            cache_files.append((cache_file, size))
        
        total_size_mb = total_size / (1024 * 1024)
        
        if total_size_mb > self.max_size_mb:
            self.logger.info(f"Cache muito grande ({total_size_mb:.2f}MB), limpando...")
            self.cleanup_cache(cache_files)
    
    def cleanup_cache(self, cache_files: List[tuple]):
        """
        Limpa cache removendo arquivos mais antigos.
        
        Args:
            cache_files: Lista de arquivos de cache
        """
        # Ordena por data de criação (mais antigos primeiro)
        cache_files_with_time = []
        
        for cache_file, size in cache_files:
            cache_key = cache_file.stem
            if cache_key in self.metadata:
                created_time = datetime.fromisoformat(self.metadata[cache_key]['created'])
                cache_files_with_time.append((cache_file, size, created_time))
        
        cache_files_with_time.sort(key=lambda x: x[2])
        
        # Remove arquivos mais antigos até atingir o limite
        current_size = sum(size for _, size, _ in cache_files_with_time)
        target_size = self.max_size_mb * 1024 * 1024 * 0.8  # 80% do limite
        
        for cache_file, size, _ in cache_files_with_time:
            if current_size <= target_size:
                break
            
            cache_key = cache_file.stem
            self.remove_from_cache(cache_key)
            current_size -= size
    
    def load_metadata(self) -> Dict[str, Any]:
        """Carrega metadados do cache."""
        if self.cache_metadata_file.exists():
            try:
                with open(self.cache_metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Erro ao carregar metadados: {e}")
        
        return {}
    
    def save_metadata(self):
        """Salva metadados do cache."""
        try:
            with open(self.cache_metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            self.logger.error(f"Erro ao salvar metadados: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Obtém estatísticas do cache.
        
        Returns:
            Estatísticas do cache
        """
        total_files = len(self.metadata)
        total_size = sum(info.get('file_size', 0) for info in self.metadata.values())
        
        return {
            'total_files': total_files,
            'total_size_mb': total_size / (1024 * 1024),
            'max_size_mb': self.max_size_mb,
            'cache_dir': str(self.cache_dir)
        } 