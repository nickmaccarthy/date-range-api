from flask import Flask, jsonify, request, abort
import datetime
from datemath import datemath
from pprint import pprint

app = Flask(__name__)

'''
Determine if two date ranges overlap by comparing, you can evauluate the date's this way when they
in the "datetime" type/object
'''
def date_range_overlap(start1, end1, start2, end2):
    overlaps = start1 <= end2 and end1 >= start2
    if not overlaps:
        return False
    return True


@app.route("/", methods=['GET'])
def index():

    # Define the structure for our JSON response we will return
    json_response = {
        'range1': {
            'start': '',
            'end': ''
        },
        'range2': {
            'start': '',
            'end': ''
        },
        'ranges_overlap': False 
    }

    # For the sake of this exercise, only work with GET methods/requests
    # We will will ask our users to specify their ranges via: ?range1=<start>,<end>&range2=<start>,<end>
    if request.method == 'GET':
        r1 = request.args.get('range1')
        r2 = request.args.get('range2')

        assert r1 and r2, abort(400,description='please specify date ranges in the formart: ?range1=<start>,<end>&range2=<start>,<end>')
        
        r1parts = r1.split(',')
        r2parts = r2.split(',')

        assert len(r1parts) == 2, abort(400, description=f'too many ranges for range start, expected 2, got {len(r1parts)}')
        assert len(r2parts) == 2, abort(400, description=f'too many ranges for range end, expected 2, got {len(r1parts)}')

        # Covert our date ranges into the datetime format using my python-datemath module
        # This module should handle most standard date and time formats
        try:
            r1start = datemath(r1parts[0])
            r1end = datemath(r1parts[1])
            r2start = datemath(r2parts[0])
            r2end = datemath(r2parts[1])
        except Exception as e:
            abort(400,f'Unable to determine date format, reason: {e}')

        json_response['range1']['start'] = r1parts[0]
        json_response['range1']['end'] = r1parts[1]
        json_response['range2']['start'] = r2parts[0]
        json_response['range2']['end'] = r2parts[0]

        # Determine if our date ranges over lap and set the proper element in our json return response
        if date_range_overlap(r1start,r1end,r2start,r2end):
            json_response['ranges_overlap'] = True 

        return jsonify(json_response)
    
    else:
        abort(405, description='only GET method allowd with specified format: ?range1=<start>,<end>&range2=<start>,<end>')
