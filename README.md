# cv-template

A single-page CV template built with LaTeX. Personal information lives in a local `data.json` file that is gitignored. A Python build script substitutes the data into the template and compiles the PDF.

## Prerequisites

- Python 3
- TeX Live with `pdflatex` (standard full install)

Verify: `pdflatex --version`

## Setup

```sh
# 1. Clone the repo
git clone https://github.com/your-user/cv-template.git
cd cv-template

# 2. Create your personal data file (gitignored)
cp data.example.json data.json

# 3. Fill in data.json with your details

# 4. Add your headshot (filename must match the "headshot" field in data.json)
cp /path/to/photo.jpg headshot_1.jpg

# 5. Add tech-logo images referenced in the "tech_logos" array
#    e.g. rust.png, typescript.png — place them in the project root

# 6. Build
python3 build.py

# Output: cv.pdf
```

## Build options

```sh
python3 build.py            # generate cv-filled.tex and compile to cv.pdf
python3 build.py --no-pdf   # only generate cv-filled.tex, skip pdflatex
```

## data.json fields

| Field             | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| `name_first`      | First name                                                   |
| `name_last`       | Last name / full surname                                     |
| `title`           | Professional title                                           |
| `github_url`      | Full GitHub profile URL                                      |
| `github_label`    | Display text for the GitHub link                             |
| `website_url`     | Personal website URL                                         |
| `website_label`   | Display text for the website link                            |
| `email`           | Contact email                                                |
| `address_line1`   | Street address                                               |
| `address_city`    | City and postcode                                            |
| `phone`           | Phone number                                                 |
| `country`         | Country                                                      |
| `dob`             | Date of birth (e.g. `dd/mm/yyyy`)                            |
| `linkedin_url`    | Full LinkedIn profile URL                                    |
| `linkedin_label`  | Display text for the LinkedIn link                           |
| `headshot`        | Filename of your headshot image (e.g. `headshot_1.jpg`)      |
| `profile_summary` | Free-text profile paragraph                                  |
| `tech_logos`      | Array of `{ "file": "logo.png", "height": "0.9cm" }` objects |
| `skills`          | Array of `{ "category": "...", "items": [...] }` objects     |
| `languages`       | Array of spoken language strings                             |
| `employment`      | Array of job entries — see below                             |
| `education`       | Array of education entries — see below                       |

### Employment entry fields

| Field         | Description                                 |
| ------------- | ------------------------------------------- |
| `role`        | Job title + company name                    |
| `location`    | City and country                            |
| `period`      | Date range, e.g. `January 2023 --- Present` |
| `description` | Body text. Use `\n\n` for paragraph breaks. |

### Education entry fields

| Field         | Description              |
| ------------- | ------------------------ |
| `degree`      | Degree name              |
| `institution` | University name and city |
| `period`      | Date range               |
| `description` | Optional body text       |

## What is committed vs. gitignored

| Committed                             | Gitignored                                           |
| ------------------------------------- | ---------------------------------------------------- |
| `cv.tex` — template source            | `data.json` — your personal data                     |
| `data.example.json` — field reference | `cv-filled.tex` — generated (contains personal data) |
| `build.py` — build script             | `headshot*.jpg/png` — your photo                     |
| `README.md`, `LICENSE`                | `*.png`, `*.jpeg`, `*.jpg` — your logos              |
|                                       | `cv.pdf`, `*.aux`, `*.log`, … — build output         |
