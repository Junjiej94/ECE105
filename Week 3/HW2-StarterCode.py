import numpy as np
import matplotlib.pyplot as plt

"""
Junjie Jiang
14583901

ASSIGNMENT: COMPLETE function plot_eff below
"""

"""
ECE 105: Programming for Engineers 2
Created September 5, 2020
Steven Weber

Modified April 13, 2023
Naga Kandasamy

Horse race betting starter code

This code simulates betting on horses in a race using three strategies:
best: choose the best horses in the race (upper bound, best not known to bettor)
est: estimate the best horses based on observed past performance
rand: choose a random subset of horses to bet on in each race

Variable convention:
s_num: # of horses in stable
h_num: # of horses in race
b_num: # of horses in bet
k_num: exploration parameter (horses "unknown" until k bets)
N_num: # of independent Monte Carlo trials for each r_num
r_num: # of races to run
r_set: set of values of r
"""

# create random stable s with s_num horses
# a stable is a dictionary with keys = horse indices and values = quality
# each horse's quality is represented by a randomly chosen number in [0,1]
def rand_stable(s_num):
    # dictionary comprehension with random values for keys
    return {h : np.random.uniform(0, 1) for h in range(s_num)}

# select random subset of h_num horses from stable s for race
def rand_racehorses(h_num, s):
    # randomly select h_num horses (indices) from the stable (dictionary)
    h_set = np.random.choice(len(s), h_num, replace=False)
    # return these horses as a dictionary, including their qualities
    return {h : s[h] for h in h_set}

# determine the random race outcome for horses in race (in h_set)
def rand_race_outcome(h_set):
    # f is list of horses whose finish position in race is not yet decided
    # o is a dictionary representing the outcome of the race
    # o has keys = horses in race and values = position in finish
    f, o = list(h_set.keys()), {}
    # iterate over the final positions, indexed by p, of the race
    for p in range(len(h_set)):
        # add up the qualities of all horses not yet finished
        tot = sum([h_set[h] for h in h_set.keys() if h in f])
        # w is a probability distribution by dividing qualities by tot
        w = [h_set[h]/tot for h in h_set.keys() if h in f]
        # h is the randomly selected horse in position p using weights w
        h = np.random.choice(f, p = w)
        # remove h from f, as horse h now has a finish position (p)
        f.remove(h)
        # assign horse (key) h position (value) p in outcomes dictionary o
        o[h] = p
    # return outcomes dictionary
    return o

# utility function: given dictionary d with numeric values, returns a list of the keys with the top k values
def top_keys(d, k, r):
    # read about Python's sorted keyword, and lambda functions for more info
    # this sorts the dictionary keys in descending order of the key's value
    # it returns the top k items from this sorted list
    return [k for k, v in sorted(d.items(), key = lambda x: x[1], reverse = r)][0:k]

# bet_best uses knowledge of horse "qualities"
def bet_best(hr, b_num):
    # given dictionary hr of horses are in race and a bet has b_num entries
    # find the top b_num horses in hr using their qualities
    # Note: this information is NOT available to the bettor
    # Hence: bet_best is an *upper bound* on what a bettor can do
    return top_keys(hr, b_num, True)

# bet_est uses race records to choose the horses on which to bet
def bet_est(hr, b_num, rr, k_num):
    # h_unk are the *unknown horses*, here, horses with fewer than k_num bets
    h_unk = [h for h in hr.keys() if len(rr[h]) < k_num]
    # if there are more unknown horses than bet positions
    # then bet on the first b_num horses
    if len(h_unk) > b_num:
        return h_unk[0:b_num]
    # else, there are fewer unknown horses than bet positions
    else:
        # get the average performance of all "known" horses
        h_est = {h : sum(rr[h])/len(rr[h]) for h in hr if h not in h_unk}
        # get the best b_num - len(h_unk) "known" horses
        h_top = top_keys(h_est, b_num - len(h_unk), False)
        # bet on the unknown horses and the best known horses
        return [*h_unk, *h_top]

# bet on a sequence of races
def bet_races(s_num, h_num, b_num, k_num, r_num):
    # create a stable of horses
    s = rand_stable(s_num)
    # initialize total winnings for 3 strategies
    # w_best: winnings under the "bet_best" strategy
    # w_est: winnings under the "bet_est" strategy
    # w_rand: winnings under random betting
    w_best, w_est, w_rand = 0, 0, 0
    # record race positions for each horse (initially empty)
    rr = { h : [] for h in s }
    # iterate over the r_num races
    for r in range(r_num):
        # select horses to run in race
        hr = rand_racehorses(h_num, s)
        # place bets under best, estimated, and random strategies
        b_best = bet_best(hr, b_num)
        b_est = bet_est(hr, b_num, rr, k_num)
        b_rand = np.random.choice(list(hr.keys()), b_num, replace=False)
        # run the race, obtain the race outcomes, o
        o = rand_race_outcome(hr)
        # update the race records for horses in b_est
        [rr[h].append(o[h]) for h in b_est]
        # update winnings for the three strategies
        # win $1 for each horse in your bet that placed in top b_num positions
        # e.g., for b_num = 3, win $1 for each bet horse in top 3 positions
        w_best = w_best + sum([1 for h in b_best if o[h] < b_num])
        w_est = w_est + sum([1 for h in b_est if o[h] < b_num])
        w_rand = w_rand + sum([1 for h in b_rand if o[h] < b_num])
    # compute winning efficiencies under the three strategies
    # efficiency is winnings over maximum possible winnings
    # maximum possible winnings is b_num * r_num
    eta_best = w_best / (b_num * r_num)
    eta_est = w_est / (b_num * r_num)
    eta_rand = w_rand / (b_num * r_num)
    # return the three winning efficiencies
    return eta_best, eta_est, eta_rand

"""
COMPLETE:
plot_eff plots the efficiencies of the three strategies vs. # races
1. create the plot figure
2. use plt.plot to plot each efficiency vs. r_set, using label in l_set
3. also plt.scatter to also show the points on the plot
4. add x-axis label, y-axis label, plot title, and legend
include in plot title value of s_num, h_num, b_num, k_num
5. set x-axis scale to be logarithmic
6. save the figure and show the plot
"""
# plot efficiencies
def plot_eff(s_num, h_num, b_num, k_num, r_set, l_set, eta_ave, filename):
    # 1. create the plot figure
    plt.figure()
    # 2. plot the average efficiency under the three strategies vs. r_set
    for i in range(len(l_set)):
        plt.plot(r_set, eta_ave[i], label=l_set[i])
    # 3. also use scatter plot to show the points on the plot
    for i in range(len(l_set)):
        plt.scatter(r_set, eta_ave[i]) 
    # 4. add labels and title and legend
    plt.xlabel("Number of Races")
    plt.ylabel("Winning Efficiency")
    plt.title(f"Efficiency vs Number of Races")
    plt.legend()
    # 5. set x-axis to be on a logarithmic scale
    plt.xscale("log")
    # 6. save the figure and show the plot
    plt.savefig(filename)
    plt.show()

# Monte Carlo simulation for fixed r_num
if __name__ == "__main__":
    s_num = 12 # number of horses in stable
    h_num = 8 # number of horses in race
    b_num = 3 # number of horses in bet
    k_num = 5 # exploration parameter (horses "unknown" until k bets)
    r_num = 1000 # number of races on which to bet
    eta_best, eta_est, eta_rand = bet_races(s_num, h_num, b_num, k_num, r_num)
    print("Winning efficiencies") # print the winning efficiencies
    print("{:.3f}\t{:.3f}\t{:.3f}".format(eta_best, eta_est, eta_rand))

# Monte Carlo simulation plot of efficiency vs # of races (r_num)
if __name__ == "__main__":
    s_num = 12 # number of horses in stable
    h_num = 8 # number of horses in race
    b_num = 3 # number of horses in bet
    k_num = 5 # exploration parameter (horses "unknown" until k bets)
    N_num = 200 # number of independent Monte Carlo trials for each r_num
    r_set = [2**k for k in range(11)] # number of races on which to bet

    eta_ave = [] # hold Monte Carlo simulation averages here
    for r_num in r_set: # iterate over each r_num in r_set
        e = np.array([bet_races(s_num, h_num, b_num, k_num, r_num) for _ in range(N_num)]) # run N_num Monte Carlo simulations of r_num races
        eta_ave.append([np.average(s) for s in e.T]) # average results
    eta = np.array(eta_ave).T # store as numpy array, take transpose

    l_set = ['best','est','rand'] # labels for the three plots
    filename = 'HW2-SampleOutput.pdf' # name to save file
    plot_eff(s_num, h_num, b_num, k_num, r_set, l_set, eta, filename)
