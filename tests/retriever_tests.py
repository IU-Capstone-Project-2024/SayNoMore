import os
import unittest
from vllm import LLM
from request_analyzer.retreivers.destination_retriever import DestinationRetriever
from request_analyzer.retreivers.departure_retriever import DepartureRetriever
from request_analyzer.retreivers.arrival_retriever import ArrivalRetriever
from request_analyzer.retreivers.return_retriever import ReturnRetriever
from request_analyzer.retreivers.budget_retriever import BudgetRetriever
from request_analyzer.information_retriever import InformationRetriever
from request_analyzer.utils.embedding_city_search import EmbeddingCitySearch
from request_analyzer.request_fields_enum import RequestField
from request_analyzer.verifiers.abstract_verifier import ValueStages


class TestRetrievers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # # Check for the HF_TOKEN environment variable
        # if "HF_TOKEN" not in os.environ:
        #     raise EnvironmentError("The environment variable 'HF_TOKEN' is not set. "
        #                            "Please set it to your Hugging Face access token "
        #                            "before running the tests.")

        # Specify the primary GPU to use (GPU 0, which has more available memory)
        # os.environ["CUDA_VISIBLE_DEVICES"] = "0"

        # Setting PyTorch environment variable for better memory management
        # os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

        # Model configuration (assuming you have a model_name variable defined)
        model_name = "meta-llama/Meta-Llama-3-8B"

        # Initialize the LLM
        cls.llm = LLM(
            model=model_name,
            tensor_parallel_size=1,  # Adjust as needed based on your GPU setup
            gpu_memory_utilization=0.4,
            enforce_eager=True,
            enable_chunked_prefill=True,
            max_num_batched_tokens=2048)

        cls.searcher = EmbeddingCitySearch()

        cls.departure_retr = DepartureRetriever(cls.llm, cls.searcher)
        cls.destination_retr = DestinationRetriever(cls.llm, cls.searcher)
        cls.arrival_retr = ArrivalRetriever(cls.llm)
        cls.return_retr = ReturnRetriever(cls.llm)
        cls.budget_retr = BudgetRetriever(cls.llm)

        cls.information_retr = InformationRetriever(cls.llm)

    def test_departure_retriever(self):
        test_cases = [{
            "request": "Планирую уехать в Минеральные воды через три недели.",
            "expected_departure": 'None'
        }, {
            "request": "Хочу уехать из Мурома куда-нибудь на три дня",
            "expected_departure": 'Муром'
        }, {
            "request": "Уеду в Питер из Иннополиса в июле с 12 по 17 числа",
            "expected_departure": 'Иннополис'
        }, {
            "request": "Мне срочно надо достать билеты в Кисловодск",
            "expected_departure": 'None'
        }]

        for case in test_cases:
            request = case["request"]
            expected_departure = case["expected_departure"]
            retrieved_departure = self.departure_retr.retrieve(request).strip()
            self.assertEqual(retrieved_departure.lower(),
                             expected_departure.lower(),
                             f"Failed for request: {request}")

    def test_destination_retriever(self):
        test_cases = [{
            "request": "Планирую уехать в Минеральные воды через три недели.",
            "expected_destination": 'Минеральные воды'
        }, {
            "request": "Хочу уехать из Мурома куда-нибудь на три дня",
            "expected_destination": 'None'
        }, {
            "request": "Уеду в Питер из Иннополиса в июле с 12 по 17 числа",
            "expected_destination": 'Санкт-Петербург'
        }, {
            "request": "Мне срочно надо достать билеты в Кисловодск",
            "expected_destination": 'Кисловодск'
        }]

        for case in test_cases:
            request = case["request"]
            expected_destination = case["expected_destination"]
            retrieved_destination = self.destination_retr.retrieve(
                request).strip()
            self.assertEqual(retrieved_destination.lower(),
                             expected_destination.lower(),
                             f"Failed for request: {request}")

    def test_budget_retriever(self):
        test_cases = [{
            'request': 'Есть 20000 тысяч. Хочу на два дня отдохнуть в Курске',
            'expected_budget': '20000'
        }, {
            'request': 'Хочу в Калининград',
            'expected_budget': 'None'
        }, {
            'request':
            'По планам съездить в Нижний Новгород, бюджет 31 тысяча',
            'expected_budget': '31000'
        }, {
            'request':
            'Я бы съездил в Иваново в тридцатых числах. На руках 40000',
            'expected_budget': '40000'
        }, {
            'request': 'По планам съездить в Нижний Новгород',
            'expected_budget': 'None'
        }]

        for case in test_cases:
            request = case["request"]
            expected_budget = case["expected_budget"]
            retrieved_budget = self.budget_retr.retrieve(request).strip()
            self.assertEqual(retrieved_budget.lower(), expected_budget.lower())

    def test_arrival_time_retriever(self):
        # TODO: Should be changed with time, when the date in request becomes obsolete
        test_cases = [{
            'request':
            'Есть 20000 тысяч. Хочу c 1ое по 20 августа дня отдохнуть в Курске',
            'expected_arrival': '01/08/2024'
        }, {
            'request': 'Хочу в Калининград',
            'expected_arrival': 'None'
        }, {
            'request': 'Поеду в Нижний Новгород второго сентября',
            'expected_arrival': '02/09/2024'
        }]

        for case in test_cases:
            request = case["request"]
            expected_arrival = case["expected_arrival"]
            retrieved_arrival = self.arrival_retr.retrieve(request).strip()
            self.assertEqual(retrieved_arrival.lower(),
                             expected_arrival.lower())

    def test_return_time_retriever(self):
        # TODO: Should be changed with time, when the date in request becomes obsolete
        test_cases = [{
            'request':
            'Есть 20000 тысяч. Хочу c 1ое по 20 августа дня отдохнуть в Курске',
            'expected_return': '20/08/2024'
        }, {
            'request': 'Хочу в Калининград',
            'expected_return': 'None'
        }, {
            'request':
            'Поеду в Нижний Новгород второго сентября. Обратно поеду 10го',
            'expected_return': '10/09/2024'
        }]

        for case in test_cases:
            request = case["request"]
            expected_return = case["expected_return"]
            retrieved_return = self.return_retr.retrieve(request).strip()
            self.assertEqual(retrieved_return.lower(), expected_return.lower())

    def test_information_retriever(self):
        request = "Отправляюсь из Казани в город Казань c 15ое по 2ое сентября. Мой бюджет 200 тысяч."
        information_retrieved = self.information_retr.retrieve(request)
        
        test_answer = (
            {RequestField.Arrival: "RequestField.Arrival data retrieved from user's request: 15/09/2024. Verification status: OK; Description: Everything is good.",
             RequestField.Return: "RequestField.Return data retrieved from user's request: 02/09/2024. Verification status: OK; Description: Everything is good.", 
             RequestField.Departure: "RequestField.Departure data retrieved from user's request: Казань. Verification status: OK; Description: Everything is good", 
             RequestField.Destination: "RequestField.Destination data retrieved from user's request: Казань. Verification status: OK; Description: Everything is good",
             RequestField.Budget: "RequestField.Budget data retrieved from user's request: 200000. Verification status: OK; Description: Everything is good"},
             False,
             [(ValueStages.INCORRECT_VALUE, 'The time of return from a city is earlier than the time of arrival from that city.'), 
              (ValueStages.INCORRECT_VALUE, 'Destination and departure cities match')]
        )

        for key in information_retrieved[0]:
            self.assertEqual(information_retrieved[0][key], test_answer[0][key])
        
        self.assertEqual(information_retrieved[1], test_answer[1])
        self.assertEqual(len(information_retrieved[2]), len(test_answer[2]))
        for idx, retr_post_verif in enumerate(information_retrieved[2]):
            self.assertEqual(retr_post_verif, test_answer[2][idx])

"""
request = "Поеду из Казани в Москву в середине июня. Мой бюджет 200 тысяч."

({<RequestField.Arrival: 'Arrival'>: "RequestField.Arrival data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field.", 
  <RequestField.Return: 'Return'>: "RequestField.Return data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field.",
  <RequestField.Departure: 'Departure'>: "RequestField.Departure data retrieved from user's request: Казань. Verification status: OK; Description: Everything is good", 
  <RequestField.Destination: 'Destination'>: "RequestField.Destination data retrieved from user's request: Москва. Verification status: OK; Description: Everything is good", 
  <RequestField.Budget: 'Budget'>: "RequestField.Budget data retrieved from user's request: 200000. Verification status: OK; Description: Everything is good"
  }, False, [])
"""

if __name__ == '__main__':
    unittest.main()
