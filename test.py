import urllib.request, json

print('Please wait.\nFetching Prices from website.')

baseUrl = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item='
items = [4151, 30]
item_data = {}

for item in items:
    with urllib.request.urlopen(baseUrl + str(item)) as url:
        data = json.loads(url.read().decode())
        item_data[item] = data["item"]

# Print the item data dictionary
print(json.dumps(item_data, indent=4))