

conda create --name sakib_RL python=3.10 anaconda -y
conda activate sakib_RL
pip3 install 'stable-baselines3[extra]==1.7.0'
conda install pytorch::pytorch torchvision torchaudio -c pytorch -y
