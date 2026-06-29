# Cinema Management System — Analysis Report (Simplified)

> **Name:** ANDRIAMPARANY Rianala Joan  **ID:** 2504_28605  **Cohort:** BSE25A/FT/2
> File to submit as PDF: `AndriamparanyRianalaAssignment1.pdf`

> This is a **clean, simplified** version of the Cinema Management System analysis:
> 2 actors, 16 use cases and 6 tables. Everything is internally consistent and easy to
> present. (The ticket price is stored on each show, which removes the need for a separate
> pricing table.)

---

## 1. Brief Introduction (5 marks)

The **Cinema Management System (CMS)** is a desktop application that automates the main
operations of a cinema: managing movies, cinema halls, show scheduling and ticket booking.
It replaces manual, paper-based record keeping with a centralised system backed by a
relational database.

The system is operated by an **Administrator** who first logs in. The administrator
maintains the catalogue of movies, registers the cinema halls and their seating capacity,
and schedules shows (each show links a movie to a hall at a given date, time and ticket
price). The core operation is **ticket booking**: the administrator selects a show and a
seat, records the customer's details, the system saves the ticket and marks the seat as
sold so it cannot be sold twice. The administrator can also view sold tickets, cancel a
ticket and generate a simple sales report.

Main objectives:

- keep reliable records of movies, halls and shows (full CRUD);
- sell tickets while preventing double-booking of seats;
- store customer details against each ticket;
- secure access through administrator login.

**Actors:**

- **Administrator** — *primary* actor; logs in and performs every function.
- **Customer** — *secondary* actor; does not log in but takes part in ticket booking
  (provides name and phone, and receives the ticket).

---

## 2. List of Features (Use Cases) — table (5 marks)

> Also in `cinema_use_cases.csv` / `Cinema_Management_System.xlsx` (open in Excel, export to PDF).

| No | Use Case | Actor |
|----|----------|-------|
| 1 | Login | Administrator |
| 2 | Logout | Administrator |
| 3 | Add Movie | Administrator |
| 4 | Update Movie | Administrator |
| 5 | Delete Movie | Administrator |
| 6 | View / Search Movies | Administrator |
| 7 | Add Cinema Hall | Administrator |
| 8 | View Cinema Halls | Administrator |
| 9 | Add Movie Show | Administrator |
| 10 | Update Movie Show | Administrator |
| 11 | Delete Movie Show | Administrator |
| 12 | View / Search Movie Shows | Administrator |
| 13 | Book Ticket | Administrator (primary), Customer (secondary) |
| 14 | Cancel Ticket | Administrator |
| 15 | View Sold Tickets | Administrator |
| 16 | Generate Sales Report | Administrator |

---

## 3. Use Case Diagram — to draw in StarUML (25 marks)

One single, clean diagram.

### Actors
- **Administrator** — *primary* actor, stick figure on the **left**. Connected to all 16 use cases.
- **Customer** — *secondary* actor, stick figure on the **right**. Connected **only** to `Book Ticket`.

### Associations
- A plain line (Association) from **Administrator** to every use case.
- A plain line from **Customer** to `Book Ticket` only.

### Relationships that earn the marks
- **`<<include>>`** (dashed arrow, base → included). `Book Ticket` includes two mandatory steps:
  - `Book Ticket` ──▷ `Check Seat Availability`
  - `Book Ticket` ──▷ `Calculate Ticket Price`

> StarUML steps: `Model → Add Diagram → Use Case Diagram`. Drop **Actor** and **UseCase**
> elements, link them with **Association**, and use the **Include** tool for the two dashed
> `<<include>>` arrows from *Book Ticket*. (You may draw the two included use cases —
> *Check Seat Availability* and *Calculate Ticket Price* — as small ovals next to Book Ticket.)
> Export: `File → Export Diagram As → PNG`.

---

## 4. Use Case Specifications (25 marks)

Full specifications for the key use cases; replicate the short CRUD template for the rest.

### UC-13 — Book Ticket  *(the core operation)*

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-13 |
| **Use Case Name** | Book Ticket |
| **Actor(s)** | Administrator (primary), Customer (secondary) |
| **Description** | Sells a ticket for a chosen show and seat, records the customer and marks the seat as sold. |
| **Preconditions** | The administrator is logged in; at least one show with a free seat exists. |
| **Postconditions** | A ticket is saved against the show and customer; the seat becomes unavailable. |
| **Trigger** | The administrator opens the booking screen and selects a show. |

**Main Flow**
1. The administrator selects a movie show.
2. The administrator selects a seat number.
3. The system checks the seat is still free (`<<include>>` Check Seat Availability).
4. The administrator enters the customer's name and phone.
5. The system reads the show's ticket price (`<<include>>` Calculate Ticket Price).
6. The administrator confirms; the system saves the ticket and marks the seat as sold.
7. The system shows a confirmation message.

**Alternative / Exception Flows**
- *3a. Seat already sold:* the system shows "Seat already booked" and asks for another seat.
- *4a. Missing customer details:* the system shows a validation error; the ticket is not saved.

---

### UC-01 — Login

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Login |
| **Actor(s)** | Administrator |
| **Description** | Authenticates the administrator before granting access to the system. |
| **Preconditions** | The application is running; a valid account exists. |
| **Postconditions** | The administrator is authenticated and the main menu opens. |

**Main Flow**
1. The administrator enters username and password.
2. The system validates the credentials against the database.
3. On success, the main menu opens.

**Alternative Flows**
- *2a. Invalid credentials:* the system shows "Invalid login credentials" and stays on the login screen.

---

### UC-09 — Add Movie Show

| Field | Description |
|-------|-------------|
| **Use Case ID** | UC-09 |
| **Use Case Name** | Add Movie Show |
| **Actor(s)** | Administrator |
| **Description** | Schedules a movie in a hall at a given date, time and ticket price. |
| **Preconditions** | The administrator is logged in; at least one movie and one hall exist. |
| **Postconditions** | A new show record is stored. |

**Main Flow**
1. Open the Show Management screen.
2. Choose a movie and a hall, enter date, time and ticket price.
3. Click Add.
4. The system validates and saves the show, then refreshes the table.

**Alternative Flows**
- *3a. A show already exists for that hall at that date/time:* the system shows a duplicate error.

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
| **Main Flow** | 1. Open Movie Management. 2. Enter title, genre, duration. 3. Click Add. 4. Validate and save, refresh the table. |
| **Alternative Flows** | *3a. Duplicate title / missing field:* show an error; the movie is not saved. |

> **Repeat this short template** for: Update/Delete/View Movie, Add/View Hall,
> Update/Delete/View Show, Cancel Ticket, View Sold Tickets, Generate Sales Report, Logout.

---

## 5. Input Design (Forms / Dialog Boxes) (part of I/O — 25 marks)

> Hand sketches are enough; this is the field list per screen.

**F1 — Login.** Username | Password → *Login*.

**F2 — Movie Management.** Title | Genre | Duration (min) → *Add*, *Update*, *Delete*, *Clear*; table of movies.

**F3 — Hall Management.** Hall Name | Capacity → *Add*; table of halls.

**F4 — Show Management.** Movie (dropdown) | Hall (dropdown) | Date | Time | Ticket Price →
*Add*, *Update*, *Delete*; table of shows.

**F5 — Ticket Booking.** Show (dropdown) | Seat Number | Customer Name | Customer Phone |
Price (auto, read-only) → *Book*.

**F6 — Sold Tickets.** Table of sold tickets with a selectable row → *Cancel Ticket*.

---

## 6. Output Design (Screen / Paper) (part of I/O — 25 marks)

> Hand sketches are enough.

**O1 — Main menu:** buttons to Movies, Halls, Shows, Booking, Tickets, Report.
**O2 — Movies table:** title, genre, duration.
**O3 — Shows table:** movie, hall, date, time, price.
**O4 — Booking confirmation:** "Ticket booked" with seat number and price; seat shown as sold.
**O5 — Sold tickets table:** ticket id, show, seat, customer, price, purchase date.
**O6 — Sales Report (paper):** list of tickets sold for a period with the total revenue.
**O7 — Error dialogs:** invalid login, duplicate movie title, seat already booked.

---

## 7. Database Design (Tables, Attributes, Data Types) (15 marks)

> PK = Primary Key, FK = Foreign Key. Six clean tables.

### user
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| user_id | INT (auto) | PK |
| username | VARCHAR(50) | |
| password | VARCHAR(100) | |

### movie
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| movie_id | INT (auto) | PK |
| title | VARCHAR(120) | |
| genre | VARCHAR(50) | |
| duration | INT | |

### cinema_hall
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| hall_id | INT (auto) | PK |
| hall_name | VARCHAR(60) | |
| capacity | INT | |

### movie_show
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| show_id | INT (auto) | PK |
| movie_id | INT | FK → movie |
| hall_id | INT | FK → cinema_hall |
| show_date | DATE | |
| show_time | TIME | |
| ticket_price | DECIMAL(8,2) | |

### customer
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| customer_id | INT (auto) | PK |
| full_name | VARCHAR(100) | |
| phone | VARCHAR(20) | |

### ticket
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| ticket_id | INT (auto) | PK |
| show_id | INT | FK → movie_show |
| customer_id | INT | FK → customer |
| seat_number | INT | |
| price | DECIMAL(8,2) | |
| purchase_date | DATETIME | |

### Relationships summary
- movie 1—* movie_show *—1 cinema_hall  (a show links one movie and one hall)
- movie_show 1—* ticket  (a show has many tickets; one seat per show → no double-booking)
- customer 1—* ticket  (a ticket belongs to one customer)

---

### How to assemble the final PDF
1. Put sections 1, 2, 4, 5, 6, 7 in Excel/Word; the use case table comes from
   `Cinema_Management_System.xlsx`, exported to PDF.
2. Draw the single use case diagram in **StarUML** (section 3) and export as PNG.
3. Combine into one PDF named `AndriamparanyRianalaAssignment1.pdf` with your name,
   ID (2504_28605) and cohort (BSE25A/FT/2) on the first page.
