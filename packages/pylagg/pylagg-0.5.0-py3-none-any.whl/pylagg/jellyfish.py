import os
import subprocess
from typing import List, Optional

import rich.progress as prog
from rich.progress import Progress

PROGBAR_COLUMNS = (
    prog.SpinnerColumn(),
    prog.TextColumn("[progress.description]{task.description}"),
    prog.BarColumn(),
    prog.TimeElapsedColumn(),
)


def get_zcat_command() -> str:
    """
    Checks if zcat or gzcat exist on the machine, returns whichever is functional!
    """
    try:
        subprocess.run("zcat --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        try:
            subprocess.run("gzcat --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            raise Exception(
                "Error when attempting to run zcat or gzcat command for k-mer counting."
            )
        else:
            return "gzcat"
    else:
        return "zcat"


def check_jellyfish():
    """
    Checks if Jellyfish is installed by running it's help command.

    Does nothing if Jellyfish is installed, raises an exception if Jellyfish is not found.
    """
    try:
        subprocess.check_output("jellyfish --help", shell=True)
    except subprocess.CalledProcessError:
        raise Exception("Jellyfish not found. Please install Jellyfish to count kmers.")


def try_command(command: str, err_msg: str):
    """
    Runs and command and if there's an error, raises an exception with the provided error message.
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"{err_msg}{e}")


def fastq_to_kmer_counts(
    input_paths: List[str],
    kmer_length: int,
    output_dir: Optional[str] = None,
    threads: int = 10,
    hash_size: int = 100_000_000,
) -> str:
    """_summary_

    Args:
        input_paths (List[str]): The input `fastq` or `fq` files to count.
        kmer_length (int): The length of the k-mers to count.
        output_dir (Optional[str], optional): The directory to put the counts file. Defaults to None (equivalent to current working directory).
        threads (int, optional): The number of threads to count with. Defaults to 10.
        hash_size (int, optional): The hash_size for Jellyfish counting. Defaults to 100_000_000.

    Raises:
        CalledProcessError: If a jellyfish command throws a runtime error.
        ValueError: If threads or hash_size or not a postiive integer
        NotADirectoryError: If output_dir is not a value directory

    Returns:
        str: The path of the output counts file
    """
    check_jellyfish()
    
    if type(kmer_length) is not int:
        raise TypeError("Jellyfish: kmer_length must be a positive integer.")
    elif kmer_length < 1:
        raise ValueError("Jellyfish: kmer_length must be a postive integer")
    
    if type(threads) is not int:
        raise TypeError("Jellyfish: Number of threads must be a positive integer.")
    elif threads < 1:
        raise ValueError("Jellyfish: Number of threads must be a postive integer")

    if type(hash_size) is not int:
        raise TypeError("Jellyfish: hash_size must be a positive integer.")
    elif threads < 1:
        raise ValueError("Jellyfish: hash_size must be a postive integer")
    
    for path in input_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Jellyfish: Input file '{path}' for counting does not exist.")
    
    # uses the accession number as the base name of the file
    base_path = f"{os.path.basename(input_paths[0].replace('_1', ''))}"

    if output_dir is not None:
        if not os.path.exists(output_dir):
            raise NotADirectoryError(f"Jellyfish: Counts file output directory '{output_dir}' does not exist.")

        base_path = f"{output_dir}/{base_path}"

    # Modify the file extension to .jf for the output
    jf_file = base_path.replace(".fastq", f"_{kmer_length}.jf").replace(".gz", "")

    # The base command for kmer counting
    count_command = (
        f"jellyfish count -m {kmer_length} -s {hash_size} -C -t {threads} -o {jf_file}"
    )

    # modifies the base command depending on if the files are zipped or not
    if input_paths[0].endswith(".fastq.gz"):
        zcat_command = get_zcat_command()
        count_command = (
            f"cat {' '.join(input_paths)} | {zcat_command} | {count_command} /dev/fd/0"
        )
    else:
        count_command = f"{count_command} {' '.join(input_paths)}"

    # Run count and dump jellyfish commands
    with Progress(*PROGBAR_COLUMNS) as progress:
        task = progress.add_task(f"Counting {kmer_length}-mers...", total=None)

        try_command(count_command, err_msg="Jellyfish: Error running 'jellyfish count' command: ")

        counts_file = jf_file.replace(".jf", ".counts")
        dump_command = f"jellyfish dump -c {jf_file} > {counts_file}"

        try_command(dump_command, err_msg="Jellyfish: Error running 'jellyfish dump' command: ")
        progress.update(task, total=1, advance=1)

    os.remove(jf_file)

    return counts_file


def is_counts_file(file_path: str) -> bool:
    """Checks if a file at the provided path is in the same format as a counts file.

    NOTE: This does not check every line, it only looks at the first to see if it matches the "KMER COUNT" format
    of a 'jellyfish dump' output.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: Whether the file starts as a proper jellyfish counts file output.
    """
    try:
        with open(file_path, "r") as f:
            first_line = f.readline()
            split = first_line.split()
            return split[0].isalnum() and split[1].isnumeric()
    except Exception:
        return False


def try_fastq_to_kmer_counts(input_paths: List[str], **kwargs) -> str:
    """
    Attempts to run fastq_to_kmer_counts but catches the error if the keyward arguments throw an error.

    Args:
        input_paths (List[str]): The list of fastq input paths
    """
    try:
        return fastq_to_kmer_counts(input_paths, **kwargs)
    except Exception as e:
        if "unexpected keyword argument" in str(e):
            bad_key = str(e).split("'")[1]
            raise KeyError(f"Jellyfish: '{bad_key}' is not a valid argument for counting kmers.")
        elif "required" in str(e):
            bad_key = str(e).split("'")[1]
            raise KeyError(f"Jellyfish: '{bad_key}' argument is required for counting kmers.")
        else:
            raise e