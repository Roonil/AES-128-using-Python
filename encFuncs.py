from Funcs import *


def subBytes(inValue):
    subbedBytes = []

    for i in range(len(inValue)):
        subbedBytes += lookupSBox(inValue[i])

    return transposeMtrx(mtrx4x4(subbedBytes))


def prepEncValues(inValue, mode, iv):
    inValue = mtrx4x4(padHex(strToHex(inValue)))

    if(iv and mode == "CBC"):
        res = []
        for idx, value in enumerate(divInBlocks(inValue, 4)):
            if (idx == 0):
                res.append(xorMatrices(
                    value, (mtrx4x4((strToHex(iv))))))
            else:
                res.append(value)

        return res
    else:
        blocks = divInBlocks(inValue, 4)
        return blocks


def initEncRound(inValue, key):
    return(addRoundKey((inValue), mtrx4x4((key))))


def encRounds(inValue, roundKeys):
    for i in range(1, len(roundKeys)-1):
        inValue = addRoundKey(
            mixCols(shiftRows(subBytes(inValue))), mtrx4x4(roundKeys[i]))

    return inValue


def finalEncRound(inValue, key):
    return addRoundKey(shiftRows(subBytes(inValue)), mtrx4x4(key))


def encBlock(block, roundKeys):
    return finalEncRound(encRounds(initEncRound(
        block, roundKeys[0]), roundKeys), roundKeys[-1])


def encECB(inValue, roundkeys):
    res = []
    for block in inValue:
        res.append(encBlock(block, roundkeys))

    return res


def encCBC(inValue, iv, roundKeys):
    res = []
    cipherText = ""
    for block in inValue:
        if (iv and cipherText != ""):
            block = xorMatrices(block, cipherText)

        cipherText = encBlock(block, roundKeys)
        res.append(cipherText)

    return res


def encrypt(inValue, secretKey, rounds, mode="ECB", iv=None):
    roundKeys = genRoundKeys(strToHex(secretKey), rounds)
    inValue = prepEncValues(inValue, mode, iv)

    iv = mtrx4x4(strToHex(iv)) if iv else None

    if(mode == "CBC"):
        return encCBC(inValue, iv, roundKeys)

    elif(mode == "ECB"):
        return encECB(inValue, roundKeys)
