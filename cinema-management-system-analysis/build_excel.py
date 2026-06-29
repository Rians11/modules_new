"""Generate the Cinema Management System Excel workbook (aligned with the built Java system)."""
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
    ("Login", "Administrator, Cashier"),
    ("Logout", "Administrator, Cashier"),
    ("Add Movie", "Administrator"),
    ("Update Movie", "Administrator"),
    ("Delete Movie", "Administrator"),
    ("View / Search Movies", "Cashier"),
    ("Add Cinema Hall", "Administrator"),
    ("Update Cinema Hall", "Administrator"),
    ("Delete Cinema Hall", "Administrator"),
    ("View Cinema Halls", "Administrator"),
    ("Add Movie Show", "Administrator"),
    ("Update Movie Show", "Administrator"),
    ("Delete Movie Show", "Administrator"),
    ("View Movie Shows", "Cashier"),
    ("Update Ticket Pricing (Weekday/Weekend - Adult/Kid)", "Administrator"),
    ("View Ticket Pricing", "Cashier"),
    ("Book Ticket (Sell Ticket)", "Cashier (primary), Customer (secondary)"),
    ("Select Seat", "Cashier"),
    ("Check Seat Availability", "Cashier"),
    ("Calculate Ticket Price", "Cashier"),
    ("View Sold Tickets", "Cashier"),
    ("Update Ticket", "Cashier"),
    ("Cancel / Delete Ticket", "Cashier"),
]
for i, (uc, actor) in enumerate(use_cases, start=1):
    ws.append([i, uc, actor])
    ws.cell(row=2 + i, column=1).alignment = CENTER
box(ws, 2, 2 + len(use_cases), 3)
ws.column_dimensions["A"].width = 6
ws.column_dimensions["B"].width = 52
ws.column_dimensions["C"].width = 32
ws.freeze_panes = "A3"

# ---- Sheet 2 : Use Case Specifications -------------------------------------
ws2 = wb.create_sheet("Use Case Specifications")
specs = [
    ("UC-17", "Book Ticket (Sell Ticket)", "Cashier (primary), Customer (secondary)",
     "Sells a ticket for a chosen show and seat, calculates the price automatically and marks the seat as unavailable. The customer provides details and receives the ticket.",
     "Administrator is logged in; a show with a free seat exists; pricing is configured.",
     "A ticket record is saved; the chosen seat becomes unavailable.",
     "1. Select a movie show. 2. Select a seat (include Select Seat). 3. Check seat is free "
     "(include Check Seat Availability). 4. Enter customer details and ticket type (Adult/Kid). "
     "5. System calculates price from pricing rules (include Calculate Ticket Price). "
     "6. Confirm; save ticket and mark seat sold. 7. Show confirmation.",
     "3a. Seat already sold -> ask for another seat. 4a. Invalid/missing input -> validation error, not saved."),
    ("UC-01", "Login", "Administrator, Cashier",
     "Authenticates the user and opens the dashboard according to the role (ADMIN or CASHIER).",
     "Application running; a valid account exists in the users table.",
     "User authenticated; dashboard opens with role-based access.",
     "1. Enter username and password. 2. System validates against the users table and reads the role. "
     "3. On success, dashboard opens (full menu for ADMIN, ticket menu for CASHIER).",
     "2a. Invalid credentials -> show 'Invalid login credentials', stay on login screen."),
    ("UC-15", "Update Ticket Pricing", "Administrator",
     "Updates ticket prices that vary by day type (weekday/weekend) and category (adult/kid), without changing code.",
     "Administrator is logged in.",
     "New prices stored and used automatically by the booking screen.",
     "1. Open Pricing Management. 2. System shows current prices. 3. Edit prices and save. "
     "4. Store new prices; bookings use them automatically.",
     "3a. Invalid numeric input -> validation error, prices unchanged."),
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
                value="Replicate this template for the remaining CRUD use cases (Update/Delete/View of "
                      "Movie, Hall, Show; View Pricing; View/Update/Cancel Ticket; Logout).")
note.font = Font(italic=True, color="808080")
ws2.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=2)

# ---- Sheet 3 : Database Design ---------------------------------------------
ws3 = wb.create_sheet("Database Design")
tables = {
    "users": [("user_id", "INT(11)", "PK"), ("username", "VARCHAR(50)", "UQ"),
              ("password", "VARCHAR(100)", ""),
              ("role", "ENUM('ADMIN','CASHIER')", "default 'CASHIER'")],
    "customer": [("customer_id", "INT(11)", "PK"), ("full_name", "VARCHAR(100)", ""),
                 ("phone", "VARCHAR(20)", "")],
    "movie": [("movie_id", "INT(11)", "PK"), ("title", "VARCHAR(120)", "UQ"),
              ("genre", "VARCHAR(50)", ""), ("duration", "INT(11)", "")],
    "cinema_hall": [("hall_id", "INT(11)", "PK"), ("hall_name", "VARCHAR(60)", "UQ"),
                    ("capacity", "INT(11)", "")],
    "movie_show": [("show_id", "INT(11)", "PK"), ("movie_id", "INT(11)", "FK -> movie"),
                   ("hall_id", "INT(11)", "FK -> cinema_hall"), ("show_date", "DATE", ""),
                   ("show_time", "TIME", "UQ(hall_id,date,time)")],
    "pricing_config": [("id", "INT(11)", "PK"), ("weekday_adult", "INT(11)", ""),
                       ("weekday_kid", "INT(11)", ""), ("weekend_adult", "INT(11)", ""),
                       ("weekend_kid", "INT(11)", ""),
                       ("updated_at", "TIMESTAMP", "default CURRENT_TIMESTAMP")],
    "ticket": [("ticket_id", "INT(11)", "PK"), ("show_id", "INT(11)", "FK -> movie_show"),
               ("seat_number", "INT(11)", "UQ(show_id,seat)"),
               ("customer_id", "INT(11)", "FK -> customer"),
               ("ticket_type", "ENUM('Adult','Kid')", ""), ("price", "DECIMAL(10,2)", ""),
               ("purchase_date", "TIMESTAMP", "default CURRENT_TIMESTAMP")],
    "show_details": [("details_id", "INT(11)", "PK"), ("show_id", "INT(11)", "UQ -> movie_show"),
                     ("movie_name", "VARCHAR(120)", ""), ("hall_name", "VARCHAR(60)", "")],
}
r = 1
for tname, cols in tables.items():
    ws3.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    th = ws3.cell(row=r, column=1, value=tname)
    th.fill = TITLE_FILL
    th.font = Font(color="FFFFFF", bold=True)
    r += 1
    for j, head in enumerate(["Attribute", "Data Type", "Key / Note"], start=1):
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
ws3.column_dimensions["B"].width = 18
ws3.column_dimensions["C"].width = 22

out = "Cinema_Management_System.xlsx"
wb.save(out)
print("Saved", out)
