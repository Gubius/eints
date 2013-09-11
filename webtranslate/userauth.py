"""
User authentication information.

Supplies user and authentication context for requests.
"""
from webtranslate import rights

class UserAuthentication:
    """
    @ivar is_auth: Whether the user authenticated successfully. False for annonymous access.
    @type is_auth: C{bool}

    @ivar name: Username, "unknown" for annoymous access.
    @type name: C{str}
    """
    def __init__(self, is_auth, name):
        self.is_auth = is_auth
        self.name = name

    def may_access(self, pname, prjname, lngname):
        """
        Check whether to grant access to a page.

        @param pname: Page access tupel.
        @type  pname: C{list} of C{str}

        @param prjname: Project name of the page, if any.
        @type  prjname: C{str} or C{None}

        @param lngname: Language name of the page, if any.
        @type  lngname: C{str} or C{None}

        @return: Whether the user may access the page.
        @rtype:  C{bool}
        """
        raise NotImplementedError('Abstract method called')

    def may_read(self, prefix, prjname, lngname):
        """
        Check whether to grant read access to a page.

        @param prefix: Page path.
        @type  prefix: C{str}

        @param prjname: Project name of the page, if any.
        @type  prjname: C{str} or C{None}

        @param lngname: Language name of the page, if any.
        @type  lngname: C{str} or C{None}

        @return: Whether the user may access the page.
        @rtype:  C{bool}
        """
        return self.may_access([prefix, prjname, lngname, 'read'], prjname, lngname)
