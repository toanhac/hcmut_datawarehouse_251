# Bank Churn DWH & DSS - Presentation

This directory contains the Beamer LaTeX presentation for the Bank Customer Churn Data Warehouse and Decision Support System project.

## Files

- `presentation.tex` - Main Beamer LaTeX source file
- `presentation.pdf` - Compiled PDF presentation (29 slides)

## Presentation Structure

### 1. Introduction (Slides 1-4)
- Title slide
- Table of contents
- Problem statement and motivation
- Project objectives
- Data overview

### 2. Data Warehouse Design (Slides 5-7)
- Star schema overview with TikZ diagram
- Dimension tables (dim_customer, dim_geo, dim_time, dim_segment)
- Fact table (fact_customer_status)
- Benefits of star schema

### 3. ETL Process (Slides 8-10)
- ETL pipeline overview
- Feature engineering (age_group, income_group)
- ETL results and statistics

### 4. OLAP Analysis & Visualization (Slides 11-13)
- OLAP query examples
- Insights from analysis
- Visualizations (churn by geography, age, products, balance)

### 5. Machine Learning (Slides 14-15)
- ML pipeline (preprocessing, models, evaluation)
- Model results (Logistic Regression, Random Forest)
- Feature importance analysis

### 6. Decision Support System (Slides 16-20)
- DSS architecture diagram
- Interactive dashboard features
- Dashboard screenshots
- Use case: Germany churn analysis

### 7. Results & Conclusion (Slides 21-26)
- Technical achievements
- Business insights
- Limitations and future work
- Tech stack overview
- Final conclusions

### 8. Demo & References (Slides 27-28)
- Demo instructions
- Q&A
- References

### 9. Backup Slides (Slides 29-30)
- SQL DDL examples
- Python ETL code examples

## Compiling the Presentation

### Prerequisites

```bash
# Install LaTeX (if not already installed)
sudo apt-get install texlive-latex-extra texlive-fonts-extra texlive-lang-vietnamese
```

### Compilation

```bash
# Compile once
pdflatex presentation.tex

# Compile twice for proper references
pdflatex presentation.tex
pdflatex presentation.tex
```

### Quick Compile

```bash
# Single command with error suppression
pdflatex -interaction=nonstopmode presentation.tex
```

## Viewing the Presentation

```bash
# Open with default PDF viewer
xdg-open presentation.pdf

# Or use evince
evince presentation.pdf

# Or use okular
okular presentation.pdf
```

## Presentation Features

- **Modern Beamer Theme**: Madrid theme with custom HCMUT blue color scheme
- **Visual Diagrams**: TikZ diagrams for star schema and DSS architecture
- **Code Listings**: Syntax-highlighted Python and SQL code examples
- **Charts & Figures**: Integration of matplotlib visualizations from reports/figures/
- **Interactive Elements**: Structured for easy navigation and Q&A

## Customization

### Change Colors

Edit the color definitions in the preamble:

```latex
\definecolor{hcmutblue}{RGB}{0,82,155}  % Main theme color
```

### Modify Theme

Change the theme and color theme:

```latex
\usetheme{Madrid}        % Try: Berlin, Copenhagen, Warsaw
\usecolortheme{default}  % Try: dolphin, seahorse, whale
```

### Add/Remove Slides

The presentation is organized by sections. Add new frames within sections:

```latex
\begin{frame}{Your Title}
    Your content here
\end{frame}
```

## Notes for Presenters

1. **Timing**: Approximately 20-25 minutes for full presentation
2. **Demo**: Prepare to run `python run_dashboard.py` for live demo
3. **Backup Slides**: Use if audience asks for technical details
4. **Q&A**: Prepare answers for:
   - Why Germany has high churn?
   - How to improve model recall?
   - Future deployment plans?
   - Cost-benefit analysis?

## Troubleshooting

### Missing Images

If images don't appear, ensure the path is correct:

```latex
\includegraphics[width=\textwidth]{../reports/figures/your_image.png}
```

### Font Issues

If Vietnamese characters don't display:

```bash
sudo apt-get install texlive-lang-vietnamese
```

### Compilation Errors

- Check that all `\begin{frame}` have matching `\end{frame}`
- Frames with `lstlisting` need `[fragile]` option
- Ensure all images exist in `../reports/figures/`

## License

This presentation is part of the university coursework for "Data Warehouse & Decision Support System" course.

## Authors

- Hoa Toàn Hạc (2201917)
- Mai Huy Hiệp (2211045)

## Acknowledgments

- HCMUT - Ho Chi Minh City University of Technology
- Faculty of Computer Science and Engineering
- Course: Data Warehouse & Decision Support System (Semester 242)
