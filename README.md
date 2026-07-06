# Genropy Community

A [Genropy](https://www.genropy.org) application powering the Genropy developer community platform: developer profiles, community map, projects, events and communication tools for the people building with Genropy.

## Features

- **Developer profiles** — bio, skills, spoken languages, topics of interest, hobbies and badges
- **Community map** — geolocalized map of community members
- **Projects and events** — community projects, event calendar, meetings and suggestions
- **Messages** — in-app messaging with unread-message badge
- **Publications** — social posts and blog posts authored by developers
- **Subscriptions** — membership management via the `sbs` package
- **Mobile-friendly** — PWA support with app mode for developers
- **OIDC authentication** — single sign-on via the `gnrauth:oidc` package

## Repository layout

```
instances/
  gnr_comm/          # Genropy instance configuration
packages/
  comm/              # Main community package (model, webpages, resources)
```

## Dependencies

The `comm` package requires the following Genropy repositories/packages:

| Repository | Packages | Purpose |
|---|---|---|
| [genropy](https://github.com/genropy/genropy) | `adm`, `sys`, `email`, `flib`, `biz` | Core framework packages |
| gnr_it | `glbl` | Italian localization data |
| gnrextra | `wpn`, `srvy` | Web push notifications, surveys |
| gnrcommunication | `genrobot`, `social`, `video`, `wordpress`, `dem` | Communication tools (optional, enabled via package preferences) |
| gnrauth | `oidc` | OIDC authentication |
| gnrcloudtools | `github` | GitHub integration |
| gnrsubscriptions | `sbs` | Subscriptions management |

## Getting started

1. Install [Genropy](https://github.com/genropy/genropy) and the dependent repositories listed above.
2. Register the `gnr_comm` instance in your Genropy environment.
3. Create the database configured in `instances/gnr_comm/config/instanceconfig.xml` and run the standard Genropy database setup for the instance.
4. Serve the `gnr_comm` instance with your usual Genropy web server command.

## Development

- The repository uses a single `main` branch: branch from `main` and open pull requests against `main`.
- Code, comments and commit messages must be in English.
- Linting is enforced by GitHub Actions (`flake8` on Python 3.8–3.12), see `.github/workflows/python-tests.yml`.
