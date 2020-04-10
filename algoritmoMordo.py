import numpy as np

a = np.int32
b = np.int32
c = np.int32

a = 0b00000111111001110101100011111010
b = 0b00000110111101001110001011111010
c = 0b00000001000110010101010110011011



def modifyBitboardBit(integerNumber,  index,  newValue): 
    # 1 << index crea una maschera 1 con tanti zeri quanto la posizione specificata
    # ~mask è il not della maschera
    # n & ~mask fa in modo di mettere il bit desiderato a 0
    # (( b << index ) crea una maschera con valore desiderato e tanti 0 quanti le posizioni
    mask = 1 << index
    return ( integerNumber & ~mask ) | (( newValue << index ) & mask) 

def main():
    print(bin(a)[2:].zfill(27))
    print(bin((modifyBitboardBit(a, 26, 0)))[2:].zfill(27))

if __name__ == "__main__":
    main()