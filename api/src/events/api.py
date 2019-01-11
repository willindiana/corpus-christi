import json
from datetime import datetime

from flask import request
from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, jwt_optional
from marshmallow import ValidationError

from . import events
from .models import Event, Asset, Team, EventSchema, AssetSchema, TeamSchema
from .. import db

def modify_entity(entity_type, id, new_value_dict):
    item = db.session.query(entity_type).filter_by(id=id).first()

    if not item:
        return jsonify(f"Event with id #{id} does not exist."), 404

    for key, val in new_value_dict.items():
        setattr(item, key, val)
    
    db.session.commit()

    return jsonify(event_schema.dump(item)), 200

# ---- Event

event_schema = EventSchema()

@events.route('/', methods=['POST'])
@jwt_required
def create_event():
    try:
        valid_event = event_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    new_event = Event(**valid_event)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(event_schema.dump(new_event)), 201
    

@events.route('/')
@jwt_required
def read_all_events():

    query = db.session.query(Event)

    # -- return_inactives --
    # Filter events based on active status
    # True - see all events, False or missing - see only active events
    return_group = request.args.get('return_group')
    if return_group == 'inactive':
        query = query.filter_by(active=False)
    elif return_group in ('all', 'both'):
        pass # Don't filter
    else:
        query = query.filter_by(active=True)

    # -- start, end --
    # Filter events to be greater than the start date and/or earlier than the end date (inclusive)
    start_filter = request.args.get('start')
    end_filter = request.args.get('end')
    if start_filter:
        query = query.filter(Event.start >= datetime.strptime(start_filter, '%Y-%m-%d'))
    if end_filter:
        query = query.filter(Event.end <= datetime.strptime(end_filter, '%Y-%m-%d'))

    # -- title --
    # Filter events on a wildcard title string
    title_filter = request.args.get('title')
    if title_filter:
        query = query.filter(Event.title.like(f"%{title_filter}%"))

    # -- location --
    # Filter events on a wildcard location string?
    location_filter = request.args.get('location')
    if location_filter:
        # TODO FIXME
        pass

    result = query.all()

    return jsonify(event_schema.dump(result, many=True))
    

@events.route('/<event_id>')
@jwt_required
def read_one_event(event_id):
    event = db.session.query(Event).filter_by(id=event_id).first()

    if not event:
        return jsonify(f"Event with id #{event_id} does not exist."), 404

    return jsonify(event_schema.dump(event))
    

@events.route('/<event_id>', methods=['PUT'])
@jwt_required
def replace_event(event_id):
    try:
        valid_event = event_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    return modify_event(event_id, valid_event)


@events.route('/<event_id>', methods=['PATCH'])
@jwt_required
def update_event(event_id):
    try: 
        valid_attributes = event_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422
                
    return modify_event(event_id, valid_attributes)


@events.route('/<event_id>', methods=['DELETE'])
@jwt_required
def delete_event(event_id):
    event = db.session.query(Event).filter_by(id=event_id).first()

    if not event:
        return jsonify(f"Event with id #{event_id} does not exist."), 404
        
    setattr(event, 'active', False)
    db.session.commit()
    
    # 204 doesn't actually respond with any content
    return jsonify(event_schema.dump(event)), 204


# Handles PUT and PATCH requests
def modify_event(event_id, new_value_dict):
    return modify_entity(Event, event_id, new_value_dict)


# ---- Asset

asset_schema = AssetSchema()

@events.route('/assets', methods=['POST'])
@jwt_required
def create_asset():
    try:
        valid_asset = asset_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    new_asset = Asset(**valid_asset)
    db.session.add(new_asset)
    db.session.commit()
    return jsonify(asset_schema.dump(new_asset)), 201
    

@events.route('/assets')
@jwt_required
def read_all_assets():
    result = db.session.query(Asset).all()
    return jsonify(asset_schema.dump(result, many=True))
    

@events.route('/assets/<asset_id>')
@jwt_required
def read_one_asset(asset_id):
    result = db.session.query(Asset).filter_by(id=asset_id).first()
    return jsonify(asset_schema.dump(result))
    

@events.route('/assets/<asset_id>', methods=['PUT'])
@jwt_required
def replace_asset(asset_id):
    pass
    

@events.route('/assets/<asset_id>', methods=['PATCH'])
@jwt_required
def update_asset(asset_id):
    try:
        valid_asset = asset_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    asset = db.session.query(Asset).filter_by(id=asset_id).first()

    for key, val in valid_asset.items():
        setattr(asset, key, val)

    db.session.commit()
    return jsonify(asset_schema.dump(asset))
    

@events.route('/assets/<asset_id>', methods=['DELETE'])
@jwt_required
def delete_asset(asset_id):
    pass

# Handles PUT and PATCH requests
def modify_asset(asset_id, new_value_dict):
    return modify_entity(Asset, asset_id, new_value_dict)


# ---- Team

team_schema = TeamSchema()

@events.route('/teams', methods=['POST'])
@jwt_required
def create_team():
    try:
        valid_team = team_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    new_team = Team(**valid_team)
    db.session.add(new_team)
    db.session.commit()
    return jsonify(team_schema.dump(new_team)), 201
    

@events.route('/teams')
@jwt_required
def read_all_teams():
    result = db.session.query(Team).all()
    return jsonify(team_schema.dump(result, many=True))
    

@events.route('/teams/<team_id>')
@jwt_required
def read_one_team(team_id):
    result = db.session.query(Team).filter_by(id=team_id).first()
    return jsonify(team_schema.dump(result))
    

@events.route('/teams/<team_id>', methods=['PUT'])
@jwt_required
def replace_team(team_id):
    pass
    

@events.route('/teams/<team_id>', methods=['PATCH'])
@jwt_required
def update_team(team_id):
    try:
        valid_team = team_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    team = db.session.query(Team).filter_by(id=team_id).first()

    for key, val in valid_team.items():
        setattr(team, key, val)

    db.session.commit()
    return jsonify(team_schema.dump(team))
    

@events.route('/teams/<team_id>', methods=['DELETE'])
@jwt_required
def delete_team(team_id):
    pass