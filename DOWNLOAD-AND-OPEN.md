# Download and open on a laptop

The [session-files-2026-10-05 release](https://github.com/collinmpage/flwers-helix-context/releases/tag/session-files-2026-10-05) contains the complete saved Ableton project and the eight recording references used for tone building. These downloads are public.

1. Download **every `Flwers-Ableton-Project-part-XX.zip`** asset from that release. Each ZIP is independently extractable; these are not split ZIP byte segments.
2. Extract all project ZIPs into **the same parent directory**. Their shared `FLWERS SET NOV 2026 for collin Project` folder must merge. Keep `Samples/Imported` and `Samples/Processed` beneath that project folder. Do not open the set from inside a ZIP.
3. Open **FLWERS SET NOV 2026 - Helix Snapshots CC69.als** in the merged project folder. This is the corrected version. `Helix Snapshots Test.als` contains the earlier CC67 bug; the original `for collin.als` retains the old preset-per-section MIDI behavior.
4. Install/use HX Edit and the applicable Helix USB driver. For USB testing, enable Ableton MIDI output **Line 6 Helix → Track**, set **Collin Helix → MIDI To: Line 6 Helix, Ch.2**, and enable Helix MIDI Over USB/Base Channel2/PC Receive. The saved ALS output is still U6MIDI Pro Ch2; that must be changed for USB.
5. If the Standard-edition unsupported-device warning appears, Continue for manual playback testing. The Max for Live navigation device may require a compatible licensed Live/Max setup to work. No software license is granted by this archive.
6. Play The Last Time from its count-in. Confirm preset006 loads and snapshots1→2→3→2 change. Physical snapshot switching in the corrected copy remains unconfirmed as of this handoff.

If Live reports missing samples, search the merged project folder with Live's file manager. The repository contains `ableton-relative-path-audit.json` recording checks against the desktop source. Original absolute Mac paths may remain inside the ALS; the packaged relative project paths are what make this portable.

The path audit found 19 references in **Session View clips** to an unavailable old `../Backing Tracks/W: BASS/...` folder (13 distinct WAV paths). They are not in the Arrangement playback clips. Those old session clips may still show missing media. Six additional unresolved references are Live's built-in External Instrument device, not WAV files. The package contains every file actually present in the saved project; it cannot supply those absent external backing-track sources.

The repository's smaller `Ableton/` directory contains the ALS files and device but **not** the large audio dependencies. The release downloads are needed for complete playback. Clone/download the repository for the context, audits, scripts, and Helix files.

## Tone files

`artifacts/Flwers New Verified.hls` is the latest exported Helix setlist from this work. Inspect the destination before importing a whole setlist. Historical HLS/HLX versions are included for recovery and context; they can have outdated levels or failed DSP layouts. Prefer the verified export, not the various Batch/Prepared/Before files.

## Reference recordings and integrity

The `Flwers-Tone-References-part-01.zip` archive contains isolated guitar parts and full/master references for Tongue Tied, Fade, Better Than This, and Nothing At All. It is optional for playing the Ableton set, useful for further tone work.

`RELEASE-SHA256SUMS.txt` records archive hashes; `release-manifest.json` lists every archived file with its SHA256 and containing ZIP. All ZIP entries were CRC-checked locally before uploading. The source project was copied as saved on disk; unsaved Live changes were not captured.
