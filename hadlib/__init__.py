VERSION = "0.2"

import re, subprocess, pathlib, configparser, pkgutil, fnmatch

class HadError (Exception) :
    pass

_include = re.compile(r"^\s*#include\s*<([^>]+)>\s*$")

def src_parse (path) :
    for line in open(path) :
        match = _include.match(line)
        if match :
            yield match.group(1)

def cc_parse (cc, path, macros=[]) :
    out = subprocess.check_output([cc, "-xc", "-E", "-v", "-"],
                                  stdin=subprocess.DEVNULL,
                                  stderr=subprocess.STDOUT,
                                  encoding="utf-8")
    include = None
    for line in out.splitlines() :
        if line == "#include <...> search starts here:" :
            include = []
        elif line == "End of search list." :
            break
        elif include is not None :
            include.append(line.strip())
    out = subprocess.check_output([cc, "-M"]
                                  + [f"-D{m}" for m in macros]
                                  + [path],
                                  encoding="utf-8")
    for line in out.split(":", 1)[-1].splitlines() :
        for header in line.strip().rstrip("\\").strip().split() :
            if header != path :
                for inc in include :
                    try :
                        header = str(pathlib.Path(header).relative_to(inc))
                        break
                    except :
                        pass
                yield header

def pkg_config (pkg, cc, cflags, lflags) :
    args = []
    if cflags :
        args.append("--cflags")
    if lflags :
        args.append("--libs")
    return subprocess.check_output(["pkg-config"] + args + [pkg],
                                   encoding="utf-8").split()

def opt_filter (options, cflags, lflags) :
    pos = 0
    while pos < len(options) :
        if options[pos] in ("-l", "-L") :
            lflags.add(options[pos])
            lflags.add(options[pos+1])
            pos += 1
        elif options[pos].startswith("-l") or options[pos].startswith("-L") :
            lflags.add(options[pos])
        elif options[pos] == "-pthread" :
            cflags.add(options[pos])
            lflags.add(options[pos])
        elif options[pos].startswith("-") and len(options[pos]) == 2 :
            cflags.add(options[pos])
            cflags.add(options[pos+1])
            pos += 1
        else :
            cflags.add(options[pos])
        pos += 1

def getopt (sources, platform, cc, macros=[], actual=False, cflags=True, lflags=True) :
    headers = set()
    for path in sources :
        if actual :
            headers.update(cc_parse(cc, path, macros))
        else :
            headers.update(src_parse(path))
    deps = configparser.ConfigParser()
    try :
        deps.read_string(pkgutil.get_data("hadlib", f"{platform}.cfg").decode("utf-8"),
                         source=f"{platform}.cfg")
    except FileNotFoundError :
        raise HadError(f"platform {platform!r} not supported")
    lf, cf = set(), set()
    for dep in deps.sections() :
        for hdr in headers :
            if fnmatch.fnmatch(hdr, dep) :
                if cc in deps[dep] :
                    if deps[dep][cc].startswith("$") :
                        opt = deps[dep][deps[dep][cc].lstrip("$")]
                    else :
                        opt = deps[dep][cc]
                    opt_filter(opt.split(), cf, lf)
                elif "pkg-config" in deps[dep] :
                    opt_filter(pkg_config(deps[dep]["pkg-config"], cc, cflags, lflags),
                               cf, lf)
    return lf, cf
