from service.agent_basic.prompt import Prompt
from infra.openai_client import OpenAIClientFactory
from model.enum.prompt_type import PromptType

from logger import get_logger

logger = get_logger(__name__)

class BasicConnectionToOpenAI:

    def __init__(self, context: str, question: str, prompt_type: PromptType):
        self.context = context
        self.question = question
        self.prompt_type = prompt_type

    def connect(self, api_key: str) -> str:
        logger.info("Iniciando conexão com a open AI do documento...")

        prompt = self.get_current_prompt()

        chat = OpenAIClientFactory(api_key=api_key).create_basic_client()

        response = chat.invoke(prompt)

        logger.info("===================================")
        logger.info(f"OpenAI: {response.content}")
        logger.info("===================================")

        logger.info("Finalizando conexão com a open AI do documento")

        return response.content
    
    def get_current_prompt(self): 
        prompt = Prompt(question=self.question, context=self.context)

        prompt_text = ""

        if self.prompt_type == PromptType.ZERO_SHOT_PROMPT:
            prompt_text = prompt.get_zero_show_prompt()

        elif self.prompt_type == PromptType.FEW_SHOT_PROMPT:
            prompt_text = prompt.get_few_show_prompt()

        elif self.prompt_type == PromptType.CHAIN_OF_THOUGHT:
            prompt_text = prompt.get_chain_of_thought()

        elif self.prompt_type == PromptType.STYLE_SPECIFIC_PROMPTING:
            prompt_text = prompt.get_style_specific_prompting()

        elif self.prompt_type == PromptType.LENGHT_LIMITATION_PROMPTING:
            prompt_text = prompt.get_lenght_limitation_prompting()

        elif self.prompt_type == PromptType.STEP_BY_STEP_INSTRUCTION_PROMPTING:
            prompt_text = prompt.step_by_step_instruction_prompting()

        elif self.prompt_type == PromptType.DEFINITION_EXEMPLIFICATION:
            prompt_text = prompt.get_definition_exemplification()
        
        return prompt_text
