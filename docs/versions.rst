Versions
========

Version 1.0
-----------
* Removal of `patch_request_class`
* `autoserve` is now deactivated by default


Version 0.1.3
-------------
* The `_uploads` module/blueprint will not be registered if it is not needed
  to serve uploads.


Version 0.1.1
-------------
* `patch_request_class` now changes `max_content_length` instead of
  `max_form_memory_size`.
