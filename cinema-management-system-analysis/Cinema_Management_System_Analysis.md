# Cinema Management System — Analysis Report

> **Name:** ANDRIAMPARANY Rianala Joan  **ID:** 2504_28605  **Cohort:** BSE25A/FT/2
> File to submit as PDF: `AndriamparanyRianalaAssignment1.pdf`

> A realistic **counter-based** cinema: customers do not use the software. A **Cashier**
> sells tickets at the box office (entering the customer's details), takes payment and
> validates tickets at the entrance; a **Manager** runs movies, halls, showtimes, pricing
> and reports. **2 operator actors (+ 1 secondary), 20 use cases, 6 tables.**

---

## 1. Brief Introduction (5 marks)

The **Cinema Management System (CMS)** is an application that automates the operations of a
cinema. It is used by the cinema's staff at the box office; customers do not interact with
the system directly.

A **Cashier** logs in to sell tickets: they look up the movies and showtimes, choose a free
seat for the customer, enter the customer's name and phone, take payment, and the system
issues the ticket and marks the seat as sold. The cashier can also cancel a ticket, view
the list of sold tickets, and validate tickets at the auditorium entrance. A **Manager**
runs the cinema: maintaining the movie catalogue, registering the cinema halls, scheduling
showtimes, setting ticket prices and consulting sales reports. Because the manager is also
a senior member of staff, the manager can perform every cashier task as well.

The core operation is **selling a ticket**: the system shows the seats available for a
chosen showtime, the seat is reserved for the customer, payment is taken and the ticket is
issued; the seat is then marked sold so it can never be sold twice.

Main objectives:

- keep reliable records of movies, halls and showtimes (full CRUD);
- sell tickets at the counter while preventing double-booking of seats;
- take payment and issue tickets, storing the customer's details;
- give management reliable sales reports;
- secure access through staff accounts and roles (Manager, Cashier).

**Actors:**

- **Manager** — *primary* actor; manages the catalogue, halls, showtimes, pricing and reports,
  and can also perform every cashier task.
- **Cashier** — *primary* actor; sells tickets, enters customer details, takes payment and
  validates tickets at entry.
- **Customer** — *secondary* actor; does **not** use the system, but provides their name and
  phone to the cashier and receives the ticket.

---

## 2. List of Features (Use Cases) — table (5 marks)

> Also in `cinema_use_cases.csv` / `Cinema_Management_System.xlsx` (open in Excel, export to PDF).
> Note: because of the **Manager ▷ Cashier** generalization (§3), the Manager can also perform
> every Cashier use case. The table lists the most specific role for each.

| No | Use Case | Actor |
|----|----------|-------|
| 1 | Login | Manager, Cashier |
| 2 | Logout | Manager, Cashier |
| 3 | Search / View Movies | Cashier |
| 4 | View Showtimes | Cashier |
| 5 | Sell Ticket | Cashier (primary), Customer (secondary) |
| 6 | Select Seat | Cashier |
| 7 | Check Seat Availability | Cashier |
| 8 | Take Payment | Cashier |
| 9 | Cancel Ticket | Cashier |
| 10 | Validate Ticket at Entrance | Cashier |
| 11 | View Sold Tickets | Cashier |
| 12 | Add Movie | Manager |
| 13 | Update Movie | Manager |
| 14 | Delete Movie | Manager |
| 15 | Manage Cinema Halls | Manager |
| 16 | Schedule Showtime | Manager |
| 17 | Update Showtime | Manager |
| 18 | Delete Showtime | Manager |
| 19 | Set Ticket Pricing | Manager |
| 20 | View Sales Report | Manager |

---

## 3. Use Case Diagram — to draw in StarUML (25 marks)

One clean diagram.

### Actors
- **Manager** — *primary*, stick figure top-left. Connected to: Add/Update/Delete Movie,
  Manage Cinema Halls, Schedule/Update/Delete Showtime, Set Ticket Pricing, View Sales Report.
- **Cashier** — *primary*, stick figure below the Manager. Connected to: Login, Logout,
  Search Movies, View Showtimes, Sell Ticket, Cancel Ticket, Validate Ticket, View Sold Tickets.
- **Customer** — *secondary*, stick figure on the **right**. Connected **only** to `Sell Ticket`.

### Associations
- Plain lines (Association) from each actor to its use cases (list above).
- Connect both Manager and Cashier to `Login` / `Logout`.

### Relationships that earn the marks (very important)
- **Generalization** (solid line, hollow triangle ▷): **Manager ▷ Cashier**. The Manager
  inherits every Cashier use case, so you do NOT need to also link the Manager to the selling
  use cases — the generalization covers it.
- **`<<include>>`** (dashed arrow, base → included). `Sell Ticket` includes three mandatory steps:
  - `Sell Ticket` ──▷ `Select Seat`
  - `Sell Ticket` ──▷ `Check Seat Availability`
  - `Sell Ticket` ──▷ `Take Payment`

> StarUML steps: `Model → Add Diagram → Use Case Diagram`. Drop **Actor** and **UseCase**
> elements, link with **Association**, use **Generalization** from Manager to Cashier, and the
> **Include** tool for the three dashed `<<include>>` arrows from *Sell Ticket*.
> Export: `File → Export Diagram As → PNG`.

---

## 4. Use Case Specifications (25 marks)

Full specifications for the key use cases; replicate the short CRUD template for the rest.

### UC-05 — Sell Ticket  *(the core operation)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-05 |
| **Use Case Name** | Sell Ticket |
| **Actor(s)** | Cashier (primary), Customer (secondary) |
| **Description** | Sells a ticket for a chosen showtime and seat: records the customer, takes payment and marks the seat as sold. |
| **Preconditions** | The cashier is logged in; a showtime with at least one free seat exists. |
| **Postconditions** | A ticket is saved against the showtime and customer; the seat is marked sold. |
| **Trigger** | A customer asks to buy a ticket and the cashier selects a showtime. |

**Main Flow**
1. The cashier selects a movie and a showtime.
2. The cashier selects a seat for the customer (`<<include>>` Select Seat).
3. The system checks the seat is still free (`<<include>>` Check Seat Availability).
4. The cashier enters the customer's name and phone, and the ticket type (Adult/Kid).
5. The system shows the price; the cashier takes payment (`<<include>>` Take Payment).
6. The system saves the ticket and marks the seat as sold.
7. The system prints/shows the ticket with the seat number and price.

**Alternative / Exception Flows**
- *3a. Seat already sold:* the system shows "Seat already booked" and asks for another seat.
- *5a. Payment not completed:* the seat is released and no ticket is issued.
- *4a. Missing customer details:* the system shows a validation error.

---

### UC-01 — Login

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Login |
| **Actor(s)** | Manager, Cashier |
| **Description** | Authenticates a staff member and opens the menu according to their role. |
| **Preconditions** | The application is running; a valid staff account exists. |
| **Postconditions** | The staff member is authenticated with role-based access. |

**Main Flow**
1. The staff member enters username and password.
2. The system validates the credentials and reads the role (Manager or Cashier).
3. On success, the menu opens (full menu for Manager, selling menu for Cashier).

**Alternative Flows**
- *2a. Invalid credentials:* the system shows "Invalid login credentials" and stays on the login screen.

---

### UC-16 — Schedule Showtime

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-16 |
| **Use Case Name** | Schedule Showtime |
| **Actor(s)** | Manager |
| **Description** | Schedules a movie in a hall at a given date, time and ticket price. |
| **Preconditions** | The manager is logged in; at least one movie and one hall exist. |
| **Postconditions** | A new showtime is stored. |

**Main Flow**
1. Open the Showtime scheduling screen.
2. Choose a movie and a hall, enter the date, time and ticket price.
3. Save.
4. The system validates and stores the showtime.

**Alternative Flows**
- *3a. A showtime already exists for that hall at that date/time:* the system shows a clash error.

---

### UC-12 — Add Movie  *(short CRUD template — copy for the other CRUD use cases)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-12 |
| **Use Case Name** | Add Movie |
| **Actor(s)** | Manager |
| **Description** | Adds a new movie to the catalogue. |
| **Preconditions** | The manager is logged in. |
| **Postconditions** | A new movie record is stored. |
| **Main Flow** | 1. Open Movie Management. 2. Enter title, genre, duration, rating. 3. Save. 4. System validates and stores the movie. |
| **Alternative Flows** | *3a. Duplicate title / missing field:* show an error; the movie is not saved. |

> **Repeat this short template** for: Update/Delete Movie, Manage Cinema Halls, Update/Delete
> Showtime, Set Ticket Pricing, Search Movies, View Showtimes, Cancel Ticket, Validate Ticket,
> View Sold Tickets, View Sales Report, Logout.

---

## 5. Input Design (Forms / Dialog Boxes) (part of I/O — 25 marks)

> Hand sketches are enough; this is the field list per screen.

**F1 — Login.** Username | Password → *Login*. (Role Manager/Cashier read from the account.)

**F2 — Movie Management (Manager).** Title | Genre | Duration | Rating →
*Add*, *Update*, *Delete*; table of movies.

**F3 — Hall Management (Manager).** Hall Name | Capacity → *Add*, *Update*, *Delete*; table of halls.

**F4 — Showtime Scheduling (Manager).** Movie (dropdown) | Hall (dropdown) | Date | Time |
Ticket Price → *Save*; table of showtimes.

**F5 — Sell Ticket (Cashier).** Showtime (dropdown) | Seat Number (selection) |
Customer Name | Customer Phone | Ticket Type (Adult/Kid) | Price (auto) → *Sell*.

**F6 — Pricing (Manager).** Base Price | Adult Price | Kid Price → *Save*.

**F7 — Sold Tickets (Cashier).** Table of sold tickets with a selectable row → *Cancel Ticket*.

---

## 6. Output Design (Screen / Paper) (part of I/O — 25 marks)

> Hand sketches are enough.

**O1 — Main menu:** buttons by role (Manager: Movies/Halls/Showtimes/Pricing/Reports;
Cashier: Sell/Tickets/Validate).
**O2 — Movies table:** title, genre, duration, rating.
**O3 — Showtimes table:** movie, hall, date, time, price.
**O4 — Ticket (printout):** cinema name, movie, date & time, hall, seat number, type, price, ticket no.
**O5 — Sold tickets table:** ticket no., showtime, seat, customer, price, date.
**O6 — Sales Report (paper):** tickets sold and revenue for a period, grand total.
**O7 — Error dialogs:** invalid login, duplicate movie title, showtime clash, seat already sold.

---

## 7. Database Design (Tables, Attributes, Data Types) (15 marks)

> PK = Primary Key, FK = Foreign Key, UQ = Unique. Six tables.

### staff
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| staff_id | INT (auto) | PK |
| full_name | VARCHAR(100) | |
| username | VARCHAR(50) | UQ |
| password | VARCHAR(255) | |
| role | ENUM('MANAGER','CASHIER') | |

### customer
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| customer_id | INT (auto) | PK |
| full_name | VARCHAR(100) | |
| phone | VARCHAR(20) | |

### movie
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| movie_id | INT (auto) | PK |
| title | VARCHAR(120) | |
| genre | VARCHAR(50) | |
| duration | INT | |
| rating | VARCHAR(10) | |

### cinema_hall
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| hall_id | INT (auto) | PK |
| hall_name | VARCHAR(60) | |
| capacity | INT | |

### showtime
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| show_id | INT (auto) | PK |
| movie_id | INT | FK → movie |
| hall_id | INT | FK → cinema_hall |
| show_date | DATE | |
| show_time | TIME | |
| ticket_price | DECIMAL(8,2) | |

*UQ (hall_id, show_date, show_time) — prevents two showtimes in the same hall at the same time.*

### ticket
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| ticket_id | INT (auto) | PK |
| show_id | INT | FK → showtime |
| customer_id | INT | FK → customer |
| seat_number | VARCHAR(8) | |
| ticket_type | ENUM('Adult','Kid') | |
| price | DECIMAL(8,2) | |
| purchase_datetime | DATETIME | |

*UQ (show_id, seat_number) — enforces no double-booking: a seat is sold only once per showtime.*

### Relationships summary
- movie 1—* showtime *—1 cinema_hall  (a showtime links one movie and one hall)
- showtime 1—* ticket  (a showtime sells many tickets; one seat per showtime → no double-booking)
- customer 1—* ticket  (a ticket records one customer)
- staff operates the system (Manager / Cashier roles)

---

### How to assemble the final PDF
1. Put sections 1, 2, 4, 5, 6, 7 in Excel/Word; the use case table comes from
   `Cinema_Management_System.xlsx`, exported to PDF.
2. Draw the use case diagram in **StarUML** (section 3) and export as PNG.
3. Combine into one PDF named `AndriamparanyRianalaAssignment1.pdf` with your name,
   ID (2504_28605) and cohort (BSE25A/FT/2) on the first page.
