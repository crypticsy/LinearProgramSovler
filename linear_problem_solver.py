import random,sys,re,copy


# The Main Database
symbol = {'=<':'SL','<=':'SL','>=':'SU','=':'A'}

option,rand = ["" for x in range(2)]
database, decisionVaraibles, objectiveFunction, constraints = [{} for x in range(4)] 
concount = 0
order = []
simplexTableCounter = 1


'''
    *** Here lies all the functions ***
'''

#varibale defining part
def defineVariables():
    global decisionVaraibles,objectiveFunction,option,constraints,order

    tempVariables = {}
    nextstep  = False

    while True:
        print("\nInput the variables you have defined for the problem [Each variable should be unique and should not contain numbers]")
        print("Example : x , y , z ")
        variable = (input("--> ").replace(" ","")).split(',')

        duplicate = False
        for i in variable:
            if i in tempVariables:
                print("\n***Duplicate variables have been deteced! Please insert again. ***")
                duplicate = True
                tempVariables.clear()
                break
            if i != "": tempVariables[i] = None
        if duplicate:continue
        if tempVariables == {}:continue

        print("\nThe detected variables are : " + ", ".join(list(tempVariables.keys())))
        while True:
            choice = input("\nDo you wish to change the variables? (Y/N) : --> ").upper()
            if choice == "Y" or choice == "YES": break
            if choice == "N" or choice == "NO":
                nextstep = True
                decisionVaraibles = tempVariables
                order = variable
                break
        
        if nextstep:break
        tempVariables.clear()
    
    while True:
        print("\n-------------------------------------------\n(1.) \tMaximize")
        print("(2.) \tMinimize")
        choice = input("Chose the option you wish to perform in this calculation (1 or 2) : ")
        if choice == "1" or choice == "2":
            option = choice
            break






def isObjFuncVaid(coef, var, func):
    if len(coef)!= len(var):return False
    for i in var:
        if i not in decisionVaraibles and i != rand :return False
    if func.count('=') != 1:return False
    return True


#objective funciton
def defineObjetiveFunction():
    global rand,order
    while True:
        rand = chr(65+random.randint(0,25))
        order = [rand] + order 
        if rand.lower() != decisionVaraibles and rand != decisionVaraibles:
            print("\nA random varaible --> " + rand + " <-- has been generated to store the final value. This must be used in the objective function below.")
            break

    while True:
        print("\nInput the objective function for the problem [Ensure that all of the predefined variables as well as the random generated varible is present]")
        print("Example : C = 10x + 20y + z ")
        function = input("--> ").replace(" ","")
        if function[0]!="-" and function[0]!="+":function= "+"+function

        invalid = True
        currcoef = re.findall(r"[\d\.\-\+]+",function)
        currvariable = re.findall(r"[_a-zA-Z][_a-zA-Z]*",function)

        if isObjFuncVaid(currcoef, currvariable , function):
            invalid = False

        if invalid: continue
        for i in range(len(currcoef)):
            value = 1 if currcoef[i] == "+" else -1 if currcoef[i] == "-" else float(currcoef[i])
            objectiveFunction[currvariable[i]] = value
        break






def isConsVaid(coef, var, func):
    if len(coef)+1!= len(var):return False
    for i in var:
        if i not in decisionVaraibles:return False
    if func.count('=') != 1 or func.count('=<') + func.count('>=') != 1:return False
    return True

#constraints
def getConstraints():
    global concount
    print("\n-------------------------------------------")
    while True:
        print("\nInput the constraints for the problem [Ensure that only one symbol out of the three =|>=|=<  are used at a time]")
        print("Example : 100x + 30y + 150z =< 3000 ")
        function = input("--> ").replace(" ","")
        if function[0]!="-" and function[0]!="+":function= "+"+function

        invalid = True
        currcoef = re.findall(r"[\d\.\-\+]+",function)
        currvariable = re.findall(r"[_a-zA-Z][_a-zA-Z]*",function)

        if isConsVaid(currcoef, currvariable , function):
            invalid = False

        nextstep = False
        while True:
            for i in range(len(currcoef)):                  #store values in constraints dictionary
                key = "Constant"+str(concount) if i >=len(currvariable) else currvariable[i] +str(concount)
                value = 1 if currcoef[i] == "+" else -1 if currcoef[i] == "-" else float(currcoef[i])
                constraints[key] = value
            if function.find('=<')!= -1 or function.find('<=')!= -1:
                constraints["sign"+str(concount)] = '=<'
            elif function.find('>=') != -1:
                constraints["sign"+str(concount)] = '>='
            else:
                constraints["sign"+str(concount)] = '='
            concount+=1

            choice = input("\nDo you wish to add another constraint? (Y/N) : --> ").upper()
            if choice == "Y" or choice == "YES": break
            if choice == "N" or choice == "NO":
                nextstep = True
                break
        
        if nextstep:break





#simplex table generator
def displaySimplexTable():
    global simplexTableCounter
    table = [ [' '] + order ]               #data extraction into a new table
    column = {i: len(table[0][i]) for i in range(len(table[0]))}            #find the longest string in a column

    for i in database.keys():
        tempo = [i]
        for j in order:
            tempo.append(round(database[i][j],3))
        table.append(tempo)
        for x in range(len(tempo)):
            column[x] = max(column[x] , len(str(tempo[x])))
    
    print("\n   ------   Simplex Table " + str( simplexTableCounter) + "   ------   ")
    simplexTableCounter +=1
    for y in table:
        output = ""
        colcounter = 0
        for x in y:
            output += str(x) +" "*(6 + column[colcounter] - len(str(x)))
            colcounter+=1
        print(output)




#caculation
def nextTable():
    if option == "1":
        keycolum,lowestval = rand, database['R0'][rand]
        for i in order[:len(order)-1]:
            if database['R0'][i]<lowestval:keycolum,lowestval = i, database['R0'][i]
    else:
        keycolum,lowestval = rand, database['R0'][rand]
        for i in order[:len(order)-1]:
            if database['R0'][i]>lowestval:keycolum,lowestval = i, database['R0'][i]

    print("Key column :", keycolum)

    keyrow, lowratio = "",sys.maxsize
    for i in range(1,len(database)):
        key = 'R'+str(i)
        try:
            ratio = database[key]["Constant"]/database[key][keycolum]
        except:
            ratio = sys.maxsize
        if ratio > 0 and ratio <lowratio: keyrow, lowratio = key, ratio
    print("Key row : ", keyrow)

    keyelement = database[keyrow][keycolum]
    for i in order:
        database[keyrow][i] = database[keyrow][i]/keyelement
    
    remainingRows = [x for x in database.keys() if x != keyrow]
    for a in remainingRows:
        keyelement = database[a][keycolum]
        for i in order:
            database[a][i] = database[a][i] - keyelement * database[keyrow][i]





#Optimum Checker
def optimum():
    global rand, database
    dontcheck = [rand, 'constant']
    for i in order[1:len(order)-1]:
        if i not in  dontcheck:
            if option == "1" and database['R0'][i] <0:
                return False
            elif option == "2" and database['R0'][i] >0:
                return False

    checker = {i : False for i in database.keys()}
    for i in order[:len(order)-1]:
        found = ""
        for a in database.keys():
            if database[a][i] == 1 and found == "":
                found = a
            elif database[a][i] != 0:
                found = "SS"
                break
        if found != "SS":checker[found] = True
    
    for i in checker:
        if not checker[i]:return False
    return True 


#For identity matrix
def identitymatrix():
    required = []
    artichecker = [x for x in order if x[0] == "A"]
    for i in range(1, len(database)):
        for b in artichecker:
            if database["R"+str(i)][b]==1:
                required.append("R"+str(i))
    
    constant = abs(database['R0']['A0'])
    for i in order:
        total = 0
        for a in required:
            total += database[a][i]
        database['R0'][i] += constant * total 




'''
    *** Here lies the brain of the program ***
'''


print("*** Welcome to the Simplex Solver ***")

try:
    defineVariables()
    defineObjetiveFunction()
    getConstraints()


    #standarized equation
    extravar = {}
    for i in range(concount):               # count slack and surplus variables as well as assign values
        temp = symbol[constraints["sign"+str(i)]]
        extravar[temp] = 1 if temp not in extravar else extravar[temp] + 1
        if temp == "SL":
            constraints[temp+str(extravar[temp]-1)+str(i)] = 1
        elif temp == "SU":
            constraints[temp+str(extravar[temp]-1)+str(i)] = -1
            constraints["A"+str(extravar[temp]-1)+str(i)] = 1

    for i in range(concount):               # count artificial variables as well as assign values
        temp = symbol[constraints["sign"+str(i)]]
        if temp == "A":
            constraints[temp+str(extravar[temp]+extravar["SU"]-1)+str(i)] = 1

            

    extra = []                              #add slack, surplus and aritficial variables to the order
    for i in extravar.keys():
        for a in range(extravar[i]):
            if i == "SU":
                extra.append(i+str(a))
                extra.append("A"+str(a))
            elif i == "SL":
                extra.append(i+str(a))
            elif i == "A":
                extra.append(i+str(a+extravar["SU"]))
    order += extra + ["Constant"]

    #add the objective function in the main database
    database['R0'] = {}
    maxlength = 0
    multiple = -1 if option == "2" else 1
    for i in order:
        if i in objectiveFunction:
            database['R0'][i] = objectiveFunction[i] if i  == rand else -objectiveFunction[i]
            maxlength = max(maxlength, len(str(abs(int(database['R0'][i])))))
        else:
            database['R0'][i] = multiple*(10**maxlength) if i[0] == "A" else 0 


    #add the constraints in the main database
    for i in range(concount):
        key = "R"+str(i+1)
        database[key] = {}
        for a in order:
            database[key][a] = 0 if a+str(i) not in constraints else constraints[a+str(i)]

    if ("SU" in extravar or "A" in extravar) and option  == "2" :
        displaySimplexTable()
        identitymatrix()



    while True:
        prevdatabase = copy.deepcopy(database)
        displaySimplexTable()
        if optimum():break
        nextTable()
        if prevdatabase == database:break


    print( "\n\n The optimum solution is reached when : ")
    print( str(rand) + " = " + str(round (database['R0']['Constant'])) )
    for i in decisionVaraibles.keys():
        foundcol = ""
        for b in range(1,len(database)):
            if foundcol == "" and database['R'+str(b)][i] == 1:
                foundcol =  'R'+str(b)
            elif  database['R'+str(b)][i] !=0:
                foundcol = ""
                break
        print(i + " = "+ str(round(database[foundcol]['Constant']))  if foundcol!="" else i + " = "+str(0))

except:
    print("***ERROR DETECTED. Please try again.***")