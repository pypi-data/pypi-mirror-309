import os
import toml
from typing import Any, Optional

from pylagg import ena, jellyfish, cgr
from pylagg.cutadapt import trim

class MissingConfigSection(KeyError): 
    pass

def load_toml_file(config_file: str) -> dict:
    """
    Reads a TOML file and returns a dictionary of the contents.
    """
    if not os.path.isfile(config_file):
        raise FileNotFoundError(
            f"No config file found at '{config_file}'. Please ensure you have given the correct path."
        )

    # read the TOML file
    try:
        config = toml.load(config_file)
    except Exception:
        raise toml.TomlDecodeError(
            "An error occurred while reading the TOML config file. Please ensure it is a valid TOML file."
        )

    return config

def get_config_key(config: dict, key: str) -> Any:
    """
    Checks if a config dictionary contains a key and it isn't empty.

    Args:
        config (dict): A dictionary of the config
        key (str): The key to search for

    Raises:
        KeyError: If the key is not found in the dictionary
        ValueError: If the key is found but is empty

    Returns:
        The value of the key in the config.
    """
    if key not in config:
        raise KeyError(f"Config error: {key} not found in config.")
    
    if config[key] is None or config[key] == {}:
        raise ValueError(f"Config error: {key} is empty.")
    
    return config[key]


def config_accession_to_cgr(config_file: str, output_dir: Optional[str] = None):
    """
    Takes a path to a config file and generates an image using the data.

    Args:
        config_file (str): The path to the config file
    """
    config = load_toml_file(config_file)

    download_args = get_config_key(config, "download")
    accession_arg = get_config_key(download_args, "accessions")
    accession_list = ena.get_run_accessions(accession_arg)
    
    for accession_number in accession_list:
        fastq_files = ena.download_fastq(accession_number, output_dir)

        jellyfish_args = get_config_key(config, "jellyfish")

        if output_dir is not None:
            jellyfish_args["output_dir"] = output_dir

        # Check if the 'cutadapt' section exists
        if "cutadapt" in config:
            trimmed_file = trim(fastq_files, config)
            
            counts_path = jellyfish.try_fastq_to_kmer_counts([trimmed_file], **jellyfish_args)

            # will activate if trim key is missing or equals "False"
            if not config.get("files", {}).get("trim", False):
                os.remove(trimmed_file)

        else:
            counts_path = jellyfish.try_fastq_to_kmer_counts(fastq_files, **jellyfish_args)

        cgr_args = config.get("cgr", {})
        with open(counts_path, "r") as f:
            try:
                cgr.count_file_to_image_file(f, counts_path.replace(".counts", ".png"), **cgr_args)
            except Exception as e:
                if "unexpected keyword argument" in str(e):
                    bad_key = str(e).split("'")[1]
                    raise KeyError(f"CGR: '{bad_key}' is not a valid argument for generating images.")
                else:
                    raise e

        if not config.get("files", {}).get("fastq", False):
            for files in fastq_files:
                os.remove(files)

        if not config.get("files", {}).get("counts", False):
            os.remove(counts_path)
