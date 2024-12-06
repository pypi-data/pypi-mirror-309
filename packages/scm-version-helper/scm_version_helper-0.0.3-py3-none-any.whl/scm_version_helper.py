'''This is called when the python package is built

'''
# https://setuptools-scm.readthedocs.io/en/latest/config/
# https://setuptools-scm.readthedocs.io/en/latest/customizing/


def get_version(version) -> str:
    import os
    from setuptools_scm.version import only_version
    return only_version(version)


def get_local_version(version) -> str:
    import os
    from setuptools_scm.version import log, get_local_node_and_date, get_no_local_node
    if os.environ.get('SCM_VERSION_HELPER_VERSION_ONLY', '0') == '1':
        log.info('Excluding local version')
        return get_no_local_node(version)
    log.info('Adding git info and timestamp to local version')
    return get_local_node_and_date(version)

