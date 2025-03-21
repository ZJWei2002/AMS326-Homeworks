import math

def is_in_kidney(x, y):
    """Check if point (x,y) is inside the kidney curve"""
    left_side = (x**2 + y**2)**2
    right_side = x**3 + y**3
    return left_side <= right_side

def is_in_disc(x, y):
    """Check if point (x,y) is inside the disc"""
    return (x - 0.25)**2 + (y - 0.25)**2 <= 0.125

def is_in_remaining_kidney(x, y):
    """Check if point (x,y) is in kidney but not in disc"""
    return is_in_kidney(x, y) and not is_in_disc(x, y)

# Find the bounds of the kidney curve manually
# From visual inspection of the problem, we can limit our search to a reasonable box
x_min, x_max = -1.0, 1.5
y_min, y_max = -1.0, 1.5

# Rectangle Method
def rectangle_method(n):
    """Compute area using rectangle method with n×n grid"""
    dx = (x_max - x_min) / n
    dy = (y_max - y_min) / n
    
    area = 0
    for i in range(n):
        for j in range(n):
            # Use the bottom-left corner of each rectangle
            x = x_min + i * dx
            y = y_min + j * dy
            
            if is_in_remaining_kidney(x, y):
                area += dx * dy
    
    return area

# Trapezoidal Method
def trapezoidal_method(n):
    """Compute area using trapezoidal method with n×n grid"""
    dx = (x_max - x_min) / n
    dy = (y_max - y_min) / n
    
    area = 0
    for i in range(n):
        for j in range(n):
            # Check the four corners of each grid cell
            corners = [
                (x_min + i * dx, y_min + j * dy),          # bottom-left
                (x_min + (i+1) * dx, y_min + j * dy),      # bottom-right
                (x_min + i * dx, y_min + (j+1) * dy),      # top-left
                (x_min + (i+1) * dx, y_min + (j+1) * dy)   # top-right
            ]
            
            # Count how many corners are in the target region
            count = 0
            for x, y in corners:
                if is_in_remaining_kidney(x, y):
                    count += 1
            
            # Add fractional contribution based on corner count
            area += (count / 4) * dx * dy
    
    return area

# Monte Carlo Method (alternative to verify results)
def monte_carlo_method(n):
    """Compute area using Monte Carlo method with n points"""
    import random
    
    area_of_box = (x_max - x_min) * (y_max - y_min)
    points_in_region = 0
    
    for _ in range(n):
        x = x_min + random.random() * (x_max - x_min)
        y = y_min + random.random() * (y_max - y_min)
        
        if is_in_remaining_kidney(x, y):
            points_in_region += 1
    
    return (points_in_region / n) * area_of_box

# Run calculations with increasing resolution until we get 4 significant digits of stability
def calculate_area_with_precision(method_func, start_n=100, max_n=1000, step=100):
    prev_area = 0
    n = start_n
    
    while n <= max_n:
        area = method_func(n)
        
        # Format and print current result
        print(f"Method: {method_func.__name__}, n={n}, area={area:.6f}")
        
        # Check if we have 4 significant digits of precision
        if prev_area > 0 and abs(area - prev_area) < 1e-4:
            return area
        
        prev_area = area
        n += step
    
    # If we didn't reach desired precision, return the last calculation
    return prev_area

def main():
    print("Calculating area using Rectangle Method...")
    rect_area = calculate_area_with_precision(rectangle_method, start_n=100, max_n=1000, step=100)
    print(f"\nFinal Rectangle Method Result: {rect_area:.4f}")
    
    print("\nCalculating area using Trapezoidal Method...")
    trap_area = calculate_area_with_precision(trapezoidal_method, start_n=100, max_n=1000, step=100)
    print(f"\nFinal Trapezoidal Method Result: {trap_area:.4f}")

    print(monte_carlo_method(1000))

if __name__ == "__main__":
    main()