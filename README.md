# Test of Younes et Al's claimed QBP=NP algorithm

This repository contains a quick-and-dirty implementation of pure and mixed states, as well as code to simulate the algorithm from [this paper](http://arxiv.org/abs/1507.05061) using that implementation.

The output shows that all the optimization power comes from post-selection, and so any speedup is exactly countered by the increase in cost due to having to retry when post-selection fails. As a result, the algorithm takes at least O(2**n) time.

Example output (cut down a bit; notice that `p_correct*p_survived` stays constant):

    iter 0;	 p_survived: 100.0000%;	 p_correct: 0.0488%;	 p_correct*p_survived: 0.0488%
    iter 10;	 p_survived: 71.6915%;	 p_correct: 0.0681%;	 p_correct*p_survived: 0.0488%
    iter 100;	 p_survived: 25.2162%;	 p_correct: 0.1936%;	 p_correct*p_survived: 0.0488%
    iter 200;	 p_survived: 8.4309%;	 p_correct: 0.5792%;	 p_correct*p_survived: 0.0488%
    iter 300;	 p_survived: 2.8427%;	 p_correct: 1.7177%;	 p_correct*p_survived: 0.0488%
    iter 400;	 p_survived: 0.9801%;	 p_correct: 4.9819%;	 p_correct*p_survived: 0.0488%
    iter 500;	 p_survived: 0.3592%;	 p_correct: 13.5918%;	 p_correct*p_survived: 0.0488%
    iter 600;	 p_survived: 0.1523%;	 p_correct: 32.0607%;	 p_correct*p_survived: 0.0488%
    iter 700;	 p_survived: 0.0833%;	 p_correct: 58.6048%;	 p_correct*p_survived: 0.0488%
    iter 800;	 p_survived: 0.0603%;	 p_correct: 80.9426%;	 p_correct*p_survived: 0.0488%
    iter 900;	 p_survived: 0.0527%;	 p_correct: 92.7231%;	 p_correct*p_survived: 0.0488%
    iter 1000;	 p_survived: 0.0501%;	 p_correct: 97.4508%;	 p_correct*p_survived: 0.0488%
    iter 1090;	 p_survived: 0.0493%;	 p_correct: 99.0362%;	 p_correct*p_survived: 0.0488%

    Samples:
        |11111111111111111111111111> True
        |11111111111111111111111111> True
        |11111111111111111111111111> True
        |11111111111111111111111111> True
        |11111111111111111111111111> True
    Chance of survival: 0.04930333%
    Chance of correct: 99.03616415%
    Chance of survived and correct: 0.04882813%
    Expected number of attempts needed: 2048.0
    2**n: 2048
