"""Generate the (realistic) Cinema Management System Excel workbook."""
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
    ("Register Account", "Customer"),
    ("Login", "Customer, Cashier, Manager"),
    ("Logout", "Customer, Cashier, Manager"),
    ("Search / Browse Movies", "Customer, Cashier"),
    ("View Showtimes", "Customer, Cashier"),
    ("Book Ticket", "Customer, Cashier"),
    ("Select Seats", "Customer, Cashier"),
    ("Make Payment", "Customer, Cashier"),
    ("View My Bookings", "Customer"),
    ("Cancel Booking", "Customer, Cashier"),
    ("Validate Ticket at Entrance", "Cashier"),
    ("Add Movie", "Manager"),
    ("Update Movie", "Manager"),
    ("Delete Movie", "Manager"),
    ("Schedule Showtime", "Manager"),
    ("Update Showtime", "Manager"),
    ("Delete Showtime", "Manager"),
    ("Manage Cinema Halls", "Manager"),
    ("Set Ticket Pricing", "Manager"),
    ("View Sales Report", "Manager"),
]
for i, (uc, actor) in enumerate(use_cases, start=1):
    ws.append([i, uc, actor])
    ws.cell(row=2 + i, column=1).alignment = CENTER
box(ws, 2, 2 + len(use_cases), 3)
ws.column_dimensions["A"].width = 6
ws.column_dimensions["B"].width = 34
ws.column_dimensions["C"].width = 30
ws.freeze_panes = "A3"

# ---- Sheet 2 : Use Case Specifications -------------------------------------
ws2 = wb.create_sheet("Use Case Specifications")
specs = [
    ("UC-06", "Book Ticket", "Customer (online), Cashier (counter)",
     "Reserves one or more seats for a showtime, takes payment and issues a ticket.",
     "Actor is logged in; a showtime with at least one free seat exists.",
     "A booking and ticket are saved; the chosen seats are marked sold.",
     "1. Select a movie and showtime. 2. System shows the seat map. 3. Select seats (include Select "
     "Seats). 4. System reserves seats and shows total. 5. Confirm and pay (include Make Payment). "
     "6. On success, save booking, issue ticket(s), mark seats sold. 7. Show ticket with reference.",
     "3a. Seat taken meanwhile -> choose another seat. 5a. Payment fails -> release seats, error, no ticket."),
    ("UC-08", "Make Payment", "Customer, Cashier",
     "Charges the customer for a booking.",
     "A booking with a total amount is awaiting payment.",
     "A payment record is created with status Paid or Failed.",
     "1. Show amount due and methods (Card, Mobile Money, Cash). 2. Choose method, enter details. "
     "3. Process payment, record as Paid.",
     "3a. Declined -> record Failed, notify; booking stays unpaid."),
    ("UC-15", "Schedule Showtime", "Manager",
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
     "1. Open Movie Management. 2. Enter title, genre, duration, language, rating. 3. Save. "
     "4. Validate and store the movie.",
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
                value="Replicate this template for: Update/Delete Movie, Update/Delete Showtime, "
                      "Manage Cinema Halls, Set Ticket Pricing, Register Account, View My Bookings, "
                      "Cancel Booking, Validate Ticket, View Sales Report, Logout.")
note.font = Font(italic=True, color="808080")
ws2.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=2)

# ---- Sheet 3 : Database Design ---------------------------------------------
ws3 = wb.create_sheet("Database Design")
tables = {
    "customer": [("customer_id", "INT (auto)", "PK"), ("full_name", "VARCHAR(100)", ""),
                 ("email", "VARCHAR(100)", ""), ("phone", "VARCHAR(20)", ""),
                 ("password", "VARCHAR(255)", "")],
    "staff": [("staff_id", "INT (auto)", "PK"), ("full_name", "VARCHAR(100)", ""),
              ("username", "VARCHAR(50)", ""), ("password", "VARCHAR(255)", ""),
              ("role", "ENUM('MANAGER','CASHIER')", "")],
    "movie": [("movie_id", "INT (auto)", "PK"), ("title", "VARCHAR(120)", ""),
              ("genre", "VARCHAR(50)", ""), ("duration", "INT", ""),
              ("language", "VARCHAR(40)", ""), ("rating", "VARCHAR(10)", "")],
    "cinema_hall": [("hall_id", "INT (auto)", "PK"), ("hall_name", "VARCHAR(60)", ""),
                    ("capacity", "INT", "")],
    "showtime": [("show_id", "INT (auto)", "PK"), ("movie_id", "INT", "FK -> movie"),
                 ("hall_id", "INT", "FK -> cinema_hall"), ("show_date", "DATE", ""),
                 ("show_time", "TIME", ""), ("ticket_price", "DECIMAL(8,2)", "")],
    "booking": [("booking_id", "INT (auto)", "PK"), ("customer_id", "INT", "FK -> customer"),
                ("show_id", "INT", "FK -> showtime"), ("booking_datetime", "DATETIME", ""),
                ("status", "ENUM('Paid','Cancelled','Pending')", ""),
                ("total_amount", "DECIMAL(8,2)", "")],
    "ticket": [("ticket_id", "INT (auto)", "PK"), ("booking_id", "INT", "FK -> booking"),
               ("seat_number", "VARCHAR(8)", ""), ("price", "DECIMAL(8,2)", "")],
    "payment": [("payment_id", "INT (auto)", "PK"), ("booking_id", "INT", "FK -> booking"),
                ("amount", "DECIMAL(8,2)", ""), ("method", "ENUM('Card','MobileMoney','Cash')", ""),
                ("payment_datetime", "DATETIME", ""), ("status", "ENUM('Paid','Failed')", "")],
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
