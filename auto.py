import sys
import requests
import string
import xmltodict

sentence = sys.argv[1].strip()

replacements = dict()

if len(sys.argv) > 2:
    for replacement in sys.argv[2].split(";"):
        key, value = replacement.split(":")
        replacements[key] = value

all_suggestions = set()

def replace(s, replacements):
    for (key, value) in replacements.iteritems():
        if key in s:
            s = s.replace(key, value)
    return s


url = "http://google.com/complete/search"

for letter in string.ascii_lowercase:
    r = requests.get(url, params={
        'output': 'toolbar',
        'q': sentence + " " + letter
    })

    xml = xmltodict.parse(r.text)

    if "toplevel" not in xml:
        continue

    if not xml["toplevel"]:
        continue

    if "CompleteSuggestion" not in xml["toplevel"]:
        continue

    if not xml["toplevel"]["CompleteSuggestion"]:
        continue

    if type(xml["toplevel"]["CompleteSuggestion"]) is not list:
        xml["toplevel"]["CompleteSuggestion"] = [xml["toplevel"]["CompleteSuggestion"]]

    for suggestion_xml in xml["toplevel"]["CompleteSuggestion"]:
        if "suggestion" not in suggestion_xml:
            continue

        if not suggestion_xml["suggestion"]:
            continue

        if "@data" not in suggestion_xml["suggestion"]:
            continue

        if not suggestion_xml["suggestion"]["@data"]:
            continue

        suggestion = replace(
            suggestion_xml["suggestion"]["@data"],
            replacements
        )

        if not suggestion.lower().startswith(sentence.lower()):
            continue

        all_suggestions.add(suggestion)

for suggestion in sorted(all_suggestions):
    print suggestion
