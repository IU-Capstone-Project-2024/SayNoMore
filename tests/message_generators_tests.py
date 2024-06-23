import unittest
from request_analyzer.llm import LLM

from request_analyzer.information_retriever import InformationRetriever
from request_analyzer.more_info_required_message_generator import MoreInfoRequiredMessageGenerator


class TestMessageGenerators(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUp(cls):
        # Initialize the LLM
        cls.llm = LLM()

        cls.information_retr = InformationRetriever(cls.llm)
        cls.more_info_required_msg_gen = MoreInfoRequiredMessageGenerator(
            cls.llm)

    async def test_more_info_required_msg_gen(self):
        request = "Хочу сгонять в Магадан из Санкт Петербурга. Планирую лететь туда 12 августа."
        information_retriever_result = await self.information_retr.retrieve(
            request)
        field_verification_map, _, post_verification_results = information_retriever_result
        message_generated = await self.more_info_required_msg_gen.generate_message(
            request, field_verification_map, post_verification_results)
        self.assertIn("бюджет", message_generated)
        self.assertIn("дату возвращения", message_generated)


if __name__ == '__main__':
    unittest.main()
