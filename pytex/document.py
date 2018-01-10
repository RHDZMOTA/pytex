from .elements import *

import os
import subprocess


class Document(object):

    def __init__(self, filename, path="", institution="", mayor_heading="", minor_heading="", title="", author="", supervisor="", date=""):
        self.type = "article"
        self.filename = filename
        self.path = path
        self.elements = [Cover(institution, mayor_heading, minor_heading, title, author, supervisor, date)]

    def add_element(self, element):
        self.elements.append(element)

    def add_table_of_contents(self):
        self.elements.append(TableOfContents())

    def add_section(self, title):
        self.elements.append(Section(title))

    def add_subsection(self, subtitle):
        self.elements.append(Subsection(subtitle))

    def add_paragraph(self, content):
        self.elements.append(Paragraph(content))

    def add_image(self, path):
        self.elements.append(Image(path))

    def add_equation(self, eq, label=None):
        self.elements.append(Equation(eq, label))

    def add_code(self, code_string, run=False):
        self.elements.append(Code(code_string, run))

    def add_items(self, items):
        self.elements.append(Itemize(items))

    def to_tex(self):
        tex = r"""
            \documentclass[11pt]{article}
            \usepackage[utf8]{inputenc}
            \usepackage[T1]{fontenc}
            \usepackage{amsmath}
            \usepackage{fancyhdr}
            \usepackage{listings}
            \usepackage{color}


            \definecolor{codegreen}{rgb}{0,0.6,0}
            \definecolor{codegray}{rgb}{0.5,0.5,0.5}
            \definecolor{codepurple}{rgb}{0.58,0,0.82}
            \definecolor{backcolour}{rgb}{0.95,0.95,0.92}


            \lstdefinestyle{mystyle}{
                backgroundcolor=\color{backcolour},   
                commentstyle=\color{codegreen},
                keywordstyle=\color{magenta},
                numberstyle=\tiny\color{codegray},
                stringstyle=\color{codepurple},
                basicstyle=\footnotesize,
                breakatwhitespace=false,         
                breaklines=true,                 
                captionpos=b,                    
                keepspaces=true,                 
                numbers=left,                    
                numbersep=5pt,                  
                showspaces=false,                
                showstringspaces=false,
                showtabs=false,                  
                tabsize=2
            }
 
            \lstset{style=mystyle}


            \parindent 0em
            \parskip 2ex
            \pagestyle{fancy}
            \setlength{\textfloatsep}{5pt}
            \begin{document}
        """
        for element in self.elements:
            tex += "\n" + element.to_tex()
        return tex + "\n" + r"\end{document}"

    def create_tex(self):
        tex_name = os.path.join(self.path, self.filename + ".tex")
        with open(tex_name, 'w') as f:
            f.write(self.to_tex())
        return tex_name

    def compile(self, delete_tex=True):
        generic_filename = os.path.join(self.path, self.filename)
        pdf_name = generic_filename + ".pdf"
        tex_name = generic_filename + ".tex"
        with open(tex_name, 'w') as f:
            f.write(self.to_tex())
        cmd = ['pdflatex', '-interaction', 'nonstopmode', tex_name]
        proc = subprocess.Popen(cmd)
        proc.communicate()
        retcode = proc.returncode
        if not retcode == 0:
            os.unlink(pdf_name)
            raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
        if delete_tex:
            os.unlink(tex_name)
        for file_end in [".aux", ".log", ".toc"]:
            temp = generic_filename + file_end
            if os.path.exists(temp):
                os.unlink(temp)
