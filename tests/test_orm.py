import pytest
import models
from models import Company, CompanyName


def test_create_db():
    models.create_db()


def test_create_data():
    models.create_data()


def test_get_company_by_name():
    session = models.db.session()
    wanted = session.query(Company).join(Company.name).filter(CompanyName.name == "원티드").first()
    assert wanted.id
    assert wanted.name[0].name == "원티드"
    assert wanted.tags
