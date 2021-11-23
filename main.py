from grammarconverter import getCNF
from cyk_parser import CYKParser
import sys
import re

mkey = {"if" : "a", "elif" : "b", "else" : "c", "for" : "d", "in" : "e", "while" : "f", "continue" : "g", "pass" : "h", "break" : "i", "class" : "j", "def" : "k", "return" : "l", "as" : "m", "import" : "n", "from" : "o", "raise" : "p", "and" : "q", "or" : "r", "not" : "s", "is" : "t", "True" : "u", "False" : "v", "None" : "w", "with" : "A"}

# Color code
normal = "\033[1;37;40m"
red = "\033[1;37;41m"

def preprocessInput(inp):
    kataBaru = ""
    res1 = inp.split('\n')
    for res2 in res1:
        res = []
        res2 = res2.translate({ord(":"): " : "})
        res2 = res2.translate({ord("("): " ( "})
        res2 = res2.translate({ord(")"): " ) "})
        res2 = res2.translate({ord("["): " [ "})
        res2 = res2.translate({ord("]"): " ] "})
        res2 = res2.translate({ord('"'): ' """ '})
        res2 = res2.translate({ord('\''): ' """ '})
        res2 = res2.translate({ord(','): ' , '})
        res2 = res2.translate({ord('+'): ' + '})
        res2 = res2.translate({ord('-'): ' - '})
        res2 = res2.translate({ord('/'): ' / '})
        res2 = res2.translate({ord('%'): ' % '})
        res2 = res2.translate({ord('*'): ' * '})
        res2 = res2.translate({ord('^'): ' ^ '})
        res2 = res2.translate({ord('!'): ' ! '})
        res3 = res2.split()
        res = res3
        open1 = True
        open2 = True
        newLine = True
        newLineActive = True
        for i in range(len(res)):
            if(res[i] == "\n"):
                kataBaru += "\n"
                continue
            if(len(res[i]) == 1 and open2):
                j = ord(res[i])
                if(j == 95 or (j > 64 and j < 91) or (j > 96 and j < 123) and open1):
                    kataBaru += "x"
                    newLine = False
                elif(j > 47 and j < 58 and open1):
                    kataBaru += "y"
                    newLine = False
                elif(open1):
                    kataBaru += res[i]
                    newLine = False
            elif(open1):
                if(res[i] in mkey and open2):
                    kataBaru += mkey.get(res[i])
                    newLine = False
                elif(res[i] == "**" or res[i] == "==" and open2):
                    kataBaru += res[i]
                    newLine = False
                elif(res[i] == '"""' or res[i] == '\''):
                    if(open2):
                        open2 = False
                        if(newLine):
                            kataBaru += "x=x"
                            newLine = False
                            newLineActive = False
                        else:
                            kataBaru == "+x"
                    else:
                        open2 = True
                        if(newLineActive):
                            kataBaru += "x"
                        else:
                            kataBaru += "+x"
                elif(open2):
                    benar = True
                    first = True
                    angka = True
                    cekAngka = True
                    for b in res[i]:
                        j = ord(b)
                   
                        if(b == "(" or b == ")" or b == "[" or b == "]"):
                            kataBaru += b
                            newLine = False
                        elif(first and benar):
                            if(j != 95 and (j <= 64 or j >= 91) and (j <= 96 or j >= 123) and (j <= 47 or j >= 58)):
                                benar = False
                                first = False
                                angka = False
                                cekAngka = False
                                kataBaru += "R"
                                newLine = False
                            else:
                                if(j > 47 and j < 58):
                                    first = False
                                    continue
                                else:
                                    first = False
                                    cekAngka = False
                        if(cekAngka):
                            if(j <= 47 or j >= 58):
                                cekAngka = False
                               
                                benar = False
                                angka = False
                        if(benar and not first and not cekAngka):
                            if((j > 47 and j < 58)):
                                continue
                            else: 
                                angka = False
                                if(j != 95 and (j <= 64 or j >= 91) and (j <= 96 or j >= 123)):
                                 
                                    benar = False
                    if(angka or cekAngka):
                        kataBaru += "y"
                        newLine = False
                    elif(benar):
                        kataBaru += "x"
                        newLine = False
                    elif(not benar and not first and not angka):
                        kataBaru += "R"
                        newLine = False
        kataBaru += "\n"
    return (kataBaru)

def highlightNameError(inp):
    newInp = ""
    while inp:
        x = re.search("[0-9]+[A-Za-z_]+", inp)
        if x != None:
            newInp += inp[:x.span()[0]] + red + x.group() + normal
            inp = inp[x.span()[1]:]
        else:
            newInp += inp
            inp = ""
    return (newInp)

def fileReader(path):
    with open(path, "r") as f:
        content = f.read()
    return content

def banner():
    print()
    print("                  ___       _   _                     ")
    print("                 / _ \_   _| |_| |__   ___  _ __      ")
    print("                / /_)/ | | | __| '_ \ / _ \| '_ \     ")
    print("               / ___/| |_| | |_| | | | (_) | | | |    ")
    print("               \/     \__, |\__|_| |_|\___/|_| |_|    ")
    print("               ___    |___/             _ _           ")
    print("              / __\___  _ __ ___  _ __ (_) | ___ _ __ ")
    print("             / /  / _ \| '_ ` _ \| '_ \| | |/ _ \ '__|")
    print("            / /__| (_) | | | | | | |_) | | |  __/ |   ")
    print("            \____/\___/|_| |_| |_| .__/|_|_|\___|_|   ")
    print("                                 |_|   version 4.05   \n\n")

if __name__ == "__main__":
    banner()

    # Get CNF
    CNF = getCNF("grammar.txt")
    namaFile = input("Masukkan nama file: ")
    # Input
    if (len(sys.argv) < 2):
        inpFilePath = namaFile
    else:
        inpFilePath = sys.argv[1]

    try:
        inp = fileReader(inpFilePath)
    except Exception as e:
        print(red + "Error:" + str(e) + normal)
        print("Using default path: 'test.py'\n")
        try:
            inpFilePath = "test.py"
            inp = fileReader(inpFilePath)
        except Exception as e:
            print(red + "Error:" + str(e) + normal)
            print("Terminating program...\n")
            exit(0)

    inpHighlighted = highlightNameError(inp)
    source = inp

    # Preprocess
    inp = preprocessInput(inp)
    

    #Waiting message
    print("Compiling " + str(inpFilePath) + "...\n")
    print("Waiting for your verdict...\n")

    # Check
    print("========================= SOURCE CODE =========================\n")
    for i, line in enumerate(inpHighlighted.split("\n")):
        idx =   f"  {i + 1} | " if len(str(i + 1)) == 1 else\
                f" {i + 1} | " if len(str(i + 1)) == 2 else\
                f"{i + 1} | "
        print(idx + line)
    # print(inpHighlighted.replace("\n", "\n"))
    print("\n=========================== VERDICT ===========================\n")
    if (len(inp) == 0):
        print("Accepted")
        print("\n===============================================================")
        exit(0)

    # Parse
    CYKParser(inp, CNF, source)
    print("\n===============================================================")