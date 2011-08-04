===========
taguchi-api
===========

A Python wrapper for the Taguchi HTTP APIs.

Executables
===========

* taguchi-client: provides a command-line interface to the APIs

Modules
=======

* taguchi: provides the following classes, each of which wraps a Taguchi
  resource:

  - Activity: enables activities to be created, retrieved, updated, deleted,
    proofed, and triggered;

  - Campaign: provides create, retrieve, update and delete operations for
    campaigns;

  - Template: provides create, retrieve, update and delete operations for
    templates;

  - Subscriber: provides create, retrieve, update, delete, subscribe and
    unsubscribe operations for subscribers;

  - SubscriberList: provids create, retrieve, update, delete and member list
    operations for subscriber lists.