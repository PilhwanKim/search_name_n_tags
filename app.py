from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
import service


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def main():
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

        if company_name:
            companies = service.get_companies_by_name(company_name)
        else:
            companies = service.get_companies_by_tags(company_tag)

        response_data = {
            'search': {
                'name': company_name,
                'tag': company_tag,
            },
            'companies': companies,
        }
        return jsonify(response_data)

    @app.route('/companies/<int:company_id>/tags/<int:tag_id>', methods=['POST'])
    def attach_tag(company_id, tag_id):
        service.attach_tag(company_id, tag_id)
        return jsonify({
            'company_id': company_id,
            'tag_id': tag_id
        })

    @app.route('/companies/<int:company_id>/tags/<int:tag_id>', methods=['DELETE'])
    def detach_tag(company_id, tag_id):
        service.detach_tag(company_id, tag_id)
        return jsonify({
            'company_id': company_id,
            'tag_id': tag_id
        })

    @app.errorhandler(404)
    def page_not_found(error):
        return 'This page does not exist', 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
