================
Flask-Reuploaded
================

.. currentmodule:: flask_uploads

Flask-Reuploaded provides file uploads for Flask.

This extension allows your application to flexibly and efficiently handle file
uploading and serving the uploaded files.
You can create different sets of uploads - one for document attachments, one
for photos, etc. and the application can be configured to save them all in
different places and to generate different URLs for them.


Notes on this package
---------------------

This is an independently maintained version of `Flask-Uploads` including
several years of unreleased changes, at least not released to PyPI. Noteworthy
is the fix for the `Werkzeug` API change. If you have used `Flask-Uploads` and
want to migrate to `Flask-Reuploaded`, please see the :ref:`migration-guide` .

Goals
-----

- provide a stable drop-in replacement for `Flask-Uploads`
- regain momentum for this widely used package
- provide working PyPI packages


Contents
--------

.. toctree::
   :titlesonly:
   :maxdepth: 1

   self
   Installation <installation>
   Getting Started <getting_started>
   Configuration <configuration>
   Minimal Application <minimal_app>
   Explanation <explanation>   
   API <api>
   Versions <versions>
   Contributing <contributing_link>
