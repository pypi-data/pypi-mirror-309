# Miplib Benchmark
This repository contains code to benchmark the MIPLIB (Mixed Integer Programming Library) using HiGHS solver.

## Features

- Downloads MIPLIB benchmark instances automatically (link: https://miplib.zib.de/)
- Solves MIP instances using HiGHS solver
- Stores results in SQLite database using Prisma ORM
- Includes Modal.com deployment support for cloud execution

## Installation

1. Install Poetry (Python package manager)
2. Clone this repository
3. Install dependencies:

    poetry install

4. Set up environment variables and aliases:

    source env.sh

5. Initialize database:

    prisma_generate

    prisma_migrate

## Download Benchmark Instances

    poetry run python examples/download.py

## Solve First Instance

    poetry run python examples/solve.py

# Deploy 
Using Modal for cloud execution (https://modal.com/): 

    pip install modal 
    modal setup 
    modal run deploy.py