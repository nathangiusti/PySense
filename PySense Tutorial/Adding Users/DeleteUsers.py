import csv

from PySense import PySense

py_client = PySense.authenticate_by_file('/Users/nathan.giusti/Documents/PySense/VmConfig.yaml')

with open('new_users.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    users_to_delete = []
    for row in reader:
        user_to_delete = py_client.get_user_by_email(row['email'])
        if user_to_delete is not None:
            users_to_delete.append(user_to_delete)
        else:
            print("No such user {}".format(row['email']))

    py_client.delete_users(users_to_delete)


