from dataclasses import dataclass

@dataclass
class StreamlitConfig:
    """Configurações do Streamlit."""
    page_title: str = "Doc Expert Agent"
    page_icon: str = ""
    layout: str = "wide"
    initial_sidebar_state: str = "expanded"
