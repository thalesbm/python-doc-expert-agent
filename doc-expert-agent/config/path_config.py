from dataclasses import dataclass

@dataclass
class PathConfig:
    """Configurações de caminhos."""
    tcc_path: str = "files/tcc.pdf"
    hp_path: str = "files/harry-potter-1-cap-1.pdf"