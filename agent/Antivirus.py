import psutil

def runscan(result):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if "lsass" in str(pinfo):
                result["lsass"] = "Activated"
            if "ekrn" in str(pinfo):
                result["antivirus"] = "ESET"

    return result
        