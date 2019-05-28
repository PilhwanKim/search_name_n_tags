from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from pyexcel_xlsx import get_data

db = SQLAlchemy()

CompanyTags = db.Table('company_tags',
                       db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True),
                       db.Column('tags_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
                       )


class Company(db.Model):
    """
    다국어 영향 받지 않는 회사 정보
    """
    id = db.Column(db.Integer, db.Sequence('company_id_seq'), primary_key=True)


class CompanyName(db.Model):
    """
    회사 이름(다국어)
    """
    id = db.Column(db.Integer, db.Sequence('company_name_id_seq'), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('names', lazy=True))
    language = db.Column(db.String(80))
    name = db.Column(db.String(120), nullable=True)
    isDefault = db.Column(db.Boolean, default=False)


class Tags(db.Model):
    """
    회사 검색 테그(다국어)
    """
    id = db.Column(db.Integer, db.Sequence('company_name_id_seq'), primary_key=True)
    tag_id = db.Column(db.Integer)
    language = db.Column(db.String(80))
    name = db.Column(db.String(120), nullable=True)
    companies = db.relationship("Company", secondary=CompanyTags,
                                backref=db.backref('tags', lazy=True))
    UniqueConstraint(tag_id, language)


def create_db():
    db.create_all()


def create_db_data():
    # _make_tags()
    _insert_data_from_excel_to_db()


def setup_db():
    create_db()
    create_db_data()


def _make_tags():
    for i in range(30):
        tag_id = i + 1
        db.session.add(Tags(tag_id=tag_id, language="ko", name="태그_{}".format(tag_id)))
        db.session.add(Tags(tag_id=tag_id, language="en", name="tag_{}".format(tag_id)))
        db.session.add(Tags(tag_id=tag_id, language="ja", name="タグ_{}".format(tag_id)))
    db.session.commit()


def _insert_data_from_excel_to_db():
    xls_data = get_data("wanted_temp_data.xlsx")
    sheet = xls_data['시트 1 - company_tag_sample']
    for record in sheet[2:]:
        company = Company()
        if record[0]:
            company.names.append(CompanyName(language="ko", name=record[0], isDefault=True))
        if record[1]:
            company.names.append(CompanyName(language="en", name=record[1], isDefault=True))
        if record[2]:
            company.names.append(CompanyName(language="ja", name=record[2], isDefault=True))
        if record[3]:
            for tag_name in record[3].split("|"):
                tag_id = tag_name.split("_")[1]
                tag = db.session.query(Tags) \
                    .filter(Tags.tag_id == tag_id, Tags.language == "ko") \
                    .one()
                company.tags.append(tag)
        db.session.add(company)
    db.session.commit()


def get_companies_by_name(name, language="ko"):
    return Company.query\
        .join(CompanyName, Company.names)\
        .filter(CompanyName.name.ilike("%" + name + "%"), CompanyName.language == language)


def get_companies_by_tags(tag_name, language="ko"):
    return Company.query\
        .join(Tags, Company.tags)\
        .filter(Tags.language == language, Tags.name == tag_name)


def attach_tag(company_id, tag_id):
    company = db.session.query(Company).get(company_id)
    target_tag = db.session.query(Tags).filter(Tags.tag_id == tag_id).first()
    if target_tag:
        company.tags.append(target_tag)
        db.session.commit()


def detach_tag(company_id, tag_id):
    company = db.session.query(Company).get(company_id)
    target_tag = None
    for tag in company.tags:
        if tag.tag_id == tag_id:
            target_tag = tag
    if target_tag:
        company.tags.remove(target_tag)
        db.session.commit()
