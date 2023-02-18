from re import split

string = "country, nation, land, asdf, qwer"
meanings = split(", ", string)
main = meanings.pop(0)
sliced = meanings[0:3]
print(len(sliced))

html = main
if len(sliced) > 1:
    html += "<br>("
    html += ",".join(sliced)
    html += ")"
elif len(sliced) > 0:
    html += f", {sliced[0]}"

print(html)
