from vllm import LLM, SamplingParams
from datetime import datetime
from request_analyzer.retreivers.abstract_retriever import BaseRetriever


# retreive the date of the return from the destination city
class ReturnRetriever(BaseRetriever):

    def __init__(self, llm: LLM) -> None:
        self.llm = llm
        # Setting up sampling parameters for deterministic output
        self.sampling_params = SamplingParams(temperature=0, stop='"')
        # Defining a prompt template to guide the model extract return date
        self.cur_day = datetime.now()
        self.prefix_prompt = \
            '''Today is June 9, 2024. Sunday. Your task is to extract the return time from the destination city from the user's request. Examples:
            Q: "Планирую сгонять в Хабаровск через три недели."
            A: Return date: "None"
            
            Q: "Я хочу в Бийск, но нужно вернуться в середине августа."
            A: Return date: "15/08/2024"
              
            Q: "Я хочу поехать в отпуск и вернуться 22 октября"
            A: Return date: "22/10/2024"
            
            Q: "Хочу уехать из Москвы куда-нибудь на три дня, есть двадцать тысяч"
            A: Return date: "None"

            Q: "Уеду в Питер из Казани в июле с 12 по 17 числа +- 300000 рублей"
            A: Return date: "17/07/2024"

            Q: "Уеду в Москву из Рязани в августе с 10 по 30. Бюджет 70 тысяч."
            A: Return date: "30/08/2024"

            Q: "Уеду из Рязани в августе с 10 по 30. Есть 70 тысяч."
            A: Return date: "30/08/2024"

            Q: "Я в Тольятти. Мне срочно надо достать билеты в Кисловодск"
            A: Return date: "None"

            Q: "Я в Москву в среду"
            A: Return date: "None"

            Q: "Я в Москву в с 1ое по 5ое мая"
            A: Return date: "05/05/2025"

            Today is {self.cur_day.strftime('%B %d, %Y. %A.') } Your task is to extract the return time from the destination city from the user's request.

            Q: "USER_REQUEST"
            A: Return date: "'''

    def retrieve(self, request: str) -> str:
        """
        Generates a response from the VLLM based
        on the user's travel request, aiming to
        extract the return date from the destination city.

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
        # Generate a response from the VLLM using
        # the customized prompt and sampling parameters
        vllm_output = self.llm.generate(prompt, self.sampling_params)
        # Extract and return the generated text as
        # the return time from the destination city
        return vllm_output[0].outputs[0].text
