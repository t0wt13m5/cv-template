#!/usr/bin/env python3
"""
CV build script.

Reads data.json, substitutes %%PLACEHOLDER%% tokens in cv.tex,
writes cv-filled.tex, then compiles it with pdflatex.

Usage:
    python build.py              # reads data.json, outputs cv.pdf
    python build.py --no-pdf    # only generate cv-filled.tex, skip pdflatex
"""

import json
import os
import re
import subprocess
import sys

DATA_FILE    = "data.json"
TEMPLATE     = "cv.tex"
FILLED       = "cv-filled.tex"
OUTPUT_PDF   = "cv.pdf"


# ---------------------------------------------------------------------------
# LaTeX escaping
# ---------------------------------------------------------------------------
_SPECIAL = str.maketrans({
    "&":  r"\&",
    "%":  r"\%",
    "$":  r"\$",
    "#":  r"\#",
    "_":  r"\_",
    "{":  r"\{",
    "}":  r"\}",
    "~":  r"\textasciitilde{}",
    "^":  r"\^{}",
    "\\": r"\textbackslash{}",
})

def tex(s: str) -> str:
    """Escape a plain string for safe use in LaTeX."""
    return str(s).translate(_SPECIAL)


# ---------------------------------------------------------------------------
# Block generators
# ---------------------------------------------------------------------------
def make_tech_logos(logos: list) -> str:
    parts = []
    for logo in logos:
        parts.append(
            rf'\includegraphics[height={logo["height"]}]{{{logo["file"]}}}\hspace{{10pt}}%'
        )
    return "\n    ".join(parts)


def make_skills(skills: list) -> str:
    lines = []
    for group in skills:
        lines.append(rf'\item \textbf{{{tex(group["category"])}}}')
        lines.append(r'      \begin{itemize}[leftmargin=8pt, label={}, itemsep=1pt, topsep=1pt]')
        for item in group["items"]:
            lines.append(rf'          \skillitem{{{tex(item)}}}')
        lines.append(r'      \end{itemize}')
    return "\n        ".join(lines)


def make_languages(languages: list) -> str:
    return "\n        ".join(rf'\skillitem{{{tex(lang)}}}' for lang in languages)


def make_entry(role_or_degree: str, location_or_inst: str, period: str, description: str) -> str:
    # Convert literal \n\n (two chars) in JSON description to paragraph spacing
    desc = tex(description)
    desc = desc.replace(r"\n\n", r"\vspace{4pt} ")
    desc = desc.replace(r"\n", " ")
    return (
        rf'\employmentHistoryEntry{{{tex(role_or_degree)}}}'
        rf'{{{tex(location_or_inst)}}}'
        rf'{{{tex(period)}}}'
        rf'{{{desc}}}'
    )


def make_employment(entries: list) -> str:
    return "\n\n    ".join(
        make_entry(e["role"], e["location"], e["period"], e.get("description", ""))
        for e in entries
    )


def make_education(entries: list) -> str:
    return "\n\n    ".join(
        make_entry(e["degree"], e["institution"], e["period"], e.get("description", ""))
        for e in entries
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    no_pdf = "--no-pdf" in sys.argv

    if not os.path.exists(DATA_FILE):
        sys.exit(
            f"Error: {DATA_FILE} not found.\n"
            f"Copy data.example.json to {DATA_FILE} and fill in your details."
        )

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()

    substitutions = {
        "%%FIRSTNAME%%":      tex(data["name_first"]),
        "%%LASTNAME%%":       tex(data["name_last"]),
        "%%TITLE%%":          tex(data["title"]),
        "%%GITHUB_URL%%":     data["github_url"],
        "%%GITHUB_LABEL%%":   tex(data["github_label"]),
        "%%WEBSITE_URL%%":    data["website_url"],
        "%%WEBSITE_LABEL%%":  tex(data["website_label"]),
        "%%EMAIL%%":          data["email"],          # used raw inside \href and as display
        "%%HEADSHOT%%":       data["headshot"],
        "%%ADDRESS_LINE1%%":  tex(data["address_line1"]),
        "%%ADDRESS_CITY%%":   tex(data["address_city"]),
        "%%PHONE%%":          tex(data["phone"]),
        "%%COUNTRY%%":        tex(data["country"]),
        "%%DOB%%":            tex(data["dob"]),
        "%%LINKEDIN_URL%%":   data["linkedin_url"],
        "%%LINKEDIN_LABEL%%": tex(data["linkedin_label"]),
        "%%PROFILE_SUMMARY%%": tex(data["profile_summary"]),
        "%%TECH_LOGOS%%":     make_tech_logos(data["tech_logos"]),
        "%%SKILLS%%":         make_skills(data["skills"]),
        "%%LANGUAGES%%":      make_languages(data["languages"]),
        "%%EMPLOYMENT%%":     make_employment(data["employment"]),
        "%%EDUCATION%%":      make_education(data["education"]),
    }

    filled = template
    for token, value in substitutions.items():
        filled = filled.replace(token, value)

    # Warn about any unresolved tokens
    remaining = re.findall(r'%%\w+%%', filled)
    if remaining:
        print(f"Warning: unresolved tokens: {', '.join(set(remaining))}", file=sys.stderr)

    with open(FILLED, "w", encoding="utf-8") as f:
        f.write(filled)

    print(f"Generated {FILLED}")

    if no_pdf:
        return

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-jobname=cv", FILLED],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        # Print only the error lines from the log for a clean summary
        errors = [l for l in result.stdout.splitlines() if l.startswith("!")]
        if errors:
            print("pdflatex errors:", file=sys.stderr)
            for e in errors:
                print(" ", e, file=sys.stderr)
        else:
            print(result.stdout[-3000:], file=sys.stderr)
        sys.exit(1)

    print(f"Output: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
