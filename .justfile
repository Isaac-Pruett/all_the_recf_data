alias e := matches
alias r := run
alias d := discord

set dotenv-load := true

# default
list:
    just --list

install:
    @uv sync
    @mkdir -p data
    @mkdir -p savedata

# wrapper to run uv
run FILE:
    uv run {{ FILE }}

# cleans the uv cache
clean:
    rm -rf .venv __pycache__

# resets entire project
nuke: clean reset
    @echo NUUUUUUUUUUKED

alias re := reset

# resets the data cache
reset:
    rm -rf data savedata
    mkdir data
    mkdir savedata

# creates graph for season
matches START END CODE:
    uv run elo_sos_season_graph.py {{ START }} {{ END }} {{ CODE }}

# runs the discord bot
discord: install
    @uv run discordbot.py
