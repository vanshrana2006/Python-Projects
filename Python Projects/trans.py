def transpose_matrix():
    r=int(input())
    c=int(input())
    matrix = []

    for _ in range(r):
        row = list(map(int, input().split()))
        matrix.append(row)

    transposed = []
    for j in range(c):
        new_row = []
        for i in range(r):
            new_row.append(matrix[i][j])
        transposed.append(new_row)

    for row in transposed:
        print(*row, sep='-')

transpose_matrix()
