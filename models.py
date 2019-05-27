from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


company_tags_table = db.Table('company_tags', db.metadata,
                              db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
                              db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'))
                              )


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class CompanyName(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('name', lazy=True))
    language = db.Column(db.String(80))
    name = db.Column(db.String(120), nullable=True)
    isDefault = db.Column(db.Boolean, default=False)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    companies = db.relationship("Company", secondary=company_tags_table,
                                back_populates="tags", lazy=True)
