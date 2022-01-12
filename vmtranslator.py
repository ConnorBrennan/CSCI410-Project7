import sys

def translator(input):
    filei = open(input[0], "r")
    global fileo
    fileo = open(input[0][0:-2]+'asm', "w")
    #Parser
    for line in filei:

        if(len(line) > 0 and not line.isspace() and line[0:2] !='//'):

            curr = line.split()
            currCom = commandType(curr)

            if(currCom == 'C_RETURN'):
                print('Handle C_RETURN')
            else:
                currArg1 = arg1(curr, currCom)

                if(currCom == 'C_PUSH' or currArg1 == 'C_POP' or currArg1 == 'C_FUNCTION' or currArg1 == 'C_CALL'):
                    currArg2 = arg2(curr)
                    writePushPop(currCom, currArg1, currArg2)
                else: #I guarentee there will be more ifs here
                    writeArtithmetic(currArg1)

def commandType(curr):
    #print(curr)
    if curr[0] == 'push':
        return 'C_PUSH'
    if curr[0] == 'pop':
        return 'C_POP'
    if curr[0] == 'label':
        return 'C_LABEL'
    if curr[0] == 'goto':
        return 'C_GOTO'
    if curr[0] == 'if-goto':
        return 'C_IF'
    if curr[0] == 'function':
        return 'C_FUNCTION'
    if curr[0] == 'return':
        return 'C_RETURN'
    if curr[0] == 'call':
        return 'C_CALL'
    if curr[0] in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
        return 'C_ARITHMETIC'
            

def arg1(curr, currCom):
    if currCom == 'C_ARITHMETIC':
        return curr[0]
    else:
        return curr[1]

def arg2(curr):
    return curr[2]

def writeArtithmetic(command):
    global fileo
    #print(command)
    if(command == 'add'):
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('D=M\n')

        fileo.write('A=A-1\n')
        fileo.write('M=D+M\n')
        
        decreaseSP()

    elif(command == 'sub'):
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('D=M\n')

        fileo.write('A=A-1\n')
        fileo.write('M=D-M\n')
        
        decreaseSP()

    elif(command == 'neg'):
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=-M\n')

    elif(command == 'eq'):
        #print('Deal with eq')
        #Plan: subtract the first value from the second, store  
        #Figure out how JEQ works (what does it jump to vs where does it read from)
        #JEQ line
        #Set value to false line
        #Jump unconditional line
        #JEQ goes here
        #Set value to true line
        #Jump unconditional goes here
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('D=M\n')

        fileo.write('A=A-1\n')
        fileo.write('D=M-D\n')

        decreaseSP() #We do this now to avoid headache of moving around by 2 later

        #Heres where we find out if I get to use labels LMAO
        fileo.write('@FALSE\n')
        fileo.write('D;JEQ\n')

        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=1\n') #Here's hoping it uses 1 for true and 0 for false cause IDK what to do otherwise, I don't think I can just give it the word True
        fileo.write('@DONECHECK\n') #If this breaks the first thing to try is checking for a label length limit
        fileo.write('JMP\n')
        
        fileo.write('(FALSE\n')
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=0\n')

        fileo.write('(DONECHECK)\n')

    elif(command == 'gt'):
        #print('Deal with gt')
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('D=M\n')

        fileo.write('A=A-1\n')
        fileo.write('D=M-D\n')

        decreaseSP() #We do this now to avoid headache of moving around by 2 later

        #Heres where we find out if I get to use labels LMAO
        fileo.write('@FALSE\n')
        fileo.write('D;JGT\n')

        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=1\n') #Here's hoping it uses 1 for true and 0 for false cause IDK what to do otherwise, I don't think I can just give it the word True
        fileo.write('@DONECHECK\n') #If this breaks the first thing to try is checking for a label length limit
        fileo.write('JMP\n')
        
        fileo.write('(FALSE\n')
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=0\n')

        fileo.write('(DONECHECK)\n')

    elif(command == 'lt'):
        #print('Deal with lt')
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('D=M\n')

        fileo.write('A=A-1\n')
        fileo.write('D=M-D\n')

        decreaseSP() #We do this now to avoid headache of moving around by 2 later

        #Heres where we find out if I get to use labels LMAO
        fileo.write('@FALSE\n')
        fileo.write('D;JLT\n')

        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=1\n') #Here's hoping it uses 1 for true and 0 for false cause IDK what to do otherwise, I don't think I can just give it the word True
        fileo.write('@DONECHECK\n') #If this breaks the first thing to try is checking for a label length limit
        fileo.write('JMP\n')
        
        fileo.write('(FALSE\n')
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=0\n')

        fileo.write('(DONECHECK)\n')
        
    elif(command == 'and'):
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('D=M\n')
        
        fileo.write('A=A-1\n')
        fileo.write('M=D&M\n')

        decreaseSP()

    elif(command == 'or'):
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('D=M\n')
        
        fileo.write('A=A-1\n')
        fileo.write('M=D|M\n')

        decreaseSP()
        
    elif(command == 'not'):
        fileo.write('@SP\n')
        fileo.write('A=M-1\n')
        fileo.write('M=!M\n')

def writePushPop(command, segment, index):
    global fileo
    if command == 'C_PUSH': #Might have to change what's passed to this later.
        #print('Handle Push')

        if(segment == 'constant'):
            fileo.write('@'+index+'\n')
            fileo.write('D=A\n')
            fileo.write('@SP\n')
            fileo.write('M=D\n')

        else:
            loadSeg(segment, index)

            fileo.write('D=M\n')
            fileo.write('@SP\n')
            fileo.write('M=D\n')

        increaseSP()

    if command == 'C_POP':
        #print('Handle Pop')

        loadSeg(segment, index)
        fileo.write('D=A\n')
        fileo.write('@R13\n')
        fileo.write('M=D\n') #The address we need to go to is now stored in R13

        fileo.write('@SP\n')
        fileo.write('D=M\n')

        decreaseSP()

        fileo.write('@R13\n')
        fileo.write('A=M\n')
        fileo.write('M=D\n')

            

def loadSeg(segment, index):
    global fileo
    if(segment == 'local'):
        seg = 'LCL'
    elif(segment == 'argument'):
        seg = 'ARG'
    elif(segment == 'this'):
        seg = 'THIS'
    elif(segment == 'that'):
        seg = 'THAT'
    elif(segment == 'temp'):
        seg = 'TEMP'
    elif(segment == 'pointer'):
        seg = 'THIS' #Pointer refers to this on a zero and that on a one.  This these are sequential we can just handle it like this.
    elif(segment == 'static'): #Static doesn't have a built-in segment name so we reference its starting location, 16, directly.
        fileo.write('@16.'+index+'\n')
        return
    else:
        print('Invalid segment')
        exit() #Real error detection PLS?

    fileo.write('@'+seg+'\n') #Get the address of the segment from its hiding place
    fileo.write('D=M\n')
    fileo.write('@'+index+'\n') #This is how we add an arbitrary number because of course it is
    fileo.write('A=D+A\n') #This is how you set the address to the output of an OP.  If it's a different op not involving A you store that in D and then set A to D
    
def putDOnStack():
    #I made this because I thought it would be a little more efficient but it was easier to just do shit in place.  Delete this.
    global fileo
    fileo.write('@SP\n')
    fileo.write('A=M\n')
    fileo.write('M=D\n')
    increaseSP()

def increaseSP():
    global fileo
    fileo.write('@SP\n')
    fileo.write('M=M+1\n')

def decreaseSP():
    global fileo
    fileo.write('@SP\n')
    fileo.write('M=M-1\n')

if __name__ == "__main__":
    translator(sys.argv[1:])