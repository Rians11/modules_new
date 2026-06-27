"""Generate the Cinema Management System Excel workbook for the assignment."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ---- styling helpers -------------------------------------------------------
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

# ===========================================================================
# Sheet 1 : Use Cases (features table)
# ===========================================================================
ws = wb.active
ws.title = "Use Cases"
ws.merge_cells("A1:C1")
t = ws["A1"]
t.value = "Cinema Management System"
t.fill = TITLE_FILL
t.font = Font(color="FFFFFF", bold=True, size=14)
t.alignment = CENTER
ws.row_dimensions[1].height = 24

headers = ["No", "Use Case", "Actor"]
ws.append(headers)
style_header(ws, 2, 3)

use_cases = [
    ("Add Movie", "Manager"),
    ("Update Movie", "Manager"),
    ("Delete Movie", "Manager"),
    ("Search Movie by Title / Genre / Language / Rating", "Manager, Cashier, Customer"),
    ("Add Genre", "Manager"),
    ("Update Genre", "Manager"),
    ("Delete Genre", "Manager"),
    ("Search Genre by Name", "Manager"),
    ("Add Cinema Hall (Screen)", "Manager"),
    ("Update Cinema Hall", "Manager"),
    ("Delete Cinema Hall", "Manager"),
    ("Search Cinema Hall by Name / Capacity / Type", "Manager"),
    ("Configure Seat Layout", "Manager"),
    ("Update Seat", "Manager"),
    ("Delete Seat", "Manager"),
    ("Search Seat by Hall / Row / Type", "Manager, Cashier"),
    ("Add Screening (Showtime)", "Manager"),
    ("Update Screening", "Manager"),
    ("Delete Screening", "Manager"),
    ("Search Screening by Date / Movie / Hall / Time", "Manager, Cashier, Customer"),
    ("Register Customer", "Customer, Cashier"),
    ("Update Customer", "Customer, Cashier"),
    ("Delete Customer", "Manager"),
    ("Search Customer by Id / Name / Email / Phone", "Cashier, Manager"),
    ("Add Staff", "Manager"),
    ("Update Staff", "Manager"),
    ("Delete Staff", "Manager"),
    ("Search Staff by Id / Name / Role", "Manager"),
    ("Check Seat Availability", "Customer, Cashier"),
    ("Select Seats", "Customer, Cashier"),
    ("Create Booking (Reservation)", "Customer, Cashier"),
    ("Update Booking", "Customer, Cashier"),
    ("Cancel Booking", "Customer, Cashier"),
    ("Search Booking by Id / Customer / Date / Screening", "Cashier, Manager"),
    ("Process Payment", "Customer, Cashier, Payment Gateway"),
    ("Issue Refund", "Cashier, Manager, Payment Gateway"),
    ("Search Payment by Id / Date / Customer / Method", "Cashier, Manager"),
    ("Generate Ticket (QR Code)", "Cashier, Customer"),
    ("Cancel Ticket", "Cashier, Customer"),
    ("Validate Ticket at Entrance", "Usher"),
    ("Search Ticket by Code / Booking", "Usher, Cashier"),
    ("Add Snack / Concession Item", "Manager"),
    ("Update Snack", "Manager"),
    ("Delete Snack", "Manager"),
    ("Search Snack by Name / Category", "Cashier, Manager"),
    ("Create Snack Order", "Customer, Cashier"),
    ("Update Snack Order", "Customer, Cashier"),
    ("Cancel Snack Order", "Customer, Cashier"),
    ("Search Snack Order by Id / Customer", "Cashier, Manager"),
    ("Add Promotion / Discount", "Manager"),
    ("Update Promotion", "Manager"),
    ("Delete Promotion", "Manager"),
    ("Apply Promotion to Booking", "Cashier, Customer"),
    ("Search Promotion by Code / Period", "Cashier, Manager"),
    ("Generate Sales Report", "Manager"),
    ("Generate Hall Occupancy Report", "Manager"),
    ("Generate Movie Performance Report", "Manager"),
    ("Manage User Roles / Permissions", "Manager"),
    ("Login", "Customer, Cashier, Usher, Manager"),
    ("Logout", "Customer, Cashier, Usher, Manager"),
]
for i, (uc, actor) in enumerate(use_cases, start=1):
    ws.append([i, uc, actor])
    ws.cell(row=2 + i, column=1).alignment = CENTER
box(ws, 2, 2 + len(use_cases), 3)
ws.column_dimensions["A"].width = 6
ws.column_dimensions["B"].width = 55
ws.column_dimensions["C"].width = 34
ws.freeze_panes = "A3"

# ===========================================================================
# Sheet 2 : Use Case Specifications
# ===========================================================================
ws2 = wb.create_sheet("Use Case Specifications")
specs = [
    ("UC-31", "Create Booking", "Customer (primary), Cashier, Payment Gateway",
     "Allows a customer to reserve one or more seats for a chosen screening and pay for them.",
     "User is logged in; at least one screening with free seats exists.",
     "Booking recorded as Confirmed; selected seats marked Booked; ticket generated.",
     "1. Select screening. 2. System shows seat map (include Check Seat Availability). "
     "3. Select seats (include Select Seats). 4. System holds seats and shows total. "
     "5. Confirm booking. 6. Pay (include Process Payment). 7. Generate ticket with QR "
     "(include Generate Ticket). 8. Show confirmation.",
     "4a. Seat taken meanwhile -> ask for another seat. 6a. Payment fails -> release seats, "
     "show error. 5a. Promotion entered -> apply discount (extend) and recalculate."),
    ("UC-35", "Process Payment", "Customer/Cashier (primary), Payment Gateway",
     "Charges the customer for a booking and/or snack order.",
     "A pending booking/order with a total amount exists.",
     "A payment record is created with status Paid or Failed.",
     "1. Show amount due and methods. 2. Choose method, enter details. 3. Send to gateway. "
     "4. Gateway authorises and returns reference. 5. Record Paid, return success.",
     "4a. Declined -> record Failed, notify, no booking. 2a. Cash -> record cash received and change."),
    ("UC-40", "Validate Ticket at Entrance", "Usher",
     "Verifies a ticket is valid for the current screening and marks it used.",
     "Usher is logged in; ticket exists.",
     "Ticket status becomes Used; entry granted or refused.",
     "1. Scan QR code. 2. Look up ticket and screening. 3. Check Valid, right screening, not used. "
     "4. Mark Used, show Access granted with seat number.",
     "3a. Already used -> refuse. 3b. Wrong screening/expired -> Invalid ticket, refuse."),
    ("UC-01", "Add Movie", "Manager",
     "Adds a new movie to the catalogue.",
     "Manager is logged in.",
     "A new movie record is stored.",
     "1. Open Add Movie form. 2. Enter title, genre, duration, language, rating, synopsis, "
     "poster, release date. 3. Submit. 4. Validate and save, then confirm.",
     "3a. Required field missing / duplicate title -> validation error, not saved."),
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
    values = [uc_id, name, actors, desc, pre, post, main, alt]
    for fname, val in zip(fields, values):
        fc = ws2.cell(row=r, column=1, value=fname)
        fc.fill = SUB_FILL
        fc.font = BOLD
        fc.alignment = WRAP
        ws2.cell(row=r, column=2, value=val).alignment = WRAP
        r += 1
    r += 1  # blank spacer row
box(ws2, 1, r, 2)
ws2.column_dimensions["A"].width = 22
ws2.column_dimensions["B"].width = 85

note = ws2.cell(row=r + 1, column=1,
                value="Replicate this template for the remaining CRUD use cases "
                      "(Update/Delete/Search of each entity, Login, Logout).")
note.font = Font(italic=True, color="808080")
ws2.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=2)

# ===========================================================================
# Sheet 3 : Database Design
# ===========================================================================
ws3 = wb.create_sheet("Database Design")
tables = {
    "MOVIE": [("movie_id", "INT (auto)", "PK"), ("title", "VARCHAR(150)", ""),
              ("genre_id", "INT", "FK -> GENRE"), ("duration_min", "INT", ""),
              ("language", "VARCHAR(40)", ""), ("rating", "VARCHAR(10)", ""),
              ("release_date", "DATE", ""), ("synopsis", "TEXT", ""),
              ("poster_url", "VARCHAR(255)", ""), ("status", "VARCHAR(20)", "")],
    "GENRE": [("genre_id", "INT (auto)", "PK"), ("name", "VARCHAR(50)", "")],
    "CINEMA_HALL": [("hall_id", "INT (auto)", "PK"), ("name", "VARCHAR(50)", ""),
                    ("type", "VARCHAR(20)", ""), ("capacity", "INT", "")],
    "SEAT": [("seat_id", "INT (auto)", "PK"), ("hall_id", "INT", "FK -> CINEMA_HALL"),
             ("row_label", "VARCHAR(2)", ""), ("seat_number", "INT", ""),
             ("seat_type", "VARCHAR(20)", "")],
    "SCREENING": [("screening_id", "INT (auto)", "PK"), ("movie_id", "INT", "FK -> MOVIE"),
                  ("hall_id", "INT", "FK -> CINEMA_HALL"), ("show_date", "DATE", ""),
                  ("start_time", "TIME", ""), ("end_time", "TIME", ""),
                  ("base_price", "DECIMAL(8,2)", ""), ("format", "VARCHAR(10)", "")],
    "CUSTOMER": [("customer_id", "INT (auto)", "PK"), ("first_name", "VARCHAR(50)", ""),
                 ("last_name", "VARCHAR(50)", ""), ("email", "VARCHAR(100)", ""),
                 ("phone", "VARCHAR(20)", ""), ("password_hash", "VARCHAR(255)", "")],
    "STAFF": [("staff_id", "INT (auto)", "PK"), ("first_name", "VARCHAR(50)", ""),
              ("last_name", "VARCHAR(50)", ""), ("role", "VARCHAR(20)", ""),
              ("username", "VARCHAR(50)", ""), ("password_hash", "VARCHAR(255)", "")],
    "BOOKING": [("booking_id", "INT (auto)", "PK"), ("customer_id", "INT", "FK -> CUSTOMER"),
                ("screening_id", "INT", "FK -> SCREENING"), ("booking_datetime", "DATETIME", ""),
                ("status", "VARCHAR(20)", ""), ("total_amount", "DECIMAL(8,2)", ""),
                ("promotion_id", "INT", "FK -> PROMOTION (null)")],
    "BOOKING_SEAT": [("booking_seat_id", "INT (auto)", "PK"), ("booking_id", "INT", "FK -> BOOKING"),
                     ("seat_id", "INT", "FK -> SEAT"), ("price", "DECIMAL(8,2)", "")],
    "TICKET": [("ticket_id", "INT (auto)", "PK"), ("booking_id", "INT", "FK -> BOOKING"),
               ("qr_code", "VARCHAR(255)", ""), ("status", "VARCHAR(20)", ""),
               ("issued_at", "DATETIME", "")],
    "PAYMENT": [("payment_id", "INT (auto)", "PK"), ("booking_id", "INT", "FK -> BOOKING"),
                ("amount", "DECIMAL(8,2)", ""), ("method", "VARCHAR(20)", ""),
                ("status", "VARCHAR(20)", ""), ("paid_at", "DATETIME", ""),
                ("reference", "VARCHAR(50)", "")],
    "SNACK": [("snack_id", "INT (auto)", "PK"), ("name", "VARCHAR(50)", ""),
              ("category", "VARCHAR(30)", ""), ("price", "DECIMAL(8,2)", "")],
    "SNACK_ORDER": [("order_id", "INT (auto)", "PK"), ("customer_id", "INT", "FK -> CUSTOMER"),
                    ("order_datetime", "DATETIME", ""), ("total_amount", "DECIMAL(8,2)", "")],
    "SNACK_ORDER_ITEM": [("order_item_id", "INT (auto)", "PK"), ("order_id", "INT", "FK -> SNACK_ORDER"),
                         ("snack_id", "INT", "FK -> SNACK"), ("quantity", "INT", ""),
                         ("line_price", "DECIMAL(8,2)", "")],
    "PROMOTION": [("promotion_id", "INT (auto)", "PK"), ("code", "VARCHAR(20)", ""),
                  ("description", "VARCHAR(100)", ""), ("discount_percent", "DECIMAL(5,2)", ""),
                  ("start_date", "DATE", ""), ("end_date", "DATE", "")],
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
    r += 1  # spacer
ws3.column_dimensions["A"].width = 22
ws3.column_dimensions["B"].width = 22
ws3.column_dimensions["C"].width = 26

out = "Cinema_Management_System.xlsx"
wb.save(out)
print("Saved", out)
