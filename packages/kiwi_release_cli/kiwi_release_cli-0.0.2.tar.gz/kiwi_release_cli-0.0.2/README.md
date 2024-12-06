# Release CLI

Small CLI utility to handle semantic versioning via git tag

```
% poetry run release tag --help
Usage: release tag [OPTIONS]

  Cut a new tag for the release.

Options:
  --major   Bump major version
  --minor   Bump minor version
  --patch   Bump patch version
  --dryrun  Preview the release tag change
  --help    Show this message and exit.
```