import unittest

from request_analyzer.llm import LLM
from request_analyzer.request_analyzer import RequestAnalyzer


class TestRequestAnalyzer(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUp(cls):
        # Initialize the LLM
        cls.llm = LLM()


    async def test_request_analyzer(self):
        requests = [
            "Хочу уехать в Москву c 1го по 15 декабря",
            "Я поеду из Казани. Бюджет примерно 35 тысяч"
        ]
        request_idx = 0
        message = ""
        request_analyzer = RequestAnalyzer(self.llm)
        while True:
            are_all_fields_retireved, message = await \
                request_analyzer.analyzer_step(requests[request_idx])
            # print(message)
            if are_all_fields_retireved is True:
                break
            request_idx += 1

        self.assertEqual(message, "Arrival:01/12/2024;Return:15/12/2024;Departure:Казань;Destination:Москва;Budget:35000")


        requests = [
            "Хочу уехать из Казани 1го декабря",
            "Я уеду в Москву. Обратно отправляюсь 22го декабря"
        ]
        request_idx = 0
        message = ""
        request_analyzer = RequestAnalyzer(self.llm)
        while True:
            are_all_fields_retireved, message = await \
                request_analyzer.analyzer_step(requests[request_idx])
            # print(message)
            if are_all_fields_retireved is True:
                break
            request_idx += 1
        
        self.assertEqual(message, "Arrival:01/12/2024;Return:22/12/2024;Departure:Казань;Destination:Москва;Budget:None")


if __name__ == '__main__':
    unittest.main()
