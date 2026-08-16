# Backup scope — what is and isn't in this repo

This repo (`video_pipeline_workspace`) is an off-machine backup of the
verifiability-compiler / video-production workspace. It is a **fresh history**:
the initial commit is an import of the working tree as of 2026-08-15. The
pre-import local history was parked at `.git_pre_import_history/` on the
origin machine and is not published here (it carried ~400 MB of regenerable
media plus a credentials file).

The rule for what is tracked: **source, scripts, manifests, and prose are in;
anything a pipeline can rebuild is out.**

## Deliberately excluded

| Path | Size | Why | How to get it back |
| --- | --- | --- | --- |
| `*/out/` (all pipelines) | ~1.1 GB | Rendered video, frames, PDFs, page rasters | Re-run the owning pipeline; see each dir's `README.md` |
| `representation_transform_visuals/assets/human_audio/` | 350 MB | Human voice takes — **not regenerable**, but too large for plain git | Local backup only (see below) |
| `representation_transform_visuals/source_frame_pipeline/out/downloads/` | 168 MB | Third-party YouTube source video | Re-fetch via `source_videos.json` + `capture_youtube_frames.py` |
| `refrence_literature/Developing_safety_critical_software/` | 6 MB | Third-party copyrighted book | Not redistributed; local copy only |
| `.env_temp`, `.env*` | — | API credentials | Recreate locally; format documented in `mailers/letterstream_client.py` |
| `__pycache__/`, `*.pyc` | — | Build cruft | n/a |

Derived artifacts that were small and useful were **kept**: the whitepaper
diagram PNGs, `assets/reference_frames/` contact sheets, and the
`verification_prototype` data set.

## The one irreplaceable exclusion

`assets/human_audio/` is the only excluded content that no pipeline can
reproduce. It lives in the full-workspace backup at:

    /home/lpurdy/repos/verifiability_compiler_backup_20260815

That backup is on the same machine, so it does **not** count as off-site.
Getting the audio somewhere durable is the outstanding follow-up — Git LFS on
this repo, a separate media repo, or ordinary object storage.

## Restoring a working copy

```sh
git clone git@github.com:lpurdy01/video_pipeline_workspace.git
cd video_pipeline_workspace
python -m venv .venv && source .venv/bin/activate
pip install -r representation_transform_visuals/requirements.txt
# then copy assets/human_audio/ back in from the media backup
```
