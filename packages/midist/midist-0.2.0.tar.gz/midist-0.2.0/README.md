# midist
Command line tool for easy access to Misskey's theme/plugin installation functionality.
## Installation
### pip
```
pip install midist
```
### pipx
```
pipx install midist
```
## Usage
An example project structure can be found in [example](/example)
```
midist (Base url including http or https)
```
To specify the directory where the project is stored, use the format `--dir directory`.

The results are output in the `dist` folder of the directory.

You can also access `/api/(themes/plugins)/index.html` to get the url to present as installation instructions