# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v1.1.0 

* [GlobalFishingWatch/GFW-Tasks#887](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/1113): Fixes time range when running daily mode.
* Upgrades google SDK TO 255.0.0
* Fixes Python version to 2.7 Strech

## v1.0.0 

### Added

* [GlobalFishingWatch/GFW-Tasks#887](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/887): Adds a new task which exports the vessel information data into an elastic search index. This requires some additional configuration settings to point the pipeline to the ElasticSearch server, and to setup the query that generates the information to import to ElasticSearch. Check the [README.md](README.md#Configuration) for more information.

* [GlobalFishingWatch/GFW-Tasks#958](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/958): Adds vessel track aggregation steps to the pipeline.

### Changed

* [GlobalFishingWatch/GFW-Tasks#985](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/985): Changes the way the tracks are published to postgres. They are now published to a single table, we no longer need a separate tracks and vessel table, and the individual, unaggregated points are stored instead of the old accumulated track record. This also makes this pipeline run for the given dates only.
