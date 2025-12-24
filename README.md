# A data bot for collecting stuff from RobotEvents' api, and a discord bot to interface with it.

If you intend to host, ensure you have `just` and `uv` installed on your system. 

## Using the discord bot:
```
$summary <teamname> <start> <end> <program code>
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
