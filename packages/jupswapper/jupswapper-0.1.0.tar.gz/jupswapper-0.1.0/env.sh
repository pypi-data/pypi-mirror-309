
alias create_venv="uv venv --python 3.12"
alias activate_venv="source .venv/bin/activate"
alias pip="uv pip"
alias pipinstall="pip install -e ."

if [ -d ".venv" ]; then
    activate_venv
fi


export SECRET_WORDS="op://Personal/Worker1/recovery phrase"
export HELIUS_API_KEY="op://Personal/HELIUS_API_KEY/credential"

alias swap="op run -- uv run examples/swap_sol_for_bonk.py"
alias wallet="op run -- uv run examples/wallet.py"

# build and publish
alias install_twine="pip install build twine"
alias build="python -m build"
alias publish="python -m twine upload dist/*"
