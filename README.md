# A data bot for collecting stuff from [RobotEvents' api](https://www.robotevents.com/api/v2), and a discord bot to interface with it.

Created by: [Isaac Pruett](https://github.com/Isaac-Pruett)

If you intend to host the bot, ensure you have [just](https://just.systems) and [uv](https://docs.astral.sh/uv/) installed on your system. 

## Using the discord bot:
```
$summary <teamname> <start yr> <end yr> <program code>
```
EX:
```
$summary cpslo
```

```
$summary cpslo 2024 2025 vurc
```

```
$summary CPSLO 2025 2026 vUrC
```

## Running the bot:
Ensure that you have a `.env` file in the project root as such:
```
DISCORD_TOKEN=your_token_here
RECF_TOKEN=your_token_here
```
Start the bot:
```
just discord
```
```
just d
```

## Reset all data:
```
just nuke
```

## Show the elo-strength-of-schedule graph for a given year

```
just e <start yr> <end yr> <program code>
```
EX:
```
just e 2024 2025 VURC
```
