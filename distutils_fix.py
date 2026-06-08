"""
Patch distutils.util.strtobool for Python 3.12+ compatibility.

Import this module at the very start of your application to ensure
distutils.strtobool is available for packages that depend on it.
"""

import sys


def _strtobool_impl(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError(f"invalid truth value {val!r}")


def patch_distutils():
    """Patch distutils.util with strtobool if running Python 3.12+."""
    try:
        # Check if strtobool already exists (Python < 3.12)
        from distutils.util import strtobool
        return  # Already available, no patch needed
    except (ImportError, ModuleNotFoundError, AttributeError):
        pass

    # Try to import distutils and add strtobool
    try:
        import distutils
        import distutils.util
        if not hasattr(distutils.util, 'strtobool'):
            distutils.util.strtobool = _strtobool_impl
    except ImportError:
        # distutils doesn't exist at all, create it
        import os
        site_packages = next((p for p in sys.path if 'site-packages' in p), None)
        if site_packages:
            distutils_dir = os.path.join(site_packages, 'distutils')
            os.makedirs(distutils_dir, exist_ok=True)

            # Create __init__.py
            init_path = os.path.join(distutils_dir, '__init__.py')
            if not os.path.exists(init_path):
                with open(init_path, 'w') as f:
                    f.write('# distutils compatibility package\n')

            # Create util.py with strtobool
            util_path = os.path.join(distutils_dir, 'util.py')
            if not os.path.exists(util_path):
                with open(util_path, 'w') as f:
                    f.write('''# distutils.util compatibility for Python 3.12+

def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0)."""
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError(f"invalid truth value {val!r}")
''')


# Apply patch immediately when this module is imported
patch_distutils()
