from typing import Union
from src.utils.json_utils import add_data_to_json, read_data_from_json_as_list, write_data_to_json_as_list, clear_data
from src.models.models import Company, Employee

class CompanyAPI:
    def __init__(self, storage_path: str):
        self.__storage_path = storage_path

    async def create(self, company: Company) -> Company:
        companies = await read_data_from_json_as_list(self.__storage_path)
        company_model = company.model_dump()
        if company_model not in companies:
            await add_data_to_json(company_model, self.__storage_path)

        return company
    
    async def exist(self, company_name: str) -> bool:        
        companies = await read_data_from_json_as_list(self.__storage_path)
        companies = [Company.model_validate(company).name for company in companies]

        return True if company_name in companies else False

    async def handle_company(self, owner_id: int) -> Union[Company, None]:
        companies = await read_data_from_json_as_list(self.__storage_path)
        companies = [Company.model_validate(company) for company in companies]        
        company = [Company.model_validate(company) for company in companies if company.owner_id == owner_id]
        
        return company.pop() if len(companies) != 0 else None 

    async def add_employee(self, employee: Employee, company_name: str) -> Company:
        companies = await read_data_from_json_as_list(self.__storage_path)
        companies = [Company.model_validate(company) for company in companies]
        company = [company for company in companies if company.name == company_name].pop()
        company.employees.append(employee)

        other_company = [company for company in companies if company.name != company_name]
        
        companies = [company for company in other_company]
        companies.append(company)
        
        company_models = [Company.model_validate(company).model_dump() for company in companies]

        await clear_data(self.__storage_path)
        await write_data_to_json_as_list(company_models, self.__storage_path) 

        return company
    
    async def handle_employee(self, employee_name: str, company_name: str) -> Union[Employee, None]:
        companies = await read_data_from_json_as_list(self.__storage_path)
        companies = [Company.model_validate(company) for company in companies]
        employees = [company.employees for company in companies if company.name == company_name].pop()
        
        employees = [employee for employee in employees if employee.username == employee_name]
        
        if len(employees) == 0:
            return None

        return employees.pop()