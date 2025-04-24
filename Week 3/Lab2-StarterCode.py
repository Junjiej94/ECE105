import numpy as np
import matplotlib.pyplot as plt

"""
Junjie Jiang
14583901

ASSIGNMENT: COMPLETE plot_MAB function below
"""

"""
ECE 105: Programming for Engineers 2
Created September 5, 2020
Steven Weber

Modified April 11, 2023 
Naga Kandasamy

Multi-armed bandit starter code

This code simulates play on a multi-armed bandit

Variable convention:
k: actual number of "explore" pulls on each arm
m: number of arms
M: outcomes of the arm pulls
n: number of pulls
N: number of independent trials for Monte Carlo averaging
p: probability of win (either scalar or vector)
t: maximum number of "explore" pulls
"""

# return random result of n pulls on an arm with win prob. p
def pull_arm(p, n):
    # return random length n list with values {0,1}
    # each entry equals  0 w.p. 1-p or 1 w.p. p
    return np.random.choice([0,1], p=[1-p,p], size=n)

# create MAB: m arms, n pulls, random arm win probabilities
def create_MAB(m, n):
    # select random win probability p for each of m arms
    p = np.random.uniform(0, 1, m)
    # pull each arm n times, creating m x n random binary array
    # M[a,j] = 1 (0) if arm a on trial j is a win (loss)
    M = np.array([pull_arm(pe, n) for pe in p])
    return p, M

# compute # of "explore" pulls using (m, n, t) as inputs
# t is target # of explore pulls per arm,
# if n/m < t (not enough turns) return n/m (rounded down)
# else (n/m > t): return t
def explore_MAB(m, n, t):
    return int(1.*n/m) if n/m < t else t

# play the MAB with m arms, n pulls, and t max explore pulls
def play_MAB(m, n, t):
    # call create_MAB to obtain the win probabilities p and the outcomes M
    p, M = create_MAB(m, n)
    # call explore_MAB to determine the number of trials per arm, k
    k = explore_MAB(m, n, t)
    """
    access the specific entries of each row a of the outcomes M for each arm
    for arm a = 0,...,m-1 we access k entries
    starting with index a * k, and ending with index (a+1)*k-1
    then, sum these entries up to get the number of wins from each arm a
    so, w_est is a list of length m, holding # wins on each arm out of k pulls
    """
    w_est = [np.sum(M[a, a*k : (a+1)*k]) for a in range(m)]
    """
    a_est is the best guess for the best arm, based upon the results in w_est
    use the np.where command to obtain the indices in w_est holding the max
    it is possible for there to be multiple maxima, we break ties by choosing
    the maximum with the lowest index
    """
    a_est = np.where(np.array(w_est) == max(w_est))[0][0]
    """
    having tested each of the arms, and guessed the best arm, now use the rest
    of the trials to pull that arm.  As we have used m * k trials exploring,
    we start at trial index m *k and go through the end, i.e., to n-1
    add the sum of wins from these trials to the list w_est using append
    """
    w_est.append(np.sum(M[a_est, m*k : n]))
    """
    now, use np.where to identify the arm with the actual best win probability
    from the list of win probabilities p (break ties by choosing lowest index)
    """
    a_best = np.where(np.array(p) == max(p))[0][0]
    """
    now, suppose you knew the value of p in advance, and then pulled that arm
    for all n trials, yielding the best possible win w_best
    """
    w_best = M[a_best,:]
    """
    it is possible that w_best sums to zero, e.g., if all values of p are
    very small.  In this case, we report a value of -1, and will interpret it
    as a failed trial.  Otherwise, sum up w_est and w_best and return their
    fraction, which represents the fraction of the maximum possible wealth
    obtained without foreknowledge of p
    """
    return np.sum(w_est)/np.sum(w_best) if np.sum(w_best) > 0 else -1

# Monte Carlo average of play_MAB(m,n,t) over N trials
def play_MAB_ave(m, n, t, N):
    # call play_MAB N times and store results in res
    res = [play_MAB(m, n, t) for _ in range(N)]
    """
    not all trials succeed: some have w_best holding all 0's
    unsuccessful trial returns -1, but successful trials
    return value in [0,1], fraction of wealth obtained over
    the maximum possible wealth obtainable
    res_cal sums the outcomes of trials with r >= 0
    res_cnt counts the number of trials with r >= 0
    """
    res_val = sum([r for r in res if r >= 0])
    res_cnt = sum([1 for r in res if r >= 0])
    # return the average value of the successful trials
    return res_val / res_cnt

"""
COMPLETE:
plot_MAB takes m, N, n_set, t_set, f_set, and filename, where
m: number of arms (display in plot title)
N: number of Monte-Carlo trials (display in plot title)
n_set: set of n values (number of trials), x-axis values
t_set: explore parameter (one curve for each t, add label to plot)
f_set: the data, the fraction of wealth obtained for each (n,t) pair
filename: the name of the file where plot is to be saved

plot_MAB should produce a plot similar to "Lab2-SampleOutput.pdf"

required steps:
1. create the figure using plt
2. use plt.plot to plot n_set vs. each f, with label (hint, use list comprehension and zip over f_set and t_set)
3. add an x-axis label
4. add a y-axis label
5. add a plot title
6. add a plot legend
7. save the plot to the filename
8. show the plot
"""
# plot average frac. of maximum wealth achieved vs. # pulls n
def plot_MAB(m, N, n_set, t_set, f_set, filename):
    # 1. create figure using appropriate command from plt
    plt.figure()

    # 2. plot the results for each value t in t_set
    # x-axis is the number of trials, given by n_set
    # y-axis is the average fraction of wealth obtained
    # use zip to allow labels for each value of t in t_set
    for t, f in zip(t_set, f_set):
        plt.plot(n_set, f, label=f't = {t}')
    
    # 3. Add x-axis label
    plt.xlabel('Number of pulls (n)')
    
    # 4. Add y-axis label
    plt.ylabel('Fraction of maximum wealth obtained')

    # 5. add plot title, including values of m, N
    plt.title(f'MAB with {m} arms, averaged over {N} trials')
    
    # 6. Add plot legend
    plt.legend()
    
    # 7. Save plot to filename
    plt.savefig(filename)
    
    # 8. Show plot
    plt.show()


if __name__ == "__main__":
    # m, N: number of arms, trials
    m, N = 2, 100 # during development, reduce N to 100 for faster run times
    # n_set: set of # of pulls (20, 40, 60, ..., 580, 600)
    n_set = np.arange(20,601,20)
    # t_set: set of max # explore pulls
    t_set = [1, 2, 4, 8, 16, 32]
    # f_set: average fraction of max wealth achieved
    f_set = [[play_MAB_ave(m, n, t, N) for n in n_set] for t in t_set]
    # plot filename
    filename = "Lab2-MySampleOutput.pdf"
    # plot the results
    plot_MAB(m, N, n_set, t_set, f_set, filename)
