Summary

This pull request improves the student activity registration system by:

- Adding server-side validation to prevent duplicate registrations and to validate input.
- Introducing a capacity field on activities and enforcing capacity limits in the registration flow (database migration included).
- Updating controller logic and views to provide clear success/error messages for registration and unregistration actions.
- Adding unit and request specs that cover the new validation and capacity behavior.

Files changed (high level)

- app/models/activity.rb
- app/models/registration.rb
- db/migrate/<timestamp>_add_capacity_to_activities.rb
- app/controllers/registrations_controller.rb
- app/views/activities/index.html.erb
- spec/models/registration_spec.rb
- spec/requests/registrations_spec.rb

How to test

1. Run migrations: rails db:migrate
2. Install gems / prepare environment if needed: bundle install
3. Run the test suite: bundle exec rspec
4. Manual verification steps:
   - Sign in as a student account.
   - Visit the Activities page and register for an activity with available capacity.
   - Try registering again for the same activity; the second attempt should be blocked with an informative message.
   - Register until the activity reaches capacity; further registration attempts should be blocked and show the appropriate message.

Notes

- The migration adds a capacity column with a sensible default to maintain backwards compatibility.
- No breaking API changes are introduced.
- If you'd like different UX text or a different default capacity, I can update the PR.

What I changed

- Implemented validations and capacity checks in models and controller.
- Added tests covering duplicate registration and capacity edge cases.
- Updated views to show registration status and messages.

Requested reviewers

Please review the registration logic, model validations, and the new tests.