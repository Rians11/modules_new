"""Generate the Cinema Management System deliverables:
   - Cinema_Management_System.xlsx  (Use Cases, all 57 Use Case Specifications, Database Design)
   - Cinema_Management_System_Report.html  (full all-in-one report -> converted to PDF by LibreOffice)
"""
import html
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ===========================================================================
# DATA (single source of truth)
# ===========================================================================
STUDENT = dict(name="ANDRIAMPARANY Rianala Joan", sid="2504_28605", cohort="BSE25A/FT/2")

USE_CASES = [  # (name, actor)
    ("Add Movie", "Manager"), ("Update Movie", "Manager"), ("Delete Movie", "Manager"),
    ("Search Movie by Title, Genre, Language", "Cashier"),
    ("Add Genre", "Manager"), ("Update Genre", "Manager"), ("Delete Genre", "Manager"),
    ("Search Genre by Name", "Manager"),
    ("Add Cinema Hall", "Manager"), ("Update Cinema Hall", "Manager"), ("Delete Cinema Hall", "Manager"),
    ("Search Cinema Hall by Name, Type, Capacity", "Manager"),
    ("Add Showtime", "Manager"), ("Update Showtime", "Manager"), ("Delete Showtime", "Manager"),
    ("Search Showtime by Date, Movie, Hall, Time", "Cashier"),
    ("Add Customer", "Cashier"), ("Update Customer", "Cashier"), ("Delete Customer", "Cashier"),
    ("Search Customer by Id, Name, Phone", "Cashier"),
    ("Add Staff", "Manager"), ("Update Staff", "Manager"), ("Delete Staff", "Manager"),
    ("Search Staff by Id, Name, Role", "Manager"),
    ("Add Booking", "Cashier"), ("Update Booking", "Cashier"), ("Delete Booking", "Cashier"),
    ("Search Booking by Id, Customer, Date, Showtime", "Cashier"),
    ("Add Ticket", "Cashier"), ("Update Ticket", "Cashier"), ("Delete Ticket", "Cashier"),
    ("Search Ticket by Code, Showtime, Customer", "Cashier"),
    ("Add Payment", "Cashier"), ("Update Payment", "Cashier"), ("Delete Payment", "Cashier"),
    ("Search Payment by Id, Date, Method, Customer", "Cashier"),
    ("Add Snack", "Manager"), ("Update Snack", "Manager"), ("Delete Snack", "Manager"),
    ("Search Snack by Name, Category", "Cashier"),
    ("Sell Snack", "Cashier"),
    ("Add Promotion", "Manager"), ("Update Promotion", "Manager"), ("Delete Promotion", "Manager"),
    ("Search Promotion by Code, Period", "Cashier"),
    ("Post Showtime", "Manager"), ("Unpost Showtime", "Manager"),
    ("Select Seat", "Cashier"), ("Apply Promotion to Booking", "Cashier"),
    ("Generate Ticket", "Cashier"), ("Validate Ticket at Entrance", "Cashier"),
    ("Issue Refund", "Cashier"),
    ("Generate Sales Report", "Manager"), ("Generate Hall Occupancy Report", "Manager"),
    ("Manage User Roles", "Manager"),
    ("Login", "Cashier"), ("Logout", "Cashier"),
]

# Detailed specifications for business operations (keyed by exact use case name)
BUSINESS = {
    "Add Booking": dict(
        desc="The cashier creates a booking for a showtime on behalf of a customer: selects seats, applies any promotion, takes payment and issues the ticket.",
        pre="The cashier is logged in; a posted showtime with a free seat exists.",
        post="A booking, ticket and payment are saved; the seats are marked sold.",
        main="1. Select a posted showtime. 2. Select one or more seats («include» Select Seat). "
             "3. Enter/select the customer. 4. (optional) Apply a promotion («extend» Apply Promotion). "
             "5. Take payment («include» Add Payment). 6. Save the booking and issue the ticket "
             "(«include» Generate Ticket); mark the seats sold. 7. Print/show the ticket.",
        alt="2a. Seat already sold → choose another seat. 5a. Payment fails → release the seats, no ticket."),
    "Select Seat": dict(
        desc="Chooses one or more available seats for a showtime.",
        pre="A showtime is selected; a seat map is displayed.",
        post="The chosen seats are reserved for the booking.",
        main="1. The system shows available seats. 2. The cashier selects the seat(s). 3. The seats are held.",
        alt="2a. Seat just taken → ask for another seat."),
    "Add Payment": dict(
        desc="Charges the customer for a booking.",
        pre="A booking with a total amount is awaiting payment.",
        post="A payment record is created (Paid or Failed).",
        main="1. Show the amount due and methods (Card, Mobile, Cash). 2. Choose a method. 3. Process payment, record as Paid.",
        alt="3a. Declined → record Failed; booking stays unpaid."),
    "Generate Ticket": dict(
        desc="Issues the ticket(s) for a paid booking with a unique code.",
        pre="The booking is paid.",
        post="Ticket(s) are created with status Valid and printed/shown.",
        main="1. Create a ticket per seat with a unique code. 2. Print/show the ticket(s).",
        alt="—"),
    "Validate Ticket at Entrance": dict(
        desc="Checks that a presented ticket is valid for the current showtime and marks it used.",
        pre="The cashier is logged in; the ticket exists.",
        post="The ticket is marked Used; entry granted or refused.",
        main="1. Scan/enter the ticket code. 2. Find the ticket and showtime. 3. Check it is Valid, "
             "for the right showtime and not used. 4. Mark Used and show 'Access granted' with the seat.",
        alt="3a. Already used / wrong showtime → 'Invalid ticket', refuse entry."),
    "Apply Promotion to Booking": dict(
        desc="Applies a valid promotion code to a booking to reduce the total.",
        pre="A booking is in progress; a valid promotion exists.",
        post="The discount is applied and the total recalculated.",
        main="1. Enter the promotion code. 2. The system checks it is valid and in date. 3. Apply the discount.",
        alt="2a. Invalid/expired code → no discount; show a message."),
    "Issue Refund": dict(
        desc="Refunds a cancelled booking.",
        pre="The booking is paid and being cancelled.",
        post="A refund payment is recorded; the ticket status becomes Refunded.",
        main="1. Select the cancelled booking. 2. Confirm the refund. 3. Record the refund and mark the ticket Refunded.",
        alt="2a. Booking not paid → nothing to refund."),
    "Sell Snack": dict(
        desc="Sells one or more snacks to a customer and records the snack order.",
        pre="The cashier is logged in; snacks exist in the menu.",
        post="A snack order is saved with its line(s) and total.",
        main="1. Select the snack(s) and quantity. 2. The system computes the total. 3. Take payment. 4. Save the snack order.",
        alt="2a. Snack out of stock → choose another."),
    "Post Showtime": dict(
        desc="Publishes a showtime so it becomes available for selling tickets.",
        pre="The manager is logged in; the showtime exists.",
        post="The showtime status becomes Posted.",
        main="1. Select the showtime. 2. Click Post. 3. The status becomes Posted.",
        alt="—"),
    "Unpost Showtime": dict(
        desc="Hides a showtime so tickets can no longer be sold for it.",
        pre="The manager is logged in; the showtime is Posted.",
        post="The showtime status becomes Unposted.",
        main="1. Select the showtime. 2. Click Unpost. 3. The status becomes Unposted.",
        alt="2a. Tickets already sold → warn before unposting."),
    "Generate Sales Report": dict(
        desc="Produces a report of tickets sold and revenue for a chosen period.",
        pre="The manager is logged in.",
        post="A report is displayed/printed.",
        main="1. Choose the period. 2. The system totals tickets sold and revenue. 3. Display the report with a grand total.",
        alt="1a. No data → zero totals."),
    "Generate Hall Occupancy Report": dict(
        desc="Shows, per showtime, the seats sold versus capacity and the occupancy rate.",
        pre="The manager is logged in.",
        post="An occupancy report is displayed/printed.",
        main="1. Choose the period/hall. 2. The system computes seats sold / capacity per showtime. 3. Display the report.",
        alt="—"),
    "Manage User Roles": dict(
        desc="Assigns or changes the role (Manager/Cashier) of a staff account.",
        pre="The manager is logged in.",
        post="The staff member's role is updated.",
        main="1. Select the staff account. 2. Choose the role. 3. Save.",
        alt="—"),
    "Login": dict(
        desc="Authenticates a staff member and opens the menu according to their role.",
        pre="The application is running; a valid staff account exists.",
        post="The staff member is authenticated with role-based access.",
        main="1. Enter username and password. 2. The system validates and reads the role. 3. Open the menu (full for Manager, selling for Cashier).",
        alt="2a. Invalid credentials → show 'Invalid login credentials', stay on the login screen."),
    "Logout": dict(
        desc="Ends the staff member's session securely.",
        pre="A staff member is logged in.",
        post="The session is closed; the login screen is shown.",
        main="1. Click Logout. 2. The system closes the session and returns to the login screen.",
        alt="—"),
}


def split_search(name):
    """'Search Movie by Title, Genre' -> ('Movie', 'Title, Genre')"""
    core = name[len("Search "):]
    if " by " in core:
        entity, crit = core.split(" by ", 1)
    else:
        entity, crit = core, "the given criteria"
    return entity.strip(), crit.strip()


def make_spec(no, name, actor):
    """Return dict(id,name,actor,desc,pre,post,main,alt) for any use case."""
    uc_id = f"UC-{no:02d}"
    if name in BUSINESS:
        b = BUSINESS[name]
        return dict(id=uc_id, name=name, actor=actor, **b)
    pre = f"The {actor} is logged in."
    if name.startswith("Add "):
        e = name[4:]
        return dict(id=uc_id, name=name, actor=actor,
                    desc=f"Adds a new {e.lower()} to the system.", pre=pre,
                    post=f"A new {e.lower()} record is stored.",
                    main=f"1. Open the {e} form. 2. Enter the {e.lower()} details. 3. Click Save. "
                         f"4. The system validates the data and stores the new {e.lower()}.",
                    alt="3a. A required field is missing or a duplicate exists → the system shows an error and nothing is saved.")
    if name.startswith("Update "):
        e = name[7:]
        return dict(id=uc_id, name=name, actor=actor,
                    desc=f"Modifies the details of an existing {e.lower()}.", pre=pre,
                    post=f"The {e.lower()} record is updated.",
                    main=f"1. Search and select the {e.lower()}. 2. Edit the details. 3. Click Save. "
                         f"4. The system validates and updates the record.",
                    alt="3a. Invalid data → error, no change is saved.")
    if name.startswith("Delete "):
        e = name[7:]
        return dict(id=uc_id, name=name, actor=actor,
                    desc=f"Removes a {e.lower()} from the system.", pre=pre,
                    post=f"The {e.lower()} record is deleted.",
                    main=f"1. Select the {e.lower()}. 2. Confirm the deletion. 3. The system removes the record.",
                    alt=f"2a. The {e.lower()} is referenced elsewhere → the deletion is blocked with a warning.")
    if name.startswith("Search "):
        e, crit = split_search(name)
        return dict(id=uc_id, name=name, actor=actor,
                    desc=f"Finds {e.lower()} records by {crit.lower()}.", pre=pre,
                    post="The matching records are displayed.",
                    main=f"1. Enter the search criteria ({crit}). 2. The system displays the matching {e.lower()} records.",
                    alt="2a. No match → the system shows an empty result.")
    # fallback (shouldn't happen)
    return dict(id=uc_id, name=name, actor=actor, desc="", pre=pre, post="", main="", alt="—")


UC_INFO = {name: (i, actor) for i, (name, actor) in enumerate(USE_CASES, start=1)}

# Representative set: 4 CRUD templates (on Movie) + every business operation.
SPEC_ORDER = [
    "Add Movie", "Update Movie", "Delete Movie", "Search Movie by Title, Genre, Language",
    "Add Booking", "Select Seat", "Add Payment", "Generate Ticket",
    "Apply Promotion to Booking", "Issue Refund", "Validate Ticket at Entrance",
    "Sell Snack", "Post Showtime", "Unpost Showtime",
    "Generate Sales Report", "Generate Hall Occupancy Report",
    "Manage User Roles", "Login", "Logout",
]
SPECS = [make_spec(UC_INFO[n][0], n, UC_INFO[n][1]) for n in SPEC_ORDER]

SPEC_NOTE = ("Full specifications are given for the four CRUD templates (Add / Update / Delete / Search, "
             "illustrated on Movie) and for every business operation. All the other CRUD use cases — "
             "Update / Delete / Search of Genre, Cinema Hall, Showtime, Customer, Staff, Booking, Ticket, "
             "Payment, Snack and Promotion — follow exactly the same four templates and are not repeated here.")

TABLES = {
    "staff": [("staff_id", "INT", "PK"), ("full_name", "VARCHAR(100)", ""),
              ("username", "VARCHAR(50)", ""), ("password", "VARCHAR(255)", ""),
              ("role", "VARCHAR(10)", "Manager / Cashier")],
    "customer": [("customer_id", "INT", "PK"), ("full_name", "VARCHAR(100)", ""),
                 ("phone", "VARCHAR(20)", ""), ("email", "VARCHAR(100)", "")],
    "genre": [("genre_id", "INT", "PK"), ("name", "VARCHAR(50)", "")],
    "movie": [("movie_id", "INT", "PK"), ("title", "VARCHAR(120)", ""),
              ("genre_id", "INT", "FK -> genre"), ("duration", "INT", ""),
              ("language", "VARCHAR(40)", ""), ("rating", "VARCHAR(10)", "")],
    "cinema_hall": [("hall_id", "INT", "PK"), ("hall_name", "VARCHAR(60)", ""),
                    ("hall_type", "VARCHAR(20)", ""), ("capacity", "INT", "")],
    "showtime": [("show_id", "INT", "PK"), ("movie_id", "INT", "FK -> movie"),
                 ("hall_id", "INT", "FK -> cinema_hall"), ("show_date", "DATE", ""),
                 ("show_time", "TIME", ""), ("ticket_price", "DECIMAL(8,2)", ""),
                 ("status", "VARCHAR(10)", "Posted / Unposted")],
    "booking": [("booking_id", "INT", "PK"), ("customer_id", "INT", "FK -> customer"),
                ("show_id", "INT", "FK -> showtime"), ("promotion_id", "INT", "FK -> promotion (null)"),
                ("booking_datetime", "DATETIME", ""), ("status", "VARCHAR(10)", "Confirmed / Cancelled"),
                ("total_amount", "DECIMAL(8,2)", "")],
    "ticket": [("ticket_id", "INT", "PK"), ("booking_id", "INT", "FK -> booking"),
               ("seat_number", "VARCHAR(8)", ""), ("price", "DECIMAL(8,2)", ""),
               ("status", "VARCHAR(10)", "Valid / Used / Refunded")],
    "payment": [("payment_id", "INT", "PK"), ("booking_id", "INT", "FK -> booking"),
                ("amount", "DECIMAL(8,2)", ""), ("method", "VARCHAR(10)", "Card / Mobile / Cash"),
                ("payment_datetime", "DATETIME", ""), ("status", "VARCHAR(10)", "Paid / Refunded")],
    "snack": [("snack_id", "INT", "PK"), ("name", "VARCHAR(50)", ""),
              ("category", "VARCHAR(30)", ""), ("price", "DECIMAL(8,2)", "")],
    "snack_order": [("order_id", "INT", "PK"), ("booking_id", "INT", "FK -> booking"),
                    ("snack_id", "INT", "FK -> snack"), ("quantity", "INT", ""),
                    ("line_total", "DECIMAL(8,2)", "")],
    "promotion": [("promotion_id", "INT", "PK"), ("code", "VARCHAR(20)", ""),
                  ("description", "VARCHAR(100)", ""), ("discount_percent", "DECIMAL(5,2)", ""),
                  ("start_date", "DATE", ""), ("end_date", "DATE", "")],
}

INTRO = (
    "The Cinema Management System (CMS) is an application that automates the operations of a cinema, "
    "from maintaining the movie catalogue and scheduling showtimes to selling tickets, handling payments "
    "and producing management reports. It is used by the cinema's staff; customers do not operate the system.\n\n"
    "A Manager maintains the reference data (movies, genres, cinema halls, showtimes, staff, snacks and "
    "promotions), publishes the showtimes (Post/Unpost), manages user roles and produces reports. A Cashier "
    "registers customers and sells tickets at the box office: creating a booking, selecting seats, applying "
    "promotions, taking payment, generating the ticket and validating tickets at the entrance. Because the "
    "manager is a senior member of staff, the Manager can also perform every Cashier task (generalisation "
    "Manager ▷ Cashier). The customer is a data entity (the customer table), not an actor.\n\n"
    "The core operation is selling a ticket: the system shows the seats available for a chosen showtime, the "
    "seat is reserved, payment is taken and the ticket is issued; the seat is then marked sold so it can never "
    "be sold twice."
)

INPUTS = [
    ("Login", "Username | Password"),
    ("Movie", "Title | Genre (dropdown) | Duration | Language | Rating"),
    ("Genre", "Name"),
    ("Cinema Hall", "Hall Name | Type (2D/3D) | Capacity"),
    ("Showtime", "Movie (dropdown) | Hall (dropdown) | Date | Time | Ticket Price | Status (Posted)"),
    ("Customer", "Full Name | Phone | Email"),
    ("Staff", "Full Name | Username | Password | Role (Manager/Cashier)"),
    ("Booking / Seat selection", "Showtime (dropdown) | Seat map | Customer | Promotion code | Total"),
    ("Payment", "Amount Due | Method (Card/Mobile/Cash)"),
    ("Snack", "Name | Category | Price (Manager manages the menu)"),
    ("Sell Snack", "Booking (dropdown) | Snack (dropdown) | Quantity | Line Total"),
    ("Promotion", "Code | Description | Discount % | Start Date | End Date"),
]

OUTPUTS = [
    ("Listing tables", "one per entity: Movies, Genres, Halls, Showtimes, Customers, Staff, Bookings, Tickets, Payments, Snacks, Promotions"),
    ("Ticket (printout)", "cinema name, movie, date/time, hall, seat(s), price, ticket code/QR"),
    ("Payment receipt", "receipt no., amount, method, date"),
    ("Sales Report", "tickets sold and revenue for a period, grand total"),
    ("Hall Occupancy Report", "per showtime: seats sold / capacity / occupancy %"),
    ("Error dialogs", "invalid login, duplicate title, showtime clash, seat already sold"),
]

DIAGRAMS = [
    "1 - Movie & Genre Management", "2 - Hall & Showtime Management",
    "3 - Customer & Staff Management", "4 - Booking, Ticket & Payment",
    "5 - Snack & Promotion", "6 - Reporting & Security",
]

# ===========================================================================
# 1) EXCEL
# ===========================================================================
TITLE_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FILL = PatternFill("solid", fgColor="4472C4")
SUB_FILL = PatternFill("solid", fgColor="D9E1F2")
WHITE = Font(color="FFFFFF", bold=True)
BOLD = Font(bold=True)
thin = Side(style="thin", color="B0B0B0")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center")


def build_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Use Cases"
    ws.merge_cells("A1:C1")
    t = ws["A1"]; t.value = "Cinema Management System"; t.fill = TITLE_FILL
    t.font = Font(color="FFFFFF", bold=True, size=14); t.alignment = CENTER
    ws.row_dimensions[1].height = 24
    ws.append(["No", "Use Case", "Actor"])
    for c in range(1, 4):
        cell = ws.cell(row=2, column=c); cell.fill = HEAD_FILL; cell.font = WHITE
        cell.alignment = CENTER; cell.border = BORDER
    for i, (uc, actor) in enumerate(USE_CASES, start=1):
        ws.append([i, uc, actor]); ws.cell(row=2 + i, column=1).alignment = CENTER
    for r in range(2, 3 + len(USE_CASES)):
        for c in range(1, 4):
            cell = ws.cell(row=r, column=c); cell.border = BORDER
            if not cell.alignment.wrap_text:
                cell.alignment = WRAP
    ws.column_dimensions["A"].width = 6
    ws.column_dimensions["B"].width = 48
    ws.column_dimensions["C"].width = 18
    ws.freeze_panes = "A3"

    ws2 = wb.create_sheet("Use Case Specifications")
    fields = [("Use Case ID", "id"), ("Use Case Name", "name"), ("Actor(s)", "actor"),
              ("Description", "desc"), ("Preconditions", "pre"), ("Postconditions", "post"),
              ("Main Flow", "main"), ("Alternative Flows", "alt")]
    ws2.merge_cells("A1:B1")
    nt = ws2.cell(row=1, column=1, value=SPEC_NOTE)
    nt.alignment = WRAP; nt.font = Font(italic=True, color="595959")
    ws2.row_dimensions[1].height = 46
    r = 3
    black = Side(style="thin", color="000000")
    BORDER_BK = Border(left=black, right=black, top=black, bottom=black)
    for s in SPECS:
        ws2.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
        h = ws2.cell(row=r, column=1, value=f"{s['id']}  —  {s['name']}")
        h.font = Font(bold=True, color="000000")
        h.alignment = Alignment(horizontal="left", vertical="center")
        h.border = BORDER_BK
        ws2.cell(row=r, column=2).border = BORDER_BK
        r += 1
        for label, key in fields:
            fc = ws2.cell(row=r, column=1, value=label); fc.font = BOLD
            fc.alignment = WRAP; fc.border = BORDER_BK
            vc = ws2.cell(row=r, column=2, value=s[key]); vc.alignment = WRAP; vc.border = BORDER_BK
            r += 1
        r += 1
    ws2.column_dimensions["A"].width = 20
    ws2.column_dimensions["B"].width = 95

    ws3 = wb.create_sheet("Database Design")
    r = 1
    for tname, cols in TABLES.items():
        ws3.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        th = ws3.cell(row=r, column=1, value=tname); th.fill = TITLE_FILL
        th.font = Font(color="FFFFFF", bold=True); r += 1
        for j, head in enumerate(["Attribute", "Data Type", "Key"], start=1):
            c = ws3.cell(row=r, column=j, value=head); c.fill = SUB_FILL; c.font = BOLD; c.border = BORDER
        r += 1
        for attr, dtype, key in cols:
            for j, val in enumerate((attr, dtype, key), start=1):
                ws3.cell(row=r, column=j, value=val).border = BORDER
            r += 1
        r += 1
    ws3.column_dimensions["A"].width = 20
    ws3.column_dimensions["B"].width = 28
    ws3.column_dimensions["C"].width = 22
    wb.save("Cinema_Management_System.xlsx")
    print("Saved Cinema_Management_System.xlsx")


# ===========================================================================
# 2) HTML  (-> PDF via LibreOffice)
# ===========================================================================
def esc(x):
    return html.escape(str(x)).replace("\n", "<br>")


def build_html():
    p = []
    p.append("""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    @page { size: A4; margin: 2cm; }
    body { font-family: 'Liberation Sans', Arial, sans-serif; color:#1a1a1a; font-size:11pt; line-height:1.4; }
    h1 { color:#1F3864; font-size:20pt; border-bottom:3px solid #4472C4; padding-bottom:4px; }
    h2 { color:#1F3864; font-size:15pt; margin-top:22px; border-bottom:1px solid #cdd6e8; padding-bottom:3px; }
    h3 { color:#2a4a8a; font-size:12pt; margin-top:16px; }
    table { border-collapse:collapse; width:100%; margin:8px 0 14px 0; }
    th,td { border:1px solid #b0b0b0; padding:5px 7px; text-align:left; vertical-align:top; font-size:10pt; }
    th { background:#4472C4; color:#fff; }
    .small td, .small th { font-size:9.5pt; }
    .spec { margin-bottom:10px; }
    .spec th, .spec td { border:1px solid #000; }
    .spec th { background:#fff; color:#000; width:22%; }
    .spec .hdr { background:#fff; color:#000; font-weight:bold; text-align:left; }
    .cover { text-align:center; margin-top:30%; }
    .cover .title { font-size:30pt; color:#1F3864; font-weight:bold; }
    .cover .sub { font-size:14pt; color:#444; margin-top:8px; }
    .cover .meta { margin-top:60px; font-size:13pt; line-height:1.8; }
    .ph { border:2px dashed #9aa7c7; background:#f3f6fc; color:#5a6b94; text-align:center;
          padding:40px; margin:10px 0; border-radius:6px; font-style:italic; }
    .note { background:#fff7e6; border-left:4px solid #d9a200; padding:6px 10px; font-size:10pt; }
    .pb { page-break-before: always; }
    </style></head><body>""")

    # Cover
    p.append(f"""<div class="cover">
      <div class="title">Cinema Management System</div>
      <div class="sub">Analysis Report — Assignment 1</div>
      <div class="meta">
        <b>Name:</b> {esc(STUDENT['name'])}<br>
        <b>Student ID:</b> {esc(STUDENT['sid'])}<br>
        <b>Cohort:</b> {esc(STUDENT['cohort'])}
      </div></div>""")

    # 1 Intro
    p.append('<div class="pb"></div><h1>1. Introduction</h1>')
    p.append(f"<p>{esc(INTRO)}</p>")
    p.append("<p><b>Actors:</b> Manager (primary), Cashier (primary). "
             "<b>Generalisation:</b> Manager ▷ Cashier.</p>")

    # 2 Features table
    p.append('<div class="pb"></div><h1>2. List of Features (Use Cases)</h1>')
    p.append('<table class="small"><tr><th style="width:6%">No</th><th>Use Case</th><th style="width:18%">Actor</th></tr>')
    for i, (uc, actor) in enumerate(USE_CASES, start=1):
        p.append(f"<tr><td>{i}</td><td>{esc(uc)}</td><td>{esc(actor)}</td></tr>")
    p.append("</table>")

    # 3 Diagrams (placeholders)
    p.append('<div class="pb"></div><h1>3. Use Case Diagrams</h1>')
    p.append('<p class="note">Replace each placeholder below with the matching PNG you exported from StarUML '
             '(File &rarr; Export Diagram As &rarr; PNG).</p>')
    for d in DIAGRAMS:
        p.append(f'<h3>{esc(d)}</h3><div class="ph">[ Insert StarUML diagram &laquo;{esc(d)}&raquo; here ]</div>')

    # 4 Specifications
    p.append('<div class="pb"></div><h1>4. Use Case Specifications</h1>')
    p.append(f'<p class="note">{esc(SPEC_NOTE)}</p>')
    labels = [("Use Case ID", "id"), ("Use Case Name", "name"), ("Actor(s)", "actor"),
              ("Description", "desc"), ("Preconditions", "pre"), ("Postconditions", "post"),
              ("Main Flow", "main"), ("Alternative Flows", "alt")]
    for s in SPECS:
        p.append(f'<table class="spec"><tr><th colspan="2" class="hdr">{esc(s["id"])} — {esc(s["name"])}</th></tr>')
        for label, key in labels[2:]:
            p.append(f"<tr><th>{esc(label)}</th><td>{esc(s[key])}</td></tr>")
        p.append("</table>")

    # 5 Input design
    p.append('<div class="pb"></div><h1>5. Input Design (Forms / Dialog Boxes)</h1>')
    p.append('<p class="note">Hand sketches are acceptable. The fields of each form are listed below.</p>')
    p.append("<table><tr><th style='width:28%'>Form</th><th>Fields</th></tr>")
    for f, flds in INPUTS:
        p.append(f"<tr><td><b>{esc(f)}</b></td><td>{esc(flds)}</td></tr>")
    p.append("</table>")

    # 6 Output design
    p.append('<h1 class="pb">6. Output Design (Screen / Paper)</h1>')
    p.append("<table><tr><th style='width:28%'>Output</th><th>Content</th></tr>")
    for o, c in OUTPUTS:
        p.append(f"<tr><td><b>{esc(o)}</b></td><td>{esc(c)}</td></tr>")
    p.append("</table>")

    # 7 Database
    p.append('<div class="pb"></div><h1>7. Database Design</h1>')
    for tname, cols in TABLES.items():
        p.append(f"<h3>{esc(tname)}</h3>")
        p.append('<table class="small"><tr><th style="width:30%">Attribute</th><th style="width:35%">Data Type</th><th>Key</th></tr>')
        for attr, dtype, key in cols:
            p.append(f"<tr><td>{esc(attr)}</td><td>{esc(dtype)}</td><td>{esc(key)}</td></tr>")
        p.append("</table>")

    p.append("</body></html>")
    with open("Cinema_Management_System_Report.html", "w") as f:
        f.write("".join(p))
    print("Saved Cinema_Management_System_Report.html")


if __name__ == "__main__":
    build_excel()
    build_html()
    print("Use cases:", len(USE_CASES), "| Specs:", len(SPECS), "| Tables:", len(TABLES))
