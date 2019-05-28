from models import db, Company, CompanyName, Tags


def get_companies_by_name(name):
    companies = Company.query.join(CompanyName, Company.names).filter(CompanyName.name.ilike("%" + name + "%"))
    return companies


def get_companies_by_tags(tag_name):
    companies = Company.query.join(Tags, Company.tags).filter(Tags.name == tag_name)
    return companies
