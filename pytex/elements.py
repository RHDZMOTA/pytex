import hashlib


class Cover(object):

    def __init__(self, institution="", mayor_heading="", minor_heading="", title="", author="", supervisor="", date=""):
        self.contens = {
            "institution_name": institution,
            "mayor_heading": mayor_heading,
            "minor_heading": minor_heading,
            "title": title,
            "author": author,
            "supervisor": supervisor,
            "date": date if date else r"\today"
        }

    def to_tex(self):
        tex = r"""
            \begin{titlepage}
            \newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
            \center

            \textsc{\LARGE %(institution_name)s}\\[1.5cm]
            \textsc{\Large %(mayor_heading)s}\\[0.5cm]
            \textsc{\large %(minor_heading)s}\\[0.5cm]


            \HRule\\[0.4cm]
            {\huge\bfseries %(title)s}\\[0.4cm]
            \HRule\\[1.5cm]

            \begin{minipage}{0.4\textwidth}
                \begin{flushleft}
                \large
                \textit{Author}\\
                %(author)s
                \end{flushleft}
            \end{minipage}
            ~
            \begin{minipage}{0.4\textwidth}
                \begin{flushright}
                \large
                \textit{Supervisor}\\
                %(supervisor)s
                \end{flushright}
            \end{minipage}

            \vfill\vfill\vfill
            {\large%(date)s}
            
            \vfill
            \end{titlepage}
            
        """
        return tex % self.contens


class TableOfContents(object):

    @staticmethod
    def to_tex():
        tex = r"\tableofcontents\newpage"
        return tex


class Section(object):

    def __init__(self, title):
        self.title = title

    def to_tex(self):
        tex = r"""\section{""" + self.title + "}"
        return tex


class Subsection(object):

    def __init__(self, subtitle):
        self.subtitle = subtitle

    def to_tex(self):
        tex = r"""\subsection{""" + self.subtitle + "}"
        return tex


class Paragraph(object):

    def __init__(self, content):
        self.content = content

    def to_tex(self):
        tex = self.content
        return tex


class Image(object):

    def __init__(self, title, path, caption):
        self.content = {
            "title": title,
            "path": path,
            "caption": caption
        }

    def to_tex(self):
        tex = r"""
            \begin{frame}
            \begin{figure}[H]\centering
            \subfloat[%(title)s]{\includegraphics[width = 6cm]{%(path)s}}
            \caption{%(caption)s}
            \end{figure}
            \end{frame}
        """
        return tex % self.content


class Itemize(object):

    def __init__(self, items):
        self.content = {"items": r"\item " + r"\item ".join(items)}

    def to_tex(self):
        tex = r"""
            \begin{itemize}
            %(items)s
            \end{itemize}  
        """
        return tex % self.content


class Equation(object):

    def __init__(self, eq, label=None):
        self.content = {"eq": eq, "label": label if label else hashlib.sha1(eq.encode()).hexdigest()}

    def to_tex(self):
        tex = r"""
            \begin{equation} \label{%(label)s}
            %(eq)s
            \end{equation}
        """
        return tex % self.content


class Code(object):

    def __init__(self, code_string, run=False, output=None):
        self.content = {"code_string": code_string}
        self.run = run
        self.output = output

    def to_tex(self):
        tex = r"""
            \begin{lstlisting}[language=Python]
            %(code_string)s
            \end{lstlisting}
        """
        return tex % self.content
