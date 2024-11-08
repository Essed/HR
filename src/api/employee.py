from src.models.models import Employee

class EmployeeAPI:
    def __init__(self, storage_path: str) -> None:
        self.__storage_path = storage_path

    async def register(self, employee: Employee) -> Employee:
        return employee