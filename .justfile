alias e := event
alias r := run
alias d := discord

set dotenv-load := true

# default
list:
    just --list

run FILE:
    uv run {{ FILE }}

# gets event graph
event:
    uv run get_event_deets.py

clean:
    rm -rf .venv __pycache__

nuke: clean
    rm -rf data savedata
    mkdir data
    mkdir savedata

matches START END CODE:
    uv run elo_sos_season_graph.py {{ START }} {{ END }} {{ CODE }}

skills START END CODE:
    uv run elo_skills_data.py {{ START }} {{ END }} {{ CODE }}

discord:
    @uv run discordbot.py
