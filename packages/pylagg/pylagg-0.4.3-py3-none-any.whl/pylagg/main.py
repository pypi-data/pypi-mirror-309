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
    run_accessions = ena.get_run_accessions([accession])

    for acc in run_accessions:
        files = ena.download_fastq(acc, output_dir) 
        counts_path = jellyfish.fastq_to_kmer_counts(files, k, output_dir, threads)

        with open(counts_path, 'r') as f:
            cgr.count_file_to_image_file(f, counts_path.replace(".counts", ".png"), size = size)


@app.command(name="cgr")
def cgr_command(
    input: str = typer.Option(
        None,
        "--input",
        "-i",
        help = "File name if using k-mer input you already have. Must be a .txt file for a single image.",
    ),
    accession_number: str = typer.Option(
        None,
        "--accession-number",
        "-a",
        help = 'Generate an image using an NCBI database accession number. If you would like to use more than one accession number, please list them in quotation marks, separated by commas, or put them in a .txt file with one accession number per line, and input the file name with this flag.',
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
    config: str = typer.Option(
        None,
        "--config",
        "-c",
        help = "Use a config file to specify your options. Please include only an input (accession number(s) or kmer file(s)) and the config file's path. If any other options are also specified they will be ignored."
        ),
):
    """
    Generate your graph. Type "lagg cgr --help" to see all options for this command.
    """
    
    # INPUT ERROR CHECKING
    if input and accession_number:
        raise Exception("Please only include a file name OR an accession number(s).\nIf you need help, type 'lagg --help'.")
    # NOTE: melanie edited this to include config. pls change if you want a diff logic here @ollie!
    if not (input or accession_number or config):
        raise Exception("Please include an input, either an accession number(s), the name of a file containing k-mer input(s), or a config file path.\nIf you need help, type 'lagg --help'.")
    if size and (size > 2**kmer or size < 1):
        raise Exception("Your size is invalid. Please check and try again. Size cannot exceed 2^k, or be less than 1.\nIf you need help, type 'lagg --help'.")
    if kmer <= 0:
        raise Exception("Invalid k-mer count. Please use a k-mer count greater than 0. \nIf you need help, type 'lagg --help'.")
    if not(os.path.exists(output_dir)):
        raise Exception("The given output path does not exist. Please double check your path and try again. \nIf you need help, type 'lagg --help'.")
    
    #if no size is specified we need a default, and since it relies on other parameters it has to be done here.
    if not size:
        size = 2**kmer
    
    # Pre Process Accession number
    if config:
        conf.config_accession_to_cgr(config, output_dir)

    elif accession_number:
        
        if(accession_number.rfind(".txt") != -1):
            f = open(accession_number)
            for number in f:
                number = number.replace("\n", "")
                accession_to_cgr(number, kmer, output_dir, thread_count, size)
            f.close()
        else:
            #remove white spaces
            accession_number = accession_number.replace(" ", "")
            
            accession_list = accession_number.split(",")
            
            # Image generation with accession number:
            for number in accession_list:
                accession_to_cgr(number, kmer, output_dir, thread_count, size)
        
    elif input:

        input = input.replace(" ", "")
        inputlist = input.split(",")
        for file in inputlist:
            if not os.path.exists(file):
                raise Exception("There's an error with one of your input files " + file + ". Please double check your input and try again.")
        
        for file in inputlist:
            counts_file_path = file
            with open(counts_file_path) as f:
                
                # .txt case
                if(file.rfind(".txt") != -1):
                    file = file.replace(".txt", "")
                    
                    inputname = file[file.rfind("/") + 1:]
                    
                    cgr.count_file_to_image_file(f, output_dir + "/" + inputname + ".png", size=size)
                    print("Successfully created image called '" + inputname + ".png' at " + output_dir)
                else:
                    raise Exception("The input is not a supported file type. Supported types are '.txt'. Please convert to a supported file type and try again.\nIf you need help, type 'lagg --help'.")
        
    else:
        raise Exception("No valid flag. Please use either -a or -i or -c")
 

@app.command(name="ena")               
def ena_command(
    accession_number: str = typer.Option(
        None,
        "--accession-number",
        "-a",
        help = 'Download a fastq file using an NCBI database accession number. If you would like to use more than one accession number, please list them in quotation marks, separated by commas, or put them in a .txt file with one accession number per line, and input the file name with this flag.',
    ),
    kmer_length: Optional[int] = typer.Option(
        None,
        "--kmer",
        "-k",
        help = "If you would also like your download to be k-mer counted as well, provide a kmer length."
    ),
    output_dir: str = typer.Option(
        os.getcwd(),
        "--output-dir",
        "-o",
        help="Use this to specify a specific directory for your downloaded files (and k-mer count files, if counting). If nothing is specified, the default location is where the terminal is located.",
    ),
    thread_count: int = typer.Option(
        16,
        "--thread-count",
        "-t",
        help = "Amount of threads you wish to use. Threads are only used for k-mer counting.",
    ),
):
    """
    Only download a fastq file from ENA without generating a graph, and optionally k-mer count it too!
    """
    
    accession_number = accession_number.replace(" ", "")
        
    accession_list = accession_number.split(",")
        
    if(accession_number.rfind(".txt") != -1):
        raise Exception("detecting .txt of accession numbers (not implemented)")
    
    for number in accession_list:  
        files = ena.download_fastq(number, output_dir)
    
        if kmer_length is not None:
            print(files)
            jellyfish.fastq_to_kmer_counts(files, kmer_length, output_dir, thread_count)
            print("Successfully downloaded and created k-mer counts at " + output_dir)
        else:
            print("Successfully downloaded file(s) at " + output_dir)


@app.command(name="jellyfish")
def jellyfish_command(
    input_fastq: str = typer.Option(
        None,
        "--input-fastq",
        "-i",
        help = 'Convert a fastq file you already have downloaded. Input the file path and name using this flag.',
    ),
    kmer: int = typer.Option(
        10,
        "--kmer",
        "-k",
        help = "Specify your desired k-mer length for counting."
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
        help = "Amount of threads you wish to use for your kmer counting.",
    ),
    ):
    """
    Generate a k-mer count from a fastq file already downloaded on your computer!
    """
    
    jellyfish.fastq_to_kmer_counts([input_fastq], kmer, output_dir, thread_count)


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
