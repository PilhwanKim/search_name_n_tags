import pytest
import models
from models import Company, CompanyName, Tags
import pyexcel
from pyexcel_xlsx import get_data


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


def test_insert_data_from_excel_to_db():
    for i in range(30):
        tag_id = i + 1
        models.db.session.add(Tags(id=tag_id, language="ko", name="태그_{}".format(tag_id)))
        models.db.session.add(Tags(id=tag_id, language="en", name="tag_{}".format(tag_id)))
        models.db.session.add(Tags(id=tag_id, language="ja", name="タグ_{}".format(tag_id)))
    models.db.session.commit()

    xls_data = get_data("wanted_temp_data.xlsx")
    sheet = xls_data['시트 1 - company_tag_sample']
    for record in sheet[2:]:
        company = Company()
        if record[0]:
            company.name.append(CompanyName(language="ko", name=record[0], isDefault=True))
        if record[1]:
            company.name.append(CompanyName(language="en", name=record[1], isDefault=True))
        if record[2]:
            company.name.append(CompanyName(language="ja", name=record[2], isDefault=True))

        if record[3]:
            for tag_name in record[3].split("|"):
                tag_id = tag_name.split("_")[1]
                # company.tags.append(Tags(id=tag_id, language="ko", name=tag_name).get(id=tag_id, language="ko"))
                tag = models.db.session.query(Tags) \
                    .filter(Tags.id == tag_id, Tags.language == "ko") \
                    .one()
                company.tags.append(tag)
        if record[4]:
            for tag_name in record[4].split("|"):
                tag_id = tag_name.split("_")[1]
                # company.tags.append(Tags(id=tag_id, language="en", name=tag_name))
                tag = models.db.session.query(Tags) \
                    .filter(Tags.id == tag_id, Tags.language == "en") \
                    .one()
                company.tags.append(tag)
        if record[5]:
            for tag_name in record[5].split("|"):
                tag_id = tag_name.split("_")[1]
                tag = models.db.session.query(Tags)\
                    .filter(Tags.id == tag_id, Tags.language == 'ja')\
                    .one()
                # company.tags.append(Tags(id=tag_id, language="ja", name=tag_name))
                company.tags.append(tag)
        models.db.session.add(company)
        models.db.session.commit()
