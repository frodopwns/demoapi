import json
import requests
from eve import Eve
import flask
from settings import eve_settings
from pprint import pprint

app = Eve(settings=eve_settings)


def post_POST_event_callback(request, response):
    """
    After POST create site if it does not exist. Update site with increments
    based on event paylod.
    """
    try:
        response_data = json.loads(response.get_data())
    except ValueError:
        response_data = {}

    # allow bulk inserts
    if not isinstance(response_data, list):
        if '_items' in response_data:
            response_data = response_data['_items']
        else:
            response_data = [response_data]

    # loop through individual events posted
    for event in response_data:
        if 'site_id' not in event:
            print event
            continue

        updates = {
            'active': 0,
            'messages': 0,
            'emails': 0,
            'operators': 0,
            'visitors': 0
        }

        sid = event['site_id']
        sites = app.data.driver.db['sites']
        site = sites.find_one({'site_id': sid})
        if not site:
            site = updates.copy()
            site['site_id'] = sid
            rep = sites.insert_one(site)

        if event['type'] == 'status':
            print 'status message received'
            if event['data_status'] == 'online':
                updates['active'] += 1
            else:
                updates['active'] -= 1
        else:
            print 'chat message received'
            if site['active']:
                updates['messages'] += 1
            else:
                updates['emails'] += 1

        sites.update_one({'site_id': sid}, {'$inc': updates})


@app.route('/stats.json')
def get_stats():
    """
    Query events and sites calculating distinct operators and visitors then return them as json list.
    """
    out = []
    events = app.data.driver.db['events']
    sites = app.data.driver.db['sites']
    all_sites = sites.find()
    for site in all_sites:
        users = events.distinct('from', {'site_id': site['site_id']})
        for user in users:
            if user.startswith('visitor'):
                site['visitors'] += 1
            else:
                site['operators'] += 1
        del site['_id']
        out.append(site)


    resp = flask.Response(json.dumps(out, indent=2))
    resp.headers['Content-Type'] = 'application/json'
    return resp

# enable post POST hook
app.on_post_POST_events += post_POST_event_callback

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
