"""Taller evaluable"""

from glob import glob
import pandas as pd
import os


def load_input(input_directory: str) -> pd.DataFrame:
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    files: list[str] = glob(os.path.join(input_directory, "*.txt"))
    dataframes: list[pd.DataFrame] = [
        pd.read_csv(file, names=["linea"], sep="\t", header=None) for file in files
    ]
    return pd.concat(dataframes, ignore_index=True)


def clean_text(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe["linea"] = (
        dataframe["linea"].str.replace("[^A-Za-z0-9\s]", "", regex=True).str.lower()
    )
    return dataframe


def count_words(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Count words"""
    #
    # Cuente el número de palabras en el texto.

    serie = dataframe["linea"].str.split(expand=True).stack().value_counts()
    dataframe = pd.DataFrame({"word": serie.index, "count": serie.values})
    dataframe = dataframe.sort_values(by="word")
    return dataframe


def save_output(dataframe: pd.DataFrame, output_filename: str) -> None:
    """Save output to a file."""
    dataframe.to_csv(output_filename, header=False, index=False, sep="\t")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory: str, output_filename: str) -> None:
    dataframe: pd.DataFrame = load_input(input_directory)
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_filename)
    """Call all functions."""


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
