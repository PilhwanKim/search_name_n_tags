import service


def test_get_companies_by_name():
    company_name = "코리아"
    language = "ko"
    companies = service.get_companies_by_name(company_name)
    for company in companies:
        for name in company.names:
            if name.language == language:
                assert company_name in name.name

    company_name = "co"
    language = "en"
    companies = service.get_companies_by_name(company_name)
    for company in companies:
        for name in company.names:
            if name.language == language:
                assert company_name in name.name.lower()


def test_get_companies_by_tags():
    tag_name = "태그_4"
    companies = service.get_companies_by_tags(tag_name)
    for company in companies:
        assert any([
            True if tag_name == tag.name
            else False
            for tag in company.tags
        ])

    tag_name = "tag_19"
    companies = service.get_companies_by_tags(tag_name)
    for company in companies:
        assert any([
            True if tag_name == tag.name
            else False
            for tag in company.tags
        ])

    tag_name = "タグ_22"
    companies = service.get_companies_by_tags(tag_name)
    for company in companies:
        assert any([
            True if tag_name == tag.name
            else False
            for tag in company.tags
        ])
