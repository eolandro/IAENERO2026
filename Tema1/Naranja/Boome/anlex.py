def numhex(Str):
    if not Str:
        return False
    #La cadena si o si tiene que empezar con caracteres:
    #Si tengo '0x000'[0x]
    if "0x"==Str[0:2]:
        RS=Str[2:]#Es desde el 2 para tomar la parte de los numeros
        #Si la longitud de la cadena va ser igual a len RS
        LS=len(RS)
        if LS==2 or LS==4:
            try:
                int(RS,16)
                return True
            except ValueError:
                return False
    return False



#Siguiente predicado oper
def oper(Str):
    if not Str:
        return False
    return Str in ['+','-']#Solo puede caeer en uno de los dos casos

#Sige movs
def movs(Str):
    if not Str:
        return False
    return Str in ['movi','movd','mova','movb']#Solo puede caeer en uno de los casos

#Sige los registros
def regs(Str):
    if not Str:
        return False
    return Str in ['r0','r1','r2','r3']#Solo puede caeer en uno de los casos

#Bomba
def es_deactivate(Str):
    return Str == "deactivate"

#Sensores, es el motivo del proque del lenguaje: abelardo
def sens(LStr):
    #No entra una cadena, sino entra 2 cadenas, por ende se necesita una lista de cadenas.
    #Pero la lista de cadenas no debe estart vacia
    if not LStr:
        return False
    #Se debe usar el match
    match LStr:
        case ["abelardo", dr]:
            return dr in ["ab","je","up","dw"]
    return False

#Saltos
def salt(Str):
    if not Str:
        return False
    return Str in ["salta_igual","salta_dif"]

#Asignaciones
def asignacion(LStr):
    if not LStr:
        return False
    match LStr:
        case [A, "=", B]: #if regs(A) and numhex(B):
            return regs(A) and (numhex(B) or regs(B))
        case [A,"=",B,C]:
            return regs(A) and sens([B,C])
        case [A,"=",B,C,D]:
            return regs(A) and (regs(B) or numhex(B)) and oper(C) and (regs(D) or numhex(D))
    return False

#Saltos
def saltos(LStr):
    if not LStr:
        return False
    match LStr:
        case [A,B,C,D]:
            return salt(A) and (regs(B) or numhex(B)) and (regs(C) or numhex(C)) and (regs(D) or numhex(D))
    return False

#Corrida de escritorio en linux

#import anlex
#anlex.numhex("0x00") #True
#anlex.numhex("0x0000") #True
#anlex.numhex("0x0G") #False
#anlex.oper("+") #True
#anlex.oper("-") #True
#anlex.oper("--") #False
#anlex.movs("movi") #True
#anlex.movs("movx") #False
#anlex.regs("r0") #True
#anlex.regs("r4") #False
#anlex.sens(["abelardo","ab"]) #True
#anlex.sens(["abelardo","xx"]) #False
#anlex.salt("salta_igual") #True
#anlex.salt("jump") #False
#anlex.asignación(["r0","=","0x00"]) #True
#anlex.asignación(["r2","=","0x00ff"]) #True
#anlex.asignación(["r1","=","r0"]) #True

#****************+++++++RESTO DEL CÓDIGO TAREA**************************

#
def procesar_linea(Str):
    if not Str:
        return False
    #Demasiados espacios? ¿Como solucionar.
    LStr=Str.strip().split(" ")#Separa la cadena en una lista de cadenas y la basura de la cadena
    LStr=[s for s in LStr if s]#Comprension de listas para quitar todo lo vacio, es decir para quedar con elementos que tengan algo.
    match LStr:
        case [Ins]: #Voy a retornar li que me mande movs de la instrucción.
            return movs(Ins)
        #Ahora el caso de la asignación
        case [A, "=", B]:
            return asignacion([A,"=",B])
        case [A,"=",B,C]:
            return asignacion([A,"=",B,C])
        case [A,"=",B,C,D]:
            return asignacion([A,"=",B,C,D])
        case [A,B,C,D]:
            return saltos([A,B,C,D])
        case ["deactivate"]:
            #return es_deactivate("deactivate")
            return True
    return False
#Pruebas
#import anlex
#anlex.procesar_linea("movi") #True
#anlex.procesar_linea("         movd \n\n") #True
#anlex.procesar_linea("r2     =    0xFFFF \n") #True