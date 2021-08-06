# evtx-hunter-linux

[Origin Evtx-hunter](https://github.com/NVISOsecurity/evtx-hunter)

# Requirements

It requires Python (tested in ``python 3.9`` but any version ``>=python 3.0`` will most likely work).

# Installation
```
pip install -r requirements.txt
```

# Usage
```
python evtx_hunter.py <evtx_folder>
```
Once the EVTX files have been processed, a link on the command line will be printed to view the
generated report in your browser (typically http://127.0.0.1:8050/).

## External libraries
- EVTX Parsing: https://github.com/omerbenamram/EVTX

## License
sc-evtx-parser is released under the GNU GENERAL PUBLIC LICENSE v3 (GPL-3).
[LICENSE](LICENSE)
