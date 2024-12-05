import os
import requests
from ftplib import FTP
from typing import List, Optional

import rich.progress as prog
from rich.progress import Progress

PROGBAR_COLUMNS = (
    prog.SpinnerColumn(),
    prog.TextColumn("[progress.description]{task.description}"),
    prog.BarColumn(),
    prog.DownloadColumn(),
    prog.TaskProgressColumn(),
    prog.TimeElapsedColumn(),
)

class NoAccessionsFoundError(Exception):
    """An error for when no accessions are able to be found in a text file or provided list."""
    pass

def get_run_accessions(accessions: List[str] | str):
    """
    Given a list of accessions (with possible project accessions) or a file path
    to a text file of accession numbers, returns a list of run accessions.

    Args:
        accessions (List[str] | str): Either a list of run or project accessions numbers 
            or a file path to a text file of accession numbers.

    Raises:
        TypeError: If the accessions is not a list of strings or a str
        FileNotFoundError: If the accessions file path does not exist.

    Returns:
        _type_: _description_
    """
    if not isinstance(accessions, (list, str)):
        raise TypeError(
            "Value for key 'accessions' in config file must be a list of strings or a string."
        )

    if isinstance(accessions, list):
        if not all(isinstance(item, str) for item in accessions):
            raise TypeError(
                "List of accessions in config file must be a list of strings."
            )

    # we know this will be a string format. we can check if it is a valid file path then parse throught the file
    elif isinstance(accessions, str):
        if accessions != "" and os.path.exists(accessions):
            # extract accession numbers from file into a list and set it to accession_list_config
            with open(accessions, "r") as f:
                acc_nums = f.readlines()
            accessions = [acc.strip() for acc in acc_nums]
        else:
            raise FileNotFoundError(
                "File path for accessions is invalid or does not exist."
            )

    run_accessions = []

    for accession in accessions:
        if accession[:3] == "PRJ":
            run_accessions.extend(get_project_accessions(accession))
        else:
            run_accessions.append(accession)

    if run_accessions == []:
        raise NoAccessionsFoundError("No accession numbers found.")

    return run_accessions


def get_project_accessions(prj_accession: str) -> List[str]:
    """
    Takes a project accession number and returns a list of run accessions associated with the project.

    Args:
        prj_accession (str): A project accession number (often starts with "PRJ").

    Returns:
        List[str]: A list of run accessions associated with the project.
    """
    url = f"https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=study_accession={prj_accession}&fields=run_accession"
    
    try:
        response = requests.get(url)
    except ConnectionError:
        raise ConnectionError(f"Could not find provided project accessions: {prj_accession}")

    content = response.content.decode()
    lines = content.splitlines()[1:]  # ignore the header line

    # get the first value in a line (the accession)
    return [line.split("\t")[0] for line in lines]


def download_fastq(run_accession: str, output_dir: Optional[str] = None) -> List[str]:
    """
    Downloads fastq.gz files from the ENA FTP server using an accession number.
    Returns a list of the local file paths of the downloaded files.

    Args:
        run_accession (str): A valid ERR, SRR, and DRR run acccession number.
        output_dir (str, optional): The optional directory where the downloaded files will go. 
            If None, will download files to the current working directory. Defaults to None.

    Returns:
        List[str]: A list of local file paths to the downloaded files.
    """
    # small argument validations for the accession parameter
    if (
        type(run_accession) is not str
        or not run_accession.isalnum()
        or len(run_accession) < 9
        or len(run_accession) > 11
    ):
        raise ValueError(
            f"Invalid accession number: {run_accession}. \n"
            "Valid accession numbers have between 9 and 11 characters while containing only numbers or letters."
        )
    try:
        ftp = FTP("ftp.sra.ebi.ac.uk")
    except ConnectionError:
        raise ConnectionError("Failed to connect to ENA database. Please check your connection and try again.")
    
    try:
        ftp.login()

        prefix = run_accession[:6]
        suffix = run_accession[6:]

        directory = f"/vol1/fastq/{prefix}/"

        # handles different format of directory for accession numbers
        match len(suffix):
            case 3:
                directory += f"{run_accession}"
            case 4:
                directory += f"00{suffix[-1]}/{run_accession}"
            case 5:
                directory += f"0{suffix[-2:]}/{run_accession}"

        try:
            ftp.cwd(directory)
        except Exception:
            raise NotADirectoryError(
                f"Failed to access the directory for the provided accession number of {run_accession}.\n"
                "Please ensure that the accession number is correct and the corresponding FASTQ files are available on ENA."
            )

        file_names = ftp.nlst()
        if file_names == []:
            raise FileNotFoundError(f"No files found for the accession number: {run_accession}.")

        if output_dir is not None:
            if not os.path.exists(output_dir):
                raise NotADirectoryError("Output directory given for downloading files does not exist.")
            
        output_files = []

        with Progress(*PROGBAR_COLUMNS) as progress:
            for file_name in file_names:
                size = ftp.size(f"{file_name}")
                task = progress.add_task(f"Downloading {file_name}", total=size)

                # build local file path
                if output_dir is not None:
                    local_file_path = os.path.join(output_dir, file_name)
                else:
                    local_file_path = file_name

                output_files.append(local_file_path)

                # skip download if the entire file already exists
                if (
                    os.path.isfile(local_file_path)
                    and os.path.getsize(local_file_path) == size
                ):
                    progress.update(task, advance=size)
                    continue

                try:
                    with open(local_file_path, "wb") as f:

                        def callback(data):
                            f.write(data)
                            progress.update(task, advance=len(data))

                        ftp.retrbinary(f"RETR {file_name}", callback)

                except Exception:
                    raise ConnectionError(
                        f"Download failed to complete for the accession number: {run_accession}.\n"
                        "Please check your connection and try again."
                    )
        return output_files
    finally:
        ftp.close()
