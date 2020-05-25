@staticmethod
def todo(errorMessage):
    sys.stderr.write(errorMessage)
    assert False