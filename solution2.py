
matrix = [[0,0,0,0,0,0,0,0,0,0],
          [0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,1,0,0,0,0,0],
          [0,0,0,0,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0]]

def vustrel(matrix, coord):
    k=0
    alph = 'абвгдежзи'
    output = None
    list_ship = []
    for j in range(len(alph)):
        if coord[0]==alph[j]:
            k = j

    ind = int(coord[1])
    print(matrix[ind][k])
    if matrix[ind][k]==2:
        print('ok1')
        output = 'уже'
    elif matrix[ind][k]==0:
        output = 'мимо'
        print('ok2')
    elif matrix[ind][k] == 1:
        print('ok3')
        matrix[ind][k] = 2

        if matrix[ind][k+1]==0 and matrix[ind][k-1]==0 and matrix[ind+1][k]==0 and matrix[ind-1][k]==0:
            output = 'убит'
        elif matrix[ind][k+1]==0 and matrix[ind][k-1]==0:
            for j in range(4):
                if j>=0 and j<=9:
                    if matrix[ind+j][k]==0:
                        break
                    else:
                        list_ship.append(matrix[ind+j][k])
            for j in range(1,5):
                if j>=0 and j<=9:
                    if matrix[ind-j][k]==0:
                        break
                    else:
                        list_ship.append(matrix[ind-j][k])
        elif matrix[ind+1][k]==0 and matrix[ind-1][j]==0:
            for j in range(1, 5):
                if j >= 0 and j <= 9:
                    if matrix[ind][k+j]==0:
                        break
                    else:
                        list_ship.append(matrix[ind][k+j])
            for j in range(1,5):
                if j >= 0 and j <= 9:
                    if matrix[ind][k-j]==0:
                        break
                    else:
                        list_ship.append(matrix[ind][k-j])

        if 1 in list_ship:
            output = 'ранен'
        else:
            output = 'убит'
    return output

print(vustrel(matrix, 'д3'))