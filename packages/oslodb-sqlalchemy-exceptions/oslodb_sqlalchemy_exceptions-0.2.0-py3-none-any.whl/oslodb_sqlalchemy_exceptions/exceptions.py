import six
import os
import traceback

from .reflection import get_class_name
# import reflection as reflection

from sqlalchemy import event
from sqlalchemy import exc as sqla_exc
from debtcollector import moves

from .warning import NotSupportedWarning,OsloDBDeprecationWarning


class CausedByException(Exception):
    """Base class for exceptions which have associated causes.
    NOTE(harlowja): in later versions of python we can likely remove the need
    to have a ``cause`` here as PY3+ have implemented :pep:`3134` which
    handles chaining in a much more elegant manner.
    :param message: the exception message, typically some string that is
                    useful for consumers to view when debugging or analyzing
                    failures.
    :param cause: the cause of the exception being raised, when provided this
                  should itself be an exception instance, this is useful for
                  creating a chain of exceptions for versions of python where
                  this is not yet implemented/supported natively.
    .. versionadded:: 2.4
    """
    def __init__(self, message, cause=None):
        super(CausedByException, self).__init__(message)
        self.cause = cause

    def __bytes__(self):
        return self.pformat().encode("utf8")

    def __str__(self):
        return self.pformat()

    def _get_message(self):
        # We must *not* call into the ``__str__`` method as that will
        # reactivate the pformat method, which will end up badly (and doesn't
        # look pretty at all); so be careful...
        return self.args[0]

    def pformat(self, indent=2, indent_text=" ", show_root_class=False):
        """Pretty formats a caused exception + any connected causes."""
        if indent < 0:
            raise ValueError("Provided 'indent' must be greater than"
                             " or equal to zero instead of %s" % indent)
        buf = six.StringIO()
        if show_root_class:
            buf.write(get_class_name(self, fully_qualified=False))
            buf.write(": ")
        buf.write(self._get_message())
        active_indent = indent
        next_up = self.cause
        seen = []
        while next_up is not None and next_up not in seen:
            seen.append(next_up)
            buf.write(os.linesep)
            if isinstance(next_up, CausedByException):
                buf.write(indent_text * active_indent)
                buf.write(get_class_name(next_up,
                                                    fully_qualified=False))
                buf.write(": ")
                buf.write(next_up._get_message())
            else:
                lines = traceback.format_exception_only(type(next_up), next_up)
                for i, line in enumerate(lines):
                    buf.write(indent_text * active_indent)
                    if line.endswith("\n"):
                        # We'll add our own newlines on...
                        line = line[0:-1]
                    buf.write(line)
                    if i + 1 != len(lines):
                        buf.write(os.linesep)
                # Don't go deeper into non-caused-by exceptions... as we
                # don't know if there exception 'cause' attributes are even
                # useable objects...
                break
            active_indent += indent
            next_up = getattr(next_up, 'cause', None)
        return buf.getvalue()

class DBError(CausedByException):

    """Base exception for all custom database exceptions.
    :kwarg inner_exception: an original exception which was wrapped with
        DBError or its subclasses.
    """

    def __init__(self, inner_exception=None, cause=None):
        self.inner_exception = inner_exception
        super(DBError, self).__init__(str(inner_exception), cause)


class DBDuplicateEntry(DBError):
    """Duplicate entry at unique column error.
    Raised when made an attempt to write to a unique column the same entry as
    existing one. :attr: `columns` available on an instance of the exception
    and could be used at error handling::
       try:
           instance_type_ref.save()
       except DBDuplicateEntry as e:
           if 'colname' in e.columns:
               # Handle error.
    :kwarg columns: a list of unique columns have been attempted to write a
        duplicate entry.
    :type columns: list
    :kwarg value: a value which has been attempted to write. The value will
        be None, if we can't extract it for a particular database backend. Only
        MySQL and PostgreSQL 9.x are supported right now.
    """
    def __init__(self, columns=None, inner_exception=None, value=None):
        self.columns = columns or []
        self.value = value
        super(DBDuplicateEntry, self).__init__(inner_exception)


class DBConstraintError(DBError):
    """Check constraint fails for column error.
    Raised when made an attempt to write to a column a value that does not
    satisfy a CHECK constraint.
    :kwarg table: the table name for which the check fails
    :type table: str
    :kwarg check_name: the table of the check that failed to be satisfied
    :type check_name: str
    """
    def __init__(self, table, check_name, inner_exception=None):
        self.table = table
        self.check_name = check_name
        super(DBConstraintError, self).__init__(inner_exception)


class DBReferenceError(DBError):
    """Foreign key violation error.
    :param table: a table name in which the reference is directed.
    :type table: str
    :param constraint: a problematic constraint name.
    :type constraint: str
    :param key: a broken reference key name.
    :type key: str
    :param key_table: a table name which contains the key.
    :type key_table: str
    """

    def __init__(self, table, constraint, key, key_table,
                 inner_exception=None):
        self.table = table
        self.constraint = constraint
        self.key = key
        self.key_table = key_table
        super(DBReferenceError, self).__init__(inner_exception)


class DBNonExistentConstraint(DBError):
    """Constraint does not exist.
    :param table: table name
    :type table: str
    :param constraint: constraint name
    :type table: str
    """

    def __init__(self, table, constraint, inner_exception=None):
        self.table = table
        self.constraint = constraint
        super(DBNonExistentConstraint, self).__init__(inner_exception)


class DBNonExistentTable(DBError):
    """Table does not exist.
    :param table: table name
    :type table: str
    """

    def __init__(self, table, inner_exception=None):
        self.table = table
        super(DBNonExistentTable, self).__init__(inner_exception)


class DBNonExistentDatabase(DBError):
    """Database does not exist.
    :param database: database name
    :type database: str
    """

    def __init__(self, database, inner_exception=None):
        self.database = database
        super(DBNonExistentDatabase, self).__init__(inner_exception)


class DBDeadlock(DBError):

    """Database dead lock error.
    Deadlock is a situation that occurs when two or more different database
    sessions have some data locked, and each database session requests a lock
    on the data that another, different, session has already locked.
    """

    def __init__(self, inner_exception=None):
        super(DBDeadlock, self).__init__(inner_exception)


class DBInvalidUnicodeParameter(Exception):

    """Database unicode error.
    Raised when unicode parameter is passed to a database
    without encoding directive.
    """

    def __init__(self):
        super(DBInvalidUnicodeParameter, self).__init__(
            ("Invalid Parameter: Encoding directive wasn't provided."))


class DBMigrationError(DBError):

    """Wrapped migration specific exception.
    Raised when migrations couldn't be completed successfully.
    """
    def __init__(self, message):
        super(DBMigrationError, self).__init__(message)


class DBConnectionError(DBError):

    """Wrapped connection specific exception.
    Raised when database connection is failed.
    """

    pass


class DBDataError(DBError):
    """Raised for errors that are due to problems with the processed data.
    E.g. division by zero, numeric value out of range, incorrect data type, etc
    """


class DBNotSupportedError(DBError):
    """Raised when a database backend has raised sqla.exc.NotSupportedError"""


class InvalidSortKey(Exception):
    """A sort key destined for database query usage is invalid."""

    def __init__(self, key=None):
        super(InvalidSortKey, self).__init__(
            ("Sort key supplied is invalid: %s") % key)
        self.key = key


class ColumnError(Exception):
    """Error raised when no column or an invalid column is found."""


class BackendNotAvailable(Exception):
    """Error raised when a particular database backend is not available
    within a test suite.
    """


class RetryRequest(Exception):
    """Error raised when DB operation needs to be retried.
    That could be intentionally raised by the code without any real DB errors.
    """
    def __init__(self, inner_exc):
        self.inner_exc = inner_exc


class NoEngineContextEstablished(AttributeError):
    """Error raised for enginefacade attribute access with no context.
    This applies to the ``session`` and ``connection`` attributes
    of a user-defined context and/or RequestContext object, when they
    are accessed *outside* of the scope of an enginefacade decorator
    or context manager.
    The exception is a subclass of AttributeError so that
    normal Python missing attribute behaviors are maintained, such
    as support for ``getattr(context, 'session', None)``.
    """


class ContextNotRequestedError(AttributeError):
    """Error raised when requesting a not-setup enginefacade attribute.
    This applies to the ``session`` and ``connection`` attributes
    of a user-defined context and/or RequestContext object, when they
    are accessed *within* the scope of an enginefacade decorator
    or context manager, but the context has not requested that
    attribute (e.g. like "with enginefacade.connection.using(context)"
    and "context.session" is requested).
    """


class CantStartEngineError(Exception):
    """Error raised when the enginefacade cannot start up correctly."""


moves.moved_class(NotSupportedWarning,
                  'NotSupportedWarning',
                  __name__, version='Stein')

moves.moved_class(OsloDBDeprecationWarning,
                  'OsloDBDeprecationWarning',
                  __name__, version='Stein')