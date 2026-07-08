# Genropy Community

A [Genropy](https://www.genropy.org) application powering the Genropy developer community platform: developer profiles, community map, projects, events and communication tools for the people building with Genropy.

## Features

- **Developer profiles** — bio, skills, spoken languages, topics of interest, hobbies and badges
- **Community map** — geolocalized map of community members
- **Projects and events** — community projects, event calendar, meetings and suggestions
- **Messages** — in-app messaging with unread-message badge
- **Mobile-friendly** — PWA support with app mode for developers

With the optional packages installed (see below) the platform also provides publications
(social and blog posts), subscriptions management, surveys, web push notifications,
GitHub integration and OIDC single sign-on.

## Repository layout

```
instances/
  community/         # Base Genropy instance (core packages + comm only)
packages/
  comm/              # Main community package (model, webpages, resources)
```

## Dependencies

The `comm` package only requires the core [Genropy](https://github.com/genropy/genropy)
framework packages: `adm`, `sys`, `email`, `flib`, `biz`. The bundled `community`
instance uses exactly these plus `comm`.

The following packages are optional: when they are added to the instance configuration
the related features are enabled automatically.

| Repository | Packages | Purpose |
|---|---|---|
| gnrextra | `wpn`, `srvy` | Web push notifications, surveys |
| gnrcommunication | `genrobot`, `social`, `video`, `wordpress`, `dem` | Communication tools (enabled via package preferences) |
| gnrauth | `oidc` | OIDC authentication |
| gnrcloudtools | `github` | GitHub integration |
| gnrsubscriptions | `sbs` | Subscriptions management |

The production instance of the Genropy community platform (all optional packages
enabled, Docker build and deployment) is maintained in a separate deployment repository.

## Getting started

1. Install [Genropy](https://github.com/genropy/genropy).
2. Register the `community` instance in your Genropy environment.
3. Create the database configured in `instances/community/config/instanceconfig.xml` and run the standard Genropy database setup for the instance.
4. Serve the `community` instance with your usual Genropy web server command.

## Development

- The repository uses a single `main` branch: branch from `main` and open pull requests against `main`.
- Code, comments and commit messages must be in English.
- Linting is enforced by GitHub Actions (`flake8` on Python 3.8–3.12), see `.github/workflows/python-tests.yml`.
