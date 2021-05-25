import json
from flask import request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)
from sqlalchemy import exc
from app import app, db
from models import User, Advertisement


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return {'message': 'Missing or invalid JSON request'}
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return {"message": "Missing payload"}
    user = User.query.filter(User.username == username,
                             User.password == password).first()
    if not user:
        return {"message": "Invalid credentials"}, 403
    user_data = json.dumps({
        "id": user.id,
        "username": user.username,
    })
    access_token = create_access_token(
        identity=user_data
    )
    return {
        'username': user.username,
        'access_token': access_token
    }


@app.route('/ads/list')
def get_ads():
    ads = Advertisement.query.all()
    ads_list = []
    for ad in ads:
        ads_list.append({
            'id': ad.id,
            'title': ad.title,
            'category': ad.category.value,
            'description': ad.description,
            'ad_owner_id': ad.user.id,
            'ad_owner': ad.user.username
        })
    return {'ads_list': ads_list}


@app.route('/ads/create', methods=['POST'])
@jwt_required()
def create_ad():
    if not request.is_json:
        return {'message': 'Missing or invalid JSON request'}
    try:
        request_dict = request.get_json()
        new_ad = Advertisement(
            title=request_dict["title"],
            category=request_dict["category"],
            description=request_dict["description"],
            owner_username=request_dict["owner_username"]
        )
        db.session.add(new_ad)
        db.session.commit()
    except KeyError as err:
        app.logger.error(err)
        return {'message': 'Invalid payload keys'}, 400
    except exc.DataError as err:
        app.logger.error(err)
        return {'message': 'Invalid category'}, 400
    except exc.IntegrityError as err:
        app.logger.error(err)
        return {'message': 'Invalid user'}, 400
    return {
        'new_ad': {
            'id': new_ad.id,
            'title': new_ad.title,
            'category': new_ad.category.value,
            'description': new_ad.description,
            'ad_owner_id': new_ad.user.id,
            'ad_owner': new_ad.user.username
            }
        }


@app.route('/ads/<ad_id>/update', methods=['PATCH'])
@jwt_required()
def update_ad(ad_id):
    current_user = json.loads(get_jwt_identity())
    ad_obj = Advertisement.query.filter(
        Advertisement.id == ad_id
    ).first()
    if ad_obj.owner_username != current_user["username"]:
        return {"message": "Forbidden"}, 403
    request_dict = request.get_json()
    try:
        ad_obj.update(**request_dict)
        db.session.add(ad_obj)
        db.session.commit()
    except Exception as err:
        app.logger.error(err)
        return {'message': 'Invalid payload'}
    return {'message': f"Successfully updated ad {ad_obj.title}"}


@app.route('/ads/<ad_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_ad(ad_id):
    current_user = json.loads(get_jwt_identity())
    ad_obj = Advertisement.query.filter(
        Advertisement.id == ad_id
    ).first()
    if ad_obj.owner_username != current_user["username"]:
        return {"message": "Forbidden"}, 403
    db.session.delete(ad_obj)
    db.session.commit()
    return {'deleted_ad': int(ad_id)}
