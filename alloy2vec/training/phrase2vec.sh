#!/bin/bash

#SBATCH --partition=cm3atou
#SBATCH --output=python_%J_stdout.txt
#SBATCH --error=python_%J_stderr.txt

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=80
#SBATCH --cpus-per-task=1
#SBATCH --time=100:00:00
#SBATCH --mem=64G

module load Python/3.8.6-GCCcore-10.2.0

source /home/xinwang/my_python_envs/python38/bin/activate

python "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/training/phrase2vec.py" -hs -sg --epochs=30 --corpus "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/time_slice/1cleaned_all.txt" --model_name "1model_all" -include_extra_phrases