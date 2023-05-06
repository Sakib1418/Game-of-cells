# Game-of-cells

This repository is for reproducing and using virtual CAR T-cell activation optimization using Reinforcement Learning. 

## Pre-requisites

1. You need to have Anaconda or Miniconda distribution installed in order to run the codes. Installation instruction for Anaconda can be found  at at [this link.](https://www.anaconda.com/)  and Miniconda can be found in  at [this link.](https://conda.io/miniconda.html) Anaconda version - 4.12 or more is preferred. 

2. pip version 23.0.1 used. 


## Installation 

1. After getting Anaconda installed, git-clone the repository or zip download it and navigate to this directory from Anaconda Prompt. 

* For windows OS, run this code 

```
 $.\conda_windows.bat
```

* For linux OS, run this code 

```
$./linux_conda.sh
```

* For Mac OS with zsh shell, run this code 

```
$./mac_zsh_conda.sh
```

* For Mac OS with bash shell, run this code 

```
$./mac_bash_conda.sh
```

NOTE: It will take about 15 minutes to load the codes. 

## Training Agent

After the enviornment is activated, navigate to gymcell folder - 

```
$cd gymcell/
```
Edit the testing.py script as required using any preferred text editor. Follow the comments in the script.

Run the command 

```
$python3 testing.py
```



## Demonstration 

With random action

<img src = "https://github.com/Sakib1418/Game-of-cells/blob/main/image/randompolicy.gif" width="400" height="200"/>
  


  
With trained agent

<img src = "https://github.com/Sakib1418/Game-of-cells/blob/main/image/withpolicy.gif" width="400" height="200"/>
