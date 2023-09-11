from json import dump

# Create userpass.json and add an empty dictionary
with open("settings.json", "w") as file:
    dump({}, file)