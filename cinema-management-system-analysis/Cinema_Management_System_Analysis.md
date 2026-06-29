# Cinema Management System — Analysis Report

> **Name:** ANDRIAMPARANY Rianala Joan  **ID:** 2504_28605  **Cohort:** BSE25A/FT/2
> File to submit as PDF: `AndriamparanyRianalaAssignment1.pdf`

> A realistic, coherent model of how a real cinema operates: a customer books and pays for
> a seat online or at the counter, a cashier sells and validates tickets, and a manager
> runs the catalogue, scheduling, pricing and reports. **3 actors, 20 use cases, 8 tables.**

---

## 1. Brief Introduction (5 marks)

The **Cinema Management System (CMS)** is an application that automates the operations of a
modern cinema, from publishing the movie programme to selling tickets and reporting sales.
It mirrors how a real cinema works.

A **Customer** creates an account, browses the movies currently showing, looks at the
available showtimes, selects a seat, pays and receives a ticket. The customer can review
their bookings and cancel a booking within the allowed period. A **Cashier** at the box
office performs the same booking on behalf of walk-in customers, takes payment at the
counter, and validates tickets at the auditorium entrance. A **Manager** runs the cinema:
maintaining the movie catalogue, scheduling showtimes in the cinema halls, setting ticket
prices and consulting sales reports.

The core operation is **ticket booking**: the system shows the seats available for a
chosen showtime, the seat is reserved, payment is taken and a ticket is issued; the seat is
then marked as sold so it can never be sold twice.

Main objectives:

- publish the movie programme and showtimes to customers;
- sell tickets (online and at the counter) while preventing double-booking of seats;
- handle payment and issue tickets;
- give management reliable sales reports;
- secure access through accounts and roles (Customer, Cashier, Manager).

**Actors:**

- **Customer** — registers, books and pays for tickets, receives the ticket.
- **Cashier** — sells tickets at the box office, takes payment, validates tickets at entry.
- **Manager** — manages movies, showtimes, halls, pricing and reports.

---

## 2. List of Features (Use Cases) — table (5 marks)

> Also in `cinema_use_cases.csv` / `Cinema_Management_System.xlsx` (open in Excel, export to PDF).

| No | Use Case | Actor |
|----|----------|-------|
| 1 | Register Account | Customer |
| 2 | Login | Customer, Cashier, Manager |
| 3 | Logout | Customer, Cashier, Manager |
| 4 | Search / Browse Movies | Customer, Cashier |
| 5 | View Showtimes | Customer, Cashier |
| 6 | Book Ticket | Customer, Cashier |
| 7 | Select Seats | Customer, Cashier |
| 8 | Make Payment | Customer, Cashier |
| 9 | View My Bookings | Customer |
| 10 | Cancel Booking | Customer, Cashier |
| 11 | Validate Ticket at Entrance | Cashier |
| 12 | Add Movie | Manager |
| 13 | Update Movie | Manager |
| 14 | Delete Movie | Manager |
| 15 | Schedule Showtime | Manager |
| 16 | Update Showtime | Manager |
| 17 | Delete Showtime | Manager |
| 18 | Manage Cinema Halls | Manager |
| 19 | Set Ticket Pricing | Manager |
| 20 | View Sales Report | Manager |

---

## 3. Use Case Diagram — to draw in StarUML (25 marks)

One clean diagram with three actors.

### Actors
- **Customer** — stick figure on the **left**. Connected to: Register Account, Login, Logout,
  Search Movies, View Showtimes, Book Ticket, View My Bookings, Cancel Booking.
- **Cashier** — stick figure on the **left** (below Customer). Connected to: Login, Logout,
  Search Movies, View Showtimes, Book Ticket, Cancel Booking, Validate Ticket at Entrance.
- **Manager** — stick figure on the **right**. Connected to: Login, Logout, Add/Update/Delete
  Movie, Schedule/Update/Delete Showtime, Manage Cinema Halls, Set Ticket Pricing, View Sales Report.

### Associations
- Plain lines (Association) from each actor to its use cases (list above).
- `Login` and `Logout` are shared — connect all three actors to them.
- `Book Ticket` is shared by Customer (online) and Cashier (counter).

### Relationships that earn the marks
- **`<<include>>`** (dashed arrow, base → included). `Book Ticket` includes two mandatory steps:
  - `Book Ticket` ──▷ `Select Seats`
  - `Book Ticket` ──▷ `Make Payment`
- *(Optional)* **Generalization** ▷: you may add a `Staff` parent actor for Cashier and Manager
  (both are employees who log in), with `Cashier` and `Manager` generalising `Staff`. Keep it
  only if your diagram stays readable.

> StarUML steps: `Model → Add Diagram → Use Case Diagram`. Drop **Actor** and **UseCase**
> elements, link with **Association**, and use the **Include** tool for the two dashed
> `<<include>>` arrows from *Book Ticket*. Export: `File → Export Diagram As → PNG`.

---

## 4. Use Case Specifications (25 marks)

Full specifications for the key use cases; replicate the short CRUD template for the rest.

### UC-06 — Book Ticket  *(the core operation)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-06 |
| **Use Case Name** | Book Ticket |
| **Actor(s)** | Customer (online), Cashier (counter) |
| **Description** | Reserves one or more seats for a showtime, takes payment and issues a ticket. |
| **Preconditions** | The actor is logged in; a showtime with at least one free seat exists. |
| **Postconditions** | A booking and ticket are saved; the chosen seats are marked as sold. |
| **Trigger** | The actor selects a showtime and clicks "Book". |

**Main Flow**
1. The actor selects a movie and a showtime.
2. The system displays the seat map with available seats.
3. The actor selects one or more seats (`<<include>>` Select Seats).
4. The system reserves the seats and shows the total price.
5. The actor confirms and pays (`<<include>>` Make Payment).
6. On successful payment, the system saves the booking, issues the ticket(s) and marks the seats sold.
7. The system shows/sends the ticket with a booking reference.

**Alternative / Exception Flows**
- *3a. Seat taken meanwhile:* the system warns the actor and asks them to choose another seat.
- *5a. Payment fails:* the system releases the reserved seats and shows an error; no ticket is issued.

---

### UC-08 — Make Payment

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-08 |
| **Use Case Name** | Make Payment |
| **Actor(s)** | Customer, Cashier |
| **Description** | Charges the customer for a booking. |
| **Preconditions** | A booking with a total amount is awaiting payment. |
| **Postconditions** | A payment record is created with status Paid or Failed. |

**Main Flow**
1. The system shows the amount due and the payment methods (Card, Mobile Money, Cash at counter).
2. The actor chooses a method and provides the details.
3. The system processes the payment and records it as Paid.

**Alternative Flows**
- *3a. Payment declined:* record the payment as Failed and notify the actor; the booking stays unpaid.

---

### UC-15 — Schedule Showtime

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-15 |
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
| **Main Flow** | 1. Open Movie Management. 2. Enter title, genre, duration, language, rating. 3. Save. 4. System validates and stores the movie. |
| **Alternative Flows** | *3a. Duplicate title / missing field:* show an error; the movie is not saved. |

> **Repeat this short template** for: Update/Delete Movie, Update/Delete Showtime, Manage
> Cinema Halls, Set Ticket Pricing, Register Account, View My Bookings, Cancel Booking,
> Validate Ticket, View Sales Report, Logout.

---

## 5. Input Design (Forms / Dialog Boxes) (part of I/O — 25 marks)

> Hand sketches are enough; this is the field list per screen.

**F1 — Register Account.** Full Name | Email | Phone | Password | Confirm Password → *Register*.

**F2 — Login.** Email/Username | Password → *Login*.

**F3 — Movie Management (Manager).** Title | Genre | Duration | Language | Rating →
*Add*, *Update*, *Delete*; table of movies.

**F4 — Showtime Scheduling (Manager).** Movie (dropdown) | Hall (dropdown) | Date | Time |
Ticket Price → *Save*; table of showtimes.

**F5 — Booking / Seat Selection.** Showtime (read-only info) | interactive Seat Map
(Available / Selected / Sold) | selected seats list | total price → *Continue to Payment*.

**F6 — Payment.** Amount Due (read-only) | Payment Method (Card / Mobile Money / Cash) |
payment details → *Pay*.

**F7 — Ticket Pricing (Manager).** Hall/Category | Price → *Save*.

---

## 6. Output Design (Screen / Paper) (part of I/O — 25 marks)

> Hand sketches are enough.

**O1 — Now Showing:** list/grid of movies with poster, title, genre, rating.
**O2 — Showtimes screen:** for a movie, the list of dates, times, hall and price.
**O3 — Seat map:** colour-coded seats (available / selected / sold).
**O4 — Ticket (e-ticket / printout):** cinema name, movie, date & time, hall, seat(s),
price, booking reference, QR code.
**O5 — Payment receipt:** receipt no., date, amount, method.
**O6 — My Bookings screen:** the customer's bookings with status (Paid / Cancelled).
**O7 — Sales Report (paper):** tickets sold and revenue for a period, grand total.

---

## 7. Database Design (Tables, Attributes, Data Types) (15 marks)

> PK = Primary Key, FK = Foreign Key. Eight tables.

### customer
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| customer_id | INT (auto) | PK |
| full_name | VARCHAR(100) | |
| email | VARCHAR(100) | |
| phone | VARCHAR(20) | |
| password | VARCHAR(255) | |

### staff
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| staff_id | INT (auto) | PK |
| full_name | VARCHAR(100) | |
| username | VARCHAR(50) | |
| password | VARCHAR(255) | |
| role | ENUM('MANAGER','CASHIER') | |

### movie
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| movie_id | INT (auto) | PK |
| title | VARCHAR(120) | |
| genre | VARCHAR(50) | |
| duration | INT | |
| language | VARCHAR(40) | |
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

### booking
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| booking_id | INT (auto) | PK |
| customer_id | INT | FK → customer |
| show_id | INT | FK → showtime |
| booking_datetime | DATETIME | |
| status | ENUM('Paid','Cancelled','Pending') | |
| total_amount | DECIMAL(8,2) | |

### ticket
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| ticket_id | INT (auto) | PK |
| booking_id | INT | FK → booking |
| seat_number | VARCHAR(8) | |
| price | DECIMAL(8,2) | |

### payment
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| payment_id | INT (auto) | PK |
| booking_id | INT | FK → booking |
| amount | DECIMAL(8,2) | |
| method | ENUM('Card','MobileMoney','Cash') | |
| payment_datetime | DATETIME | |
| status | ENUM('Paid','Failed') | |

### Relationships summary
- movie 1—* showtime *—1 cinema_hall  (a showtime links one movie and one hall)
- customer 1—* booking *—1 showtime  (a customer makes bookings for showtimes)
- booking 1—* ticket  (one booking can hold several seats; one seat per showtime → no double-booking)
- booking 1—1 payment  (each booking is paid once)
- staff operates the system (Manager / Cashier roles)

---

### How to assemble the final PDF
1. Put sections 1, 2, 4, 5, 6, 7 in Excel/Word; the use case table comes from
   `Cinema_Management_System.xlsx`, exported to PDF.
2. Draw the use case diagram in **StarUML** (section 3) and export as PNG.
3. Combine into one PDF named `AndriamparanyRianalaAssignment1.pdf` with your name,
   ID (2504_28605) and cohort (BSE25A/FT/2) on the first page.
