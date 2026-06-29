# Cinema Management System — Analysis Report

> **Name:** ANDRIAMPARANY Rianala Joan  **ID:** 2504_28605  **Cohort:** BSE25A/FT/2
> File to submit as PDF: `AndriamparanyRianalaAssignment1.pdf`

> This report follows the **same structure as the Student Management System example** given by
> the lecturer: full CRUD (Add / Update / Delete / Search) for every entity, plus business
> operations (Post/Unpost, Generate reports, …) and Login/Logout. **57 use cases, 3 actors,
> 12 tables.**

---

## 1. Brief Introduction (5 marks)

The **Cinema Management System (CMS)** is an application that automates the operations of a
cinema, from maintaining the movie catalogue and scheduling showtimes to selling tickets,
handling payments and producing management reports.

The system is used by the cinema's staff. A **Manager** maintains the reference data —
movies, genres, cinema halls, showtimes, staff, snacks and promotions — publishes the
showtimes (Post/Unpost), manages user roles and produces reports. A **Cashier** registers
customers and sells tickets at the box office: creating a booking, selecting seats, applying
promotions, taking payment, generating the ticket and validating tickets at the auditorium
entrance. The **Customer** is a secondary actor: they provide their details to the cashier
and receive the ticket, but do not operate the system.

Following the library/student example, every entity supports the four standard operations
(Add, Update, Delete, Search), and the system adds the cinema-specific business operations
(Post Showtime, Apply Promotion, Generate Ticket, Validate Ticket, Issue Refund, Generate
reports) together with Login and Logout.

Main objectives:

- maintain complete reference data with full CRUD on every entity;
- sell tickets while preventing double-booking of seats;
- take payment, apply promotions and issue tickets;
- give management reliable sales, occupancy and revenue reports;
- secure access through staff accounts and roles.

**Actors:** **Manager** (primary), **Cashier** (primary), **Customer** (secondary).

---

## 2. List of Features (Use Cases) — table (5 marks)

> Also in `cinema_use_cases.csv` / `Cinema_Management_System.xlsx` (open in Excel, export to PDF).

| No | Use Case | Actor |
|----|----------|-------|
| 1 | Add Movie | Manager |
| 2 | Update Movie | Manager |
| 3 | Delete Movie | Manager |
| 4 | Search Movie by Title, Genre, Language | Manager, Cashier |
| 5 | Add Genre | Manager |
| 6 | Update Genre | Manager |
| 7 | Delete Genre | Manager |
| 8 | Search Genre by Name | Manager |
| 9 | Add Cinema Hall | Manager |
| 10 | Update Cinema Hall | Manager |
| 11 | Delete Cinema Hall | Manager |
| 12 | Search Cinema Hall by Name, Type, Capacity | Manager |
| 13 | Add Showtime | Manager |
| 14 | Update Showtime | Manager |
| 15 | Delete Showtime | Manager |
| 16 | Search Showtime by Date, Movie, Hall, Time | Manager, Cashier |
| 17 | Add Customer | Cashier |
| 18 | Update Customer | Cashier |
| 19 | Delete Customer | Manager |
| 20 | Search Customer by Id, Name, Phone | Cashier |
| 21 | Add Staff | Manager |
| 22 | Update Staff | Manager |
| 23 | Delete Staff | Manager |
| 24 | Search Staff by Id, Name, Role | Manager |
| 25 | Add Booking | Cashier, Customer (secondary) |
| 26 | Update Booking | Cashier |
| 27 | Delete Booking | Cashier |
| 28 | Search Booking by Id, Customer, Date, Showtime | Cashier, Manager |
| 29 | Add Ticket | Cashier |
| 30 | Update Ticket | Cashier |
| 31 | Delete Ticket | Cashier |
| 32 | Search Ticket by Code, Showtime, Customer | Cashier |
| 33 | Add Payment | Cashier |
| 34 | Update Payment | Cashier |
| 35 | Delete Payment | Manager |
| 36 | Search Payment by Id, Date, Method, Customer | Cashier, Manager |
| 37 | Add Snack | Manager |
| 38 | Update Snack | Manager |
| 39 | Delete Snack | Manager |
| 40 | Search Snack by Name, Category | Cashier, Manager |
| 41 | Add Promotion | Manager |
| 42 | Update Promotion | Manager |
| 43 | Delete Promotion | Manager |
| 44 | Search Promotion by Code, Period | Cashier, Manager |
| 45 | Post Showtime | Manager |
| 46 | Unpost Showtime | Manager |
| 47 | Select Seat | Cashier, Customer (secondary) |
| 48 | Apply Promotion to Booking | Cashier |
| 49 | Generate Ticket | Cashier |
| 50 | Validate Ticket at Entrance | Cashier |
| 51 | Issue Refund | Cashier, Manager |
| 52 | Generate Sales Report | Manager |
| 53 | Generate Hall Occupancy Report | Manager |
| 54 | Generate Daily Revenue Report | Manager |
| 55 | Manage User Roles | Manager |
| 56 | Login | Manager, Cashier |
| 57 | Logout | Manager, Cashier |

---

## 3. Use Case Diagram(s) — to draw in StarUML (25 marks)

With 57 use cases, draw **one diagram per subsystem** (the example also allows "diagram(s)").
This is cleaner and easier to mark.

### Actors
- **Manager** — primary (reference data, reports, roles). Generalises the Cashier.
- **Cashier** — primary (customers, bookings, tickets, payments, snacks at sale).
- **Customer** — secondary (provides details at booking; does not operate the system).

### Suggested sub-diagrams (one Use Case Diagram each)
1. **Movie & Genre Management** — UC 1–8. Actor: Manager.
2. **Hall & Showtime Management** — UC 9–16, 45–46. Actors: Manager (+ Cashier for searches).
3. **Customer & Staff Management** — UC 17–24. Actors: Cashier, Manager.
4. **Booking, Ticket & Payment** — UC 25–36, 47–51. Actors: Cashier, Customer.
5. **Snack & Promotion** — UC 37–44. Actors: Manager, Cashier.
6. **Reporting & Security** — UC 52–57. Actors: Manager, all (Login/Logout).

### Relationships that earn the marks (very important)
- **Generalization** (▷ solid, hollow triangle): **Manager ▷ Cashier** (the Manager can also
  perform every Cashier use case).
- **`<<include>>`** (dashed arrow, base → included). On the booking diagram:
  - `Add Booking` ──▷ `Select Seat`
  - `Add Booking` ──▷ `Add Payment`
  - `Add Booking` ──▷ `Generate Ticket`
- **`<<extend>>`** (dashed arrow, extension → base):
  - `Apply Promotion to Booking` ··▷ `Add Booking`
  - `Issue Refund` ··▷ `Delete Booking`

> StarUML steps: `Model → Add Diagram → Use Case Diagram` (one per subsystem). Use the
> **Actor** and **UseCase** tools, link with **Association**, use **Generalization** for
> Manager ▷ Cashier, and **Include / Extend** for the dashed relationships. Export each:
> `File → Export Diagram As → PNG`.

---

## 4. Use Case Specifications (25 marks)

Following the example, write one specification per use case. The CRUD ones are short and
repetitive (template below); the business operations are fully detailed. Examples:

### UC-25 — Add Booking  *(core transaction)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-25 |
| **Use Case Name** | Add Booking |
| **Actor(s)** | Cashier (primary), Customer (secondary) |
| **Description** | Creates a booking for a showtime: selects seats, applies any promotion, takes payment and issues the ticket. |
| **Preconditions** | The cashier is logged in; a posted showtime with a free seat exists. |
| **Postconditions** | A booking, ticket and payment are saved; the seats are marked sold. |

**Main Flow**
1. The cashier selects a posted showtime.
2. The cashier selects one or more seats (`<<include>>` Select Seat).
3. The cashier enters / selects the customer.
4. *(optional)* The cashier applies a promotion code (`<<extend>>` Apply Promotion to Booking).
5. The system shows the total; the cashier takes payment (`<<include>>` Add Payment).
6. The system saves the booking and issues the ticket (`<<include>>` Generate Ticket); seats are marked sold.

**Alternative Flows**
- *2a. Seat already sold:* ask for another seat.
- *5a. Payment fails:* release the seats; no ticket issued.

---

### UC-50 — Validate Ticket at Entrance

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-50 |
| **Use Case Name** | Validate Ticket at Entrance |
| **Actor(s)** | Cashier |
| **Description** | Checks that a presented ticket is valid for the current showtime and marks it used. |
| **Preconditions** | The cashier is logged in; the ticket exists. |
| **Postconditions** | The ticket is marked Used; entry is granted or refused. |

**Main Flow**
1. The cashier scans / enters the ticket code.
2. The system finds the ticket and its showtime.
3. The system checks it is valid, for the right showtime and not yet used.
4. The system marks the ticket Used and shows "Access granted" with the seat number.

**Alternative Flows**
- *3a. Already used / wrong showtime:* show "Invalid ticket" and refuse entry.

---

### UC-52 — Generate Sales Report

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-52 |
| **Use Case Name** | Generate Sales Report |
| **Actor(s)** | Manager |
| **Description** | Produces a report of tickets sold and revenue for a chosen period. |
| **Preconditions** | The manager is logged in. |
| **Postconditions** | A report is displayed / printed. |

**Main Flow**
1. The manager chooses the period (date range).
2. The system totals the tickets sold and revenue.
3. The system displays the report with a grand total.

---

### UC-01 — Add Movie  *(short CRUD template — copy for ALL Add/Update/Delete/Search use cases)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Add Movie |
| **Actor(s)** | Manager |
| **Description** | Adds a new movie to the catalogue. |
| **Preconditions** | The manager is logged in. |
| **Postconditions** | A new movie record is stored. |
| **Main Flow** | 1. Open the Movie form. 2. Enter title, genre, duration, language, rating. 3. Save. 4. Validate and store. |
| **Alternative Flows** | *3a. Duplicate / missing field:* show an error; not saved. |

> **Repeat the CRUD template** for every Add/Update/Delete/Search use case of Movie, Genre,
> Hall, Showtime, Customer, Staff, Booking, Ticket, Payment, Snack, Promotion. Write full
> specifications (like above) for the business operations: Post/Unpost Showtime, Select Seat,
> Apply Promotion, Add Payment, Generate Ticket, Issue Refund, the three reports, Manage User
> Roles, Login, Logout.

---

## 5. Input Design (Forms / Dialog Boxes) (part of I/O — 25 marks)

> Hand sketches are enough; this is the field list per main form.

- **Login:** Username | Password.
- **Movie:** Title | Genre (dropdown) | Duration | Language | Rating.
- **Genre:** Name.
- **Cinema Hall:** Hall Name | Type (2D/3D) | Capacity.
- **Showtime:** Movie (dropdown) | Hall (dropdown) | Date | Time | Ticket Price | Status (Posted).
- **Customer:** Full Name | Phone | Email.
- **Staff:** Full Name | Username | Password | Role (Manager/Cashier).
- **Booking / Seat selection:** Showtime (dropdown) | Seat map | Customer | Promotion code | Total.
- **Payment:** Amount Due | Method (Card/Mobile/Cash).
- **Snack:** Name | Category | Price.
- **Promotion:** Code | Description | Discount % | Start Date | End Date.

Each management form also has *Add / Update / Delete / Search* buttons and a results table.

---

## 6. Output Design (Screen / Paper) (part of I/O — 25 marks)

> Hand sketches are enough.

- **Listing tables** (one per entity): Movies, Genres, Halls, Showtimes, Customers, Staff, Bookings, Tickets, Payments, Snacks, Promotions.
- **Ticket (printout):** cinema name, movie, date/time, hall, seat(s), price, ticket code/QR.
- **Payment receipt:** receipt no., amount, method, date.
- **Sales Report:** tickets sold and revenue for a period, grand total.
- **Hall Occupancy Report:** per showtime, seats sold / capacity / occupancy %.
- **Daily Revenue Report:** revenue per day.
- **Error dialogs:** invalid login, duplicate title, showtime clash, seat already sold.

---

## 7. Database Design (Tables, Attributes, Data Types) (15 marks)

> PK = Primary Key, FK = Foreign Key. One table per entity (12 tables).

### staff
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| staff_id | INT (auto) | PK |
| full_name | VARCHAR(100) | |
| username | VARCHAR(50) | |
| password | VARCHAR(255) | |
| role | ENUM('MANAGER','CASHIER') | |

### customer
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| customer_id | INT (auto) | PK |
| full_name | VARCHAR(100) | |
| phone | VARCHAR(20) | |
| email | VARCHAR(100) | |

### genre
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| genre_id | INT (auto) | PK |
| name | VARCHAR(50) | |

### movie
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| movie_id | INT (auto) | PK |
| title | VARCHAR(120) | |
| genre_id | INT | FK → genre |
| duration | INT | |
| language | VARCHAR(40) | |
| rating | VARCHAR(10) | |

### cinema_hall
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| hall_id | INT (auto) | PK |
| hall_name | VARCHAR(60) | |
| hall_type | VARCHAR(20) | |
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
| status | ENUM('Posted','Unposted') | |

### booking
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| booking_id | INT (auto) | PK |
| customer_id | INT | FK → customer |
| show_id | INT | FK → showtime |
| promotion_id | INT | FK → promotion (nullable) |
| booking_datetime | DATETIME | |
| status | ENUM('Confirmed','Cancelled') | |
| total_amount | DECIMAL(8,2) | |

### ticket
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| ticket_id | INT (auto) | PK |
| booking_id | INT | FK → booking |
| seat_number | VARCHAR(8) | |
| price | DECIMAL(8,2) | |
| status | ENUM('Valid','Used','Refunded') | |

### payment
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| payment_id | INT (auto) | PK |
| booking_id | INT | FK → booking |
| amount | DECIMAL(8,2) | |
| method | ENUM('Card','Mobile','Cash') | |
| payment_datetime | DATETIME | |
| status | ENUM('Paid','Refunded') | |

### snack
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| snack_id | INT (auto) | PK |
| name | VARCHAR(50) | |
| category | VARCHAR(30) | |
| price | DECIMAL(8,2) | |

### snack_order
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| order_id | INT (auto) | PK |
| booking_id | INT | FK → booking |
| snack_id | INT | FK → snack |
| quantity | INT | |
| line_total | DECIMAL(8,2) | |

### promotion
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| promotion_id | INT (auto) | PK |
| code | VARCHAR(20) | |
| description | VARCHAR(100) | |
| discount_percent | DECIMAL(5,2) | |
| start_date | DATE | |
| end_date | DATE | |

### Relationships summary
- genre 1—* movie 1—* showtime *—1 cinema_hall
- customer 1—* booking *—1 showtime; promotion 1—* booking
- booking 1—* ticket; booking 1—* payment; booking 1—* snack_order *—1 snack
- staff operates the system (Manager / Cashier roles)

---

### How to assemble the final PDF
1. Put sections 1, 2, 4, 5, 6, 7 in Excel/Word; the use case table comes from
   `Cinema_Management_System.xlsx`, exported to PDF.
2. Draw the use case diagrams in **StarUML** (section 3), one per subsystem, export as PNG.
3. Combine into one PDF named `AndriamparanyRianalaAssignment1.pdf` with your name,
   ID (2504_28605) and cohort (BSE25A/FT/2) on the first page.
