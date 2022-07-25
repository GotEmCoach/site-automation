import json


def main():
    lines = []
    with open("chrome_header.txt", "r") as chrome_text:
        lines = chrome_text.readlines()
    new_dict = {}
    for line in lines:
        items = line.split(": ")
        new_dict[items[0]] = items[1].replace("\n", "")
    with open("chrome_header.json", "w+") as chrome_json:
        chrome_json.write(json.dumps(new_dict, indent=4))

if __name__ == "__main__":
    main()