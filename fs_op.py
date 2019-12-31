import subprocess
from datetime import datetime


def list_files(workdir):
    # define the ls command
    ls = subprocess.Popen (["ls", "-p", workdir + "stock_dfs/"],
                           stdout=subprocess.PIPE,
                           )

    # define the grep command
    grep = subprocess.Popen (["grep", "-v", "/$"],
                             stdin=ls.stdout,
                             stdout=subprocess.PIPE,
                             )

    # read from the end of the pipe (stdout)
    endOfPipe = grep.stdout

    # output the files line by line
    lines = []
    for line in endOfPipe:
        lines.append (line)
    return lines


def remove_folder(workdir, aindex):
    # define the ls command
    ls = subprocess.Popen (["ls", "-p", workdir],
                           stdout=subprocess.PIPE,
                           )

    # define the grep command
    rm = subprocess.Popen (["rm", "-r", workdir + aindex],
                           stdin=ls.stdout,
                           stdout=subprocess.PIPE,
                           )

    # read from the end of the pipe (stdout)
    endOfPipe = rm.stdout

    # output the files line by line
    lines = []
    for line in endOfPipe:
        lines.append (line)
    lines.append ("Sucessfully Deleted " + workdir + aindex)
    return lines


def create_tarball(workdir, dirname, ):
    now = datetime.now ()  # current date and time
    date_time = now.strftime ("%d-%m-%Y_%H-%M-%S")
    # define the ls command
    ls = subprocess.Popen (["ls", "-p", workdir],
                           stdout=subprocess.PIPE,
                           )

    # define the grep command
    print ("creating Tarball from " + workdir + dirname)
    rm = subprocess.Popen (["tar", "-czvf", workdir + "/" + date_time + "_" + dirname + ".tar.gz", workdir + dirname],
                           stdin=ls.stdout,
                           stdout=subprocess.PIPE,
                           )

    # read from the end of the pipe (stdout)
    endOfPipe = rm.stdout

    # output the files line by line
    lines = []
    for line in endOfPipe:
        lines.append (line)
    lines.append ("Sucessfully Dcreated Tarball " + workdir + dirname)
    return lines
