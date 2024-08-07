from request_analyzer.llm import LLM
from datetime import datetime
from request_analyzer.retreivers.abstract_retriever import BaseRetriever
from request_analyzer.utils.extract_data import extract_data


# retreive the date of the return from the destination city
class ReturnRetriever(BaseRetriever):

    def __init__(self, llm: LLM) -> None:
        self.llm = llm
        # Setting up sampling parameters for deterministic output
        self.json_input = {"temperature": 0, "stop": '\n\n'}
        # Defining a prompt template to guide the model extract return date
        self.cur_day = datetime.now()
        self.prefix_prompt = \
'''Today is June 9, 2024. Sunday. Your task is to extract the return time from the destination city from the user's request depending on the todays date. Examples:
Q: "Планирую сгонять в Хабаровск через три недели."
A: Return date: "None"

Q: "Еду в Мурманск 20го сентября"
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

Today is INSERT_DATE Your task is to extract the return time from the destination city from the user's request depending on the todays date.

Q: "USER_REQUEST"
A: Return date: "'''

    async def retrieve(self, request: str) -> str:
        """
        Generates a response from the LLM based
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
        # Put actual information about the date in the prompt
        cur_day = datetime.now()
        prompt = self.prefix_prompt.replace("INSERT_DATE",
                                            cur_day.strftime('%B %d, %Y. %A.'))
        # Replace the placeholder in the prompt
        # template with the actual user request
        prompt = prompt.replace("USER_REQUEST", request)
        # Generate a response from the LLM using
        # the customized prompt and sampling parameters
        self.json_input["prompt"] = prompt
        result = await self.llm.get_response(self.json_input)
        result = extract_data(result)
        return result
