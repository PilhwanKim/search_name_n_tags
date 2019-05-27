from flask import Flask
from flask import request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello! This is search names and tags Project!'


@app.route('/companies', methods=['GET'])
def get_companies():
    company_name = request.args.get('name', '')
    company_tag = request.args.get('tag', '')
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
    # return '{} {}'.format(company_id, tag_name)
    return jsonify({
        'company_id': company_id,
        'tag_name': tag_name
    })


@app.route('/companies/<int:company_id>/tags/<tag_name>', methods=['DELETE'])
def delete_tags(company_id, tag_name):
    # return '{} {}'.format(company_id, tag_name)
    return jsonify({
        'company_id': company_id,
        'tag_name': tag_name
    })


if __name__ == '__main__':
    app.run()
