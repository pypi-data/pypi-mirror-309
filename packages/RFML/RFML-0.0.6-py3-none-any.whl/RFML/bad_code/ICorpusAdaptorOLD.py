# from abc import ABC, abstractmethod
# import typing as t
# 
# T = t.TypeVar("T")
# 
# 
# class ICorpusAdaptor(t.Generic[T], ABC):
#     @abstractmethod
#     def read(self, key: str) -> str:
#         # raise NotImplementedError("Please implement IPrompt")
#         pass
# 
#     @abstractmethod
#     def write(self, key: str, value: str) -> str:
#         # raise NotImplementedError("Please implement IPrompt")
#         pass
# 
#     @abstractmethod
#     def clean(self, key: str) -> str:
#         # raise NotImplementedError("Please implement IPrompt")
#         pass
# 
#     @abstractmethod
#     def is_empty(self, key: str) -> bool:
#         pass
# 
#     # @abstractmethod
#     # def get(self, query: str) -> T:
#     #     pass
#     #
#     # @abstractmethod
#     # def get_by_id(self, ids: str) -> T:
#     #     pass
#     #
#     # @abstractmethod
#     # def save(self, dataset: T):
#     #     pass
#     #
#     # @abstractmethod
#     # def delete(self, ids: str):
#     #     pass
#     #
#     # @abstractmethod
#     # def update(self, dataset: T):
#     #     pass
