import uuid
from datetime import date, datetime
from typing import Optional, List
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import Field, Relationship, SQLModel, Column
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: str = Field(
        sa_column=Column(mysql.VARCHAR(36), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    )

    username: str
    password_hash: str = Field(
        sa_column=Column(mysql.VARCHAR(255), nullable=False),
        exclude=True
    )
    role: UserRole = Field(default=UserRole.USER)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(mysql.TIMESTAMP, default=datetime.now())   
    )
    updated_at: datetime = Field(
        sa_column=Column(mysql.TIMESTAMP, default=datetime.now(), onupdate=datetime.now())
    )

    def __repr__(self):
        return f"<User {self.username}>"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class MaritalStatus(str, Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    
    id: int = Field(default=None, primary_key=True)
    department_code: str = Field(
        sa_column=Column(mysql.VARCHAR(8), unique=True, index=True)
    )
    name: str = Field(sa_column=Column(mysql.VARCHAR(50)))
    
    # Relationships
    employees: List["Employee"] = Relationship(back_populates="department")

class Position(SQLModel, table=True):
    __tablename__ = "positions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    position_code: str = Field(..., max_length=10)
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None)
    
    # Relationships
    employees: List["Employee"] = Relationship(back_populates="position")

class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    
    id: int = Field(default=None, primary_key=True)
    employee_code: str = Field(
        sa_column=Column(mysql.VARCHAR(8), unique=True, index=True)
    )
    position_id: int = Field(foreign_key="positions.id")
    department_id: int = Field(foreign_key="departments.id")
    salary: float = Field(sa_column=Column(mysql.DECIMAL(12,2)))
    gender: Gender = Field(default=Gender.MALE)
    contract_id: str = Field(sa_column=Column(mysql.VARCHAR(8)))
    full_name: str = Field(sa_column=Column(mysql.VARCHAR(50)))
    birth_date: date
    birth_place: str = Field(sa_column=Column(mysql.VARCHAR(100)))
    id_number: str = Field(sa_column=Column(mysql.VARCHAR(20)))
    phone: str = Field(sa_column=Column(mysql.VARCHAR(15)))
    address: str = Field(sa_column=Column(mysql.VARCHAR(250)))
    email: str = Field(sa_column=Column(mysql.VARCHAR(50)))
    marital_status: MaritalStatus = Field(default=MaritalStatus.SINGLE)
    ethnicity: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(10), default="Kinh")
    )
    education_level_id: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(8), nullable=True)
    )
    id_card_date: Optional[date] = Field(default=None)
    id_card_place: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(50), nullable=True)
    )
    health_insurance_number: str = Field(sa_column=Column(mysql.VARCHAR(15)))
    social_insurance_number: str = Field(sa_column=Column(mysql.VARCHAR(15)))
    profile_image_path: str = Field(
        sa_column=Column(mysql.VARCHAR(40), default="none_image_profile")
    )

    # Relationships
    position: Position = Relationship(back_populates="employees")
    department: Department = Relationship(back_populates="employees")
    contracts: List["Contract"] = Relationship(back_populates="employee")
    payrolls: List["Payroll"] = Relationship(back_populates="employee")
    work_points: List["WorkPoint"] = Relationship(back_populates="employee")
    attendance: List["Attendance"] = Relationship(back_populates="employee")

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<Employee {self.full_name}>"

class Education(SQLModel, table=True):
    __tablename__ = "education"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employees.id")
    degree_name: str
    school: str
    major: str
    graduation_year: str
    ranking: str

class Contract(SQLModel, table=True):
    __tablename__ = "contracts"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employees.id")
    contract_type: str = Field(max_length=50)
    start_date: date
    end_date: Optional[date] = None
    status: str = Field(max_length=20)
    salary: float
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(
        sa_column=Column(mysql.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)
    )

    employee: Optional[Employee] = Relationship(back_populates="contracts")

class Payroll(SQLModel, table=True):
    __tablename__ = "payrolls"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employees.id", index=True)
    month: date
    base_salary: float
    allowance: float = Field(default=0)
    deduction: float = Field(default=0)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(mysql.TIMESTAMP, default=datetime.utcnow)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(mysql.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)
    )

    employee: Optional[Employee] = Relationship(back_populates="payrolls")

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<Payroll {self.employee_id} {self.month}>"

    @property
    def net_salary(self) -> float:
        """Calculate net salary"""
        return self.base_salary + self.allowance - self.deduction

class WorkPoint(SQLModel, table=True):
    __tablename__ = "work_points"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employees.id", index=True)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(...)
    day: int = Field(..., ge=1, le=31)
    points: float = Field(default=1.0)  # Default full day
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(mysql.TIMESTAMP, default=datetime.utcnow)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(mysql.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)
    )

    employee: Optional[Employee] = Relationship(back_populates="work_points")

class Attendance(SQLModel, table=True):
    __tablename__ = "attendance"

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employees.id", index=True)
    date: date
    status: str = Field(max_length=20)  # present, absent, late
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(mysql.TIMESTAMP, default=datetime.utcnow)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(mysql.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)
    )

    employee: Optional["Employee"] = Relationship(back_populates="attendance")