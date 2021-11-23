def CYKParser(input, CNF, src):
  A = len(input)
  B = len(CNF)
  newline = {}
  newlinePos = []
  newlineStr = src.split('\n')
  newlineCtr = 0

  for i in range(A):
    if (input[i] == '\n'):
      newlineCtr += 1
      newline[i] = newlineCtr
      newlinePos.append(i)
  
  P = [[[0 for x in range(B + 1)] for x in range(A + 1)] for x in range(A + 1)] 
  R = [None] * (B + 1)
  map = {}

  for i, var in enumerate(CNF):
    map[var] = i + 1
    R[i + 1] = CNF[var]
  
  for s in range(1, A+1):
    for v in range(1, B+1):
      for each in R[v]:
        if each[0] == input[s-1]:
          P[1][s][v] = True
          break
  
  iter = 1
  for l in range(2, A+1):
    for s in range(1, A-l+2):
      for p in range(1, l):
        while iter <= B:
          for each in R[iter]:
            if (len(each) != 1):
              if P[p][s][map[each[0]]] and P[l-p][s+p][map[each[1]]]:
                P[l][s][iter] = True
          iter += 1
  
  if P[A][1][1] == True:
    print("Accepted")
  else:
    i = 1
    j = A
    while (j > 0):
      if P[j][1][1] == True:
        break
      else:
        if input[j-1] == '\n':
          i = newline[j-1]
      j -= 1
    
    while (newlineStr[i-1][0] == ' '):
      newlineStr[i-1] = newlineStr[i-1][1:]
    
    print(newlineStr[i-1])
    print("Syntax Error")
    print(f"Terjadi kesalahan ekspresi pada line {i}")