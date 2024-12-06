==============================
collective.formsupport.counter
==============================

Counter integration for collective.volto.formsupport

Features
--------

- Form counter for collective.volto.formsupport


Installation
------------

Install collective.formsupport.counter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.formsupport.counter


and then running ``bin/buildout``

REST API
========

Here is the list of available REST API endpoints and how to use them.

1. **Reset form counter**

   - **Endpoint**: `/<document>/@reset-counter`.
   - **Method**: `PATCH`.
   - **Parameters**: `block_id` form block identifier.
   - **Description**: Reset form counter.
   - **Request**: No parameters required.
   - **Response**:

     - **Status Code**: `204 No Content`

Authors
-------

RedTurtle


Contributors
------------

- folix-01

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.formsupport.counter/issues
- Source Code: https://github.com/collective/collective.formsupport.counter
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: info@redturtle.it


License
-------

The project is licensed under the GPLv2.
