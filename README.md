# WP4 DigiPatch: Reddit Data Collection

[![DigiPatch](https://digipatch.eu/wp-content/uploads/2022/09/cropped-digipatch_logo-obrazek512-a.png)](https://digipatch.eu/)

A **Streamlit** application for collecting Reddit posts and comments, built as part of **Work Package 4 (WP4)** of the [DigiPatch](https://digipatch.eu/) research project.

> **DigiPatch** investigates the interaction between psychological needs and digital media use in the social sphere, and processes of identity formation and protection. The project examines how digital media drives cultural change from a traditionally networked society toward a rigidly "patchworked" one, with a focus on socio-cognitive processes and their societal consequences.
>
> DigiPatch is funded by the European Union's Horizon 2020 research and innovation programme (Grant Agreement No 101004509) as part of the [CHANSE](https://chanse.org) Collaboration of Humanities and Social Sciences in Europe.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Context](#project-context)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

This tool leverages [PRAW](https://praw.readthedocs.io/) to interact with the Reddit API, enabling researchers to harvest Reddit data with customisable parameters, adaptive rate limiting, and session resumption. Collected data can be downloaded as CSV for offline analysis.

Key capabilities:

- **Reddit API authentication** using client credentials.
- **Multi-subreddit post collection** with hot, new, top, controversial, and rising sorting.
- **Optional comment retrieval** with per-post limits.
- **Adaptive rate-limit handling** with automatic retries.
- **Session state persistence** for resumable data collection.
- **CSV export** of the full dataset.

---

## Features

- **Reddit API Integration** — Authenticate and interact with Reddit via PRAW.
- **Subreddit Data Collection** — Specify a subreddit and choose sorting methods.
- **Customisable Post & Comment Retrieval** — Set per-subreddit post limits and optional comment collection.
- **Adaptive Rate Limiting** — Automatic exponential backoff when rate-limited.
- **Session Persistence** — Streamlit session state stores progress; interruptions can be resumed.
- **Downloadable Output** — Export results as a CSV file.
- **Developer-Ready** — Includes a [devcontainer](.devcontainer/devcontainer.json) for VS Code / GitHub Codespaces with Python 3.11 pre-configured.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/gdc0000/DigiPatch_Reddit.git
   cd DigiPatch_Reddit
   ```
2. **(Optional) Create a Virtual Environment**

   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Launch the App**

   ```bash
   streamlit run src/app.py
   ```
2. **Enter Reddit API Credentials** — Provide your Client ID, Client Secret, Username, and Password.
3. **Configure Collection Parameters**

   - **Subreddit** — Name of the subreddit to collect from.
   - **Sorting Methods** — One or more of: hot, new, top, controversial, rising.
   - **Post Limit** — Number of posts per sorting method.
   - **Comments** — Optionally enable comment collection with a per-post limit.
   - **Duplicate Removal** — When comments are disabled, optionally deduplicate posts by ID.
4. **Start Collection** — Click **Start/Resume Collection** and monitor progress via the progress bar.
5. **Download** — Preview the first 10 rows and download the full dataset as a CSV file.
6. **Reset** — Use **Clear Data** to start a fresh session.

---

## Project Context

This application is developed within **Work Package 4 (WP4)** of the [DigiPatch](https://digipatch.eu/) project — *Moving from Networked to Patchworked Society*. The project is coordinated by a consortium of European research institutions and funded under the European Union's Horizon 2020 programme (GA No 101004509) through the [CHANSE](https://chanse.org) network.

For more information about the project, its objectives, and the research team, visit **[https://digipatch.eu/](https://digipatch.eu/)**.

---

## File Structure

```
.
├── digipatchapp.py          # Main Streamlit application
├── requirements.txt         # Python dependencies
├── DigiPatchLogo.png        # Project logo
└── .devcontainer/
    └── devcontainer.json    # VS Code dev container config
```

---

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

---

## License

[MIT](LICENSE)

---

---

*This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 101004509.*
