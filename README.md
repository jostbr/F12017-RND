# Research and development in F1 2017
Scripts for conducting statistical simulations of the R&D process in F1 2017. The aim is
to gain insights into the optimal way to spend resource points in order to develop
the car in the fastes possible way. The results from running the script is output data in a
text a file and some plots showing how the R&D costs behave as functions of the cost reduction
and quality control extra upgrades. In the case where cost reduction or quality control upgrades
are bought, they are assumed to be purchased at the very start of the R&D process (because this
would be cheaper than buying them later in the process if you're going to buy them anyway).

Feel free to change some of the parameters to see how they affect the results. In particular,
the parameter p_fail (describing the probability that an upgrade will fail on its first attempt
before any wuality control extra upgrades are applied) is rather uncertain, but must be larger
or equal to 0.375 and is most likely not larger than 0.5.
