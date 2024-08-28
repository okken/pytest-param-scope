# Build & Deploy

Note: If you're not Brian, don't try this.

# Modify version

Change the version in pyproject.toml

# Tag

```
(ok) $ git tag -a v0.1.2 -m 'some message'
(ok) $ git push --tags
```

# Release

Go to [new release](https://github.com/okken/pytest-param-scope/releases/new) and manually create one based on the above tag.