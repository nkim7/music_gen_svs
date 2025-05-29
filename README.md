# Educational Song Composition with LLMs & Synthesised Vocals

> **Bachelor Project — École Polytechnique Fédérale de Lausanne (EPFL) · CHILI Lab**
> **Author:** *Nagyung Kim*   
> Project code‑name: **LLM‑Powered Educational Songwriting**

---

## 📖 Overview

This project automates the creation of **children‑friendly educational songs**.
From a two‑word prompt (*mood* + *topic*), the pipeline delivers in **< 60 seconds**:

* GPT‑generated **lyrics** & **chord loop**
* MIDI **melody + accompaniment**
* AI‑sung **vocal track** (OpenUtau × DiffSinger)
* **PDF lead sheet** and fully‑mixed **WAV** file

The system targets teachers and pupils alike: teachers can illustrate new concepts without musical expertise, while pupils can explore composition interactively via a chatbot or survey interface.

---

## 🧩 Architecture at a Glance

```
┌─ React Native App ─────────────┐
│  mood + topic                  │
└─────────────┬──────────────────┘
              ▼ REST (Flask)
┌──────────────────────────────────────────────┐
│ 1 · Prompt Handler (GPT‑4o)                  │
│   ↳ tempo · 8‑chord cycle                   │
│                                              │
│ 2 · Choose Model                             │
│   A) static melody · dynamic lyrics          │
│   B) static lyrics  · dynamic music          │
│                                              │
│ 3 · Lyrics & Syllable Balancer               │
│ 4 · midi_gen → melody & accompaniment        │
│ 5 · ust_gen  → USTX (phoneme fixes)          │
│ 6 · OpenUtau (WORLDLINE‑R) → vocal.wav       │
│ 7 · FluidSynth + pydub → stems & final mix   │
└──────────────────────────────────────────────┘
              ▼
  Chatbot   or   Survey ➜ iterative refinement
```

---

## 🔬 Two Generation Modes

| Mode  | What Stays Fixed | What Varies | Ideal For                 | Key Trade‑offs                                      |
| ----- | ---------------- | ----------- | ------------------------- | --------------------------------------------------- |
| **A** | Melody           | Lyrics      | short, high‑quality songs | Lyric length must be shoe‑horned to melody (slower) |
| **B** | Lyrics           | Music       | longer, fast turnaround   | Music risk of repetition; pauses in sparse text     |

> *Empirical benchmark*: Model B keeps generation time almost flat as lyric length grows, while Model A time rises linearly but yields more polished music for ≤ 8 lines.

---

## 🚀 Quick Start

```bash
# clone & install
$ git clone https://github.com/<your‑fork>/educational‑song‑llm.git
$ cd educational‑song‑llm
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt

# generate in one go
$ python main.py "happy" "bears"

# or via REST
$ python api_server.py &
$ curl -X POST http://localhost:5000/generate-music -H "Content-Type: application/json" \
       -d '{"mood":"calm","topic":"rainforests"}'
```

Outputs are written to `music/gen/demo_outputs/` and `final_music/` (WAV, MIDIs, USTX, PDF).

---

## 📱 Front‑End Highlights

* **Input screen** → mood & topic fields
* **Playback screen** → lyrics card, waveform seek/loop, stems toggle
* **Chatbot** → relevance checking, sentiment, fun facts, emoji cues
* **Survey** → 1‑tap Likert + free‑text; CSV export for classroom analytics

Younger children (≈ 7 y) preferred the concise **Survey**; older kids (10 – 14 y) spent more time and reported higher enjoyment with the **Chatbot** mode.

---

## 🛠 Requirements (tested)

| Tool          | Version                           |
| ------------- | --------------------------------- |
| Python        | 3.10 64‑bit                       |
| Node / npm    | ≥ 18 / 9                          |
| OpenAI API    | GPT‑4o access                     |
| FluidSynth    | 2.3 + FluidR3\_GM.sf2             |
| MuseScore CLI | 3.x                               |
| OpenUtau      | 0.1.529 + **Hanami VCCV‑EN** bank |
| Windows 10/11 | GUI automation (`uiautomation`)   |

---

## 📊 Results Snapshot

* **Generation time** (RTX T4, 16 bars) — 50 s average.
* **User study** (n = 4) — Chatbot mode preferred by older children; survey faster for younger pupils.
* **Audio quality** — DiffSinger shallow diffusion + phoneme offset hacks yielded noticeably clearer *it's / that's* articulation.

See full evaluation in the *Report* PDF (docs/).
Benchmarks reproduced in `/notebooks/`.

---

## 🔮 Roadmap

* Simplify chatbot language & add TTS for pre‑readers.
* Expand instrument palette & vocal styles.
* Accept **voice or drawing** prompts to seed songs.
* Replace brute‑force syllable balancer with dynamic programming to cut latency.

---

## 📜 License & Citation

Code released under **MIT**; third‑party models retain their own licenses.

Please cite if you use this work:

```bibtex
@bachelorthesis{kim2025educSongLLM,
  title  = {Educational Song Composition using Large Language Models with Synthesised Vocal Singing},
  author = {Kim, Nagyung and Tozadore, Daniel},
  school = {EPFL — CHILI Lab},
  year   = {2025}
}
```

---

Made with ☕ + ✨ in Lausanne.
