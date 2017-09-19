# Simulation of Research and Development in F1 2017
Scripts for conducting statistical simulations of the R&D process in F1 2017. The aim is
to gain insights into the optimal way to spend resource points in order to develop
the car in the fastes possible way. The results from running the script is output data in a
text a file and some plots showing how the R&D costs behave as functions of the cost reduction
and quality control extra upgrades. In the case where cost reduction or quality control upgrades
are bought, they are assumed to be purchased at the very start of the R&D process (because this
would be cheaper than buying them later in the process if you're going to buy them anyway).

Feel free to change some of the parameters to see how they affect the results. In particular,
the parameter p_fail (describing the probability that an upgrade will fail on its first attempt
before any quality control extra upgrades are applied) is the only uncertain parameter in the
simulation. Based on the wuality control upgrades reducing failure probability by 0.075, it seems
like p_fail must at least be 0.375 and is most likely not larger than 0.5. Below is and example
result of the simulation:

![Visualization of R&D simulation](results_visual.png)
