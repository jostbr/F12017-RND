
import random

class Department(object):
    """Class for simulating a development department in an F1 team in the F1 2017 game.
    Possible departments are 'engine', 'aero', and 'chassis'. Class consist of attributes
    and methods for computing the resource point usage when purchasing all upgrades."""
    departments = ["engine", "aero", "chassis"]
    upgrade_costs = {"minor": 1000.0, "major": 1500.0, "ultimate": 2000.0}
    durability_upg_cost = 23*500   # Holds total cost of the durability department

    def __init__(self, department_type, cost_reduc, fail_reduc, p_fail):
        self.dep_type = department_type
        self.cost_reduc = cost_reduc
        self.fail_reduc = fail_reduc

        self.p_cost_reduc = 0.1
        self.p_fail_reduc = 0.075
        self.p_fail = p_fail - self.fail_reduc*self.p_fail_reduc

        self.total_cost = None              # To hold total cost of a performance department

        if (department_type == Department.departments[0]):
            self.upgrades = {"minor": 9, "major": 4, "ultimate": 2}
            self.cost_upg_costs = [600.0, 800.0, 1000.0, 1200.0, 1400.0]
            self.fail_upg_costs = [300.0, 450.0, 600.0, 750.0, 900.0]

        elif (department_type == Department.departments[1]):
            self.upgrades = {"minor": 16, "major": 7, "ultimate": 3}
            self.cost_upg_costs = [1000.0, 1250.0, 1500.0, 1750.0, 2000.0]
            self.fail_upg_costs = [500.0, 750.0, 1000.0, 1250.0, 1500.0]

        elif (department_type == Department.departments[2]):
            self.upgrades = {"minor": 13, "major": 5, "ultimate": 3}
            self.cost_upg_costs = [750.0, 1000.0, 1250.0, 1500.0, 1750.0]
            self.fail_upg_costs = [400.0, 600.0, 800.0, 1000.0, 1200.0]

        self.upg_costs = {upg_type : upg_cost - self.cost_reduc*self.p_cost_reduc*upg_cost
            for upg_type, upg_cost in Department.upgrade_costs.items()}

    def _buy_upgrade(self, upg_type):
        """Function that simulates investing in R&D on an upgrade of upg_type. There's a
        probabilty the upgrade will fail, and when failing, the fail probability for further
        R&D on that upgrade is reduced. Maximum number of possible fails is 2 meaning the
        upgrade will be successful on the third attempt. Also cost is reduced for each attempt."""
        attempt = 0
        prob_fail = self.p_fail
        upg_cost = self.upg_costs[upg_type]

        while ((random.random() < prob_fail) and (attempt < 2)):    # While upgrade fails
            attempt += 1
            prob_fail -= attempt*self.p_fail_reduc                                 # Assumes probability halfes
            upg_cost += self.upg_costs[upg_type] / (2*attempt)      # Add cost for new attempt

        return upg_cost

    def get_total_costs(self, num_samples = 100):
        """Function that buys (through call to _buy_upgrade()) all upgrades within the
        department and computes the total cost. Does this many time to get an average."""
        sum_total_cost = 0.0           # To hold sum of total_cost

        for i in range(num_samples):    # Sample many times to get average
            total_cost = 0.0

            for upg_type in self.upgrades.keys():
                for upg_num in range(self.upgrades[upg_type]):
                    total_cost += self._buy_upgrade(upg_type)   # Cost of one upgrade

            sum_total_cost += total_cost    # Add total department upgrade cost

        total_cost = sum_total_cost/num_samples   # Average of all samples
        total_cost += sum(self.cost_upg_costs[:self.cost_reduc]) +\
            sum(self.fail_upg_costs[:self.fail_reduc])  # Add costs of facility upgrades

        self.total_cost = total_cost
        return total_cost

if (__name__ == "__main__"):
    department = Department("engine", 5, 5, 0.5)
    print("Total costs: {:.2f}".format(department.get_total_costs()))


