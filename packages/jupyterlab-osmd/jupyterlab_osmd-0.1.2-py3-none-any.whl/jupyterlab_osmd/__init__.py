import requests
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path
from typing import Union, Optional
from IPython.display import display

try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'jupyterlab_osmd' outside a proper installation.")
    __version__ = "dev"


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "jupyterlab-osmd"
    }]


def OSMD(data: Union[str, Path, bytes] = "") -> Optional[str]:
    """
    Load and display MusicXML data from various sources.

    Args:
        data: Can be a URL, file path, .mxl file, or direct MusicXML text

    Returns:
        The MusicXML data as a string, or None if loading fails
    """
    musicxml_data: Optional[str] = None

    try:
        # Handle URL input
        if isinstance(data, str) and data.startswith("http"):
            response = requests.get(data)
            response.raise_for_status()
            musicxml_data = response.text

        # Handle file path input
        elif isinstance(data, Path) or (
            isinstance(data, str) and not data.startswith("<") and Path(data).is_file()
        ):
            path = Path(data)

            # Handle .mxl compressed files
            if path.suffix == ".mxl":
                with zipfile.ZipFile(path, "r") as zip_ref:
                    # Look for container.xml to find the root file
                    if "META-INF/container.xml" in zip_ref.namelist():
                        container_xml = zip_ref.read("META-INF/container.xml").decode(
                            "utf-8"
                        )
                        root = ET.fromstring(container_xml)

                        # Find the rootfile path
                        rootfile = root.find(".//rootfile")
                        if rootfile is not None:
                            rootfile_path = rootfile.get("full-path")

                            # Read the actual MusicXML file
                            if rootfile_path and rootfile_path in zip_ref.namelist():
                                musicxml_data = zip_ref.read(rootfile_path).decode(
                                    "utf-8"
                                )
                            else:
                                raise ValueError(
                                    f"Rootfile {rootfile_path} not found in archive"
                                )
                        else:
                            raise ValueError("No rootfile found in container.xml")
                    else:
                        raise ValueError("No container.xml found in .mxl archive")

            # Handle .musicxml files
            elif path.suffix in [".musicxml", ".xml"]:
                with open(path, "r", encoding="utf-8") as f:
                    musicxml_data = f.read()

            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")

        # Handle direct MusicXML string input
        elif isinstance(data, str) and data.startswith("<"):
            musicxml_data = data

        else:
            raise TypeError(
                "Invalid input type. Expected URL, file path, or MusicXML text."
            )

        # Display the MusicXML data
        if musicxml_data:
            bundle = {"application/vnd.recordare.musicxml": musicxml_data}
            display(bundle, raw=True)
            # return musicxml_data

    except Exception as e:
        print(f"Error processing MusicXML data: {e}")
        return None
