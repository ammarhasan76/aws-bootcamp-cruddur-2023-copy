from datetime import datetime, timedelta, timezone
# Import the X-Ray SDK
from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

class UserActivities:
  def run(user_handle):
    # X-Ray ---
    # Start a segment
    
    parent_subsegment = xray_recorder.begin_subsegment('user-activities')
    parent_subsegment.put_annotation('notes','this is an annotation!!')
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    parent_xray_dict = {
      "now": now.isoformat()
    }
    
    parent_subsegment.put_metadata('key', parent_xray_dict, 'user_activities')

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      now = datetime.now()
      results = [{
        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
        'handle':  'Andrew Brown',
        'message': 'Cloud is fun!',
        'created_at': (now - timedelta(days=1)).isoformat(),
        'expires_at': (now + timedelta(days=31)).isoformat()
      }]
      model['data'] = results
  
    # X-Ray ---
    subsegment = xray_recorder.begin_subsegment('user-activities_subsegment')

    dict = {
      "now": now.isoformat(),
      "results-size": len(model['data'])
    }

    subsegment.put_metadata('results', dict, 'user_activities_subsegment')

    subsegment.put_annotation('notes','this is another annotation!!')

    xray_recorder.end_subsegment()

    xray_recorder.end_subsegment()
    return model