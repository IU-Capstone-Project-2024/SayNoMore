from request_analyzer.llm import LLM
from request_analyzer.retreivers.abstract_retriever import BaseRetriever
from request_analyzer.utils.embedding_city_search import EmbeddingCitySearch
from request_analyzer.utils.extract_data import extract_data


class DestinationRetriever(BaseRetriever):
    """
    A class designed to retrieve destination cities 
    from user travel requests using a VLLM.

    Attributes:
        llm (LLM): An instance of a VLLM used for 
                   generating text based on prompts.
        json_input (dict): Parameters
                   for controlling the sampling behavior
                   of the VLLM during text generation.
        prefix_prompt (str): A predefined prompt template 
                   that guides the VLLM to focus on 
                   extracting destination cities from user
                   requests.
    """

    def __init__(self, llm: LLM, searcher: EmbeddingCitySearch) -> None:
        """
        Initializes the DestinationRetriever with
        a given VLLM instance and sets up default 
        sampling parameters and a prompt template.

        Args:
            llm (LLM): The VLLM instance to be used
                       for text generation.
            searcher (EmbeddingCitySearch): Class, to
                       search for all Russian cities 
                       to ignore grammatical errors 
                       entered by the user
        """
        self.llm = llm
        # Setting up sampling parameters for deterministic output
        self.json_input = {"temperature": 0, "stop": '\n\n'}
        # Defining a prompt template to guide the model towards
        # extracting destination cities
        self.prefix_prompt = \
'''Your task is to extract destination city from user request. Examples:
Q: "Планирую сгонять в Хабаровск через три недели."
A: Destination: "Хабаровск"

Q: "Хочу уехать из Москвы куда-нибудь на три дня"
A: Destination: "None"

Q: "Уеду в Питер из Казани в июле с 12 по 17 числа"
A: Destination: "Санкт-Петербург"

Q: "Уеду в Москву из Рязани в августе с 10 по 30. Бюджет 70 тысяч."
A: Destination: "Москва"

Q: "Уеду из Рязани в августе с 10 по 30. Бюджет 70 тысяч."
A: Destination: "None"

Q: "Я в Тольятти. Мне срочно надо достать билеты в Кисловодск"
A: Destination: "Кисловодск"

Q: "USER_REQUEST"
A: Destination: "'''

        self.searcher = searcher

    async def retrieve(self, request: str) -> str:
        """
        Generates a response from the LLM based 
        on the user's travel request, aiming to 
        extract the destination city.

        Args:
            request (str): The user's travel 
                           request as a string.

        Returns:
            str: The extracted destination city 
                 as a string, or a message indicating 
                 no destination was found.
        """
        # Replace the placeholder in the prompt
        # template with the actual user request
        prompt = self.prefix_prompt.replace("USER_REQUEST", request)
        # Generate a response from the LLM using
        # the customized prompt and sampling parameters
        self.json_input["prompt"] = prompt
        result = await self.llm.get_response(self.json_input)
        result = extract_data(result)
        if not result == 'None':
            found_russian_city = self.searcher.search_city(result)
            return found_russian_city[0][0]
        return result
