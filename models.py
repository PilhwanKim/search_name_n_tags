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


def create_data():
    en_tags = []
    ko_tags = []
    jp_tags = []
    for i in range(30):
        tag_id = i + 1
        ko_tags.append(Tags(id=tag_id, language="ko", name="태그_{}".format(tag_id)))
        en_tags.append(Tags(id=tag_id, language="en", name="tag_{}".format(tag_id)))
        jp_tags.append(Tags(id=tag_id, language="jp", name="タグ_{}".format(tag_id)))

    company = Company()
    company_name = CompanyName(language="ko", name="원티드", isDefault=True)
    company.name.append(company_name)
    db.session.add(company)
    db.session.commit()

