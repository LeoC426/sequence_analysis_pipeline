from Bio import SeqIO, Entrez
import pandas as pd
import argparse

# Get GC content 

def gc_content(sequence):
    g = sequence.count("G")
    c = sequence.count("C")
    return (g + c) / len(sequence) * 100 if len(sequence) > 0 else 0

# Kmers counts 

def kmer_count(sequence, k=2):
    kmers = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        kmers[kmer] = kmers.get(kmer, 0) + 1
    return kmers

# download fasta from ncbi 

def fetch_sequence(accession_id):
    handle = Entrez.efetch(
        db="nucleotide",
        id=accession_id,
        rettype="fasta",
        retmode="text"
    )
    record = SeqIO.read(handle, "fasta")
    handle.close()
    return record

# Apply functions to the seq 

def analyze_record(record):
    seq = str(record.seq)
    return {
        "id": record.id,
        "length": len(seq),
        "gc_content": round(gc_content(seq), 2),
        "kmer_sample": list(kmer_count(seq, 2).items())[:5]
    }

def analyze_fasta(file_path):
    results = []
    for record in SeqIO.parse(file_path, "fasta"):
        results.append(analyze_record(record))
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="FASTA file")
    parser.add_argument("--id", help="NCBI accession ID")
    parser.add_argument("--output", default="results_output.csv")
    parser.add_argument("--email", help="Email for NCBI (required if using --id)")
    args = parser.parse_args()
    results = []
    if args.id:
        if not args.email:
            print("Must provide --email to use NCBI")
            exit()
        Entrez.email = args.email
    # Saving the default input or use the NCBI id 
    if args.input:
        results = analyze_fasta(args.input)
    elif args.id:
        record = fetch_sequence(args.id)
        # save downloaded FAST file 
        with open("data/downloaded.fasta", "w") as f:
            SeqIO.write(record, f, "fasta")
        results.append(analyze_record(record))
    else:
        print("Use --input or --id")
        exit()
    # Save CSV
    df = pd.DataFrame(results)
    df.to_csv(args.output, index=False)
    print(df)