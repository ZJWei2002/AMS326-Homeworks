# 1
def lagrange(points = {1: 412, 2: 407, 3: 397, 4: 398, 5: 417}, x = 6):
    Pn = 0
    for point in points:
        c = 1
        for tt in points.keys():
            if tt != point:
                c *= (x - tt) / (point - tt)
        Pn += c * points.get(point)
    return Pn

# 2
def quadratic(x, points = {1: 412, 2: 407, 3: 397, 4: 398, 5: 417}):
    # calculation for A^T * A
    n = len(points)
    sum_x4 = sum(t**4 for t in points.keys())
    sum_x3 = sum(t**3 for t in points.keys())
    sum_x2 = sum(t**2 for t in points.keys())
    sum_x = sum(points.keys())
    sum_y = sum(points.values())
    sum_xy = sum(p * points[p] for p in points)
    sum_x2y = sum(p**2 * points[p] for p in points)
    # calculation for A^T * b
    LHS = [[sum_x4, sum_x3, sum_x2], [sum_x3, sum_x2, sum_x], [sum_x2, sum_x, n]]
    RHS = [sum_x2y, sum_xy, sum_y]

    # Solve for LHS * [a2, a1, a0]^T = RHS, method borrowed from chatGPT
    # Gaussian elimination
    for i in range(3):
        max_row = max(range(i, 3), key=lambda r: abs(LHS[r][i]))
        LHS[i], LHS[max_row] = LHS[max_row], LHS[i]
        RHS[i], RHS[max_row] = RHS[max_row], RHS[i]
        for j in range(i + 1, 3):
            factor = LHS[j][i] / LHS[i][i]
            for k in range(i, 3):
                LHS[j][k] -= factor * LHS[i][k]
            RHS[j] -= factor * RHS[i]

    # Back substitution
    a0 = RHS[2] / LHS[2][2]
    a1 = (RHS[1] - LHS[1][2] * a0) / LHS[1][1]
    a2 = (RHS[0] - LHS[0][1] * a1 - LHS[0][2] * a0) / LHS[0][0]

    return a0 + a1 * x + a2 * x**2