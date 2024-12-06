from Packages.SingleTableQueries.SelectQueries import SingletableSelect as sts

stmt = sts()

stmt.doctype = 'xxxxxx'
stmt.select_columns = ['aaa', 'bbb', 'ccc']
# Define conditions: column_name -> (operator, value, datatype)
conditions = {
'name': ('LIKE', '%Laptop%', 'str'), # name contains 'Laptop'
'price': ('>=', 1000, 'int'),  # price is greater than or equal to 1000
'OS': ('IN', ['Android', 'mac', 'linux'], 'lst'),
'discount': ('>=', 50.99, 'flt'),
'unsupportedbefore': ('<=', '05-25-2021', 'dt')
}

"""
    

"""
logical_operator = ['AND', 'OR' , 'or' , 'g' , 'x' ,'y', 'z']

    #    ["AND", "OR", "AND", "AND"]
# Get results with AND operator (default)
query = stmt.get_results(conditions, [])
print(query)
# Get results with OR operator
