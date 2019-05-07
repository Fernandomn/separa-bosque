def reconstroiProf(frase, lista):
    if len(frase) == 1 or len(frase) == 0:
        return frase
    for i in range(len(frase)):
        caracter = frase[i]
        if caracter == '(':
            reconstroiProf(frase[i+1:], lista)
        elif caracter == ')':
            classe = frase.split(' ')[0][1:].split(':')[1]
            return lista.append([classe])
        # elif i =='\n' and linha < len()


# frase = '012345'
# frase[2]
# frase = 'a vida é bela'
frase = '(FRASE CP1-1 (UTT:np (>N:art:um:M_S::arti: Um)(H:n:revivalismo:M_S::np-idf: revivalismo)(N<:adjp (H:adj:refrescante:M_S: refrescante))))'

a = []

b = reconstroiProf(frase, a)

print(b)
