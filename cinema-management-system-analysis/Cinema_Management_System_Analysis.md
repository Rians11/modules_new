# Cinema Management System — Analysis Report

> **Name:** ANDRIAMPARANY Rianala Joan  **ID:** 2504_28605  **Cohort:** BSE25A/FT/2
> File to submit as PDF: `AndriamparanyRianalaAssignment1.pdf`

> ⚠️ This report is aligned with the **actual system** you built (Java Swing + MySQL + JDBC):
> classes Movie, CinemaHall, MovieShow, Ticket, Pricing; frames Login, AdminDashboard,
> MovieManagement, HallManagement, ShowManagement, TicketBooking, TicketList,
> PricingManagement. Keeping the analysis faithful to the built system avoids losing marks.

---

## 1. Brief Introduction (5 marks)

The **Cinema Management System (CMS)** is a Java desktop application that automates the
day-to-day operations of a cinema: managing movies, cinema halls, show scheduling,
ticket pricing and ticket booking. It replaces manual, paper-based record keeping with a
centralised system backed by a MySQL database (accessed through JDBC) and a graphical
user interface built with Java Swing.

The system is used by an **Administrator**, who first authenticates through a login
screen. From the admin dashboard the administrator can maintain the catalogue of movies,
the cinema halls and their seating capacity, schedule shows (linking a movie to a hall at
a given date and time), and configure ticket prices (which vary by weekday/weekend and by
adult/kid). The core transaction is **ticket booking**: the administrator selects a show
and a seat, enters the customer details, the system automatically calculates the price
from the pricing rules, saves the ticket and marks the seat as unavailable.

The main objectives of the system are to:

- avoid double-booking of seats through seat locking;
- apply pricing rules automatically and consistently;
- keep reliable records of movies, halls, shows and sold tickets (full CRUD);
- secure access through administrator authentication.

**Actors** (the `users` table defines a `role` of either ADMIN or CASHIER, so the system
has two operator roles plus the customer):

- **Administrator (Admin)** — *primary* actor with full access: manages movies, halls,
  shows and pricing, and can also perform every cashier task.
- **Cashier** — *primary* actor who logs in to sell tickets and manage ticket records.
- **Customer** — *secondary* actor who does not log in but takes part in ticket booking
  (provides name/phone, stored in the `customer` table, and receives the ticket).

---

## 2. List of Features (Use Cases) — table (5 marks)

> Also provided in `cinema_use_cases.csv` / `Cinema_Management_System.xlsx` (open in Excel,
> export to PDF as the assignment requires).

> Note: thanks to the **Administrator ▷ Cashier generalization** (see §3), the Admin can
> also perform every Cashier use case. The table lists the most specific role for each.

| No | Use Case | Actor |
|----|----------|-------|
| 1 | Login | Administrator, Cashier |
| 2 | Logout | Administrator, Cashier |
| 3 | Add Movie | Administrator |
| 4 | Update Movie | Administrator |
| 5 | Delete Movie | Administrator |
| 6 | View / Search Movies | Cashier |
| 7 | Add Cinema Hall | Administrator |
| 8 | Update Cinema Hall | Administrator |
| 9 | Delete Cinema Hall | Administrator |
| 10 | View Cinema Halls | Administrator |
| 11 | Add Movie Show | Administrator |
| 12 | Update Movie Show | Administrator |
| 13 | Delete Movie Show | Administrator |
| 14 | View Movie Shows | Cashier |
| 15 | Update Ticket Pricing (Weekday/Weekend – Adult/Kid) | Administrator |
| 16 | View Ticket Pricing | Cashier |
| 17 | Book Ticket (Sell Ticket) | Cashier (primary), Customer (secondary) |
| 18 | Select Seat | Cashier |
| 19 | Check Seat Availability | Cashier |
| 20 | Calculate Ticket Price | Cashier |
| 21 | View Sold Tickets | Cashier |
| 22 | Update Ticket | Cashier |
| 23 | Cancel / Delete Ticket | Cashier |

---

## 3. Use Case Diagram — to draw in StarUML (25 marks)

One single diagram is enough (~23 use cases). Structure to reproduce in StarUML:

### Actors
- **Cashier** — *primary* actor, stick figure on the **left**. Connected to Login, Logout,
  View Movies, View Shows, View Pricing, and all the ticket use cases (Book Ticket, View
  Sold Tickets, Update Ticket, Cancel Ticket).
- **Administrator** — *primary* actor, stick figure on the **left**, **above** the Cashier.
  Connected to the management use cases (Add/Update/Delete Movie, Hall, Show; Update Pricing;
  View Halls).
- **Customer** — *secondary* actor, stick figure on the **right**. Connected **only** to
  `Book Ticket`.

### Use cases (ovals) — group them visually by area
- **Authentication:** Login, Logout
- **Movie Management:** Add Movie, Update Movie, Delete Movie, View/Search Movies
- **Hall Management:** Add Hall, Update Hall, Delete Hall, View Halls
- **Show Management:** Add Show, Update Show, Delete Show, View Shows
- **Pricing:** Update Ticket Pricing, View Ticket Pricing
- **Ticket Booking:** Book Ticket, View Sold Tickets, Update Ticket, Cancel/Delete Ticket
  plus the sub-behaviours Select Seat, Check Seat Availability, Calculate Ticket Price.

### Associations
- Connect each actor to its use cases with a plain line (Association), as listed above.
- Connect **Customer** to `Book Ticket` only — secondary actor on that single use case.

### Relationships that earn the marks (very important)
- **Generalization** (solid line, hollow triangle ▷): **Administrator ▷ Cashier**. This means
  the Admin inherits every Cashier use case (so you do NOT need to also link the Admin to the
  ticket use cases — the generalization covers it). Justified by `users.role ENUM(ADMIN, CASHIER)`.
- **`<<include>>`** (dashed arrow, base → included). *Book Ticket* must include:
  - `Book Ticket` ──▷ `Select Seat`
  - `Book Ticket` ──▷ `Check Seat Availability`
  - `Book Ticket` ──▷ `Calculate Ticket Price`

> StarUML steps: `Model → Add Diagram → Use Case Diagram`. Use the **Actor** and **UseCase**
> tools, link with **Association**, use **Generalization** from Administrator to Cashier, and
> the **Include** tool for the three dashed `<<include>>` arrows from *Book Ticket*.
> Export: `File → Export Diagram As → PNG`.

---

## 4. Use Case Specifications (25 marks)

Full specifications for the key use cases. Replicate the short CRUD template for the rest.

### UC-17 — Book Ticket (Sell Ticket)  *(the core transaction)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-17 |
| **Use Case Name** | Book Ticket |
| **Actor(s)** | Cashier (primary), Customer (secondary) |
| **Description** | Sells a ticket for a chosen show and seat, calculates the price automatically and marks the seat as unavailable. The customer provides their details and receives the ticket. |
| **Preconditions** | The administrator is logged in; at least one show with a free seat exists; pricing is configured. |
| **Postconditions** | A ticket record is saved; the chosen seat becomes unavailable. |
| **Trigger** | The administrator opens the Ticket Booking screen and selects a show. |

**Main Flow**
1. The administrator selects a movie show.
2. The administrator selects a seat number (`<<include>>` Select Seat, UC-18).
3. The system checks the seat is still free (`<<include>>` Check Seat Availability, UC-19).
4. The administrator enters the customer details and ticket type (Adult/Kid).
5. The system calculates the price from the pricing rules (`<<include>>` Calculate Ticket
   Price, UC-20) based on weekday/weekend and adult/kid.
6. The administrator confirms; the system saves the ticket and marks the seat as sold.
7. The system shows a confirmation message.

**Alternative / Exception Flows**
- *3a. Seat already sold:* the system shows "Seat already booked" and asks for another seat.
- *4a. Invalid / missing input:* the system shows a validation error; the ticket is not saved.

---

### UC-01 — Login

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Login |
| **Actor(s)** | Administrator, Cashier |
| **Description** | Authenticates the user and opens the dashboard according to their role (ADMIN or CASHIER). |
| **Preconditions** | The application is running; a valid user account exists in the `users` table. |
| **Postconditions** | The user is authenticated and the dashboard opens with role-based access. |

**Main Flow**
1. The user enters username and password.
2. The system validates the credentials against the `users` table and reads the role.
3. On success, the dashboard opens (full menu for ADMIN, ticket menu for CASHIER).

**Alternative Flows**
- *2a. Invalid credentials:* the system shows "Invalid login credentials" and stays on the login screen.

---

### UC-15 — Update Ticket Pricing

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-15 |
| **Use Case Name** | Update Ticket Pricing |
| **Actor(s)** | Administrator |
| **Description** | Updates ticket prices that vary by day type (weekday/weekend) and category (adult/kid), without changing code. |
| **Preconditions** | The administrator is logged in. |
| **Postconditions** | New prices are stored and used automatically by the booking screen. |

**Main Flow**
1. The administrator opens the Pricing Management screen.
2. The system displays current prices (weekday/weekend, adult/kid).
3. The administrator edits the prices and saves.
4. The system stores the new prices; subsequent bookings use them automatically.

**Alternative Flows**
- *3a. Invalid numeric input:* the system shows a validation error; prices are not changed.

---

### UC-03 — Add Movie  *(short CRUD template — copy for the other CRUD use cases)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-03 |
| **Use Case Name** | Add Movie |
| **Actor(s)** | Administrator |
| **Description** | Adds a new movie to the catalogue. |
| **Preconditions** | The administrator is logged in. |
| **Postconditions** | A new movie record is stored. |
| **Main Flow** | 1. Open the Movie Management screen. 2. Enter title, genre, duration. 3. Click Add. 4. System validates and saves the movie, then refreshes the table. |
| **Alternative Flows** | *3a. Duplicate movie title / missing field:* system shows an error; the movie is not saved. |

> **Repeat this short template** for: Update/Delete/View Movie, Hall (Add/Update/Delete/View),
> Show (Add/Update/Delete/View), View Pricing, View/Update/Cancel Ticket, and Logout.

---

## 5. Input Design (Forms / Dialog Boxes) (part of I/O — 25 marks)

> Hand sketches are enough. Field list per screen so your sketches match the real frames.

**F1 — Login (LoginFrame).** Username | Password → Button: *Login*. (The role ADMIN/CASHIER is read from the `users` table.)

**F2 — Movie Management (MovieManagementFrame).** Title | Genre | Duration (min) →
*Add*, *Update*, *Delete*, *Clear*; plus a table listing movies.

**F3 — Hall Management (HallManagementFrame).** Hall Name | Seating Capacity →
*Add*, *Update*, *Delete*; plus a table listing halls.

**F4 — Show Management (ShowManagementFrame).** Movie (dropdown) | Hall (dropdown) |
Date | Time → *Add*, *Update*, *Delete*; plus a table listing shows.

**F5 — Ticket Booking (TicketBookingFrame).** Show (dropdown) | Seat number (selection) |
Customer Full Name | Customer Phone | Ticket Type (Adult/Kid) | Price (auto, read-only) → *Book / Sell*.

**F6 — Pricing Management (PricingManagementFrame).** Weekday Adult | Weekday Kid |
Weekend Adult | Weekend Kid → *Save*.

**F7 — Ticket List (TicketListFrame).** Table of sold tickets with selectable row →
*Update*, *Delete*.

---

## 6. Output Design (Screen / Paper) (part of I/O — 25 marks)

> Hand sketches are enough.

**O1 — Admin Dashboard:** navigation buttons to each management screen.
**O2 — Movies table:** list of movies (title, genre, duration).
**O3 — Halls table:** list of halls (name, capacity).
**O4 — Shows table:** list of shows (movie, hall, date, time).
**O5 — Booking confirmation:** message "Ticket booked" with seat number and price; seat shown as unavailable.
**O6 — Sold tickets table:** ticket id, show, seat, type, price, customer, purchase date.
**O7 — Error/validation dialogs:** invalid login, duplicate title, duplicate show, seat already sold, invalid number.

---

## 7. Database Design (Tables, Attributes, Data Types) (15 marks)

> PK = Primary Key, FK = Foreign Key, UQ = Unique. This matches exactly the `cinema_db`
> database (phpMyAdmin export).

### users
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| user_id | INT(11) | PK |
| username | VARCHAR(50) | UQ |
| password | VARCHAR(100) | |
| role | ENUM('ADMIN','CASHIER') | default 'CASHIER' |

### customer
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| customer_id | INT(11) | PK |
| full_name | VARCHAR(100) | |
| phone | VARCHAR(20) | |

### movie
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| movie_id | INT(11) | PK |
| title | VARCHAR(120) | UQ |
| genre | VARCHAR(50) | |
| duration | INT(11) | |

### cinema_hall
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| hall_id | INT(11) | PK |
| hall_name | VARCHAR(60) | UQ |
| capacity | INT(11) | |

### movie_show
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| show_id | INT(11) | PK |
| movie_id | INT(11) | FK → movie |
| hall_id | INT(11) | FK → cinema_hall |
| show_date | DATE | |
| show_time | TIME | |

*UQ (hall_id, show_date, show_time) — prevents scheduling two shows in the same hall at the same time.*

### pricing_config
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| id | INT(11) | PK |
| weekday_adult | INT(11) | |
| weekday_kid | INT(11) | |
| weekend_adult | INT(11) | |
| weekend_kid | INT(11) | |
| updated_at | TIMESTAMP | default CURRENT_TIMESTAMP |

### ticket
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| ticket_id | INT(11) | PK |
| show_id | INT(11) | FK → movie_show |
| seat_number | INT(11) | |
| customer_id | INT(11) | FK → customer |
| ticket_type | ENUM('Adult','Kid') | |
| price | DECIMAL(10,2) | |
| purchase_date | TIMESTAMP | default CURRENT_TIMESTAMP |

*UQ (show_id, seat_number) — enforces seat locking: a seat can be sold only once per show.*

### show_details
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| details_id | INT(11) | PK |
| show_id | INT(11) | UQ → movie_show |
| movie_name | VARCHAR(120) | |
| hall_name | VARCHAR(60) | |

### Relationships summary
- movie 1—* movie_show *—1 cinema_hall  (a show links one movie and one hall)
- movie_show 1—* ticket  (unique seat per show → seat locking via UQ (show_id, seat_number))
- customer 1—* ticket  (a ticket belongs to one customer)
- pricing_config holds one row with the four prices used when a ticket is created
- show_details holds 1—1 denormalised display info per movie_show

---

### How to assemble the final PDF
1. Put sections 1, 2, 4, 5, 6, 7 in Excel/Word as instructed; the use case table comes
   from `Cinema_Management_System.xlsx`, exported to PDF.
2. Draw the single use case diagram in **StarUML** (section 3) and export as PNG.
3. Combine everything into one PDF named `AndriamparanyRianalaAssignment1.pdf` with your
   name, ID (2504_28605) and cohort (BSE25A/FT/2) on the first page.
