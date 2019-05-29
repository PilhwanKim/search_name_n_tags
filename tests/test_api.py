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
            {'id': 29, 'name': '주식회사 링크드코리아', 'tags': ['태그_6', '태그_8', '태그_12']},
            {'id': 48, 'name': '오케이코인코리아', 'tags': ['태그_3', '태그_25']},
            {'id': 60, 'name': '지오코리아(페루관광청)', 'tags': ['태그_17', '태그_28']},
            {'id': 87, 'name': '더락포트컴퍼니코리아-중복', 'tags': ['태그_7']},
            {'id': 91, 'name': '보비어스코리아', 'tags': ['태그_3', '태그_4', '태그_8', '태그_11']}],
        'search': {
            'name': '코리아',
            'tag': ''
        }
    }


def test_get_companies_by_tag(client):
    result = client.get(url_for("get_companies", tag="태그_4"))
    assert result.status_code == 200
    assert result.headers.get('Content-Type') == 'application/json'
    assert result.json == {
        'companies': [
            {'id': 1, 'name': '원티드랩', 'tags': ['태그_4', '태그_16', '태그_20']},
            {'id': 2, 'name': 'OKAY.com', 'tags': ['태그_4', '태그_24', '태그_27']},
            {'id': 36, 'name': '젠틀파이', 'tags': ['태그_4', '태그_14', '태그_17', '태그_18']},
            {'id': 39, 'name': 'Rejoice Pregnancy', 'tags': ['태그_4', '태그_7', '태그_22', '태그_30']},
            {'id': 51, 'name': '투게더앱스', 'tags': ['태그_4', '태그_10', '태그_22', '태그_28']},
            {'id': 64, 'name': '아이엠에이치씨(IMHC)', 'tags': ['태그_4', '태그_19', '태그_28', '태그_30']},
            {'id': 91, 'name': '보비어스코리아', 'tags': ['태그_3', '태그_4', '태그_8', '태그_11']},
            {'id': 99, 'name': 'Machipopo Inc.', 'tags': ['태그_4', '태그_10', '태그_19', '태그_20']}],
        'search': {
            'name': '',
            'tag': '태그_4',
        }
    }


def test_add_tags(client):
    company_id = 1
    tag_id = 30
    result = client.post(url_for("attach_tag", company_id=company_id, tag_id=tag_id))
    assert result.status_code == 200
    assert result.headers.get('Content-Type') == 'application/json'
    assert result.json == {
            'company_id': company_id,
            'tag_id': tag_id
        }


def test_delete_tags(client):
    company_id = 1
    tag_id = 30
    result = client.delete(url_for("detach_tag", company_id=company_id, tag_id=tag_id))
    assert result.status_code == 200
    assert result.headers.get('Content-Type') == 'application/json'
    assert result.json == {
            'company_id': company_id,
            'tag_id': tag_id
        }
