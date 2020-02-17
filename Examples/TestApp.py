import PySense

pyClient = PySense.pysense_by_file('C:\\PySenseConfig.yaml')
if not pyClient:
    print("Auth error")
    exit(1)

temp = pyClient.get_dashboards()
print(temp)




