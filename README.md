# michinobumaeda.github.io

## Development

### Prerequisites

- Markdown to HTML
    - `pyenv` or Python >= 3.9
- Tailwind To CSS
    - `nvm` or Node.js >= 16

### Initialize environment

```bash
git clone git@github.com:MichinobuMaeda/MichinobuMaeda.github.io.git
cd MichinobuMaeda.github.io
python -m venv .venv
npm install
```

### Use environment

```bash
. .venv/bin/activate
pip install -r requirements.txt
```

Generate indexes manually

```bash
python mkindex.py
```
