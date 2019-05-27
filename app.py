from flask import Flask
from flask import request, jsonify, abort

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello! This is search names and tags Project!'


@app.route('/companies', methods=['GET'])
def get_companies():
    company_name = request.args.get('name', '')
    company_tag = request.args.get('tag', '')

    # 파라메터 유무 체크
    if not company_tag and not company_name:
        return "name or tag parameter is empty.", 400

    # 파라메터 길이 체크 1
    if company_name and len(company_name) > 255:
        return "name parameter is too long.", 400
    if company_tag and len(company_tag) > 255:
        return "tag parameter value is too long.", 400

    companies = [
        {
            "id": 2,
            "name": "이상한마케팅",
            "tags": ["태그_25", "태그_6", "태그_14", "태그_9"]
        }
    ]
    response_data = {
        'name': company_name,
        'tag': company_tag,
        'companies': companies,
    }
    return jsonify(response_data)


@app.route('/companies/<int:company_id>/tags/<tag_name>', methods=['POST'])
def add_tags(company_id, tag_name):
    return jsonify({
        'company_id': company_id,
        'tag_name': tag_name
    })


@app.route('/companies/<int:company_id>/tags/<tag_name>', methods=['DELETE'])
def delete_tags(company_id, tag_name):
    return jsonify({
        'company_id': company_id,
        'tag_name': tag_name
    })


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


if __name__ == '__main__':
    app.run()
