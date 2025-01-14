from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from db.models import Gender, MaritalStatus

class EmployeeCreate(BaseModel):
    employee_code: str = Field(..., min_length=1, max_length=8)
    position_id: int = Field(...)
    department_id: int = Field(...)
    salary: float = Field(..., gt=0)
    gender: Gender = Field(default=Gender.MALE)
    contract_id: str = Field(..., min_length=1, max_length=8)
    full_name: str = Field(..., min_length=1, max_length=50)
    birth_date: date
    birth_place: str = Field(..., max_length=100)
    id_number: str = Field(..., max_length=20)
    phone: str = Field(..., max_length=15)
    address: str = Field(..., max_length=250)
    email: EmailStr
    marital_status: MaritalStatus = Field(default=MaritalStatus.SINGLE)
    ethnicity: Optional[str] = Field(default="Kinh")
    education_level_id: Optional[str] = Field(default=None)
    id_card_date: Optional[date] = Field(default=None)
    id_card_place: Optional[str] = Field(default=None, max_length=50)
    health_insurance_number: str = Field(..., max_length=15)
    social_insurance_number: str = Field(..., max_length=15)
    profile_image_path: str = Field(default="none_image_profile", max_length=40)

class EmployeeUpdateModel(BaseModel):
    EmployeeName: str = Field(..., min_length=1, max_length=50)
    DateOfBirth: date
    PlaceOfBirth: str = Field(..., max_length=100)
    IDNumber: str = Field(..., max_length=20)
    Phone: str = Field(..., max_length=20)
    Address: str = Field(..., max_length=250)
    Email: EmailStr
    MaritalStatus: str = Field(default="Single")
    Ethnicity: Optional[str] = Field(default="Kinh")
    EducationLevelID: Optional[str] = None
    IDCardDate: Optional[date] = None
    IDCardPlace: Optional[str] = None
    HealthInsurance: str = Field(..., max_length=15)
    SocialInsurance: str = Field(..., max_length=15)
    ID_profile_image: str = Field(default="none_image_profile") 