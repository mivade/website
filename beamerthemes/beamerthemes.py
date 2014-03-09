import os
import shutil

TMP = "/tmp"

themes = ("Antibes", "Bergen", "Berkeley", "Berlin", "Boadilla", \
          "Copenhagen", "Darmstadt", "Dresden", "Frankfurt", \
          "Goettingen", "Hannover", "Ilmenau", "JuanLesPins", \
          "Madrid", "Malmoe", "Marburg", "Montpellier", "PaloAlto", \
          "Pittsburgh", "Rochester", "Singapore", "Szeged", "Warsaw")

title_frame = r"""\begin{frame}
  \titlepage
\end{frame}
"""

regular_frame = r"""\begin{frame}{Frametitle}
  \begin{enumerate}
    \item Item 1
    \item Item 2
    \item Item 3
  \end{enumerate}
\end{frame}
"""

def writeLaTeXFile(theme):
    """Writes the .tex file for the given theme."""
    filename = "%s.tex" % theme
    texfile = open(filename, 'w')

    preamble = r"""\documentclass{beamer}
\mode<presentation>
{
  \usetheme{%s}
}
""" % theme
    
    title_string = r"""\title{\LaTeX ~Beamer}
    \subtitle{Theme: %s}
    \author{J.~Q.~Adams}
    \institute[George Washington University]
    {
      Department of Physics\\
      George Washington University
    }
    \date{5 March 1770}
    """ % theme
    
    texfile.writelines((preamble, title_string, r"\begin{document}", \
                        title_frame, regular_frame, r"\end{document}"))
    texfile.close()
    return filename

def convertToPNG(pdf_filename):
    """Converts the PDF file into PNG images using convert."""
    png_filename = pdf_filename[:-4] + ".png"
    os.system("convert -density 120 %s %s" % (pdf_filename, png_filename))
    img = (png_filename[:-4] + "-0.png", png_filename[:-4] + "-1.png")
    os.system("convert +append %s %s %s" % (img[0], img[1], png_filename))
    return png_filename

if __name__ == "__main__":

    old_dir = os.getcwd()
    os.chdir(TMP)
    for theme in themes:
        filename = writeLaTeXFile(theme)
        os.system("pdflatex %s" % filename)
        pdf_filename = filename[:-4] + ".pdf"
        png_filename = convertToPNG(pdf_filename)
        shutil.move("%s" % png_filename, old_dir)
