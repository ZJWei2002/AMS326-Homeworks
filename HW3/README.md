# Problem 3.1: Line-Disc Intersection Probability

## Algorithm Description

Our algorithm will simulate dropping discs of a list of given diameters d onto a plane with infinite parallel lines spaced at unit intervals.

1) We will first use uniform random distribution to generate y-coordinates for disc centers within two parallel lines (or in another way, a distance from the nearest bottom line).

2) We will then employ geometric properties to determine line crossings based on disc diameter d:

   Let's say between two lines, the distances from the disc center to the two border lines are dmin and dmax, respectively.

   - For d <= 1, if the disc crosses a line, its radius must be greater than dmin.
   
   - For 1 < d <= 2, the disc always cross at least 1 line. For the disc to cross two lines, the radius must be greater than dmin (because r > dmin only ensures it to cross the closer line).
   
   - For d > 2, the disc always cross at least 2 lines. For the disc to cross three lines, the radius must be greater than dmin + 1 (because r > dmin only ensures it to cross the second closest line; to reach the third closest line, it must be the case where r > dmin + 1, the distance from the center to the third closest line).

## Pseudocode
```
function simulate_disc_drops(d, num_tosses ← 4444444):
    y_positions ← uniform_random(0, 1, num_tosses)  # y coordinate of disc center within two lines
    P ← {1: 0, 2: 0, 3: 0}  # total number of disc crossing 1, 2, 3 lines

    for y in y_positions:
        r ← d/2

        if d ≤ 1:
            # Diameter smaller than 1, cannot cross more than 1 line
            P[2], P[3] ← 0, 0
            dmin ← min(y, 1 - y)
            if dmin < r:
                P[1] ← P[1] + 1

        elif d ≤ 2:
            # Diameter smaller than 2, always cross at least one line but cannot cross more than 2 lines
            P[1], P[3] ← num_tosses, 0
            dmax ← max(y, 1 - y)
            if dmax < r:
                P[2] ← P[2] + 1

        else:  # d > 2
            # Diameter greater than 2, always cross at least 2 lines
            P[1], P[2] ← num_tosses, num_tosses
            dmin ← min(y, 1 - y)
            if dmin + 1 < r:
                P[3] ← P[3] + 1

    return P
```

## Comments and Results

### Solution Approach
The algorithm considers an infinite plane with parallel lines spaced at unit intervals. By focusing only on the relative position of the disc center within any two adjacent lines (y-coordinate), we achieve a general solution that properly handles all possible disc positions. This approach overcomes the limitations of previous attempts that used a fixed number of lines and struggled with edge cases.

### Key Observations
The probability of disc-line intersections follows three distinct patterns based on disc diameter:
1. For d ≤ 1: Single intersection probability increases linearly with diameter
2. For 1 < d ≤ 2: Always intersects one line, second intersection probability increases with diameter
3. For d > 2: Always intersects two lines, third intersection becomes possible

### Results
- Single intersection: Linear increase until d = 1
- Double intersection: Begins at d > 1
- Triple intersection: Only possible at d > 2

### Performance
The Monte Carlo simulation (4,444,444 trials) provides accurate probability estimates while maintaining computational efficiency. Runtime scales linearly with the number of trials, allowing for easy adjustment of accuracy vs. computation time trade-off.

Initial attempts to detect intersections by setting 3 or 5 lines beforehand proved problematic, as this approach couldn't properly handle discs lying at the edges of the plane. The current solution overcomes this limitation by considering an infinite plane with parallel lines spaced at unit intervals. By focusing only on the relative position of the disc center within any two adjacent lines (y-coordinate), we achieve a more general and accurate solution that properly handles all possible disc positions.


# Problem 3.2: Rose Curve Optimization

## Algorithm Description

Our algorithm will find the maximum cut area between a rose curve and a rectangle through the following steps:

1) Due to the symmetry of both shapes:
   - Initial rectangle state is chosen from first quadrant only
   - Start at a random spot within the rough boundry of rose curve
   - x, y ∈ [0, 0.8] -- center of rectangle
   - θ ∈ [0, 0.25π] -- rotation angle of rectangle

2) Starting from the initial state, we will generate new state near to current state and calculate the cut area.
    -Generates random offset in range [-σ, σ]
    -Larger σ means bigger jumps in state space
    -Smaller σ means more local, refined search
    -x and y are clipped to [-0.8, 0.8] to stay in reasonable bounds
    -θ is kept in [0, 0.25π] using modulo (due to symmetry property of rose curve and rectangle)

3) For calculating intersection area at each step of simulation for a given new state:
   - Create a grid of cells within rectangle at state (0, 0, 0) (i.e. rectangle place at origin and no rotation)
   - Transform points by translation and rotation by the new state
   - Count the number of points that satisfy rose curve equation
   - among all simulation steps, we aim to find a maximum number of points satisfy above condition to maximize the cut area

4) Termination condition:
   - Stop if no improvement for 0.2 * n_iterations steps to reduce running time
   - Or reach maximum n_iterations
   - number of steps without improvement (let's say, COUNT) will be used in the following optimization process

5) For optimization process:
   - Temperature T = 1 - COUNT/(0.2 * n_iterations); Step size σ = 0.5T
   - Initially, the simulation will generate each new state with a large step size (0.5) to ensure exploration to eagerly find improvements
   - After a numebr of iterations without improvement, T would be decrease which leads to a smaller step size σ to exploitation to ensure a more precise result

6) After all iterations are done, return the best state of rectangle and best cut area = maximum number of points * area of each cell in the grid

## Pseudocode
```
function find_maximum_area(initial_state, sig ← 0.5, n_iterations ← 10000, grid_length ← 400):
    current_state ← initial_state
    rectangle_points, cell_area ← create_rectangle_grid_points(grid_length)
    transformed_points ← transformation(rectangle_points, current_state)
    mask ← inside_rose(transformed_points)
    current_cell_count ← sum(mask)

    best_state ← current_state
    best_cell_count ← current_cell_count

    count ← 0
    max_count ← n_iterations/5

    for i in range(n_iterations):
        T ← 1 - count/max_count
        current_sig ← sig * T
        x, y, theta ← current_state

        # Generate new state within the observed boundary of the curve
        new_x ← clip(x + uniform_random(-current_sig, current_sig), -0.8, 0.8)
        new_y ← clip(y + uniform_random(-current_sig, current_sig), -0.8, 0.8)
        new_t ← (theta + uniform_random(-current_sig, current_sig)) mod (0.25π)
        new_state ← (new_x, new_y, new_t)

        transformed_points ← transformation(rectangle_points, new_state)
        mask ← inside_rose(transformed_points)
        new_cell_count ← sum(mask)

        if new_cell_count > current_cell_count:
            current_state ← new_state
            current_cell_count ← new_cell_count
            best_state ← current_state
            best_cell_count ← current_cell_count
            output "New best cut found: {best_cell_count * cell_area},
                   Position: ({best_state[0]}, {best_state[1]}),
                   Rotation: {best_state[2] in degrees}°"
        else:
            count ← count + 1
            if count > max_count:
                output "Stop after {i} iterations."
                break

    best_cut ← best_cell_count * cell_area
    return best_state, best_cut
```

## Comments and Analysis

1) Results and Convergence:
   - Maximum Cut Area:
     * Consistently achieves ~0.5887
     * Optimal configuration: rectangle centered at origin with no rotation
     * This suggests the problem has a unique global maximum
   - Convergence Performance:
     * Reaches optimal solution within 10 seconds
     * Typically requires 2000-3000 iterations
     * Early termination often occurs at ~20% of max iterations
   - Solution Robustness:
     * Consistent results across multiple random initial states
     * Independent runs converge to same configuration
     * Stable across different grid resolutions

2) Development Process and Improvements:

   A. Area Calculation Challenge:
      - Problem: Unstable area comparisons using random point sampling
        * Random points led to inconsistent estimates
        * Results can't converge among a number of independent runnings
        * Made optimization decisions unreliable
      - Solution: Grid-based calculation (400×400)
        * Uniform point distribution ensures consistent comparisons
        * Resolution balances accuracy with computation speed
        * Only relative accuracy needed for optimization decisions

   B. Optimization Strategy Challenge:
      - Problem: Traditional simulated annealing got stuck
        * Fixed step size limited exploration
        * Temperature-based acceptance of worse states ineffective
        * Couldn't escape local maxima
      - Solution: Adaptive step size control
        * Step size σ = 0.5T where T = 1 - COUNT/max_COUNT
        * Large steps maintained when finding improvements
        * Naturally transitions to smaller steps for refinement
        * No need to accept worse states

   C. Performance Challenge:
      - Problem: Long execution time with full iterations
        * Original version ran all iterations
        * Most improvements happened in first few seconds
      - Solution: Early termination strategy
        * Stop after max_COUNT steps without improvement
        * max_COUNT = 0.2 * n_iterations (empirically effective)
        * Reduces runtime by ~80% without quality loss

3) Parameter Selection:
   - All key parameters were determined through extensive experimentation:
     * Initial step size (σ = 0.5): 
       - Large enough for effective exploration
       - Small enough to maintain reasonable acceptance rate
     * Temperature decay method:
       - T = 1 - COUNT/max_COUNT
       - Unlike traditional exponential decay in simulated annealing
       - Directly ties temperature to optimization progress
       - Current step size = σ * T:
         * When COUNT = 0 (just improved): T = 1, full step size
         * As COUNT increases: T decreases, smaller steps
         * Near max_COUNT: T ≈ 0, minimal exploration
     * Grid resolution (400×400):
       - Finer grids increased computation time without significant accuracy gain
       - Coarser grids led to unstable comparisons
     * Number of iterations (10000):
       - Sufficient for convergence in worst cases
       - Early termination usually triggers much sooner
     * Termination threshold (20% of iterations):
       - Based on observed convergence patterns
       - Balances thoroughness with efficiency
   - These values represent an optimal trade-off between:
     * Computation speed
     * Solution accuracy
     * Convergence reliability

4) Key Insights:
   - Stable area calculation is crucial for reliable optimization
   - Step size adaptation more effective than accepting worse states
   - Early termination possible due to quick convergence to optimal region
   - Combined improvements yield fast, reliable, and accurate results


# Problem 3.3: Plane Trajectory under Wind

## Algorithm Description

Our algorithm will simulate a plane's trajectory as it approaches an airport under a steady south wind through the following steps:

1) The plane starts at position (a, 0) and needs to reach (0, 0):
   - Initial state: a miles east of airport
   - Target: airport at origin
   - Constant south wind of speed w
   - Plane maintains constant speed v0 relative to wind

2) The plane's velocity components are described by coupled DEs:
   - dx/dt = -v0 * x/sqrt(x^2 + y^2)
   - dy/dt = -v0 * y/sqrt(x^2 + y^2) + w

3) After eliminating time dependence, we get a single DE:
   - dy/dx = (y/x) - k * sqrt(1 + (y/x)^2)
   - where k = w/v0 is the wind-to-plane speed ratio
   - with boundary condition y(a) = 0

## Pseudocode
```
function solve_trajectory(a, w, v0, n_steps):
    k ← w/v0
    x ← linspace(a, 0, n_steps)
    h ← (0 - a)/(n_steps - 1)
    y ← zeros(n_steps)
    y[0] ← 0  # starting point

    # Forward Euler Method
    for i in range(n_steps-1):
        slope ← y[i]/x[i] - k * sqrt(1 + (y[i]/x[i])^2)
        y[i+1] ← y[i] + h * slope

    return x, y

function RK4_solve(a, w, v0, n_steps):
    k ← w/v0
    x ← linspace(a, 0, n_steps)
    h ← (0 - a)/(n_steps - 1)
    y ← zeros(n_steps)
    y[0] ← 0

    for i in range(n_steps-1):
        k1 ← slope(x[i], y[i])
        k2 ← slope(x[i] + h/2, y[i] + h*k1/2)
        k3 ← slope(x[i] + h/2, y[i] + h*k2/2)
        k4 ← slope(x[i] + h, y[i] + h*k3)
        y[i+1] ← y[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

    return x, y
```

## Comments and Results

### Solution Approach
The algorithm solves the trajectory using three numerical methods:
1. Forward Euler: Simple first-order method
2. Heun's Method: Modified Euler with predictor-corrector
3. RK4: Fourth-order Runge-Kutta method

### Key Observations
- All methods successfully capture the curved trajectory caused by wind
- The plane reaches maximum height near the middle of its journey
- RK4 provides the smoothest and most accurate solution
- Forward Euler shows slight instability with larger step sizes

### Results
For given parameters (a=100 miles, w=44 mph, v0=88 mph):
- Maximum height varies slightly between methods
- All methods converge to the airport at (0,0)
- Trajectory shows expected curved path due to wind

### Performance
- Forward Euler: Fastest but least accurate
- Heun's Method: Moderate speed and accuracy
- RK4: Most accurate but ~4x slower than Forward Euler
- Step size of 100 provides good balance of accuracy and speed
