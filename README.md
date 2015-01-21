Tax Calculator
=======
The Tax Calculator is a calculator for the US federal individual income tax system. In conjunction with micro data that represents US taxpayer characteristics and a set of behavioral assumptions, we use the Tax Calculator to conduct revenue scoring and distributional analyses of tax policies. 

Data
========
Documentation for many of the core variables used by the Tax Calculator is available at http://users.nber.org/~taxsim/gdb/gdb08.pdf. 

Disclaimer
========
The Tax-Calculator is currently under development. Users should be forewarned that the API could change significantly. Additionally, the implementation is subject to wild change. Therefore, there is NO GUARANTEE OF ACCURACY. THE CODE SHOULD NOT CURRENTLY BE USED FOR PUBLICATIONS, JOURNAL ARTICLES, OR RESEARCH PURPOSES.  Essentially, you should assume the calculations are unreliable until we finish the code re-architecture and have checked the results against other existing implementations of the tax code. The package will have released versions, which will be checked against existing code prior to release. Stay tuned for an upcoming release!

Using Tax Calculator
========
TK 

Tax Calculator Contributors
=======
The Tax Calculator is derived from taxcalc.sas, a program written by Dan Feenberg (NBER) and Inna Shapiro (NBER). Dan Feenberg, Sameer Sarkar, Matt Jensen, Ilia Kurenkov, and T.J. Alumbaugh have contributed to OSPC's Tax Calculator. 


About OSPC
=======
The Open-Source Policy Center (OSPC) is a project of the American Enterprise Institute that seeks to make policy analysis more transparent, trustworthy, and collaborative by harnessing open-source methods to build cutting-edge economic models. 

Policymakers increasingly rely on computer-driven models to predict the budgetary and broader economic impacts of current and proposed policies, especially those involving taxes and entitlements. Estimates from these models often determine a bill’s success or failure in the legislative process and public sphere. Despite their importance, however, existing models are proprietary and not subject to significant peer review or oversight. The computer code that comprises the models is not visible to outsiders, and only a few organizations and political leadership can use the models to analyze their policy ideas. Simple miscalculation and biases are difficult to discern, and when problems are perceived, they are difficult or impossible to correct. For non-leadership politicians or citizens without access to these models, it is nearly impossible to participate in the policy debate, and democracy is undermined.

OSPC's first project is building tools to analyze the budgetary and broader economic impact of taxes. These models are to be completely transparent and freely available to researchers across the country, and an easy-to-use online interfaces will allow students, policymakers, journalists, and informed citizens to interact with the models and learn for themselves about the effects of policies. 

Installation
=======
The taxcalc package is installable via `python setup.py install`. We currently test against Python 2.7 and 3.4. You can install the latest conda package via

```
conda install -c ospc taxcalc
```

which will grab the latest taxcalc package from binstar.org. Currently, we host Python 3.4 packages for Linux and OS X.
For contributors, the conda recipe is located in the `conda.recipe` directory. You can build the conda package via the `conda build` command:

```
conda build --python 3.4 conda.recipe/
```

To learn more about the conda package manager, go to conda.pydata.org.

References
=======
Documentation for our peers' revenue estimating models:

Joint Committee on Taxation https://www.jct.gov/publications.html?func=startdown&id=4500

Tax Policy Center http://www.urban.org/publications/411136.html 
