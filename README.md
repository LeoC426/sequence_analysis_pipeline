# Sequence Analysis Pipeline 

A Python-based bioinformatics pipeline for analyzing DNA sequences from FASTA files or directly from NCBI.

### Features 
- GC content calculation
- Sequence length analysis
- k-mer frequency analysis
- Fetch sequences from NCBI
- Export results to CSV

### Usage with demo input data
python src/main.py --input data/sample.fasta --output output_name.csv 

### Usage with NCBI data
python scr/main.py --id NCBI_ID --output output_name.csv

### Output
CSV file with sequence statistics