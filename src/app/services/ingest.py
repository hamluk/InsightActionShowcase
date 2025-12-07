import os

from src.app.config import Settings


def show_files(
        settings: Settings
):
    """
    Main function to show files. Only returning fixed string of uploaded file.
    This Demo is not providing the functionality to uplaod files
    :param settings:
    :return:
    """
    list_of_files = ["Unilever Annual Report 2022.pdf"]

    return {"files": list_of_files}
