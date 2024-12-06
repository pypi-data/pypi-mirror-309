Changelog
=========


1.2.3 (2024-11-18)
------------------

- Add support of German language for legal gdpr text and cookies policy
  [boulch]


1.2.2 (2022-03-22)
------------------

- Remove plone.app.registry template override as it is now released:
  Plone 6.0.0a3 / plone.app.registry 2.0.0a7
  [laulaz]

- Add specific controlpanel permission and give this permission to site administrator
  [boulch]


1.2.1 (2022-01-25)
------------------

- Add icons for control panel settings (Plone5 / 6 size)
  [boulch]

- Override a plone.app.registry template to have structured (html) description
  [boulch]


1.2 (2021-12-13)
----------------

- Add cookies policy default text & logic (same as legal mentions)
  [laulaz]


1.1.1 (2021-06-10)
------------------

- Fix unicode error in Plone52
  [boulch]


1.1.0 (2020-06-09)
------------------

- Revert "Fix missing dependency (breaks cpskin.core tests)"
  [mpeeters]

- Remove unwanted dependencies
  [mpeeters]

- Avoid UnicodeEncodeError if gdpr text browser view is already Unicode
  [laulaz]


1.0.4 (2019-11-20)
------------------

- Fix WrongType when inserting string in registry
  [laulaz]

- Fix missing dependency (breaks cpskin.core tests)
  [laulaz]

- Add css for document.
  [mgennart]

1.0.3 (2018-08-26)
------------------

- Inherit from website content styles
  [mpeeters]


1.0.2 (2018-07-16)
------------------

- Avoid an error when the package is not installed
  [mpeeters]


1.0.1 (2018-06-18)
------------------

- Translations
  [bsuttor]


1.0.0 (2018-06-14)
------------------

- Update gdpr default template.
  [bsuttor]


1.0a4 (2018-06-13)
------------------

- Add is_text_ready record.
  [bsuttor]


1.0a3 (2018-05-31)
------------------

- Use view instead of page.
  [bsuttor]


1.0a2 (2018-05-31)
------------------

- Fix i18n compilation.
  [bsuttor]


1.0a1 (2018-05-31)
------------------

- Initial release.
  [bsuttor]
