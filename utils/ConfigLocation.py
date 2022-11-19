import os


def ConfigRootLoc():
    path = os.path.join((os.getcwd()[:os.getcwd().find("dataManager")]), "dataManager")
    return path


def ConfigStatic():
    path = os.path.join(ConfigRootLoc(), "static")
    return path


def ConfigTemplate():
    path = os.path.join(ConfigRootLoc(), "template")
    return path


def ConfigUtils():
    path = os.path.join(ConfigRootLoc(), "utils")
    return path


def ConfiglocalSources():
    path = os.path.join(ConfigRootLoc(), "localSources")
    return path


if __name__ == '__main__':
    print(ConfigRootLoc())
    # print(ConfigStatic())
    # print(ConfigTemplate())
