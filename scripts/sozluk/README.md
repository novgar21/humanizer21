# Turkmen word list

`tk_TM.aff.gz` and `tk_TM.dic.gz` are the Hunspell affix and dictionary files of
[nazartm/turkmen-spell-check-dictionary](https://github.com/nazartm/turkmen-spell-check-dictionary)
(commit 07912a9), compressed with gzip and otherwise unchanged. They are
licensed under the Apache License 2.0; see `LICENSE` in this folder.

`gosmaca.txt` is ours (MIT, like the rest of humanizer21): correct Turkmen words the
dictionary does not know, one per line. A line `stem/model` gives a stem the same
endings as an existing word of the dictionary (`olimpiada/mekdep` would be wrong,
because harmony differs; pick a model with the same last vowel and final sound).

`barla.py --dict` uses both files. A word the list does not know is only a note:
check it, do not change it because of the list.
