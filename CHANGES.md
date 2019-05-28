# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* [#887](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/887): Adds a new task which exports the vessel information data into an elastic search index. This requires some additional configuration settings to point the pipeline to the ElasticSearch server, and to setup the query that generates the information to import to ElasticSearch. Check the [README.md](README.md#Configuration) for more information.

* [#958](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/958): Adds vessel track aggregation steps to the pipeline.

### Changed

* [#985](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/985): Changes the way the tracks are published to postgres. They are now published to a single table, we no longer need a separate tracks and vessel table, and the individual, unaggregated points are stored instead of the old accumulated track record.
