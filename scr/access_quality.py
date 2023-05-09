import os
import click
import pandas as pd
from Bio import SeqIO


def contig_length_df(gbk_file):
    """
    This function takes in a .gbk file and returns a pandas dataframe with a row for each contig and its sequence length.
    """
    contig_lengths = []
    
    for record in SeqIO.parse(gbk_file, "genbank"):
        contig_lengths.append((record.id, len(record.seq)))
        
    contig_length_df = pd.DataFrame(contig_lengths, columns=["Contig", "Length"])
    
    return contig_length_df


def top_contigs_for_percent(df,total_length, percent):
    """
    This function takes in a pandas dataframe with a "Contig" column and a "Length" column,
    and returns the number of contigs from the top of the dataframe that their cumulative length is equal to or greater than the input percentage of the total length of all contigs.
    """
    target_length = total_length * percent
    
    df_sorted = df.sort_values("Length", ascending=False)
    
    cum_length = 0
    for i in range(len(df)):
        cum_length += df.iloc[i]["Length"]
        if cum_length >= target_length:
            return i+1
    
    return len(df_sorted)


@click.command()
@click.argument("src", nargs=2)
@click.argument("dst", nargs=1)

def access_quality(src, dst):

    heads = {
    "gbk": [],
    "total_length": [],
    "how_many": [],
    }

    df_to_forward = pd.DataFrame(data=heads)

    dir={}

    df = contig_length_df(src[0])

    percentage = float(src[1])

    total_length = df["Length"].sum()

    gbkfilename = os.path.basename(src[0]).split(".")[0]

    dir.update({"total_length" : total_length, "how_many": top_contigs_for_percent(df,total_length, percentage), "gbk" : gbkfilename})

    df_to_forward.loc[0] = dir

    df_to_forward.to_csv(f"{dst}/{gbkfilename}.csv", index=False)






access_quality()