class Input:
    def __init__(
            self, 
            question: str, 
            connection_type: str, 
            prompt_type: str
        ):

        self.question = question
        self.connection_type = connection_type
        self.prompt_type = prompt_type
