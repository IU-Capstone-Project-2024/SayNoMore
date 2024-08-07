from request_analyzer.llm import LLM
from request_analyzer.retreivers.abstract_retriever import BaseRetriever
from request_analyzer.utils.extract_data import extract_data


class BudgetRetriever(BaseRetriever):
    """
    A class designed to retrieve the user's available
    budget from their travel requests using a LLM API call.

    Attributes:
        llm (LLM): An instance of a LLM used for 
            generating text based on prompts.
        json_input (dict): Parameters 
            for controlling the sampling behavior of 
            the LLM during text generation.
        prefix_prompt (str): A predefined prompt 
            template that guides the VLLM to focus 
            on extracting the user's budget from their 
            requests.
    """

    def __init__(self, llm: LLM) -> None:
        """
        Initializes the BudgetRetriever with a given
        VLLM instance and sets up default sampling 
        parameters and a prompt template.

        Args:
            llm (LLM): The VLLM instance to be used 
                for text generation.
        """
        self.llm = llm
        # Setting up sampling parameters for deterministic
        #  output
        self.json_input = {"temperature": 0, "stop": '\n\n'}
        # Defining a prompt template to guide the model towards
        #  extracting the user's budget
        self.prefix_prompt = \
'''Your task is to extract the user's available budget from his request. Examples:
Q: "Планирую сгонять в Хабаровск через три недели."
A: Budget: "None"

Q: "Хочу уехать из Москвы куда-нибудь на три дня, есть двадцать тысяч"
A: Budget: "20000"

Q: "Уеду в Питер из Казани в июле с 12 по 17 числа +- 300000 рублей"
A: Budget: "300000"

Q: "Уеду в Москву из Рязани в августе с 10 по 30. Бюджет 70 тысяч."
A: Budget: "70000"

Q: "Уеду из Рязани в августе с 10 по 30. Есть 70 тысяч."
A: Budget: "70000"

Q: "Я в Тольятти. Мне срочно надо достать билеты в Кисловодск"
A: Budget: "None"

Q: "USER_REQUEST"
A: Budget: "'''

    async def retrieve(self, request: str) -> str:
        """
        Generates a response from the VLLM based 
        on the user's travel request, aiming to 
        extract the user's budget.

        Args:
            request (str): The user's travel request 
                as a string.

        Returns:
            str: The extracted budget amount as a string,
                or a message indicating no budget was 
                found.
        """
        # Replace the placeholder in the prompt template with
        # the actual user request
        prompt = self.prefix_prompt.replace("USER_REQUEST", request)
        # Generate a response from the LLM using the customized
        # prompt and sampling parameters
        self.json_input["prompt"] = prompt
        result = await self.llm.get_response(self.json_input)
        result = extract_data(result)
        return result
