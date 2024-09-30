from flask import Blueprint, request, jsonify, render_template
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    action = ""
    from_branch = None
    if data.get('action') == 'closed' and data.get('pull_request', {}).get('merged'):
        action = "MERGE"
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
    elif 'pusher' in data:
        action = 'PUSH'
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        
    elif 'pull_request' in data:
        action = 'PULL_REQUEST'
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']

    timestamp = datetime.now().strftime('%d %B %Y - %I:%M %p')
    event = {
        'action': action,
        'author': author,
        'from_branch': from_branch,
        'to_branch': to_branch,
        'timestamp': timestamp
    }
    
    mongo.db.events.insert_one(event) 
    
    return jsonify({'status': 'event received'}), 201

@webhook.route('/latest_events', methods=['GET'])
def get_latest_events():
    try:
        events = mongo.db.events.find().sort([('_id', -1)]).limit(10)
        event_list = []
        for event in events:
            event_type = event.get('action')
            author = event.get('author')
            to_branch = event.get('to_branch')
            from_branch = event.get('from_branch', '')
            timestamp = event.get('timestamp', 'Unknown time')

            if event_type == 'PUSH':
                formatted_event = f'"{author}" pushed to "{to_branch}" on {timestamp}'
            elif event_type == 'PULL_REQUEST':
                formatted_event = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
            elif event_type == 'MERGE':
                formatted_event = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
            else:
                formatted_event = f'Unknown event by {author} on {timestamp}'
            print(formatted_event)

            event_list.append(formatted_event)
        return jsonify(event_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

