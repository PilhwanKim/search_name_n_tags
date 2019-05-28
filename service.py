import models


def get_companies_by_name(name, language="ko"):
    companies_query = models.get_companies_by_name(name, language)
    return convert_company_to_list(companies_query, language)


def get_companies_by_tags(tag_name, language="ko"):
    companies_query = models.get_companies_by_tags(tag_name, language)
    return convert_company_to_list(companies_query, language)


def convert_company_to_list(companies, language):
    to_companies = []
    for company in companies:
        to_companies.append({
            "id": company.id,
            "name": convert_name(company.names, language),
            "tags": convert_tags_to_list(company.tags, language)
        })
    return to_companies


def convert_name(names, language):
    for name in names:
        if name.language == language:
            return name.name

    if names:
        return names[0].name

    return None


def convert_tags_to_list(tags, language):
    to_tags = []
    for tag in tags:
        if tag.language == language:
            to_tags.append(tag.name)
    return to_tags
