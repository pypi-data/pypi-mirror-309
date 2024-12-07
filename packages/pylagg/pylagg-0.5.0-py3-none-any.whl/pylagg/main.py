import os
import sys
from typing import Optional
from importlib.metadata import version

import typer
from rich import print, panel

from pylagg import cgr, ena, jellyfish
import pylagg.config as conf

app = typer.Typer(add_completion=False)

def accession_to_cgr(accession: str, k: int, output_dir: str, threads: int, size : int):
    '''
    Takes an accession number and k-mer count and returns a CGR image. 

    NOTE: If accession refers to a project, will convert all runs in project to an image.
    '''
    run_accessions = ena.get_run_accessions(accession)

    for acc in run_accessions:
        files = ena.download_fastq(acc, output_dir) 
        counts_path = jellyfish.fastq_to_kmer_counts(files, k, output_dir, threads)

        with open(counts_path, 'r') as f:
            cgr.count_file_to_image_file(f, counts_path.replace(".counts", ".png"), size = size)


@app.command(name="cgr")
def cgr_command(
    input: str = typer.Argument(
        show_default=False,
        help=""" Must be one of the following:
        \n\n - A path to a text file containing k-mer counts.
        \n\n - An SRA accession number. 
        \n\n - A path to a text file containing line-separated SRA accession numbers.
        \n\n - A config file containing specialized options (Note: For config inputs only, only the 'output-dir' is usable).
        \n\n To use multiple inputs, provide a comma-separated list of any of the above.
        """,
    ),
    kmer: int = typer.Option(
        10,
        "--kmer",
        "-k",
        help = "Specify your desired k-mer length (Only used when generating from an accession number, if your input is already in k-mer form it will be detected)."
    ),
    output_dir: str = typer.Option(
        os.getcwd(),
        "--output-dir",
        "-o",
        help="Use this to specify an alternate save directory for your generated images. If nothing is specified, the default location is where the terminal is located.",
    ),
    size: Optional[int] = typer.Option(
        None,
        "--size",
        "-s",
        show_default=False,
        help = "Define an alternative side length for your image. Cannot exceed default value of 2^k.",
    ),
    thread_count: int = typer.Option(
        16,
        "--thread-count",
        "-t",
        help = "Amount of threads you wish to use. Threads are only used for k-mer counting when generating from an accession number.",
    ),
):
    """
    Generate your image based on the Chaos Game Representation (CGR) algorithm.
    """
    
    # INPUT ERROR CHECKING
    if size is not None and (size > 2**kmer or size < 1):
        raise Exception("Your size is invalid. Please check and try again. Size cannot exceed 2^k, or be less than 1.\nIf you need help, type 'lagg cgr --help'.")
    if not(os.path.exists(output_dir)):
        raise Exception("The given output path does not exist. Please double check your path and try again. \nIf you need help, type 'lagg cgr --help'.")
    
    #if no size is specified we need a default, and since it relies on other parameters it has to be done here.
    if size is None:
        size = 2**kmer

    inputs = input.split(",")
    
    for i in inputs:
        if i.endswith(".toml"):
            conf.config_accession_to_cgr(i, output_dir)

        elif jellyfish.is_counts_file(i):
            try:
                with open(i) as f:
                    base_name = os.path.basename(i)
                    input_name, _ = os.path.splitext(base_name)
                    cgr.count_file_to_image_file(f, f"{output_dir}/{input_name}.png", size=size)
                    print("Successfully created image '" + input_name + ".png' at " + output_dir)
            except FileNotFoundError:
                raise FileNotFoundError(f"Path for input file '{i}' does not exist.")
            
        else: # final option is for this to be an accession number or file to an accession number
            accession_to_cgr(i, kmer, output_dir, thread_count, size)

    print("Successfully generated CGR image(s)! Output located at " + output_dir)

@app.command(name="ena")               
def ena_command(
    accession_number: str = typer.Argument(
        show_default=False,
        help = 'A valid SRA accession number. Note that this can also be a comma-separated list of accession numbers or a text-file with line-separated accession numbers.',
    ),
    output_dir: str = typer.Option(
        os.getcwd(),
        "--output-dir",
        "-o",
        help="Use this to specify a specific directory for your downloaded files. If nothing is specified, the default location is where the terminal is located.",
    ),
):
    """
    Download fastq data directly from the European Nucleotide Archive (ENA).
    """
    run_accessions = ena.get_run_accessions(accession_number)
    
    for acc in run_accessions:
        ena.download_fastq(acc, output_dir)
    
    print("Successfully downloaded file(s)! Output located at " + output_dir)


@app.command(name="jellyfish")
def jellyfish_command(
    input: str = typer.Argument(
        show_default=False,
        help=""" Must be one of the following:
        \n\n - A path to a .fastq or .fastq.gz file. 
        \n\n - An SRA accession number. 
        \n\n - A path to a file containing line-separated SRA accession numbers. 
        \n\n To use multiple inputs, provide a comma-separated list of any of the above.
        """,
    ),
    kmer: int = typer.Option(
        10, "--kmer", "-k", help="Specify your desired k-mer length for counting."
    ),
    output_dir: str = typer.Option(
        os.getcwd(),
        "--output-dir",
        "-o",
        help="Use this to specify an specific directory for your k-mer count files. If nothing is specified, the default location is where the terminal is located.",
    ),
    thread_count: int = typer.Option(
        16,
        "--thread-count",
        "-t",
        help="Amount of threads you wish to use for your kmer counting.",
    ),
):
    """
    Count k-mers using Jellyfish with fastq files or accession numbers.
    """
    
    inputs = input.split(",")

    for i in inputs:
        if i.endswith((".fastq", ".fastq.gz")):
            jellyfish.fastq_to_kmer_counts([i], kmer, output_dir, thread_count)
        else:
            run_accessions = ena.get_run_accessions(i)

            for acc in run_accessions:
                files = ena.download_fastq(acc, output_dir) 
                jellyfish.fastq_to_kmer_counts(files, kmer, output_dir, thread_count)

    print(f"Successfully counted {kmer}-mers! Output located at " + output_dir)


def version_callback(value: bool):
    if value:
        print(f"LAGG {version('pylagg')}")
        raise typer.Exit()


@app.callback()
def common(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the current LAGG version and exit.",
    ),
):
    pass


def cli():
    try:
        app()
    except Exception as e:
        msg = str(e).strip('"')
        print(panel.Panel(msg, title="[red]Error", title_align="left", border_style="red"))
        sys.exit()
