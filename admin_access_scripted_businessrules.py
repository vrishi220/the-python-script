import sys
import time
import json
import requests

instance_prefix = raw_input('Please enter your instance prefix to continue.Your prefix is located before .service-now.com in your URL: ')
user = raw_input('Please enter Read/Write Role enabled user ID: ')
pwd = raw_input('Please enter that users password (Warning- characters will be visible): ')
print('You can enter the dictionary entries you want to have admin access to your self or you can stick with the default values provided for you')
answer = raw_input('If you would like to choose your own table and snippets enter y then press enter. If not, type n then press enter: ')
while(answer!='y' and answer!='n'):
    answer = raw_input('Please enter either y on n: ')
role_permissions = ["read_roles","write_roles","create_roles","delete_roles"]
selected_role_permissions=[]
if answer=='y':
  Is='%3D'
  And='%5E'
  Or='OR'
  comma='%2C'
  A=[]
  O='y'
  W=0

  table = raw_input('What is the name of your table you\'ll be searching: ')
  table_column = raw_input('What is the name of your table column you\'ll be searching: ')

  while O=='y':
    snippet = raw_input('enter snippet: ')
    A.insert(W,snippet)
    O = raw_input('Would you like to enter another snippet? Enter y for yes or n for no: ')
    while(O!='y' and O!='n'):
        print(O)
        O = raw_input('Please enter either y on n: ')

  url = 'https://' + instance_prefix + '.service-now.com/api/now/table/' + table + '?sysparm_query=name' + Is + table_column

  for index, snippet in enumerate(A):
    if index==0:
      url = url + And +'sys_name' + Is + snippet
    else:
	  url = url + And + Or +'sys_name' + Is + snippet
  url = url + '&sysparm_fields=sys_name' + comma + 'sys_id' + comma + 'read_roles' + comma + 'write_roles' + comma + 'create_roles' + comma + 'delete_roles'
  for count, permission in enumerate(role_permissions):
    print(count)
    role_acceptance = raw_input('Would you like to manipulate \'' + permission + '\' permission, enter y for yes or n for no: ')
    while(role_acceptance!='y' and role_acceptance!='n'):
      role_acceptance = raw_input('Please enter either y on n: ')
    if role_acceptance=='y':
        selected_role_permissions.append(permission)
  print(role_permissions)
  print(selected_role_permissions)

else:
  url = 'https://' + instance_prefix + '.service-now.com/api/now/table/sys_dictionary?sysparm_query=name%3Dsys_script%5Esys_name%3Dadvanced%5EORsys_name%3Dcondition%5EORsys_name%3Dscript&sysparm_fields=sys_name%2Csys_id%2Cread_roles%2Cwrite_roles%2Ccreate_roles%2Cdelete_roles%2Cactive'

headers = {"Accept":"application/json"}
response = requests.get(url, auth=(user, pwd), headers=headers)
jsoned_response = json.loads(response.text)
print(selected_role_permissions)
testdata = raw_input('Retrieval of dictionary roles and updates commencing, press anything to continue: ')
if not selected_role_permissions:
  selected_role_permissions = role_permissions
  print(selected_role_permissions)
for x in jsoned_response['result']:
  print(x)
  for permission in selected_role_permissions:
    print("testing")
    if "admin" not in x[permission]:
      x[permission] = "admin," + x[permission]
  print(x)
  if answer=='y':
    url2 = 'https://' + instance_prefix + '.service-now.com/api/now/table/' + table + '/' + x["sys_id"]
  else:
    url2 = 'https://' + instance_prefix + '.service-now.com/api/now/table/sys_dictionary/' + x["sys_id"]
  response = requests.put(url2, auth=(user, pwd), headers=headers, data=json.dumps(x))
  print(response.status_code)

testdata = raw_input('Deactivating Query BR, press anything to continue: ')
br_query_br = 'https://' + instance_prefix + '.service-now.com/api/now/table/sys_script/3bb0ccebd7321100b9a5c7400e6103b9'
data = {'active':'false'}
response = requests.put(br_query_br, auth=(user, pwd), headers=headers, data=json.dumps(data))
print(response.status_code)
