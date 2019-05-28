import pytest
import models


def test_create_db(app):
    models.create_db()


def test_create_data(app):
    models.create_db_data()


def test_setup_db(app):
    models.setup_db()


def test_get_companies_by_name(app):
    company_name = "코리아"
    language = "ko"
    companies = models.get_companies_by_name(company_name, language)
    for company in companies:
        for name in company.names:
            if name.language == language:
                assert company_name in name.name

    company_name = "co"
    language = "en"
    companies = models.get_companies_by_name(company_name, language)
    for company in companies:
        for name in company.names:
            if name.language == language:
                assert company_name in name.name.lower()


def test_get_companies_by_tags(app):
    tag_name = "태그_4"
    language = "ko"
    companies = models.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            True if tag_name == tag.name
            else False
            for tag in company.tags
        ])

    tag_name = "tag_19"
    language = "en"
    companies = models.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            True if tag_name == tag.name
            else False
            for tag in company.tags
        ])

    tag_name = "タグ_22"
    language = "ja"
    companies = models.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            True if tag_name == tag.name
            else False
            for tag in company.tags
        ])


def test_attach_tag(app):
    company_id = 1
    tag_id = 22
    models.attach_tag(company_id, tag_id)

    tag_name = "タグ_22"
    language = "ja"
    companies = models.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            True if tag_name == tag.name
            else False
            for tag in company.tags
        ])


def test_detach_tag(app):
    company_id = 1
    tag_id = 22
    models.detach_tag(company_id, tag_id)

    tag_name = "タグ_22"
    language = "ja"
    companies = models.get_companies_by_tags(tag_name, language)
    for company in companies:
        assert any([
            False if tag_name == tag.name
            else True
            for tag in company.tags
        ])
