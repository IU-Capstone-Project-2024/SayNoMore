from request_analyzer.retreivers.abstract_retriever import BaseRetriever

class ArrivalRetriever(BaseRetriever):
    def __init__(self): #тут как будто llm не нужна
        pass 

    def retrieve(request: str) -> str:
        pass