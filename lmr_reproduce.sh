#!/bin/bash

#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=40:00:00

module purge
eval "$(conda shell.bash hook)"

conda activate cfr-env

python lmr_reproduce.py
