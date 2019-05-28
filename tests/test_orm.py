import pytest
import models
from models import Company, CompanyName, Tags


def test_create_db():
    models.create_db()


def test_create_data():
    models.create_db_data()


def test_setup_db():
    models.setup_db()


def test_get_company_by_name():
    company_name = "원티드랩"
    wanted = Company.query\
        .join(CompanyName, Company.names)\
        .filter(CompanyName.name.ilike("%" + company_name + "%"))\
        .first()
    assert wanted.id
    assert wanted.names[0].name == company_name
    assert wanted.tags
