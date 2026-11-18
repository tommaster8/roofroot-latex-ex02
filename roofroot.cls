%% =====================================================================
%%  roofroot.cls — "Green Roof" document class for the RoofRoot business plan
%%  Engine : LuaLaTeX only            Languages : Hebrew (main) + English
%%  Rule   : every systemic fix goes HERE (or into a Skill) — never into
%%           chapter text. Bump the version line on every change and log
%%           it in the CHANGELOG block below (checked by qa-cls-version).
%% =====================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{roofroot}[2026/11/18 v1.2 RoofRoot business-plan class]
\def\rr@clsversion{1.2}
%% CHANGELOG
%%  v1.0  initial: palette, fonts, babel bidi, chapter band, banner/footer,
%%        info boxes, pythonbox, tables, IEEE biblatex.
%%  v1.1  INC-004: drop babel layout=counters — under bidi=basic it split
%%        every "3.1" into reversed glyphs (TOC, captions, \ref). Cover title
%%        block: align=left (= flush right in RTL) and sun moved west.
%%  v1.2  red-team round 1 (#1-#4, INC-005): \cite wrapped in an LTR island
%%        (\babelsublr) so brackets and the following period stay in place, also
%%        inside captions/LoF; \rrbibliography typesets the (English) entries in
%%        an LTR list so [n] labels no longer collide with the names; DOI/URL
%%        line-break penalties + emergencystretch remove bib overfull boxes.

\LoadClass[11pt,a4paper,oneside]{report}

%% ---------------------------------------------------------------- engine
\RequirePackage{iftex}
\ifluatex\else
  \ClassError{roofroot}{This class requires LuaLaTeX}{Compile with lualatex.}
\fi

%% ---------------------------------------------------------------- page
\RequirePackage[a4paper,top=30mm,bottom=26mm,inner=24mm,outer=24mm,
                headheight=16pt,headsep=12mm,footskip=14mm]{geometry}

%% ---------------------------------------------------------------- palette
\RequirePackage[table]{xcolor}
\definecolor{rrForest}{HTML}{1F4D3A}   % primary — deep forest green
\definecolor{rrLeaf}{HTML}{8CC63F}     % accent  — leaf lime
\definecolor{rrTerra}{HTML}{D9663B}    % warning — terracotta roof tile
\definecolor{rrCream}{HTML}{F6F1E7}    % paper   — box background
\definecolor{rrSky}{HTML}{CFE6E2}      % soft    — sky / table stripe
\definecolor{rrInk}{HTML}{22312B}      % text
\definecolor{rrStone}{HTML}{8A8F87}    % muted   — captions, rules
\color{rrInk}

%% ---------------------------------------------------------------- language + bidi
\RequirePackage[bidi=basic,layout=tabular.graphics]{babel}
\babelprovide[main,import,onchar=ids fonts]{hebrew}
\babelprovide[import,onchar=ids fonts]{english}

%% Fonts ship with TeX Live / MiKTeX (Culmus, TeX Gyre, Fira) — no system
%% fonts, so the PDF is reproducible on any machine.
\babelfont{rm}[Ligatures=TeX]{TeX Gyre Pagella}
\babelfont{sf}[Ligatures=TeX]{Fira Sans}
\babelfont{tt}[Scale=0.88]{Fira Mono}
\babelfont[hebrew]{rm}[Extension=.otf,
    UprightFont=DavidCLM-Medium,BoldFont=DavidCLM-Bold,
    ItalicFont=DavidCLM-MediumItalic,BoldItalicFont=DavidCLM-BoldItalic,
    Scale=1.08]{DavidCLM}
\babelfont[hebrew]{sf}[Extension=.otf,
    UprightFont=NachlieliCLM-Light,BoldFont=NachlieliCLM-Bold,
    ItalicFont=NachlieliCLM-LightOblique,BoldItalicFont=NachlieliCLM-BoldOblique]{NachlieliCLM}
\babelfont[hebrew]{tt}[Extension=.ttf,
    UprightFont=MiriamMonoCLM-Book,BoldFont=MiriamMonoCLM-Bold,
    ItalicFont=MiriamMonoCLM-BookOblique,BoldItalicFont=MiriamMonoCLM-BoldOblique]{MiriamMonoCLM}

\linespread{1.12}
\setlength{\parskip}{0.45em}
\setlength{\parindent}{0pt}
\RequirePackage[protrusion=false]{microtype}

%% New Israeli Shekel sign (U+20AA) — in the Hebrew font
\newcommand{\shekel}{\char"20AA\relax}

%% Inline English term inside a Hebrew sentence: \en{Business Model Canvas}
\newcommand{\en}[1]{\foreignlanguage{english}{#1}}

%% ---------------------------------------------------------------- core packages
\RequirePackage{graphicx}
\RequirePackage{amsmath,amssymb}
\RequirePackage{booktabs,tabularx,array,multirow}
\RequirePackage{enumitem}
\RequirePackage{csquotes}
\DeclareQuoteAlias{english}{hebrew}
\RequirePackage{siunitx}
\sisetup{group-separator={,},group-minimum-digits=4}
\RequirePackage{tikz}
\usetikzlibrary{positioning,shapes.geometric,arrows.meta,calc,
                backgrounds,shadows,fit,decorations.pathmorphing}
\RequirePackage[most]{tcolorbox}
\RequirePackage{listings}
\RequirePackage{float}
\graphicspath{{figures/generated/}}

\setlist{itemsep=2pt,topsep=4pt,leftmargin=*}
\setlist[itemize]{label={\color{rrLeaf}\rule[0.15em]{0.5em}{0.5em}}}

%% ---------------------------------------------------------------- captions
\RequirePackage{caption}
\captionsetup{font={small,color=rrStone},labelfont={bf,color=rrForest},
              labelsep=colon,skip=6pt}

%% ---------------------------------------------------------------- chapter + sections
\RequirePackage{titlesec}
\titleformat{\chapter}[display]
  {\sffamily\bfseries\color{rrForest}}
  {\begin{tikzpicture}
     \fill[rrForest] (0,0) rectangle (\linewidth,1.6);
     \fill[rrLeaf]   (0,0) rectangle (\linewidth,0.18);
     \node[text=white,font=\sffamily\bfseries\fontsize{40}{40}\selectfont,
           anchor=east] at (\linewidth-0.4cm,0.88) {\thechapter};
     \foreach \x in {0.5,1.1,1.7} \fill[rrLeaf!70] (\x,1.6) -- ++(0.25,0.35) -- ++(0.25,-0.35);
   \end{tikzpicture}}
  {8pt}
  {\Huge}
  [\vspace{2pt}{\color{rrLeaf}\titlerule[1.2pt]}]
\titleformat{name=\chapter,numberless}[display]
  {\sffamily\bfseries\color{rrForest}}{}{0pt}{\Huge}
  [\vspace{2pt}{\color{rrLeaf}\titlerule[1.2pt]}]
\titlespacing*{\chapter}{0pt}{-10mm}{8mm}

\titleformat{\section}
  {\sffamily\Large\bfseries\color{rrForest}}
  {\colorbox{rrLeaf}{\color{rrForest}\thesection}}{0.6em}{}
\titleformat{\subsection}
  {\sffamily\large\bfseries\color{rrForest!85}}{\thesubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{14pt}{6pt}
\titlespacing*{\subsection}{0pt}{10pt}{4pt}

%% ---------------------------------------------------------------- banner + footer
\RequirePackage{fancyhdr}
\newcommand{\rr@doctitle}{RoofRoot · גגון — תוכנית עסקית 2027}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyhead[C]{%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[rrForest] (current page.north west) rectangle
                    ([yshift=-13mm]current page.north east);
    \fill[rrLeaf] ([yshift=-13mm]current page.north west) rectangle
                  ([yshift=-14.2mm]current page.north east);
    \node[text=white,font=\sffamily\small\bfseries,anchor=center]
      at ([yshift=-6.5mm]current page.north) {\leftmark};
  \end{tikzpicture}}
\fancyfoot[C]{%
  \begin{tikzpicture}[remember picture,overlay]
    \draw[rrStone!60,line width=0.4pt]
      ([xshift=24mm,yshift=17mm]current page.south west) --
      ([xshift=-24mm,yshift=17mm]current page.south east);
    \node[font=\sffamily\footnotesize,text=rrStone,anchor=center]
      at ([yshift=12mm]current page.south) {\rr@doctitle};
    \node[font=\sffamily\small\bfseries,text=white,fill=rrForest,
          circle,inner sep=2pt,minimum size=7mm]
      at ([xshift=-20mm,yshift=12mm]current page.south east) {\thepage};
  \end{tikzpicture}}
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{%
  \begin{tikzpicture}[remember picture,overlay]
    \node[font=\sffamily\small\bfseries,text=white,fill=rrForest,
          circle,inner sep=2pt,minimum size=7mm]
      at ([xshift=-20mm,yshift=12mm]current page.south east) {\thepage};
  \end{tikzpicture}}}

%% ---------------------------------------------------------------- info boxes
\tcbset{rrbase/.style={enhanced,breakable,arc=2mm,boxrule=0pt,
        left=4mm,right=4mm,top=2mm,bottom=2mm,
        fonttitle=\sffamily\bfseries,coltitle=white}}
%% insight — a takeaway for the investor
\newtcolorbox{insightbox}[1][תובנה]{rrbase,colback=rrCream,colframe=rrForest,
  title={#1},borderline west={3pt}{0pt}{rrLeaf}}
%% risk — something that can go wrong
\newtcolorbox{riskbox}[1][סיכון]{rrbase,colback=rrTerra!8,colframe=rrTerra,
  title={#1}}
%% keynumber — one big metric:  \keynumber{₪4.2M}{הכנסות שנה 3}
\newcommand{\keynumber}[2]{%
  \begin{tcolorbox}[enhanced,width=0.31\linewidth,nobeforeafter,box align=top,
     colback=rrForest,colupper=white,arc=2mm,boxrule=0pt,halign=center,
     top=3mm,bottom=3mm]
     {\sffamily\bfseries\fontsize{20}{22}\selectfont\foreignlanguage{english}{#1}}\par\vspace{2pt}
     {\sffamily\small\color{rrLeaf!60!white}#2}
  \end{tcolorbox}}

%% ---------------------------------------------------------------- code box (LTR)
\lstdefinestyle{rrpython}{language=Python,basicstyle=\ttfamily\small,
  keywordstyle=\color{rrForest}\bfseries,stringstyle=\color{rrTerra},
  commentstyle=\color{rrStone}\itshape,numbers=left,numberstyle=\tiny\color{rrStone},
  numbersep=6pt,breaklines=true,columns=fullflexible,keepspaces=true,
  showstringspaces=false,tabsize=4}
%% listings builds each code line in its own box; force LTR there or babel
%% (bidi=basic) reorders the tokens right-to-left (incident INC-001).
\lst@AddToHook{Init}{\selectlanguage{english}\pardir TLT\textdir TLT\bodydir TLT}
\newtcblisting{pythonbox}[1][RootOS · Python]{enhanced,listing only,
  colback=rrCream,colframe=rrForest,boxrule=0.6pt,arc=2mm,
  left=8mm,right=3mm,top=1mm,bottom=1mm,
  title={\foreignlanguage{english}{#1}},fonttitle=\ttfamily\small\bfseries,
  listing options={style=rrpython},
  before={\par\selectlanguage{english}}}

%% ---------------------------------------------------------------- tables
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcommand{\rrtablehead}{\rowcolor{rrForest}}
\newcommand{\rrth}[1]{{\leavevmode\color{white}\sffamily\bfseries #1}}
\renewcommand{\arraystretch}{1.3}
\newcommand{\rrstripes}{\rowcolors{2}{rrSky!45}{white}}

%% ---------------------------------------------------------------- bibliography
\RequirePackage[backend=biber,style=ieee,autolang=other,language=english]{biblatex}
\setcounter{biburlnumpenalty}{100}
\setcounter{biburlucpenalty}{200}
\setcounter{biburllcpenalty}{200}
\AtBeginBibliography{\emergencystretch=3em\small}

%% Citations are LTR islands inside Hebrew text (INC-005): without the box the
%% bidi algorithm reorders "[1], [2]." into "]1[,]2[." and breaks captions.
\AtBeginDocument{%
  \let\rr@origcite\cite
  \DeclareRobustCommand{\cite}{\@ifnextchar[{\rr@citeopt}{\rr@citeplain}}}
\def\rr@citeopt[#1]#2{\babelsublr{\rr@origcite[#1]{#2}}}
\def\rr@citeplain#1{\babelsublr{\rr@origcite{#1}}}

%% Bibliography: Hebrew heading, English LTR list (labels on the correct side).
\newcommand{\rrbibliography}[1][מקורות]{%
  \chapter*{#1}\addcontentsline{toc}{chapter}{#1}\markboth{#1}{}%
  \begin{otherlanguage}{english}\printbibliography[heading=none]\end{otherlanguage}}

%% ---------------------------------------------------------------- hyperref (last)
\RequirePackage[hidelinks,unicode]{hyperref}
\hypersetup{pdftitle={RoofRoot Business Plan 2027},
            pdfauthor={RoofRoot team},pdfcreator={LuaLaTeX + roofroot.cls v\rr@clsversion}}

%% ---------------------------------------------------------------- cover page
%% \rrcover{title}{subtitle}{tagline}{meta line}
\newcommand{\rrcover}[4]{%
  \begin{titlepage}
    \input{figures/tikz/cover.tex}%
    \begin{tikzpicture}[remember picture,overlay]
      \node[anchor=north east,align=left,text width=15cm,inner sep=0]
        at ([xshift=-2.2cm,yshift=-3.0cm]current page.north east) {%
        {\sffamily\bfseries\color{rrForest}\fontsize{54}{56}\selectfont #1}\par\vspace{4mm}
        {\sffamily\color{rrForest!85}\fontsize{20}{24}\selectfont #2}\par\vspace{6mm}
        {\color{rrTerra}\rule{3cm}{3pt}}\par\vspace{4mm}
        {\large\color{rrInk}#3}};
      \node[anchor=south,fill=rrInk,text=rrCream,font=\sffamily\small,
            minimum width=\paperwidth,minimum height=9mm]
        at (current page.south) {#4};
    \end{tikzpicture}
  \end{titlepage}}
