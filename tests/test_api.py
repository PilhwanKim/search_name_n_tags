import pytest
from flask import url_for


def test_main_url(client):
    result = client.get(url_for("main"))
    assert result.status_code == 200
    assert result.data == b"Hello! This is search names and tags Project!"


def test_get_companies_by_name(client):
    result = client.get(url_for("get_companies", name="코리아"))
    assert result.status_code == 200
    assert result.headers.get('Content-Type') == 'application/json'
    assert result.json == {
        'companies': [
            {'id': 2, 'name': '이상한마케팅', 'tags': ['태그_25', '태그_6', '태그_14', '태그_9']}
        ],
        'search': {
            'name': '코리아',
            'tag': '',
        }
    }


def test_get_companies_by_tag(client):
    result = client.get(url_for("get_companies", tag="태그_4"))
    assert result.status_code == 200
    assert result.headers.get('Content-Type') == 'application/json'
    assert result.json == {
        'companies': [
            {'id': 2, 'name': '이상한마케팅', 'tags': ['태그_25', '태그_6', '태그_14', '태그_9']}
        ],
        'search': {
            'name': '',
            'tag': '태그_4',
        }
    }


def test_add_tags(client):
    company_id = 1
    tag_name = "태그_4"
    result = client.post(url_for("attach_tag", company_id=company_id, tag_name=tag_name))
    assert result.status_code == 200
    assert result.headers.get('Content-Type') == 'application/json'
    assert result.json == {
            'company_id': company_id,
            'tag_name': tag_name
        }


def test_delete_tags(client):
    company_id = 1
    tag_name = "태그_4"
    result = client.delete(url_for("detach_tag", company_id=company_id, tag_name=tag_name))
    assert result.status_code == 200
    assert result.headers.get('Content-Type') == 'application/json'
    assert result.json == {
            'company_id': company_id,
            'tag_name': tag_name
        }
