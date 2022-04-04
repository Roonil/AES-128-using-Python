def strToHex(inValue):
    res_list = []
    for i in inValue:
        for x in i:
            res_list.append(hex(ord(x)))

    return res_list


def nestedToSingleList(inValue):
    try:
        return nestedToSingleList(inValue[0]) + (nestedToSingleList(inValue[1:]) if len(inValue) > 1 else []) if type(inValue) is list else [inValue]
    except IndexError:
        return []


def prettify(inValue):
    inValue = nestedToSingleList(inValue)
    res = []
    for i in inValue:
        if i[:2] == '0x':
            if len(i[2:]) == 1:
                res.append("0" + i[2:])
            else:
                res.append(i[2:])
        elif (len(i) == 1):
            res.append("0" + i)
        else:
            res.append(i)

    return(''.join(res))


def padHex(inValue):
    padFactor = 16 - (len(inValue) % 16)
    return inValue + [hex(padFactor)] * padFactor


def mtrx4x4(inValue):
    return [inValue[i:i+4] for i in range(0, len(inValue), 4)]


def xorMatrices(inValue1, inValue2):
    res_list = []
    for i, j in zip(inValue1, inValue2):
        for idx in range(0, len(i)):
            res_list.append(hex(int(i[idx], base=16) ^ int(j[idx], base=16)))

    return mtrx4x4(res_list)


def xorHexRows(row1, row2):
    res = []
    for i in range(len(row1)):
        res.append(hex(int(row1[i], base=16) ^ int(row2[i], base=16)))

    return res


def lookupSBox(inValue):
    sBox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]

    res = []

    for i in range(len(inValue)):
        res.append(hex(sBox[int(inValue[i], base=16)]))

    return res


def rotRowLeft(row, n=1):
    return row[n:] + row[: n]


def transposeMtrx(inValue):
    return list(map(list, zip(*inValue)))


def genRoundKeys(key, rounds):

    roundKeys = []
    roundKeys.append(key)
    roundConstant = [[1, 0, 0, 0]]

    for _ in range(1, rounds):
        roundConstant.append([roundConstant[-1][0]*2, 0, 0, 0])
        if roundConstant[-1][0] > 0x80:
            roundConstant[-1][0] ^= 0x11b

    for i, j in enumerate(roundConstant):
        roundConstant[i] = list(map(hex, roundConstant[i]))

    for i in range(rounds):
        keySeg = []

        sBoxKey = lookupSBox(mtrx4x4(key)[3])
        keySeg.append(xorHexRows(mtrx4x4(key)[0], xorHexRows(
            rotRowLeft(sBoxKey), roundConstant[i])))

        for i in range(0, 3):
            keySeg.append(xorHexRows(keySeg[i], mtrx4x4(key)[1+i]))

        roundKey = []
        for i in range(4):
            for j in range(4):
                roundKey.append(keySeg[i][j])

        key = roundKey
        roundKeys.append(roundKey)

    return roundKeys


def shiftRows(inValue):
    for idx, i in enumerate(inValue):
        inValue[idx] = rotRowLeft(i, idx)

    return transposeMtrx(inValue)


def gFieldMult2(inValue):
    res = 0
    if (format(inValue, '008b')[0] == '1'):
        res ^= inValue << 1 ^ int('11b', base=16)
    else:
        res ^= inValue << 1

    return res


def gFieldMult3(inValue):
    return gFieldMult2(inValue) ^ inValue


def gFieldMult(inValue1, inValue2):
    res = []
    for row in inValue1:
        for col in inValue2:
            cellRes = 0
            for cell1, cell2 in zip(row, col):
                if(cell1 == '0x1'):
                    cellRes ^= (int(cell2, 16))
                elif(cell1 == '0x2'):
                    cellRes ^= (gFieldMult2(int(cell2, 16)))
                elif(cell1 == '0x3'):
                    cellRes ^= (gFieldMult3(int(cell2, 16)))

            res.append(hex(cellRes))

    return res


def mixCols(inValue):
    mat1 = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    for i, j in enumerate(mat1):
        mat1[i] = list(map(hex, mat1[i]))

    res = []

    res = gFieldMult(mat1, inValue)

    return(transposeMtrx(mtrx4x4(res)))


def addRoundKey(inValue, key):
    return xorMatrices((inValue), (key))


def divInBlocks(inValue, blockSize):
    return [(inValue[i:i+blockSize]) for i in range(0, len(inValue), blockSize)]
