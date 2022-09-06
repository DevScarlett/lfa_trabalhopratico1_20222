f = open("automato.txt", "r")
lines = f.readlines()
newLines = []
        
for line in lines:
    sp = line.split("\n")
    newLines.append(sp[0])
    f.close()

#joia em

print(newLines)