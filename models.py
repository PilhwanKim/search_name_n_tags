from pyexcel_xlsx import get_data

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


CompanyTags = db.Table('company_tags',
                       db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True),
                       db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
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
    company = db.relationship('Company', backref=db.backref('name', lazy=True))
    language = db.Column(db.String(80))
    name = db.Column(db.String(120), nullable=True)
    isDefault = db.Column(db.Boolean, default=False)


class Tags(db.Model):
    """
    회사 검색 테그(다국어)
    """
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    companies = db.relationship("Company", secondary=CompanyTags,
                                backref=db.backref('tags', lazy=True))


def create_db():
    db.create_all()


def create_db_data():
    _make_tags()
    _insert_data_from_excel_to_db()


def setup_db():
    create_db()
    create_db_data()


def _make_tags():
    for i in range(30):
        tag_id = i + 1
        db.session.add(Tags(id=tag_id, language="ko", name="태그_{}".format(tag_id)))
        db.session.add(Tags(id=tag_id, language="en", name="tag_{}".format(tag_id)))
        db.session.add(Tags(id=tag_id, language="ja", name="タグ_{}".format(tag_id)))
    db.session.commit()


def _insert_data_from_excel_to_db():
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
                tag = db.session.query(Tags) \
                    .filter(Tags.id == tag_id, Tags.language == "ko") \
                    .one()
                company.tags.append(tag)
        db.session.add(company)
    db.session.commit()

