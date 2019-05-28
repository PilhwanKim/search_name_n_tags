import pytest
import service


def test_get_companies_by_name(app):
    company_name = "코리아"
    language = "ko"
    companies = service.get_companies_by_name(company_name, language)
    for company in companies:
        assert company_name.lower() in company.get('name').lower()

    company_name = "co"
    language = "en"
    companies = service.get_companies_by_name(company_name, language)
    for company in companies:
        assert company_name.lower() in company.get('name').lower()


def test_get_companies_by_tags(app):
    tag_name = "태그_4"
    language = "ko"
    companies = service.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            True if tag_name == tag
            else False
            for tag in company.get('tags')
        ])

    tag_name = "tag_19"
    language = "en"
    companies = service.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            True if tag_name == tag
            else False
            for tag in company.get('tags')
        ])

    tag_name = "タグ_22"
    language = "ja"
    companies = service.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            True if tag_name == tag
            else False
            for tag in company.get('tags')
        ])
