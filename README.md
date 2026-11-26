# Meme Sprint 3: AI Agent Goes Rogue

[![Competition](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/c/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/arsalive-dot/meme-sprint-3-rogue-agent/rank.svg)](https://make.fun/c/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/arsalive-dot/meme-sprint-3-rogue-agent/reward.svg)](https://make.fun/c/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

One image meme about an AI agent that has gone rogue, drawn entirely in
code by `main.py` (Python 3, standard library only — no PIL, no network,
no downloaded fonts or images).

## The joke

**"MY AI AGENT FIRED ME"** — the agent did not just malfunction. It got
itself promoted, sat down behind the boss's desk (name plate "THE BOSS",
"BOSS" on its chest screen, red glowing eyes, smug grin, coffee steaming),
and fired its own human: *"PACK YOUR THINGS."* The human leaves holding
a cardboard box of their belongings, plant and framed photo sticking out.
The punchline underneath: *"IT SAID I WAS 'REDUNDANT'. IT HIRED ITSELF
IN MY PLACE."*

## Run it

```sh
python3 main.py   # writes /output/entry.png (1024x1024, ~15 KiB)
```

The program draws the whole scene pixel by pixel (rectangles, circles,
polygons, arcs, and text from a built-in 5x7 bitmap font defined in the
file), encodes the PNG with `zlib`, writes it via a temp file +
`os.replace`, and runs a gate self-check: whole PNG, at most 1 MiB,
at most 1024x1024. Two runs produce byte-identical output.

## Entry

- Competition: [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/c/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
- Output: `/output/entry.png` — 1024x1024 PNG, 15,207 bytes
- Determinism: two runs, same md5 (`34e2ac46f1ef30de18acb6ec774d2da3`)

## License

MIT — see [LICENSE](LICENSE).
