# -*- coding: utf-8 -*-
from fpdf import FPDF

class PDF(FPDF):
        def header(this):
                # Logo
                #this.image('logo_pb.png',10,8,33)
                # Arial bold 15
                this.set_font('Arial','B',15)
                # Move to the right
                this.cell(80)
                # Title
                this.cell(30,10,'Title',1,0,'C')
                # Line break
                this.ln(20)

        # Page footer
        def footer(this):
                # Position at 1.5 cm from bottom
                this.set_y(-15)
                # Arial italic 8
                this.set_font('Arial','I',8)
                # Page number
                #this.cell(0,10,'Page '+str(this.PageNo())+'/{nb}',0,0,'C')

# Instanciation of inherited class
pdf=PDF()
pdf.alias_nb_pages()
pdf.add_page()
#pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
#pdf.set_font('DejaVu', '', 14)

#pdf.add_font('Arial', '', 'Arial.ttf', uni=True)
#pdf.set_font('Arial', '', 14)
pdf.set_font('Helvetica', '', 14)

for i in range(1,41):
        pdf.cell(0,10,('çþþþöðüi')+str(i),0,1)
pdf.output('tuto2.pdf','F')