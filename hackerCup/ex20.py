import string

__author__ = 'ciemny'


if __name__ == '__main__' :
    N = int(input().split()[0])
    for i in range(N) :
        S = input()
        S = S.upper()
        L = [0]*300
        for j in S :
            L[ord(j)]+=1
        L = L[ord('A'):ord('Z')+1]
        L.sort(reverse=True)
        wynik = 0
        for j in range(26):
            wynik += L[j]*(26-j)

        print("Case #" + str(i+1) + ": " + str(wynik))
