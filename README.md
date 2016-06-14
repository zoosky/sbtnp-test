sbtnp-test
==========

A project for demonstrating RPM package relocation and replacing maintainer scripts in systemv

## Tool Installation

On SUSE SLES 12 or SUSE Leap 42:

* Install sbt 0.13.11
* Install rpmbuild
* Install rpmlint

## Generate the rpm

* `sbt uniMappings` # shows the duplicate files
* `sbt rpm:packageBin` # create the rpm in `target/rpm/RPMS/..`
* Check if it is OK: `rpm:rpm-lint`

Helpful to debug the mappings is `show rpm:linuxPackageMappings`

## Deploy rpm locally

* `sudo rpm -ihv <rpm-name>`


## Uninstall rpm

* `sudo rpm -e <rpm-package-name>`


## sbt-native-packager

Docs: [https://github.com/sbt/sbt-native-packager/](https://github.com/sbt/sbt-native-packager/)

To debug, in sbt console: `set logLevel := Level.Debug`

