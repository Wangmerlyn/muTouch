# IEEE Strict Artifact Guide Package

This folder is an isolated package to minimize template mismatch risk.

## What is enforced here

- `main.tex` is the artifact guide source (copied from `artifact/artifact_guide.tex`).
- `main.tex` uses `\documentclass[conference]{IEEEtran}`.
- The `IEEEtran.cls` in this folder is copied from your uploaded official template folder.
- `upstream_template/IEEEtran.cls` is the original reference copy from your upload.

## Verify template identity (mandatory check)

Run:

```bash
cd artifact/ieee_strict_artifact_guide
./verify_template.sh
```

Expected output:

`OK: IEEEtran.cls matches upstream template copy`

## Compile

```bash
cd artifact/ieee_strict_artifact_guide
latexmk -pdf -interaction=nonstopmode main.tex
```

Output PDF:

- `artifact/ieee_strict_artifact_guide/main.pdf`

## Notes

- This package is intentionally self-contained for PDF eXpress/manual rendering.
- Keep this folder as the source-of-truth submission package if strict template provenance is required.
