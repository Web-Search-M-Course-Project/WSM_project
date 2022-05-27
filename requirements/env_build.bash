# install conda in advance

conda create -n WSM python=3.6
conda activate WSM

conda install pandas -y
conda install -c conda-forge tqdm -y
conda install numpy -y
conda install pylint -y
conda install nltk -y
conda install -c conda-forge textblob -y

python ntlk_build.py