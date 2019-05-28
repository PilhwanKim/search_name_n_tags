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
    session = models.db.session()
    wanted = session.query(Company).join(Company.name).filter(CompanyName.name == "원티드랩").first()
    assert wanted.id
    assert wanted.name[0].name == "원티드랩"
    assert wanted.tags
