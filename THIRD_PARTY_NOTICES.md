# Third-party notices

## Humanizer by Siqi Chen

The general AI writing patterns in `references/ai-patterns.md`, the draft, audit and final workflow, and the voice-matching approach in `SKILL.md` are adapted from [Humanizer](https://github.com/blader/humanizer) by Siqi Chen. humanizer21 rewrites them for Turkmen, with Turkmen examples and genre rules, and adds the Turkmen spelling, grammar and interference rules.

Humanizer is distributed under the MIT License:

```
MIT License

Copyright (c) 2025 Siqi Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Humanizer in turn draws on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

## Ene dilim

The Turkmen orthography, morphology, punctuation and lexicon rules in `references/` are summarized in our own words from [Ene dilim](https://enedilim.com/) and are used with the permission of the Ene dilim project. No text or dictionary data from Ene dilim is copied into this repository.

## Turkmen spell-check dictionary by nazartm

`scripts/sozluk/tk_TM.aff.gz` and `scripts/sozluk/tk_TM.dic.gz` are the Hunspell files of [turkmen-spell-check-dictionary](https://github.com/nazartm/turkmen-spell-check-dictionary), compressed with gzip and otherwise unchanged. `barla.py --dict` reads them. They are distributed under the Apache License 2.0; the full license text is in `scripts/sozluk/LICENSE`. `scripts/sozluk/gosmaca.txt` (our additions) is part of humanizer21 and under its MIT License.
