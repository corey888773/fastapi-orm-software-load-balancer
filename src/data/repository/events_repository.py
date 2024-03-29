from .abstractions import ReadRepositoryInterface, WriteRepositoryInterface
from ..database import DatabaseWrapper
from ..events import *
from ..models.todo_item import TodoItem
from schemas import TodoItemSchema, Response

class EventsReadRepository(ReadRepositoryInterface):
    def __init__(self, dbw: DatabaseWrapper):
        self.db_wrapper = dbw

    async def list_todo_items(self) -> list[TodoItem]:
        if self.db_wrapper.is_connected():
            with self.db_wrapper.make_session() as db:
                return db.query(TodoItem).all()

    async def get_todo_item_by_id(self, id: int) -> TodoItem:
        if self.db_wrapper.is_connected():
            with self.db_wrapper.make_session() as db:
                return db.query(TodoItem).filter(TodoItem.id == id).first()


class EventsWriteRepository(WriteRepositoryInterface):
    def __init__(self, dbw: DatabaseWrapper):
        self.db_wrapper = dbw

    async def create_todo_item(self, todo_item: TodoItemSchema) -> TodoItem:
        event = TodoItemCreatedEvent(title=todo_item.title, description=todo_item.description, completed=todo_item.completed)
        self.db_wrapper.register_event(event)

        if self.db_wrapper.is_connected():
            self.db_wrapper.commit_events()

    async def update_todo_item(self, id: int, todo_item: TodoItemSchema) -> TodoItem:
        event = TodoItemUpdatedEvent(id=id, title=todo_item.title, description=todo_item.description, completed=todo_item.completed)
        self.db_wrapper.register_event(event)

        if self.db_wrapper.is_connected():
            self.db_wrapper.commit_events()

    async def delete_todo_item(self, id: int) -> Response:
        event = TodoItemDeletedEvent(id=id)
        self.db_wrapper.register_event(event)

        if self.db_wrapper.is_connected():
            self.db_wrapper.commit_events()