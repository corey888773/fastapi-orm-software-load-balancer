import abc
from ..repository.abstractions import ReadRepositoryInterface, WriteRepositoryInterface, UnitOfWorkInterface
class CommandInterface(metaclass=abc.ABCMeta):
    pass


class CommandHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def handle(self, command: CommandInterface):
        raise NotImplementedError


class QueryInterface(metaclass=abc.ABCMeta):
    pass

class QueryHandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def handle(self, query: QueryInterface):
        raise NotImplementedError
