"""Generate the (counter-based, realistic) Cinema Management System Excel workbook."""
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
    ("Login", "Manager, Cashier"),
    ("Logout", "Manager, Cashier"),
    ("Search / View Movies", "Cashier"),
    ("View Showtimes", "Cashier"),
    ("Sell Ticket", "Cashier (primary), Customer (secondary)"),
    ("Select Seat", "Cashier"),
    ("Check Seat Availability", "Cashier"),
    ("Take Payment", "Cashier"),
    ("Cancel Ticket", "Cashier"),
    ("Validate Ticket at Entrance", "Cashier"),
    ("View Sold Tickets", "Cashier"),
    ("Add Movie", "Manager"),
    ("Update Movie", "Manager"),
    ("Delete Movie", "Manager"),
    ("Manage Cinema Halls", "Manager"),
    ("Schedule Showtime", "Manager"),
    ("Update Showtime", "Manager"),
    ("Delete Showtime", "Manager"),
    ("Set Ticket Pricing", "Manager"),
    ("View Sales Report", "Manager"),
]
for i, (uc, actor) in enumerate(use_cases, start=1):
    ws.append([i, uc, actor])
    ws.cell(row=2 + i, column=1).alignment = CENTER
box(ws, 2, 2 + len(use_cases), 3)
ws.column_dimensions["A"].width = 6
ws.column_dimensions["B"].width = 32
ws.column_dimensions["C"].width = 36
ws.freeze_panes = "A3"

# ---- Sheet 2 : Use Case Specifications -------------------------------------
ws2 = wb.create_sheet("Use Case Specifications")
specs = [
    ("UC-05", "Sell Ticket", "Cashier (primary), Customer (secondary)",
     "Sells a ticket for a chosen showtime and seat: records the customer, takes payment and marks the seat sold.",
     "Cashier is logged in; a showtime with at least one free seat exists.",
     "A ticket is saved against the showtime and customer; the seat is marked sold.",
     "1. Select a movie and showtime. 2. Select a seat (include Select Seat). 3. Check seat is free "
     "(include Check Seat Availability). 4. Enter customer name, phone and ticket type (Adult/Kid). "
     "5. Show price and take payment (include Take Payment). 6. Save ticket and mark seat sold. "
     "7. Print/show the ticket.",
     "3a. Seat already sold -> choose another seat. 5a. Payment not completed -> release seat, no ticket. "
     "4a. Missing details -> validation error."),
    ("UC-01", "Login", "Manager, Cashier",
     "Authenticates a staff member and opens the menu according to their role.",
     "Application running; a valid staff account exists.",
     "Staff authenticated with role-based access.",
     "1. Enter username and password. 2. System validates and reads the role. 3. On success, the menu "
     "opens (full for Manager, selling for Cashier).",
     "2a. Invalid credentials -> show 'Invalid login credentials', stay on login screen."),
    ("UC-16", "Schedule Showtime", "Manager",
     "Schedules a movie in a hall at a given date, time and ticket price.",
     "Manager is logged in; at least one movie and one hall exist.",
     "A new showtime is stored.",
     "1. Open Showtime scheduling. 2. Choose movie and hall, enter date, time, ticket price. 3. Save. "
     "4. Validate and store the showtime.",
     "3a. A showtime already exists for that hall at that date/time -> clash error."),
    ("UC-12", "Add Movie", "Manager",
     "Adds a new movie to the catalogue.",
     "Manager is logged in.",
     "A new movie record is stored.",
     "1. Open Movie Management. 2. Enter title, genre, duration, rating. 3. Save. 4. Validate and store.",
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
ws2.column_dimensions["B"].width = 92
note = ws2.cell(row=r + 1, column=1,
                value="Replicate this template for: Update/Delete Movie, Manage Cinema Halls, "
                      "Update/Delete Showtime, Set Ticket Pricing, Search Movies, View Showtimes, "
                      "Cancel Ticket, Validate Ticket, View Sold Tickets, View Sales Report, Logout.")
note.font = Font(italic=True, color="808080")
ws2.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=2)

# ---- Sheet 3 : Database Design ---------------------------------------------
ws3 = wb.create_sheet("Database Design")
tables = {
    "staff": [("staff_id", "INT (auto)", "PK"), ("full_name", "VARCHAR(100)", ""),
              ("username", "VARCHAR(50)", "UQ"), ("password", "VARCHAR(255)", ""),
              ("role", "ENUM('MANAGER','CASHIER')", "")],
    "customer": [("customer_id", "INT (auto)", "PK"), ("full_name", "VARCHAR(100)", ""),
                 ("phone", "VARCHAR(20)", "")],
    "movie": [("movie_id", "INT (auto)", "PK"), ("title", "VARCHAR(120)", ""),
              ("genre", "VARCHAR(50)", ""), ("duration", "INT", ""), ("rating", "VARCHAR(10)", "")],
    "cinema_hall": [("hall_id", "INT (auto)", "PK"), ("hall_name", "VARCHAR(60)", ""),
                    ("capacity", "INT", "")],
    "showtime": [("show_id", "INT (auto)", "PK"), ("movie_id", "INT", "FK -> movie"),
                 ("hall_id", "INT", "FK -> cinema_hall"), ("show_date", "DATE", ""),
                 ("show_time", "TIME", "UQ(hall,date,time)"), ("ticket_price", "DECIMAL(8,2)", "")],
    "ticket": [("ticket_id", "INT (auto)", "PK"), ("show_id", "INT", "FK -> showtime"),
               ("customer_id", "INT", "FK -> customer"), ("seat_number", "VARCHAR(8)", "UQ(show,seat)"),
               ("ticket_type", "ENUM('Adult','Kid')", ""), ("price", "DECIMAL(8,2)", ""),
               ("purchase_datetime", "DATETIME", "")],
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
ws3.column_dimensions["A"].width = 20
ws3.column_dimensions["B"].width = 28
ws3.column_dimensions["C"].width = 20

out = "Cinema_Management_System.xlsx"
wb.save(out)
print("Saved", out)
