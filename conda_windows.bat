@echo off
call conda create --name sakib_RL python=3.10 anaconda -y
call conda activate sakib_RL
call pip install stable-baselines3[extra]==1.7.0
call conda install pytorch::pytorch torchvision torchaudio -c pytorch -y
echo All packages installed successfully!
pause
