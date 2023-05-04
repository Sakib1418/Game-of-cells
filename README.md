# Game-of-cells

This is a paper replicating car t cell activation. 

## Installation 

To install the required dependencies and run the program one needs to have the Anaconda distribution. How to install Anaconda can be found at [this link.](https://www.anaconda.com/) 

After getting Anaconda installed, git-clone the repository or zip download it and navigate to this directory from terminal. 

Run the following code - 

```
$conda env create -f environment_droplet.yml
```


## Training Agent

After the enviornment is activated, navigate to gymcell folder - 

```
$cd gymcell/
```
Edit the testing.py script as required using any preferred text editor. Follow the comments in the script.

Run the command 

```
python testing.py
```



## Demonstration 

With random action

<img src = "https://github.com/Sakib1418/Game-of-cells/blob/main/image/randompolicy.gif" width="400" height="200"/>
  


  
With trained agent

<img src = "https://github.com/Sakib1418/Game-of-cells/blob/main/image/withpolicy.gif" width="400" height="200"/>
