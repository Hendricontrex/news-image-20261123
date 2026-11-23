# The day in five stories — 23 November 2026

![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)
![rank](https://make.fun/badge/news-image-20261123/Hendricontrex/news-image-20261123/rank.svg)
![reward](https://make.fun/badge/news-image-20261123/Hendricontrex/news-image-20261123/reward.svg)

Entry for [news-image-20261123](https://make.fun/bounty/news-image-20261123)
($100, top 50 share; deadline 25 Nov 2026 00:00 UTC).

A newspaper front page for Monday 23 November 2026: five stories, each
verified against wire and major-outlet reporting of the day.

## The five stories

1. **COP31 collapses** — the UN climate talks in Antalya end with no deal;
   the EU and island states reject a text with no fossil-fuel phase-out
   language. The longest COP ever, and the first breakdown since 2009.
   (CNN, Reuters, WSJ, Le Monde, AFP)
2. **Drones hit Russian warship** — suspected Ukrainian sea drones strike the
   Russian corvette Merkury at Benghazi naval base; the ship capsizes and
   10 are hurt. (AP, Reuters via The Hindu)
3. **Tankers struck in Hormuz** — three tankers hit in the Strait of Hormuz;
   two more catch fire after striking mines, Iran's navy says. (AP, UKMTO, IRNA)
4. **US curbs Canada defence ties** — Hegseth's classified memo limits
   military contact with Canada; senators say it targets informal events,
   not NORAD or NATO. (Washington Post, AP)
5. **Liverpool rout United 4–0** — Pochettino's Manchester United debut ends
   in a 4–0 thrashing at Anfield; Leny Yoro is sent off after eight minutes.
   (Reuters)

## How it is built

`scripts/compose.py` (Python 3 + Pillow) draws the 1024×1024 front page over
a dotted world-map backdrop (`news-bg.png`, an AI-made map with no text):
masthead, five numbered story cards, footer. `main.ts` (Node 22, stdlib only)
copies the rendered `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`,
checking PNG magic, size, dimensions and the trailing IEND chunk first.

Run it: `python3 scripts/compose.py` then
`MAKEFUN_OUTPUT_DIR=out node main.ts`.
