from behave import *
import requests
import jsonschema
import simplejson as json

# Вызовем api.
@given('domru-api-service with params="{url_params}"')
def step_impl(context, url_params):
    context.responses = dict()
    context.responses['auth'] = requests.get('http://tv.domru.ru/api/token/device?'+url_params)

@given('domru-api-service')
def step_impl(context):
    context.execute_steps(u"""
    Given domru-api-service with params="client_id=er_ottweb_device&timestamp=1497861974&device_id=123"
    """)

@then('"{response_name}" result is successful')
def step_impl(context, response_name):
    json_resp = context.responses[response_name].json()
    assert (json_resp['result'] == 1)

@then('"{response_name}" result is match to schema "{schema_name}"')
def step_impl(context, response_name, schema_name):
    schema = read_json_schema(schema_name)
    json_resp = context.responses[response_name].json()
    jsonschema.validate(json_resp, schema)

@given('schedule for channel "{lcn}" max "{limit}" elements from time "{time}"')
def step_impl(context, lcn, time, limit):
    token = context.responses['auth'].json()['token']
    url='http://tv.domru.ru/epg/schedule/{0},{1},{2}'.format(lcn, time, limit)
    headers={'X-Auth-Token': token}
    context.responses['schedule'] = requests.get(url, headers=headers)
    print (context.responses['schedule'].text)

# Вызовем api с ошибочными параметрами. 
@given('domru-api-service with missing argument')
def step_impl(context):
    context.execute_steps(u"""
    Given domru-api-service with params="_4fakeParam"
    """)

@then('"{response_name}" result is failed and error is "{err_msg}"')
def step_impl(context, response_name, err_msg):
    json_resp = context.responses[response_name].json()
    assert (json_resp['result'] == 0)
    assert (json_resp['error']['message'] == err_msg)

@then('"{response_name}" result error contains "{field}" equals "{value}"')
def step_impl(context, response_name, field, value):
    json_resp = context.responses[response_name].json()
    assert (json_resp['error'][field] == value)

@given('schedule for channel with wrong token')
def step_impl(context):
    url='http://tv.domru.ru/epg/schedule/{0},{1},{2}'.format(1, 5, 1497861974)
    headers={'X-Auth-Token': 'wrong token'}
    context.responses['schedule'] = requests.get(url, headers=headers)

@then('"{response_name}" result return status {status_code}')
def step_impl(context, response_name, status_code):
    resp = context.responses[response_name]
    assert (resp.status_code == int(status_code))

# tools:

def read_json_schema(schema_name):
    with open('schemas\{0}.json'.format(schema_name), 'r') as f:
        schema_data = f.read()
    return json.loads(schema_data)
