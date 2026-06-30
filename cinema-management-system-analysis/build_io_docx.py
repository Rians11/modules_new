"""Generate an editable Word .docx of the Input & Output Design (no external libs)."""
import zipfile
from xml.sax.saxutils import escape

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def para(text="", bold=False, center=False, size=None):
    rpr = ""
    if bold or size:
        rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + (f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>' if size else "") + "</w:rPr>"
    ppr = "<w:pPr>" + ('<w:jc w:val="center"/>' if center else "") + "</w:pPr>"
    run = f"<w:r>{rpr}<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r>" if text else ""
    return f"<w:p>{ppr}{run}</w:p>"


def heading(text):
    return para(text, bold=True, size=30)


BORDERS = ('<w:tblBorders>'
           '<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
           '</w:tblBorders>')


def table(rows, header=True):
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>{BORDERS}</w:tblPr>']
    for ri, row in enumerate(rows):
        out.append("<w:tr>")
        for cell in row:
            b = header and ri == 0
            out.append(f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>{para(str(cell), bold=b)}</w:tc>')
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def box(paragraphs):
    """Single-cell bordered box containing the given paragraph XML strings."""
    inner = "".join(paragraphs)
    return (f'<w:tbl><w:tblPr><w:tblW w:w="7000" w:type="dxa"/>{BORDERS}</w:tblPr>'
            f'<w:tr><w:tc><w:tcPr><w:tcW w:w="7000" w:type="dxa"/></w:tcPr>{inner}</w:tc></w:tr></w:tbl>')


def form_box(title, fields, buttons):
    paras = [para(title, bold=True, center=True)]
    paras += [para(f) for f in fields]
    paras.append(para(buttons, bold=True, center=True))
    return box(paras)


def pagebreak():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


U = "______________"
body = []

# ---- Section 5 : Input ----
body.append(heading("5. Input Design (Forms / Dialog Boxes)"))
body.append(para())
body.append(form_box("LOGIN", [f"Username : {U}", f"Password : {U}"], "[ Login ]"))
body.append(para())
body.append(form_box("ADD MOVIE",
                     [f"Title : {U}", f"Genre : {U}", f"Duration : {U}", f"Language : {U}", f"Rating : {U}"],
                     "[ Add ]   [ Update ]   [ Delete ]"))
body.append(para())
body.append(form_box("ADD SHOWTIME",
                     [f"Movie : {U}", f"Cinema Hall : {U}", f"Date : {U}", f"Time : {U}", f"Ticket Price : {U}"],
                     "[ Save ]"))
body.append(para())
body.append(form_box("BOOK TICKET",
                     [f"Customer Name : {U}", f"Phone Number : {U}",
                      f"Showtime (Movie / Date / Time) : {U}", f"Seat Number : {U}",
                      f"Payment Method : {U}"],
                     "[ Book ]"))
body.append(para())
body.append(para("Note: the other data-entry forms (Add Genre, Add Cinema Hall, Add Staff, "
                 "Add Customer, Add Snack, Add Promotion) follow the same layout as the Add Movie form."))
body.append(para())
body.append(para("Dialog Boxes", bold=True, size=26))
body.append(form_box("Confirm Booking",
                     ["Would you confirm the booking of 2 seats for \"Avengers\" (15/04/2025, 17h00)?"],
                     "[ Confirm ]   [ Cancel ]"))
body.append(para())
body.append(form_box("Delete Movie",
                     ["Are you sure you want to delete this movie? This action is irreversible."],
                     "[ Yes (Delete) ]   [ No ]"))

# ---- Section 6 : Output ----
body.append(pagebreak())
body.append(heading("6. Output Design (Screen / Paper)"))
body.append(para())
body.append(para("Movie List", bold=True, size=26))
body.append(table([["ID", "Title", "Genre", "Duration", "Rating"],
                   ["1", "Avengers", "Action", "143 min", "PG-13"],
                   ["2", "The Rookie", "Series", "45 min", "PG"],
                   ["3", "Scream", "Horror", "114 min", "18"],
                   ["4", "Afterburn", "Comedy", "98 min", "PG-13"]]))
body.append(para())
body.append(para("Seat Map (plan of the room)", bold=True, size=26))
body.append(para("Rows A, B, C and columns 1-5. Colour code: Green = available, Red = sold, Blue = selected."))
body.append(table([["", "1", "2", "3", "4", "5"],
                   ["A", "A1", "A2", "A3 (sold)", "A4", "A5"],
                   ["B", "B1", "B2 (sel)", "B3 (sel)", "B4 (sold)", "B5"],
                   ["C", "C1", "C2", "C3", "C4", "C5 (sold)"]]))
body.append(para())
body.append(para("Booking Summary (before payment)", bold=True, size=26))
body.append(table([["Film", "Showtime", "Seats", "Quantity", "Unit Price", "Total"],
                   ["Avengers", "15/04/2025 17h00 - Hall 4", "B2, B3", "2", "20.00", "40.00"]]))
body.append(para())
body.append(para("Ticket (printout)", bold=True, size=26))
body.append(box([para("CINEMA MANAGEMENT SYSTEM", bold=True, center=True),
                 para("Movie : Avengers"), para("Room : 4"), para("Date : 15/04/2025"),
                 para("Time : 17h00"), para("Seat : B2, B3"), para("N° Ticket : 10066")]))
body.append(para())
body.append(para("Sales Report (paper)", bold=True, size=26))
body.append(table([["Date", "Movie", "Tickets Sold", "Revenue"],
                   ["15/04/2025", "Avengers", "120", "2,400.00"],
                   ["15/04/2025", "Scream", "80", "1,440.00"],
                   ["Total", "", "200", "3,840.00"]]))

document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document xmlns:w="{W}"><w:body>{"".join(body)}'
            f'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr>'
            f'</w:body></w:document>')

content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                 '<Default Extension="xml" ContentType="application/xml"/>'
                 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                 '</Types>')

rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')

with zipfile.ZipFile("Cinema_IO_Design.docx", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)

print("Saved Cinema_IO_Design.docx")
