import inflect
p = inflect.engine()

print(p.plural("cat"))     # cats
print(p.plural("child"))   # children
print(p.plural("octupus"))      # oxen
print(p.plural("goose"))   # geese