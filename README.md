# Sum up 22 November's world news in one image

Entry for the make.fun competition `news-image-20261122`
("Sum up 22 November's world news in one image", $100, top 50 share the prize).

## The image

`entry.png` (1024 × 1024, under 1 MiB) is a newspaper front page for
Sunday 22 November 2026: 31 stories from six continents, grouped by region
with a field tag on each item.

- **Lead:** COP31 climate talks in Antalya collapse with no deal.
- **Diplomacy:** Trump, Xi and Putin hold the first trilateral summit in Shenzhen.
- **Middle East:** Iran strikes tankers near the Strait of Hormuz and US bases
  in Bahrain; Gaza strike; settler attacks in the West Bank.
- **Europe & Ukraine:** Ukraine sinks a Russian warship off Libya; missile
  hits Kryvyi Rih; Russian missiles land in Poland; UK–EU reset deal.
- **Asia-Pacific:** Lowy Asia Power Index; China's chipmakers; Nvidia probe;
  Thai court verdict; Indonesia factory fire; Shuri Castle reopens.
- **Americas:** cartel boss captured in Mexico; US stocks in correction;
  Peru earthquake.
- **Markets & Trade:** EU–Indonesia trade deal; China margin rules; AI
  sell-off spreads to Japan and Korea.
- **World Court & Africa:** ICJ genocide ruling on Myanmar; Nigeria boat
  disaster; Rohingya reaction.

All headlines are factual summaries of reporting from 22 November 2026
(AP, Reuters, AFP, Al Jazeera and others). No photorealistic imagery, no
invented scenes, no exaggerated headlines.

## How it was built

`build_frontpage.py` renders the page with Pillow from the story list
(plain text, deterministic layout). `main.py` is the entry program: it
copies the bundled `entry.png` to `/output/entry.png`, byte for byte.

## Run

```sh
python3 main.py   # writes /output/entry.png
```

No network access needed. Running it twice produces identical bytes.

## License

MIT — see `LICENSE`.
