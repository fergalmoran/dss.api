__author__ = 'fergalm'
import re

def lreplace(string, pattern, sub):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)

def rreplace(string, pattern, sub):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' ends 'string'.
    """
    return re.sub('%s$' % pattern, sub, string)

def is_number(s):
    try:
        if len(s) > 0:
            float(s)
            return True
    except ValueError:
        pass
    except IndexError:
        pass
    except Exception:
        pass

    return False

def trunc_lines(s, linecount):
    ret = ""
    cur = 0
    for line in s.splitlines():
        if cur < linecount:
            ret += line + "\n"
            cur += 1
        else:
            break

    return ret

