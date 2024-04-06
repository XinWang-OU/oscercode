#!/bin/bash
#SBATCH --partition=cm3atou
#SBATCH --output=python_%J_stdout.txt
#SBATCH --error=python_%J_stderr.txt


#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --time=10:10:00

module load Python/3.8.6-GCCcore-10.2.0


source /home/xinwang/my_python_envs/python38/bin/activate

python "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/similar_words.py"