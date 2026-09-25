# Book intake and verification

Updated 2026-09-15. Full PDFs and generated text remain under ignored `out/`; `book_dump/` is ignored to prevent accidental redistribution or repository commits.

## Intake status

| Local item | Result | SHA-256 / notes |
|---|---|---|
| `book_9780262298247.pdf` | *Engineering a Safer World*; readable, 555 PDF pages; title and author metadata match the MIT Press open-access edition | `df4264b58711387dfa9336f37a14830ac48c9c68a77453d85fd1fad6b332ae78`; metadata verified, canonical byte comparison not claimed because the MIT endpoint returned an HTML access page during this pass |
| `978-3-662-48847-8.pdf` | *Autonomous Driving: Technical, Legal and Social Aspects*; exact match to Springer’s canonical open-access PDF | `c8c67543f88fcd81f42309880969f5528f3afb6e156e20bfc345c05b1ebe9457`; local and canonical files are byte-identical |
| Two `Verifiable Autonomous Systems` PDFs | Byte-identical duplicates; one normalized copy retained under `out/sources/book_intake/books/` | `496ff49e8d9bd7be19026f8bf64b46ca21c9b9bc20a09ff258c741ea3e00d26e`; 391 PDF pages |
| `Probabilistic Robotics` PDF | Readable 493-page early draft, not the published edition | `f1163d23db38cc3c3eef5d7177079eb55cc002164f47ba4a84524eb2969df73c`; opening page says “EARLY DRAFT—NOT FOR DISTRIBUTION” |
| FAA primary documents | Five supplied public authority PDFs were normalized into `out/sources/book_intake/authority/`, with UTF-8 extractions under `out/sources/book_intake/text/` | Zipline 19111B/19111C, Amazon 19031B, TSO-C211a and the NHTSA AQ26002 opening resume; the Zipline/TSO/Texas records are new compiler inputs and the existing NHTSA record now has full local context |
| `deeplearningbook.org` | 28 linked HTML pages scraped, preserved, and converted to clean page-aware text | Raw HTML, cleaned text, and a SHA-256 manifest are under `out/sources/deep_learning_book/` |

## Generated working formats

- Intake PDF snapshots and extracted text: `out/sources/book_intake/`
- Deep Learning raw public HTML: `out/sources/deep_learning_book/site/`
- Deep Learning cleaned text with page boundaries: `out/sources/deep_learning_book/clean_text/`
- Deep Learning retrieval manifest: `out/sources/deep_learning_book/manifest.json`
- Reproducible PDF2HTML extractor: [`clean_deeplearningbook_html.py`](tools/clean_deeplearningbook_html.py)

The generic Pandoc output was discarded because the site uses pdf2htmlEX layout markup. The structure-aware extractor reads the page text blocks directly and produces searchable text without carrying the renderer’s positioning overlays.

## Research use

The current books now have source records `S-016` through `S-020` in `research/sources.json`. They are background and method sources, not substitutes for FAA, EASA, NHTSA, state, or operator primary records.

The two Dennis/Fisher copies are byte-identical duplicates. The two local *Probabilistic Robotics* PDFs are alternate early-draft copies; neither is a publication-ready source. Keep both original files in `book_dump/`, use the normalized 493-page working copy only for internal background reading, and cite an official edition or primary paper for public claims.

The most useful initial reading targets are:

- Leveson, Chapters 4, 7–10 and 12: safety constraints, hazards, STPA, system engineering, assumptions, certification, and change control.
- *Autonomous Driving*, Part IV, Chapters 20–23: machine perception, release, learning, and safety concepts.
- *Verifiable Autonomous Systems*, Chapters 5, 9, 11 and 12: autonomous choices, unmanned-air-system certification examples, compositional verification, and runtime verification.
- *Probabilistic Robotics*, Chapters 8–10 and 15–16: sensor models, occupancy grids, SLAM, decision-making, and partial observability. Treat the local draft as provisional.
- *Deep Learning*, Chapters 3, 5, 7, 9, 11, 12, 15 and 19: probability, validation, regularization, vision, methodology, representation learning, and approximate inference. Use the public chapter pages rather than creating or distributing a PDF.

## Still critical to obtain or identify

1. **Aircraft System Safety: Assessments for Initial Airworthiness Certification — Duane Kritzinger.** Needed for the aviation safety-assessment workflow, GSN, FHA, fault trees, FMEA, common-mode analysis, development assurance, and continuing safety. Publisher: [Elsevier](https://shop.elsevier.com/books/aircraft-system-safety/kritzinger/978-0-08-100889-8).
2. **Initial Airworthiness: Determining the Acceptability of New Airborne Systems — Guy Gratton.** Needed to explain airworthiness, certification boundaries, and civil/military approval practice. Publisher: [Springer](https://link.springer.com/book/10.1007/978-3-319-75617-2).
3. **Sensing and Control for Autonomous Vehicles: Applications to Land, Water and Air Vehicles — Fossen, Pettersen and Nijmeijer, eds.** Needed for the road-to-flight bridge: navigation, sensing, tracking, and motion control across land and air. Publisher: [Springer](https://link.springer.com/book/10.1007/978-3-319-55372-6).

The first two are the most important gaps. They should be acquired through a library, publisher, or other legitimate licensed source. Until then, the project should cite the existing FAA/NASA/EASA sources for regulatory and assurance claims rather than infer aviation practice from the books already available.
