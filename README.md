# Readme

This is a Nextflow workflow that takes in one or more GenBank (.gbk) files, calculates the total length of the contigs in each file, and outputs a CSV file containing the name of the input file, the total length of the contigs, and the number of contigs required to cover a specified percentage of the genome (by default its 95%) of the total length. The output CSV file is saved in a user-defined output directory.

## Prerequisites

This workflow requires Nextflow.

## Usage

To use this workflow, clone the repository and navigate to the directory containing the workflow file (`analyze_gbk.nf`).

The workflow can be executed with the following command:

``` nextflow run analyze_gbk.nf ```

This will run the workflow using the default input directory `example_data`, which should contain one or more GenBank files. The output CSV files will be saved in the `out/` directory.

## Configuration

The behavior of the workflow can be customized with the following parameters:

- `run`: The name of the current run. This parameter is used to create a subdirectory in the output directory for each run. Default: `test`.
- `in`: The path to the input directory containing one or more GenBank files. Default: `$baseDir/example_data`.
- `out`: The path to the output directory. Default: `$baseDir/out/`.
- `percentage`: The percentage of the total length of the contigs required to cover. Default: `0.95`.

These parameters can be set by modifying by passing them as command-line arguments:

``` nextflow run analyze_gbk.nf --run myrun --in /path/to/input --out /path/to/output --percentage 0.90 ```


## Workflow Steps

The workflow consists of two processes:

- `compute_csv`: This process takes in a GenBank file and the percentage of the total contig length to cover, and calculates the number of contigs required to cover that percentage. The output is a CSV file containing the name of the input file, the total length of the contigs, and the number of contigs required to cover the specified percentage.
- `publish_csv`: This process takes in the CSV file produced by `compute_csv` and publishes it to the user-defined output directory.

