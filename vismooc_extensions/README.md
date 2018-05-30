vismooc Extensions
==================

This is the directory containing all modules for vismooc data extensions to moocdb.
Currently a courses module has been implemented as an example. An example of how
this module is used can be found in `full_pipe.py`.

Any module that intends to use username data from the edx files must hash the username strings
with the RIPEMD160 40 char hash in order to interface properly with moocdb. This is because this
is the hash `apipe` uses to generate the anonymized usernames. The usage of this hash can be found
in `edx_pipe/apipe/json_to_relation/edxTrackLogJSONParser.py`

```
oneHash = hashlib.new('ripemd160')
```

The [hashlib](https://docs.python.org/2/library/hashlib.html) library in python can perform the hashing necessary to maintain compatability.


To implement your own module, there are four primary components needed.

1. A `{module}.py` file in this directory, preferably with a corresponding `{module}_test.py` script.
2. Modifications to Step 5 of `full_pipe`. The changes should be made in the `query_vismooc` method.
3. Modifications to the `import_vismooc_to_moocdb.sql` script so that the new table and corresponding data can be imported into moocdb. The existing code in `import_vismooc_to_moocdb.sql` can likely be reused with minor modifications.
4. Any additional configuration variables in `edx_pipe/qpipe/config.py`. This will likely be the filename of the non-tracking log edx file. It is assumed that this other file will be placed in the same directory as the tracking log file.


In the case of the implemented example:

1. `courses.py` and `courses_test.py` can be found in this directory.
2. See `full_pipe.py` for how `courses.py` is imported and invoked.
3. See `import_vismooc_to_moocdb.sql` and in particular note the creation of the `courses` table and the explicit specification of `courses.csv` for importing data.
4. The `COURSE_STRUCTURE_FILE` was added as a variable to be invoked from `full_pipe.py`. This is necessary to locate and load the course structure json file.


Schema
======

For information about the schema of the `vismooc_extensions` tables it is best to see
`import_vismooc_to_moocdb.sql` as that will always have the most up to date information.

Edx course files either take the form of `.csv` or `.sql` in the case of flat tabular data,
or `.json` which consist of arbitrarily complicated dictionary objects per line according
to [Edx documentation](https://edx.readthedocs.io/projects/devdata/en/latest/data_czars/package.html#extracted-contents-of-org-date-zip)

As for the mapping from Edx course files to the fields of the `vismooc_extensions` tables,
it is largely the case that a single module (source file) is repsonsible for a `vismooc_extensions`
table. For example, `grades.py` is repsonsible for the `vismooc_extensions` `grades` table.
If you peek into the file, you can find a function `get_csv_field_to_func_map` which gives
the mapping from Edx course file fields to the final `vismooc_extensions` table field.
This is the case for most of the modules implemented, although note that `videos.py` is
responsible for two `vismooc_extensions` tables: `course_video` and `videos`. The main
function to look for to get the mapping information is this the one that returns
a csv field to function map. The `courses.py` module is the exception to this as that
was developed first before the remaining infrastructure was fleshed out, and there is
no reason (besides time) why it could not be restructured to match the remaining modules.