# My site

URL: <https://pages.michinobu.jp>

## Development

### Prerequisites

- `pyenv` or Python >= 3.9
- `nvm` or Node.js >= 16

### Initialize

```bash
git clone git@github.com:MichinobuMaeda/MichinobuMaeda.github.io.git
cd MichinobuMaeda.github.io
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm install
```

### Build and test locally

```bash
npm run build && npm run preview
```
