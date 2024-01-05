def dict2update(dict):
    arrOfStrings = [f'{key}' +'=' + f'{dict[key]}' for key in dict.keys()]
    data = ', '.join(arrOfStrings)
    print(data)
    return(data)
    
assert "name=Caheri" == dict2update({"name": "Caheri"})
assert "name=Caheri, state=IL" == dict2update({"name": "Caheri", "state": "IL"})
assert "name=Caheri, state=IL, enemy=Andrew" == dict2update({"name": "Caheri", "state": "IL", "enemy":"Andrew"})