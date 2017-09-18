
# Script for conducting statistical simulations using the Department class from
# rnd_department.py. The aim is to, through simulating the research and development
# (R&D) process in an F1 team in the game F1 2017, to gain insights into the optimal
# way to spend resource points in order to develop the car in the fastes possible way.
# The results from running the script is output data in a text a file and some plots
# showing how the R&D costs bahave as functions of the cost reduction and quality control
# extra upgrades. In the case where cost reduction or wuality control upgrades are bought,
# they are assumed to be purchased at the very start of the R&D process (because this would
# be cheaper than buying them later in the process if you're going to buy them anyway).

import rnd_department as dp
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")
fig = plt.figure(figsize = (11, 9))
ax_1 = fig.add_subplot(2, 2, 1)
ax_15 = ax_1.twinx()
ax_2 = fig.add_subplot(2, 2, 2)
ax_25 = ax_2.twinx()
ax_3 = fig.add_subplot(2, 2, 3)
ax_35 = ax_3.twinx()
ax_4 = fig.add_subplot(2, 2, 4)
ax_45 = ax_4.twinx()

p_fail = 0.5                            # Probability an upgrade will fail first attempt
cost_upgrades = [0, 1, 2, 3, 4, 5]		# Cost upgrade cases to test for
fail_upgrades = [0, 1, 2, 3, 4, 5]		# Fail upgrade cases to test for
max_cost_all_dep = 0.0                  # To hold max cost for full R&D completion
min_cost_all_dep = 0.0                  # To hold min cost for full R&D completion

tt_costs_1 = np.zeros(len(cost_upgrades))   # Total costs from all departments (cost upg)
tt_costs_2 = np.zeros(len(fail_upgrades))   # Total costs from all departments (fail upg)

rpoints_per_weekend = float(input("Earned resource points per weekend: "))
num_race_weekends = 20          # The number of races in th F1 2017 calendar

stats_str = """\nResults of R&D simulation (Assumed player earned {:.0f} resource
points per weekend to predict how many seasons until R&D completion)""".format(rpoints_per_weekend)
stats_str += "\n===================================================================="
stats_str += "\n===================================================================="
format_str = "\n{:<15}{:>8.0f}\n{:<15}{:>8}\n{:<15}{:>8}"

for curr_dep_type in dp.Department.departments:     # For each department
    dep_holder_1 = list()     # To hold departments (5 cost applied, i quality applied)
    dep_holder_2 = list()     # To hold departments (5 cost applied, i quality applied)
    max_total_cost = 0.0    # To hold max total cost of one development path
    min_total_cost = 1E+9   # To hold min total cost of one development path

    for cost_upgs in cost_upgrades:         # For each number of applied cost reduc upgrades
        for fail_upgs in fail_upgrades:     # For each number of applied fail reduc upgrades
            dep = dp.Department(curr_dep_type, cost_upgs, fail_upgs, p_fail)  # Init department
            curr_total_cost = dep.get_total_costs(num_samples = 1000)          # Compute total costs

            if (curr_total_cost > max_total_cost):
                max_total_cost = curr_total_cost        # Collect max cost path
                max_dep = dep

            if (curr_total_cost < min_total_cost):
                min_total_cost = curr_total_cost        # Collect min cost path
                min_dep = dep

            if (fail_upgs == fail_upgrades[0]):     # If no fail upgrades applied
                dep_holder_1.append(dep)            # Collect dep for each cost_upgs

            if (cost_upgs == cost_upgrades[-1]):    # If all cost upgrades applied
                dep_holder_2.append(dep)            # Collect dep for each fail_upgs

    total_costs_1 = np.array([dep_obj.total_cost for dep_obj in dep_holder_1])  # Func of cost upg
    total_costs_2 = np.array([dep_obj.total_cost for dep_obj in dep_holder_2])  # Func of fail upg
    tt_costs_1 += total_costs_1
    tt_costs_2 += total_costs_2

    ax_1.plot(cost_upgrades, total_costs_1, marker = "o", linewidth = 2, label = curr_dep_type.title())
    ax_15.plot(cost_upgrades, total_costs_1/(rpoints_per_weekend*num_race_weekends), alpha = 0.0)
    ax_2.plot(fail_upgrades, total_costs_2, marker = "o", linewidth = 2, label = curr_dep_type.title())
    ax_25.plot(fail_upgrades, total_costs_2/(rpoints_per_weekend*num_race_weekends), alpha = 0.0)

    stats_str += "\n\nResource points needed for R&D completion in {} department".format(curr_dep_type)
    stats_str += "\n----------------------------------------------------------------"
    stats_str += "\nParameters giving maximum cost:"
    stats_str += format_str.format("Total cost:", max_dep.total_cost, "Cost upgs:",
        max_dep.cost_reduc, "Fail upgs:", max_dep.fail_reduc, "Initial fail pob:", p_fail)

    stats_str += "\n\nParameters giving minimum cost:"
    stats_str += format_str.format("Total cost:", min_dep.total_cost, "Cost upgs:",
        min_dep.cost_reduc, "Fail upgs:", min_dep.fail_reduc, "Initial fail pob:", p_fail)

    max_cost_all_dep += max_dep.total_cost
    min_cost_all_dep += min_dep.total_cost

stats_str += "\n\n\nTotal amount of resource points needed for full R&D completion"
stats_str += "\n--------------------------------------------------------------"
stats_str += "\nUsing most expensive path:"
stats_str += "\nTotal costs:\t{:>10.0f}".format(max_cost_all_dep)
stats_str += "\nWeekends:\t{:>10.0f}".format(max_cost_all_dep/rpoints_per_weekend)
stats_str += "\nSeasons:\t{:>10.1f}".format(max_cost_all_dep/(rpoints_per_weekend*num_race_weekends))

stats_str += "\n\nUsing least expensive path:"
stats_str += "\nTotal costs:\t{:>10.0f}".format(min_cost_all_dep)
stats_str += "\nWeekends:\t{:>10.0f}".format(min_cost_all_dep/rpoints_per_weekend)
stats_str += "\nSeasons:\t{:>10.1f}".format(min_cost_all_dep/(rpoints_per_weekend*num_race_weekends))

print(stats_str)

with open("results_text.txt", "w") as result_file:
    result_file.write(stats_str)    # Write result stats string to file

#ax_1.set_ylim(15500, 27000)
ax_1.set_xlabel("Number of cost reduction upgrades", fontname = "serif", fontsize = 11)
ax_1.set_ylabel("R&D costs", fontname = "serif", fontsize = 11)
ax_1.set_title("R&D costs with 0 QC upgrades", fontname = "serif", fontsize = 14)
ax_1.legend(loc = "upper right", fontsize = 11)
ax_15.grid(False)
ax_15.set_ylabel("Seasons until R&D completion", fontname = "serif", fontsize = 11)

ax_2.set_ylim(15000, 27000)
ax_2.set_xlabel("Number of quality control upgrades", fontname = "serif", fontsize = 11)
ax_2.set_ylabel("R&D costs", fontname = "serif", fontsize = 11)
ax_2.set_title("R&D costs with all 5 cost upgrades", fontname = "serif", fontsize = 14)
ax_2.legend(loc = "lower right", fontsize = 11)
ax_25.grid(False)
ax_25.set_ylabel("Seasons until R&D completion", fontname = "serif", fontsize = 11)

ax_3.plot(cost_upgrades, tt_costs_1, marker = "o", linewidth = 2, color = "gray")
ax_3.set_xlabel("Number of cost reduction upgrades", fontname = "serif", fontsize = 11)
ax_3.set_ylabel("Total R&D costs", fontname = "serif", fontsize = 11)
ax_3.set_title("Total R&D costs with 0 QC upgrades", fontname = "serif", fontsize = 14)
ax_35.plot(cost_upgrades, tt_costs_1/(rpoints_per_weekend*num_race_weekends), alpha = 0.0)
ax_35.grid(False)
ax_35.set_ylabel("Seasons until R&D completion", fontname = "serif", fontsize = 11)

ax_4.plot(fail_upgrades, tt_costs_2, marker = "o", linewidth = 2, color = "gray")
ax_4.set_xlabel("Number of quality control upgrades", fontname = "serif", fontsize = 11)
ax_4.set_ylabel("R&D costs", fontname = "serif", fontsize = 11)
ax_4.set_title("Total R&D costs with all 5 cost upgrades", fontname = "serif", fontsize = 14)
ax_45.plot(fail_upgrades, tt_costs_2/(rpoints_per_weekend*num_race_weekends), alpha = 0.0)
ax_45.grid(False)
ax_45.set_ylabel("Seasons until R&D completion", fontname = "serif", fontsize = 11)

fig.tight_layout()
fig.savefig("results_visual.png")
plt.show()
