from streamlit.runtime.uploaded_file_manager import UploadedFile

class Input:
    def __init__(
            self, 
            question: str, 
            connection_type: str, 
            prompt_type: str,
            file: UploadedFile
        ):

        self.question = question
        self.connection_type = connection_type
        self.prompt_type = prompt_type
        self.file = file
