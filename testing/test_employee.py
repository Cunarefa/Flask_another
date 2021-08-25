
def test_get_employee(client, fill_database):
    rv = client.get('api/employees/2')
    assert rv.json['position'] == 'Manager'
    assert rv.json['superior_id'] == 1
