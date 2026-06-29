"""Generate the (simplified) Cinema Management System Excel workbook."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

TITLE_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FILL = PatternFill("solid", fgColor="4472C4")
SUB_FILL = PatternFill("solid", fgColor="D9E1F2")
WHITE = Font(color="FFFFFF", bold=True)
BOLD = Font(bold=True)
thin = Side(style="thin", color="B0B0B0")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center")


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEAD_FILL
        cell.font = WHITE
        cell.alignment = CENTER
        cell.border = BORDER


def box(ws, r1, r2, ncols):
    for r in range(r1, r2 + 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER
            if not cell.alignment.wrap_text:
                cell.alignment = WRAP


wb = openpyxl.Workbook()

# ---- Sheet 1 : Use Cases ----------------------------------------------------
ws = wb.active
ws.title = "Use Cases"
ws.merge_cells("A1:C1")
t = ws["A1"]
t.value = "Cinema Management System"
t.fill = TITLE_FILL
t.font = Font(color="FFFFFF", bold=True, size=14)
t.alignment = CENTER
ws.row_dimensions[1].height = 24
ws.append(["No", "Use Case", "Actor"])
style_header(ws, 2, 3)

use_cases = [
    ("Login", "Administrator"),
    ("Logout", "Administrator"),
    ("Add Movie", "Administrator"),
    ("Update Movie", "Administrator"),
    ("Delete Movie", "Administrator"),
    ("View / Search Movies", "Administrator"),
    ("Add Cinema Hall", "Administrator"),
    ("View Cinema Halls", "Administrator"),
    ("Add Movie Show", "Administrator"),
    ("Update Movie Show", "Administrator"),
    ("Delete Movie Show", "Administrator"),
    ("View / Search Movie Shows", "Administrator"),
    ("Book Ticket", "Administrator (primary), Customer (secondary)"),
    ("Cancel Ticket", "Administrator"),
    ("View Sold Tickets", "Administrator"),
    ("Generate Sales Report", "Administrator"),
]
for i, (uc, actor) in enumerate(use_cases, start=1):
    ws.append([i, uc, actor])
    ws.cell(row=2 + i, column=1).alignment = CENTER
box(ws, 2, 2 + len(use_cases), 3)
ws.column_dimensions["A"].width = 6
ws.column_dimensions["B"].width = 40
ws.column_dimensions["C"].width = 36
ws.freeze_panes = "A3"

# ---- Sheet 2 : Use Case Specifications -------------------------------------
ws2 = wb.create_sheet("Use Case Specifications")
specs = [
    ("UC-13", "Book Ticket", "Administrator (primary), Customer (secondary)",
     "Sells a ticket for a chosen show and seat, records the customer and marks the seat as sold.",
     "Administrator is logged in; a show with a free seat exists.",
     "A ticket is saved against the show and customer; the seat becomes unavailable.",
     "1. Select a movie show. 2. Select a seat number. 3. Check seat is free (include Check Seat "
     "Availability). 4. Enter customer name and phone. 5. Read show ticket price (include Calculate "
     "Ticket Price). 6. Confirm; save ticket and mark seat sold. 7. Show confirmation.",
     "3a. Seat already sold -> ask for another seat. 4a. Missing details -> validation error, not saved."),
    ("UC-01", "Login", "Administrator",
     "Authenticates the administrator before granting access to the system.",
     "Application running; a valid account exists.",
     "Administrator authenticated; main menu opens.",
     "1. Enter username and password. 2. System validates against the database. 3. On success, main menu opens.",
     "2a. Invalid credentials -> show 'Invalid login credentials', stay on login screen."),
    ("UC-09", "Add Movie Show", "Administrator",
     "Schedules a movie in a hall at a given date, time and ticket price.",
     "Administrator is logged in; at least one movie and one hall exist.",
     "A new show record is stored.",
     "1. Open Show Management. 2. Choose movie and hall, enter date, time, ticket price. 3. Click Add. "
     "4. Validate and save, refresh table.",
     "3a. A show already exists for that hall at that date/time -> duplicate error."),
    ("UC-03", "Add Movie", "Administrator",
     "Adds a new movie to the catalogue.",
     "Administrator is logged in.",
     "A new movie record is stored.",
     "1. Open Movie Management. 2. Enter title, genre, duration. 3. Click Add. 4. Validate and save, refresh table.",
     "3a. Duplicate title / missing field -> error, not saved."),
]
fields = ["Use Case ID", "Use Case Name", "Actor(s)", "Description",
          "Preconditions", "Postconditions", "Main Flow", "Alternative Flows"]
r = 1
for uc_id, name, actors, desc, pre, post, main, alt in specs:
    ws2.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
    h = ws2.cell(row=r, column=1, value=f"{uc_id}  —  {name}")
    h.fill = HEAD_FILL
    h.font = WHITE
    h.alignment = Alignment(horizontal="left", vertical="center")
    ws2.cell(row=r, column=2).fill = HEAD_FILL
    r += 1
    for fname, val in zip(fields, [uc_id, name, actors, desc, pre, post, main, alt]):
        fc = ws2.cell(row=r, column=1, value=fname)
        fc.fill = SUB_FILL
        fc.font = BOLD
        fc.alignment = WRAP
        ws2.cell(row=r, column=2, value=val).alignment = WRAP
        r += 1
    r += 1
box(ws2, 1, r, 2)
ws2.column_dimensions["A"].width = 22
ws2.column_dimensions["B"].width = 90
note = ws2.cell(row=r + 1, column=1,
                value="Replicate this template for: Update/Delete/View Movie, Add/View Hall, "
                      "Update/Delete/View Show, Cancel Ticket, View Sold Tickets, Generate Sales Report, Logout.")
note.font = Font(italic=True, color="808080")
ws2.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=2)

# ---- Sheet 3 : Database Design ---------------------------------------------
ws3 = wb.create_sheet("Database Design")
tables = {
    "user": [("user_id", "INT (auto)", "PK"), ("username", "VARCHAR(50)", ""),
             ("password", "VARCHAR(100)", "")],
    "movie": [("movie_id", "INT (auto)", "PK"), ("title", "VARCHAR(120)", ""),
              ("genre", "VARCHAR(50)", ""), ("duration", "INT", "")],
    "cinema_hall": [("hall_id", "INT (auto)", "PK"), ("hall_name", "VARCHAR(60)", ""),
                    ("capacity", "INT", "")],
    "movie_show": [("show_id", "INT (auto)", "PK"), ("movie_id", "INT", "FK -> movie"),
                   ("hall_id", "INT", "FK -> cinema_hall"), ("show_date", "DATE", ""),
                   ("show_time", "TIME", ""), ("ticket_price", "DECIMAL(8,2)", "")],
    "customer": [("customer_id", "INT (auto)", "PK"), ("full_name", "VARCHAR(100)", ""),
                 ("phone", "VARCHAR(20)", "")],
    "ticket": [("ticket_id", "INT (auto)", "PK"), ("show_id", "INT", "FK -> movie_show"),
               ("customer_id", "INT", "FK -> customer"), ("seat_number", "INT", ""),
               ("price", "DECIMAL(8,2)", ""), ("purchase_date", "DATETIME", "")],
}
r = 1
for tname, cols in tables.items():
    ws3.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    th = ws3.cell(row=r, column=1, value=tname)
    th.fill = TITLE_FILL
    th.font = Font(color="FFFFFF", bold=True)
    r += 1
    for j, head in enumerate(["Attribute", "Data Type", "Key"], start=1):
        c = ws3.cell(row=r, column=j, value=head)
        c.fill = SUB_FILL
        c.font = BOLD
        c.border = BORDER
    r += 1
    for attr, dtype, key in cols:
        ws3.cell(row=r, column=1, value=attr).border = BORDER
        ws3.cell(row=r, column=2, value=dtype).border = BORDER
        ws3.cell(row=r, column=3, value=key).border = BORDER
        r += 1
    r += 1
ws3.column_dimensions["A"].width = 18
ws3.column_dimensions["B"].width = 16
ws3.column_dimensions["C"].width = 20

out = "Cinema_Management_System.xlsx"
wb.save(out)
print("Saved", out)
