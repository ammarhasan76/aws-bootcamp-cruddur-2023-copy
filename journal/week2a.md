# Week 2 — Distributed Tracing

04/03/2023  
Watched Week 2 Live-Stream Video (Distributed Tracing)  
https://www.youtube.com/watch?v=2GD9xCzRId4&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=30  
Study Notes:

## Introdcution

*"For code there is a debugger, for everything else there is observability"*

Old world: logging   
New world: distributed tracing (example frontend + backend)

![image](https://user-images.githubusercontent.com/22940535/222910581-400fc3bb-fb6f-4bd1-bde6-de84dd1cd5b0.png)

![image](https://user-images.githubusercontent.com/22940535/222910922-69964c0d-d3e0-462a-b435-bac00cfb8d37.png)

A span = a single unit of work in a request/trace

Can spot error/failures and/or which part of a request is slow

Instrumentation = code/software/service that performs the tracing/observability

## Instrument for HoneyComb

### Setup API Key environement variable in GitPod Workspace

*note: OTEL = opentelemetry"

Action:
In UI, create a new 'bootcamp' env

*note: standard env vars naming for the API key is: honeycomb_api_key*  
`export HONEYCOMB_API_KEY="<removed>"`

*note: export means that env var is available in all the shells for that host

*note gp env is to add something to the gitpod.yml file so it doesn't need to keep getting defined every time you start a new Workspace*  
`gp env HONEYCOMB_API_KEY="<removed>"`

*note: gp env stores the variable in Variables in https://gitpod.io/user/variables*

### Add refences to environment variables in application code in docker compose

Action: (add OTEL_SERVICE_NAME to docker compose yml, you need a different service name for each service in your solution, so far we are adding to the backend-flask container)  
`OTEL_SERVICE_NAME: "backend-flask"`  
`OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"`  
`OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"`

### Setup configuration to send data to 'bootcamp' environment in Honeycomb

#### Install Packages

Action: (install python packages required to instrument and export telemetry to honeycomb to requirements.txt in ./backend-flask)
```
opentelemetry-api 
opentelemetry-sdk 
opentelemetry-exporter-otlp-proto-http 
opentelemetry-instrumentation-flask 
opentelemetry-instrumentation-requests
```

Action: (install python dependencies)  
`cd ./backend-flask`  
`pip install -r requirements.txt`

#### Initialise Packages
Action: (added packages to app.py and initialised objects and span processor)  

``` 
# Honeycomb - OTEL
# Packages
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
```

```
# Honeycomb - OTEL
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)  
```

```
# Honeycomb - Generating spans local to the backend-flask container (stdout)
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)  

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
```

```
# Honeycomb - OTEL
# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```

## Update home_activities.py to get spans instrumented
```
from datetime import datetime, timedelta, timezone
from opentelemetry import trace

#instantiate a tracer, the tracer provider was already instatiated in app.py
tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(logger):
    logger.info('Hello Cloudwatch! from home_activities /api/activities/home')
    with tracer.start_as_current_span("home-activities-mock-data"):
      # span make sure span context is the correcnt span
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())
      span.set_attribute("app.test", "hello world")  
...      
<snip>
    #with tracer.start_as_current_span("home-activities-mock-data"): if I uncomment this then it attributes make it into honeycomb but as another span, not within first span
    span = trace.get_current_span()
    span.set_attribute("app.result_length", len(results))
    span.set_attribute("app.tag", 'taggingtest')
    span.set_attribute("app.test2", 'goodbye world')
    return results
```

*note: reference: (https://docs.honeycomb.io/getting-data-in/opentelemetry/python/)*

Action: (npm install)  
(Did a rerun `npm i` inside the `frontend-react-js` because everything will be replaced at this point due to the `docker-compose` volume configuration to point to local dev container ie its not available in the dev env so the frontend-react-js container cant see npm files)

```
cd ../frontend-react-js/
npm i
```

Note: added npm i to gitpod.yml so I no longer have to do the above every time I create a new GitPod Workspace

*Note to self to look into: From livestream chatIuliana Silvasan: I've added 'npm install' via ENTRYPOINT script*

Action:
*ran docker compose up*  
*checked honeycomb for data successfully*

Evidence:
![image](https://user-images.githubusercontent.com/22940535/226122047-bf050921-8aff-4979-af10-e41e6a1e8b50.png)

![image](https://user-images.githubusercontent.com/22940535/226122232-d615a58e-0f09-4070-b3ff-d00d286b853c.png)

![image](https://user-images.githubusercontent.com/22940535/226122326-43e17156-8c7c-4b5c-a11d-ee42b04db37d.png)


Research Notes / Need to investigate further:
```
Tracer provider already instatiated in app.py

Now, we are just creating a tracer in order to create/send a span

Seems we did not need to create the tracer in app.py???
https://docs.honeycomb.io/getting-data-in/opentelemetry/python/
Could have created a new file eg tracing.py (how would this get called?)
This file would do the same as the tracer provider code added to app.py which is the entry point
https://opentelemetry-python.readthedocs.io/en/latest/api/trace.span.html  
https://docs.honeycomb.io/getting-data-in/opentelemetry/python/

#TODO: add custom attribute

*Note: Why couldn't I get this working?*
'''
span.set_attribute("app.result_length", len(results))  
span.set_attribute("app.tag", "taggingtest")
```

*Note: DataDog can also accept OTEL *

*Note: what are Git Tags (?)  


07/MAR/2023  
Watch Chirag Week 2 - Spending Considerations (Honeycomb, Rollbar, AWS X-Ray and AWS Cloudwatch Logs pricing considerations)  
https://www.youtube.com/watch?v=2W3KeqCjtDY   
Study Notes:  

Important for debugging etc

Honeycomb Pricing (tracing)
                Free tier - 20M events monthly

Rollbar (logging)
                Free tier - 5K events monthly (so better to restrict to errors)

AWS X-Ray
                Free tier
                                - 100K traces monthly
                                - 1M trace scans monthly
                                - paid tier has regional pricing

AWS Cloudwatch
                Free tier
                                - 10 custom metrics and 10 alarms
                                - 1M API requests
                                - 5GB log data ingestion and 5GB log data archive
                                - 5 dashboards with max 50 metrics each, per monthly
                                - paid tier has regional pricing
                                - can store in S3 as cheaper alternative to archiving in CW

07/MAR/2023  
Watched Ashish's Week 2 - Observability Security Considerations (Observability vs Monitoring Explained in AWS)  
https://www.youtube.com/watch?v=bOf4ITxAcXc&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=31  
Study Notes:  

Observability - centralised tracing for Security and Speed in AWS Cloud

Traditional Application Logging
                On-prem
                                Infra
                                Apps
                                AV
                                Firewall
                Cloud
                                Infra (IAAS/PAAS)
                                App (IASS/PAAS/SAAS)
                                AV
                                Firewall
Logging is sh*t
                Time consuming
                Too much data with no context
                Need in a haystack
                Monolith vs Services vs Microservices
                Modern apps are distributed
                More haystacks and more needles
                Alert fatigue

Why Observability
                Decreased alert fatigue
                End to End visibility of logs, metrics, tracing
                Troubleshoot and resolve quicker
                Cheaper to troubleshoot, operate
                Understand application health
                Improve collab between teams
                Increase CSAT

Observability vs Monitoring
                Monitoring - narrow view of specifics
                Observability - wider view of dependencies/lifecycle
                AWS context / wiki definition

Observability Pillars
                Logs
                Metrics
                Traces

Security (many more services - watch out for costs)
                Many more services available

Instrumentation
                AWS native
                OTEL / Open Source
AWS Demo
                CloudTrail logs
                CloudWatch alarms
                Tracing soluition options (Logs/Metrics/Tracing)

Security Metrics/Logs/Tracing
                Application/Solution
                Threat modelling
                Industry known attach patterns
                Instrumention
                Sec Obs dashboards or other solution

Central Observability Platform
                CloudTrail + event driven via EventBridge
                SIEM tools
                Open Source dashboards
                Event Driven Security with AWS services
                eg AWS Security Hub + EventBridge
                (SecurityHub + EventBridge->actions)

10/MAR/2023    
Watched Instrument AWS X-Ray (Week 2 Instrument XRay)  
https://www.youtube.com/watch?v=n2DTsuBrD_A&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=32  

Study Notes:  
https://docs.aws.amazon.com/#sdks  
https://aws.amazon.com/sdk-for-python/  
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/xray.html  
https://github.com/boto/boto3  
https://github.com/aws/aws-xray-sdk-python  

 
## Instrument X-Ray
Add sdk to to backend-flask/requirememnts.txt:  
`cd backend-flask`  
`aws-xray-sdk`  
`pip install -r requirements.txt`

Midldleware = service not front or backend that takes care of a particular need

*note - added pip install -r requirements.txt to gitpod.yml*

*note - added AWS configure vars to gitpod vars*

Add to app.py (backend-flask)  
```
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
```

Added to aws/json/xray.json
```
{
  "SamplingRule": {
      "RuleName": "Cruddur",
      "ResourceARN": "*",
      "Priority": 9000,
      "FixedRate": 0.1,
      "ReservoirSize": 5,
      "ServiceName": "Cruddur",
      "ServiceType": "*",
      "Host": "*",
      "HTTPMethod": "*",
      "URLPath": "*",
      "Version": 1
  }
}
```

In CLI: (to create x-ray group and what filter to use)
```
aws xray create-group \
    --group-name "Cruddur" \
    --filter-expression "service(\"backend-flask\")"
```
Output:
```
{
    "Group": {
        "GroupName": "Cruddur",
        "GroupARN": "arn:aws:xray:us-east-1:611025866129:group/Cruddur/DMGOTOZ6IIS64TUPHOQKZ555XCBBL2LDJ6H7O6H6D2FDSV4NB3MA",
        "FilterExpression": "service(\"backend-flask\")",
        "InsightsConfiguration": {
:...skipping...
{
    "Group": {
        "GroupName": "Cruddur",
        "GroupARN": "arn:aws:xray:us-east-1:611025866129:group/Cruddur/DMGOTOZ6IIS64TUPHOQKZ555XCBBL2LDJ6H7O6H6D2FDSV4NB3MA",
        "FilterExpression": "service(\"backend-flask\")",
        "InsightsConfiguration": {
            "InsightsEnabled": false,
            "NotificationsEnabled": false
        }
    }
}
```

Evidence: https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#xray:settings/groups  
![image](https://user-images.githubusercontent.com/22940535/226123395-e1384a06-936b-4a32-a685-fc29d2c72d91.png)

Can also navigate to this via:  
cloudwatch -> settings -> traces -> groups -> view settings  

Created sampling rule in CLI:
```
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```

Output:
```
{
    "SamplingRuleRecord": {
        "SamplingRule": {
            "RuleName": "Cruddur",
            "RuleARN": "arn:aws:xray:us-east-1:611025866129:sampling-rule/Cruddur",
            "ResourceARN": "*",
            "Priority": 9000,
            "FixedRate": 0.1,
            "ReservoirSize": 5,
            "ServiceName": "backend-flask",
            "ServiceType": "*",
            "Host": "*",
            "HTTPMethod": "*",
            "URLPath": "*",
            "Version": 1,
            "Attributes": {}
        },
        "CreatedAt": "2023-03-10T14:08:48+00:00",
        "ModifiedAt": "2023-03-10T14:08:48+00:00"
    }
}
```

Evidence: https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#xray:settings/sampling-rules  
![image](https://user-images.githubusercontent.com/22940535/226123638-8bcec3d7-8e7a-4a67-90a1-ec65c6ce6320.png)

Added xray env vars to backend-flask container in docker compose:  
```
version: "3.8"
services:
  backend-flask:
    environment:
      ...
      AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
      AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
      AWS_XRAY_TRACING_NAME: "Crudder"
...
```

Added separate container for xray daemon io docker compose:  
```
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "us-east-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```

*Note note from a comment I noticed*  
```
- b = bind
- o = not running on Ec2 vm (ie metada/userdata not available)
```

Notes:  
`export AWS_SECRET_ACCESS_KEY=<removed>`  
`export AWS_ACCESS_KEY_ID=<removed>`  
`export AWS_REGION=us-east-1`  
*Added the above to GP env*

*where do we use this?:*
```
EPOCH=$(date +%s)
aws xray get-service-graph --start-time $(($EPOCH-600)) --end-time $EPOCH
```

*note:*  
`aws sts get-caller-identity`

questions:  
why doesnt npm node modules get included in repo when they show in VSCode under frontend-react-js directory?

why doesnt pip installs get included in repo?  
- it does but the volume config in docker compose points back to local dev volumes(?)  

why does the xray -o cmd still output a logging error trying to hit an ec2 instance metadata? (it seems like -o isn't working)   

11/MAR/2023
Watched - X-Ray subsegments fixed  
https://www.youtube.com/watch?v=4SGTW0Db5y0&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=38

https://olley.hashnode.dev/aws-free-cloud-bootcamp-instrumenting-aws-x-ray-subsegments

Note: I got x-ray working but for spans I had actually got Olga's error and not the one Andrew showed in his videos

## Initialise X-ray recorder and middleware in app.py:
```
# Initialise X-Ray
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# Not using dynamic_naming to pickup the hostname means you can instead set, for example, the web application name, as per AWS_XRAY_TRACING_NAME: "Crudder" set in docker compose yml
#xray_recorder.configure(service='backend-flask')
XRayMiddleware(app, xray_recorder)
...
@app.route("/api/activities/home", methods=['GET'])
#@xray_recorder.capture('home_activities')
def data_home():
  data = HomeActivities.run(logger=LOGGER)
  #experiment
  xray_recorder.current_segment().put_annotation('notes','this is an annotation!!')
  now = datetime.now(timezone.utc).astimezone()
  xray_dict = {"now": now.isoformat()}
  xray_recorder.current_segment().put_metadata('key', xray_dict, 'home_activities')
  #end experiment
  return data, 200
...
@app.route("/api/activities/@<string:handle>", methods=['GET'])
#@xray_recorder.capture('user_activities_home')
def data_handle(handle):
  #experiment
  xray_recorder.current_segment().put_annotation('notes','this is an annotation!!')
  now = datetime.now(timezone.utc).astimezone()
  xray_dict = {"now": now.isoformat()}
  xray_recorder.current_segment().put_metadata('key', xray_dict, 'user_activities_root')
  #end experiment
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
```

For Spans, I added the following code to user_activitites.py  
*note: - I had to use subsegments, as by reading the documentation, the *segment* object is automatically created in app.py when the x-ray recorder and middleware is initialised*  
```
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
...
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
```

Ran docker compose up

Evidence: Traces:  
![image](https://user-images.githubusercontent.com/22940535/226125883-2b2bfaf0-570d-42f7-aaeb-9ed92647af5b.png)

Evidence: Segments:  
![image](https://user-images.githubusercontent.com/22940535/226125924-8b579cc6-8905-4b5c-b2bd-bb5fa5b82921.png)

Evidence: Annotations (note I customised the root/parent segment as Crudder instead of using dynamic URL):  
![image](https://user-images.githubusercontent.com/22940535/226126026-41bf1031-6b63-457d-9a6f-cb86e8901503.png)

Evidence: Metadata:  
![image](https://user-images.githubusercontent.com/22940535/226125938-d06fdaa4-bf2c-4845-afc1-7c454ff94a90.png)

============================

## Instrument CloudWatch

Imported watchtower into .\backend-flask\requirements.txt
```
watchtower
```

Added CloudWatch and Logging to app.py
```
# Import CloudWatch logging
import watchtower
import logging
from time import strftime
```

Instantiated logging and watchtower in app.py
```
# Initialising CloudWatch logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("Home Activities")
```

Added AWS env vars to docker compose backend-flask container:
```
AWS_DEFAULT_REGION: "${AWS_DEFAULT_REGION}"
AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
```

In order to generate some logging, added a log entry after every request in app.py:
```
# CloudWatch - create a log entry after every request
@app.after_request
def after_request(response):
  timestamp = strftime('[%Y-%b-%d %H:%M]')
  LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
  return response
```

In order to get logging from one of the routes added sending logger to the home activity route:
```
@app.route("/api/activities/home", methods=['GET'])
#@xray_recorder.capture('home_activities')
def data_home():
  data = HomeActivities.run(logger=LOGGER)
...
```

Edited home_activities.py to generate some logging to Cloudwatch
```
...
class HomeActivities:
  def run(logger):
    logger.info('Hello Cloudwatch! from home_activities /api/activities/home')
...
```

Ran docker compose up and naigated the site to generate some logging:

Evidence - Log Group:
![image](https://user-images.githubusercontent.com/22940535/226126707-4681bc44-bf48-474d-955a-cd3f63f1d868.png)

Evidence - Log entries:
![image](https://user-images.githubusercontent.com/22940535/226126790-4311e57d-5ba3-4be0-a651-68d351bd1c77.png)

Reference: pypi.org watchtower

*note: in app.py send LOGGER through as logger, and then in home activities receive logger*

===========================

## FIXING BUGS

14/MAR/2023
Fixed CW logging, I had used uppercase LOGGER in homeacitivities.py - changed to logger (lowercase) and it worked

Fixed X-Ray segments - needed to use subsegments only and segment (ie parent segment) was already auto initialised from app.py

Got Annotations working (KV pairs in a trace, objects, lists)
Got MetaData (not searchable data)

Edited journal to put the above in Journal order of work

Reference/Research:
https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-configuration.html

https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python-middleware.html#xray-sdk-python-adding-middleware-flask (didn't seem to work!)

https://olley.hashnode.dev/aws-free-cloud-bootcamp-instrumenting-aws-x-ray-subsegments

Fixed x-ray subsegments
Used Olga's blog post/guide to fix the subsegments functionality

Question: where does the xray recorder "service" get surfaced? 
Answered here: https://github.com/aaminu/aws-bootcamp-cruddur-2023/blob/main/journal/week2.md

Can not seem to be able to use:
segment = xray_recorder.begin_segment('user-activities')
I can see trace for root if I only use subsegment
This does not encase the subsegments *within* user_activities.py
@xray_recorder.capture('user_activities') <== this subsegment start and ends before the subsegments so it doesn't help

Reference: https://docs.aws.amazon.com/xray-sdk-for-python/latest/reference/basic.html

=================

## Instrument ROLLBAR

14/MAR/2023  
Watched Integrate Rollbar and capture and error (Rollbar)  
https://www.youtube.com/watch?v=xMBDAb5SEU4&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=35  
Study Notes:  

Created account on rollbar  
Created new project called Crudder  

Added env var to GitPod:  
```
export ROLLBAR_ACCESS_TOKEN="<removed>"
gp env ROLLBAR_ACCESS_TOKEN="<removed>"
```

Added reference to Rollbar env vars to backend-flask in docker-compose.yml  
```
ROLLBAR_ACCESS_TOKEN: "${ROLLBAR_ACCESS_TOKEN}"
```

Added rollbar and blinker to .\backend-flask.requirements.txt
```
blinker
rollbar
```

Imported rollbar into app.py:
```
# Import Rollbar
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
```

Initiliased rollbar in app.py including adding a new route to test rollbar
```
...
# Initalise Rollbar
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'development',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
...
@app.route("/rollbar/test")
def rollbar_test():
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"
...
```

Ran docker compose up and checked rollbar:

Evidence: 

![image](https://user-images.githubusercontent.com/22940535/226128915-11839c41-8b8f-4c5e-a7ff-4734edd7265e.png)

![image](https://user-images.githubusercontent.com/22940535/226129095-a85672b1-dccb-4509-af84-c13c9ea10890.png)

Raw JSON:
```
{
  "body": {
    "message": {
      "body": "Hello World!"
    }
  },
  "uuid": "f040e7f5-7428-4180-913a-97e573e3ea79",
  "language": "python 3.10.10",
  "level": "warning",
  "timestamp": 1678830822,
  "server": {
    "root": "/backend-flask",
    "host": "59fbceae76dd",
    "pid": 27,
    "argv": [
      "/usr/local/lib/python3.10/site-packages/flask/__main__.py",
      "run",
      "--host=0.0.0.0",
      "--port=4567"
    ]
  },
  "environment": "development",
  "framework": "flask",
  "notifier": {
    "version": "0.16.3",
    "name": "pyrollbar"
  },
  "metadata": {
    "customer_timestamp": 1678830822
  }
}
```



================================



 


