from Funcs import *


def subBytes(inValue):
    subbedBytes = []

    for i in range(len(inValue)):
        subbedBytes += lookupSBox(inValue[i])

    return transposeMtrx(mtrx4x4(subbedBytes))


def prepEncValues(inValue, mode, iv):
    if (mode == "CFB" or mode == "OFB" or mode == "CTR"):
        inValue = strToHex(inValue)

    else:
        inValue = mtrx4x4(padHex(strToHex(inValue)))

    if(mode == "CFB" or mode == "OFB" or mode == "CTR"):
        res = []

        for value in divInBlocks(inValue, 16):
            res.append(value)

        return res

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


def encBlock(block, roundKeys, rounds):
    return finalEncRound(encRounds(initEncRound(
        block, roundKeys[0]), roundKeys), roundKeys[rounds])


def encECB(inValue, roundkeys, rounds):
    res = []
    for block in inValue:
        res.append(encBlock(block, roundkeys, rounds))

    return res


def encCBC(inValue, iv, roundKeys, rounds):
    res = []
    cipherText = ""
    for block in inValue:
        if (iv and cipherText != ""):
            block = xorMatrices(block, cipherText)

        cipherText = encBlock(block, roundKeys, rounds)
        res.append(cipherText)

    return res


def encCFB(inValue, iv, roundKeys, rounds):
    res = []
    for block in inValue:
        if res != []:
            iv = (res[-4:])

        encIV = encBlock(iv, roundKeys, rounds)
        for blockIdx, block4x4 in enumerate(divInBlocks(block, 4)):
            cipCFB = xorMatrices([block4x4], [encIV[blockIdx]])
            res.extend(cipCFB)

    return res


def encOFB(inValue, iv, roundKeys, rounds):
    res = []
    oldIV = []

    for block in inValue:
        if oldIV != []:
            iv = oldIV

        encIV = encBlock(iv, roundKeys, rounds)

        for blockIdx, block4x4 in enumerate(divInBlocks(block, 4)):
            cipOFB = xorMatrices([block4x4], [encIV[blockIdx]])
            res.extend(cipOFB)

        oldIV = encIV

    return res


def increaseCTR(nonce):
    nonce = int(prettify(nonce), 16)
    nonce += 1
    nonce = hex(nonce)[2:]

    return mtrx4x4(divInBlocks(nonce, 2))


def encCTR(inValue, nonce, roundKeys, rounds):
    res = []
    oldIV = []
    for block in inValue:
        if oldIV != []:
            nonce = increaseCTR(nonce)

        encIV = encBlock(nonce, roundKeys, rounds)

        for blockIdx, block4x4 in enumerate(divInBlocks(block, 4)):
            cipCTR = xorMatrices([block4x4], [encIV[blockIdx % 4]])
            res.extend(cipCTR)

        oldIV = encIV
    return res


def encrypt(inValue, secretKey, rounds, mode="ECB", iv=None):
    roundKeys = genRoundKeys(strToHex(secretKey), rounds)
    inValue = prepEncValues(inValue, mode, iv)

    iv = mtrx4x4(strToHex(iv)) if iv else None

    if(mode == "CBC"):
        return encCBC(inValue, iv, roundKeys, rounds)

    elif(mode == "CFB"):
        return encCFB(inValue, iv, roundKeys, rounds)

    elif (mode == "CTR"):
        return encCTR(inValue, iv, roundKeys, rounds)

    elif(mode == "OFB"):
        return encOFB(inValue, iv, roundKeys, rounds)

    elif(mode == "ECB"):
        return encECB(inValue, roundKeys, rounds)
