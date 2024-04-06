#!/bin/bash

#SBATCH --partition=cm3atou
#SBATCH --output=python_%J_stdout.txt
#SBATCH --error=python_%J_stderr.txt

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=60
#SBATCH --cpus-per-task=1
#SBATCH --time=100:00:00
#SBATCH --mem=16G

module load Python/3.8.6-GCCcore-10.2.0

source /home/xinwang/my_python_envs/python38/bin/activate

python "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/training/timeslice_parallel_phrase2vec.py" -hs -sg --epochs=30 --corpus "/ourdisk/hpc/cm3atou/dont_archive/xinwang/alloy2vec-main/alloy2vec/keywords/1cleaned_all_with_py.txt" --year_ranges 2022-2023,2019-2021,2015-2018,2010-2014,2004-2009,1989-2003 --model_name "1model" -include_extra_phrases