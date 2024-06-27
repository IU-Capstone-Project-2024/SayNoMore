import unittest
from request_analyzer.llm import LLM
from request_analyzer.retreivers.destination_retriever import DestinationRetriever
from request_analyzer.retreivers.departure_retriever import DepartureRetriever
from request_analyzer.retreivers.arrival_retriever import ArrivalRetriever
from request_analyzer.retreivers.return_retriever import ReturnRetriever
from request_analyzer.retreivers.budget_retriever import BudgetRetriever
from request_analyzer.information_retriever import InformationRetriever
from request_analyzer.utils.embedding_city_search import EmbeddingCitySearch
from request_analyzer.request_fields_enum import RequestField
from request_analyzer.verifiers.abstract_verifier import ValueStages


class TestRetrievers(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUp(cls):
        cls.llm = LLM()

        cls.searcher = EmbeddingCitySearch()

        cls.departure_retr = DepartureRetriever(cls.llm, cls.searcher)
        cls.destination_retr = DestinationRetriever(cls.llm, cls.searcher)
        cls.arrival_retr = ArrivalRetriever(cls.llm)
        cls.return_retr = ReturnRetriever(cls.llm)
        cls.budget_retr = BudgetRetriever(cls.llm)

        cls.information_retr = InformationRetriever(cls.llm)

    async def test_departure_retriever(self):
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
            retrieved_departure = await self.departure_retr.retrieve(request)
            retrieved_departure = retrieved_departure.strip()
            self.assertEqual(retrieved_departure.lower(),
                             expected_departure.lower(),
                             f"Failed for request: {request}")

    async def test_destination_retriever(self):
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
            retrieved_destination = await self.destination_retr.retrieve(
                request)
            retrieved_destination = retrieved_destination.strip()
            self.assertEqual(retrieved_destination.lower(),
                             expected_destination.lower(),
                             f"Failed for request: {request}")

    async def test_budget_retriever(self):
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
            retrieved_budget = await self.budget_retr.retrieve(request)
            retrieved_budget = retrieved_budget.strip()
            self.assertEqual(retrieved_budget.lower(), expected_budget.lower())

    async def test_arrival_time_retriever(self):
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
            retrieved_arrival = await self.arrival_retr.retrieve(request)
            retrieved_arrival = retrieved_arrival.strip()
            self.assertEqual(retrieved_arrival.lower(),
                             expected_arrival.lower())

    async def test_return_time_retriever(self):
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
            retrieved_return = await self.return_retr.retrieve(request)
            retrieved_return = retrieved_return.strip()
            self.assertEqual(retrieved_return.lower(), expected_return.lower())

    async def test_information_retriever(self):
        request = "Отправляюсь из Казани в Москву c 1ое по 2ое сентября. Мой бюджет 200 тысяч."
        information_retrieved = await self.information_retr.retrieve(request)

        test_answer = ({
            RequestField.Arrival:
            "RequestField.Arrival data retrieved from user's request: 01/09/2024. Verification status: OK; Description: Everything is good.",
            RequestField.Return:
            "RequestField.Return data retrieved from user's request: 02/09/2024. Verification status: OK; Description: Everything is good.",
            RequestField.Departure:
            "RequestField.Departure data retrieved from user's request: Казань. Verification status: OK; Description: Everything is good",
            RequestField.Destination:
            "RequestField.Destination data retrieved from user's request: Москва. Verification status: OK; Description: Everything is good",
            RequestField.Budget:
            "RequestField.Budget data retrieved from user's request: 200000. Verification status: OK; Description: Everything is good"
        }, [True, True, True, True, True, True], [])

        for key in information_retrieved[0]:
            self.assertEqual(information_retrieved[0][key],
                             test_answer[0][key])

        self.assertEqual(information_retrieved[1], test_answer[1])
        self.assertEqual(len(information_retrieved[2]), len(test_answer[2]))
        for idx, retr_post_verif in enumerate(information_retrieved[2]):
            self.assertEqual(retr_post_verif, test_answer[2][idx])


if __name__ == '__main__':
    unittest.main()
