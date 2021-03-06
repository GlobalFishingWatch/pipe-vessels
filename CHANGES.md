# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v3.1.2 - 2020-08-18

### Added

* [Engeneering Incubator and chores/ENG-90](https://globalfishingwatch.atlassian.net/browse/ENG-90): Adds
  * ES7 support.
  * Uses protocol TLS to connect to ES.
  * Uses mandatory content-type to avoid 406 error.
  * Removes the mapping types.

## v3.1.1 - 2020-04-30

### Removed

* [GlobalFishingWatch/gfw-eng-tasks#75](https://github.com/GlobalFishingWatch/gfw-eng-tasks/issues/75): Removes
  * unused libraries such as `nose`, `pytz`, `udatetime` and `statistics`.

### Changed

* [GlobalFishingWatch/gfw-eng-tasks#75](https://github.com/GlobalFishingWatch/gfw-eng-tasks/issues/75): Changes
  * to last google sdk `290.0.1`
  * reduce pod name. now are limted to 63 chars.

* [GlobalFishingWatch/gfw-eng-tasks#83](https://github.com/GlobalFishingWatch/gfw-eng-tasks/issues/83): Changes
  * the syntax used to index the data in tracks over postgres to fix the publish_to_postgres task.

## v3.1.0 - 2020-04-21

### Changed

* [GlobalFishingWatch/gfw-eng-tasks#65](https://github.com/GlobalFishingWatch/gfw-eng-tasks/issues/65): Changes
  * Fixes improves the performance of track queries by adding physical clustering
    on the tracks table.
  * Also removes some deprecated messages we were echoing
    on stdout. We are no longer sending in the `segment_vessel` and
    `segment_info` tables now that the tracks aggregation query is
    parametrizable, so no need to have the source echo empty values there.

## v3.0.1 - 2020-03-12

### Changed

* [GlobalFishingWatch/gfw-eng-tasks#17](https://github.com/GlobalFishingWatch/gfw-eng-tasks/issues/17): Changes
    ujson library pin to version `1.35`.
    pipe-tools points to `v3.1.1`.

## v3.0.0 - 2020-02-29

### Added

* [GlobalFishingWatch/gfw-eng-tasks#17](https://github.com/GlobalFishingWatch/gfw-eng-tasks/issues/17): Adds
    support for python 3 and add pipe-tools:v3.1.0

## v2.1.0 - 2019-10-22

### Added

* [GlobalFishingWatch/GFW-Tasks#1138](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/1138): Adds
    a FlexibleOperator to change from bash to kubernetes operations.

## v2.0.0 - 2019-09-20

### Changed

* [GlobalFishingWatch/GFW-Tasks#1116](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/1116):
  * Removed the time partition and clustering from tracks since it can't handle more than 2000 partitions.
  * Removed the Fixed query from messages_scored and now support a query through parameters.
  * Change version of pipe-tools from 0.2.0 to 2.0.0

**NOTE** Moving to 2.0.0 since this will not work with previous 1.X

## v1.1.0 - 2019-08-23

* [GlobalFishingWatch/GFW-Tasks#1113](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/1113):
 * Fixes time range when running daily mode.
 * Upgrades google SDK TO 255.0.0
 * Fixes Python version to 2.7 Strech

## v1.0.0 - 2019-06-04

### Added

* [GlobalFishingWatch/GFW-Tasks#887](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/887):
   Adds a new task which exports the vessel information data into an elastic
   search index. This requires some additional configuration settings to point
   the pipeline to the ElasticSearch server, and to setup the query that
   generates the information to import to ElasticSearch. Check the
   [README.md](README.md#Configuration) for more information.

* [GlobalFishingWatch/GFW-Tasks#958](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/958):
 * Adds vessel track aggregation steps to the pipeline.

### Changed

* [GlobalFishingWatch/GFW-Tasks#985](https://github.com/GlobalFishingWatch/GFW-Tasks/issues/985):
   Changes the way the tracks are published to postgres. They are now published
   to a single table, we no longer need a separate tracks and vessel table, and
   the individual, unaggregated points are stored instead of the old
   accumulated track record. This also makes this pipeline run for the given
   dates only.
