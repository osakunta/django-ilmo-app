## 1.0.0
* Initial version
* EventForms as models
   - next version should clean up the legacy setup related to form template files
* Add reference number to the admin listing view of EventAttendee model
## 1.1.0
* Add test setup
  - scripts for setting up DjangoCMS test environment
* Fix CI
  - use newly created test environment for CI builds
  - add build status to README
* Move `EventForm.url_alias` as a child of `Event` model
  - including migrations for legacy data

