import argparse
import os
import subprocess

content = r'''\documentclass{article}

\usepackage{amsmath}
\usepackage{fancyhdr}

\parindent 0em
\parskip 2ex
\pagestyle{fancy}

\setlength{\textfloatsep}{5pt}



\begin{document}

\begin{titlepage}
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
\center

\textsc{\LARGE %(institution)s}\\[2cm]
\textsc{\Large %(supercourse)s}\\[1cm]
\textsc{\large %(course)s}\\[1cm]


\HRule \\[2cm]
{ \huge \bfseries %(title)s}\\[2cm] 
\HRule \\[2cm]

\begin{minipage}{0.4\textwidth}
\begin{flushleft} \large
\emph{Authors:}\\
%(name)s
\end{flushleft}
\end{minipage}

~
\begin{minipage}{0.4\textwidth}
\begin{flushright} \large
\emph{Supervisor:} \\
Dr. Juan Diego \textsc{Sánchez Torres}
\end{flushright}
\end{minipage}\\[2cm]

{\large \today}\\[1cm]

\vfill
 
\end{titlepage}
\tableofcontents




\end{document}
'''

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--institution', default='University')
parser.add_argument('-x', '--supercourse')
parser.add_argument('-c', '--course')
parser.add_argument('-t', '--title')
parser.add_argument('-n', '--name',)


args = parser.parse_args()

with open('cover.tex','w') as f:
    f.write(content%args.__dict__)

cmd = ['pdflatex', '-interaction', 'nonstopmode', 'cover.tex']
proc = subprocess.Popen(cmd)
proc.communicate()

retcode = proc.returncode
if not retcode == 0:
    os.unlink('cover.pdf')
    raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

os.unlink('cover.tex')
os.unlink('cover.log')
os.unlink('cover.aux')
