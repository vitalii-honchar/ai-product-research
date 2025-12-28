from pydantic import BaseModel


class BusinessProblem(BaseModel):
    primary_customer: str
    core_job: str
    main_pain: str
    success_metric: str


class AnalyzedProduct(BaseModel):
    origin_url: str
    product_url: str
    name: str
    problem: BusinessProblem
