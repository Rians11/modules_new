# Cinema Management System — Analysis Report

> **Name:** _Your Name Surname_  **Student ID:** _________  **Cohort:** _________
> File to submit as PDF: `YourNameSurnameAssignment1.pdf`

---

## 1. Brief Introduction (5 marks)

The **Cinema Management System (CMS)** is a software application designed to automate
and manage the day-to-day operations of a movie cinema. It replaces the manual,
paper-based handling of movie schedules, seat reservations and ticketing with a
centralised, reliable and easy-to-use system.

The system allows a **Manager** to maintain the catalogue of movies, the cinema halls
(screens) and their seat layouts, and to schedule screenings (showtimes). A
**Customer** (or a **Cashier** at the box office) can browse available screenings, check
seat availability, select seats, make a booking, pay, and receive a ticket with a QR
code. An **Usher** validates that ticket at the entrance. The system also manages a
snack/concession point, promotions/discounts, and produces management reports
(sales, hall occupancy and movie performance).

The main objectives of the system are to:

- avoid double-booking of seats and reduce queueing time;
- give customers an accurate, real-time view of seat availability;
- speed up ticketing and payment;
- give management reliable reports to support decisions;
- secure access through user authentication and role-based permissions.

**Main actors:** Customer, Cashier (Box-Office Staff), Usher (Ticket Checker),
Manager (Administrator) and an external **Payment Gateway**.

---

## 2. List of Features (Use Cases) — in a table (5 marks)

> The full table is also provided in `cinema_use_cases.csv` (open it in Excel and
> export to PDF as required by the assignment).

| No | Use Case | Actor |
|----|----------|-------|
| 1 | Add Movie | Manager |
| 2 | Update Movie | Manager |
| 3 | Delete Movie | Manager |
| 4 | Search Movie by Title / Genre / Language / Rating | Manager, Cashier, Customer |
| 5 | Add Genre | Manager |
| 6 | Update Genre | Manager |
| 7 | Delete Genre | Manager |
| 8 | Search Genre by Name | Manager |
| 9 | Add Cinema Hall (Screen) | Manager |
| 10 | Update Cinema Hall | Manager |
| 11 | Delete Cinema Hall | Manager |
| 12 | Search Cinema Hall by Name / Capacity / Type | Manager |
| 13 | Configure Seat Layout | Manager |
| 14 | Update Seat | Manager |
| 15 | Delete Seat | Manager |
| 16 | Search Seat by Hall / Row / Type | Manager, Cashier |
| 17 | Add Screening (Showtime) | Manager |
| 18 | Update Screening | Manager |
| 19 | Delete Screening | Manager |
| 20 | Search Screening by Date / Movie / Hall / Time | Manager, Cashier, Customer |
| 21 | Register Customer | Customer, Cashier |
| 22 | Update Customer | Customer, Cashier |
| 23 | Delete Customer | Manager |
| 24 | Search Customer by Id / Name / Email / Phone | Cashier, Manager |
| 25 | Add Staff | Manager |
| 26 | Update Staff | Manager |
| 27 | Delete Staff | Manager |
| 28 | Search Staff by Id / Name / Role | Manager |
| 29 | Check Seat Availability | Customer, Cashier |
| 30 | Select Seats | Customer, Cashier |
| 31 | Create Booking (Reservation) | Customer, Cashier |
| 32 | Update Booking | Customer, Cashier |
| 33 | Cancel Booking | Customer, Cashier |
| 34 | Search Booking by Id / Customer / Date / Screening | Cashier, Manager |
| 35 | Process Payment | Customer, Cashier, Payment Gateway |
| 36 | Issue Refund | Cashier, Manager, Payment Gateway |
| 37 | Search Payment by Id / Date / Customer / Method | Cashier, Manager |
| 38 | Generate Ticket (QR Code) | Cashier, Customer |
| 39 | Cancel Ticket | Cashier, Customer |
| 40 | Validate Ticket at Entrance | Usher |
| 41 | Search Ticket by Code / Booking | Usher, Cashier |
| 42 | Add Snack / Concession Item | Manager |
| 43 | Update Snack | Manager |
| 44 | Delete Snack | Manager |
| 45 | Search Snack by Name / Category | Cashier, Manager |
| 46 | Create Snack Order | Customer, Cashier |
| 47 | Update Snack Order | Customer, Cashier |
| 48 | Cancel Snack Order | Customer, Cashier |
| 49 | Search Snack Order by Id / Customer | Cashier, Manager |
| 50 | Add Promotion / Discount | Manager |
| 51 | Update Promotion | Manager |
| 52 | Delete Promotion | Manager |
| 53 | Apply Promotion to Booking | Cashier, Customer |
| 54 | Search Promotion by Code / Period | Cashier, Manager |
| 55 | Generate Sales Report | Manager |
| 56 | Generate Hall Occupancy Report | Manager |
| 57 | Generate Movie Performance Report | Manager |
| 58 | Manage User Roles / Permissions | Manager |
| 59 | Login | Customer, Cashier, Usher, Manager |
| 60 | Logout | Customer, Cashier, Usher, Manager |

---

## 3. Use Case Diagram(s) — to draw in StarUML (25 marks)

You cannot paste a `.mdj` here, so below is the **exact structure to reproduce in
StarUML**. Tip: because there are 60 use cases, draw **one diagram per subsystem**
(package) rather than a single overloaded diagram — it is cleaner and scores better.

### Actors (stick figures)

- **Customer**
- **Cashier** (Box-Office Staff)
- **Usher** (Ticket Checker)
- **Manager** (Administrator) — *generalises* Cashier when needed (a Manager can do everything a Cashier does)
- **Payment Gateway** — *external/secondary actor* (right-hand side of the diagram)

### Suggested packages (one sub-diagram each)

1. **Movie & Catalogue Management** — UC 1–8 (Movie, Genre). Actor: Manager.
2. **Hall & Seat Management** — UC 9–16 (Hall, Seat). Actor: Manager.
3. **Scheduling** — UC 17–20 (Screening). Actors: Manager, Cashier, Customer.
4. **People Management** — UC 21–28 (Customer, Staff). Actors: Customer, Cashier, Manager.
5. **Booking & Ticketing** — UC 29–41. Actors: Customer, Cashier, Usher, Payment Gateway.
6. **Concession & Promotions** — UC 42–54. Actors: Customer, Cashier, Manager.
7. **Reporting & Security** — UC 55–60. Actors: Manager, all users (Login/Logout).

### Relationships to show (this is where marks are won)

- **`<<include>>`** (mandatory sub-behaviour, dashed arrow pointing to the included UC):
  - *Create Booking* `<<include>>` *Check Seat Availability*
  - *Create Booking* `<<include>>` *Select Seats*
  - *Create Booking* `<<include>>` *Process Payment*
  - *Process Payment* `<<include>>` *Generate Ticket*
  - Every protected use case `<<include>>` *Login* (or simply connect actors to Login once).
- **`<<extend>>`** (optional behaviour, dashed arrow pointing to the base UC):
  - *Apply Promotion to Booking* `<<extend>>` *Create Booking*
  - *Create Snack Order* `<<extend>>` *Create Booking*
  - *Issue Refund* `<<extend>>` *Cancel Booking*
- **Generalisation** (solid line, hollow triangle):
  - *Manager* ▷ *Cashier* (actor generalisation).
  - Optionally *Search Movie* as a parent of more specific searches.

> In StarUML: `Model → Add → UseCaseDiagram`, drop **Actor** and **UseCase**
> elements, link with **Association** (actor↔UC), and use **Include / Extend /
> Generalization** from the toolbox for the dashed/▷ relationships.

---

## 4. Use Case Specifications (25 marks)

Below are **fully written specifications** for the most important use cases, using the
standard template. Replicate the same template for the remaining use cases (the CRUD
ones are short and very similar to one another).

### UC-31 — Create Booking (Reservation)

| Field | Description |
|-------|-------------|
| **Use Case Name** | Create Booking |
| **Use Case ID** | UC-31 |
| **Actor(s)** | Customer (primary), Cashier, Payment Gateway (secondary) |
| **Description** | Allows a customer to reserve one or more seats for a chosen screening and pay for them. |
| **Preconditions** | The user is logged in; at least one screening with free seats exists. |
| **Postconditions** | A booking is recorded as *Confirmed*; the selected seats are marked *Booked*; a ticket is generated. |
| **Trigger** | The customer selects a screening and clicks "Book". |

**Main Flow (Basic Path)**
1. The customer searches and selects a screening (UC-20).
2. The system displays the seat map (`<<include>>` Check Seat Availability, UC-29).
3. The customer selects the desired seat(s) (`<<include>>` Select Seats, UC-30).
4. The system temporarily holds the seats and shows the total price.
5. The customer confirms the booking.
6. The system requests payment (`<<include>>` Process Payment, UC-35).
7. On successful payment, the system creates the booking and generates a ticket
   with a QR code (`<<include>>` Generate Ticket, UC-38).
8. The system displays/sends the confirmation and ticket.

**Alternative / Exception Flows**
- *4a. Seat taken meanwhile:* if another user books the seat first, the system warns
  the customer and asks them to choose another seat.
- *6a. Payment fails:* the system releases the held seats and shows an error.
- *5a. Promotion code entered:* the system applies the discount (`<<extend>>` UC-53)
  and recalculates the total.

---

### UC-35 — Process Payment

| Field | Description |
|-------|-------------|
| **Use Case Name** | Process Payment |
| **Use Case ID** | UC-35 |
| **Actor(s)** | Customer / Cashier (primary), Payment Gateway (secondary) |
| **Description** | Charges the customer for a booking and/or snack order. |
| **Preconditions** | A pending booking/order with a total amount exists. |
| **Postconditions** | A payment record is created with status *Paid* or *Failed*. |
| **Trigger** | The customer confirms payment. |

**Main Flow**
1. The system displays the amount due and available payment methods (Card, Cash, Mobile/Juice).
2. The customer chooses a method and enters the details.
3. The system sends the request to the Payment Gateway.
4. The Gateway authorises the transaction and returns a reference.
5. The system records the payment as *Paid* and returns success.

**Alternative Flows**
- *4a. Authorisation declined:* record payment as *Failed*, notify the user, no booking created.
- *2a. Cash payment:* the cashier records the cash received and the change due.

---

### UC-40 — Validate Ticket at Entrance

| Field | Description |
|-------|-------------|
| **Use Case Name** | Validate Ticket at Entrance |
| **Use Case ID** | UC-40 |
| **Actor(s)** | Usher (primary) |
| **Description** | Verifies that a presented ticket is valid for the current screening and marks it as used. |
| **Preconditions** | The usher is logged in; the ticket exists. |
| **Postconditions** | The ticket status becomes *Used*; entry is granted or refused. |
| **Trigger** | The usher scans the QR code of a ticket. |

**Main Flow**
1. The usher scans the ticket QR code.
2. The system looks up the ticket and its screening.
3. The system checks that the ticket is *Valid*, for the right screening and not yet used.
4. The system marks the ticket *Used* and displays "Access granted" with the seat number.

**Alternative Flows**
- *3a. Ticket already used:* display "Already used", refuse entry.
- *3b. Wrong screening / expired:* display "Invalid ticket", refuse entry.

---

### UC-01 — Add Movie (short CRUD template — copy for the other CRUD use cases)

| Field | Description |
|-------|-------------|
| **Use Case Name** | Add Movie |
| **Use Case ID** | UC-01 |
| **Actor(s)** | Manager |
| **Description** | Adds a new movie to the catalogue. |
| **Preconditions** | The manager is logged in. |
| **Postconditions** | A new movie record is stored. |
| **Main Flow** | 1. Manager opens the "Add Movie" form. 2. Enters title, genre, duration, language, rating, synopsis, poster, release date. 3. Submits. 4. System validates and saves the movie, then confirms. |
| **Alternative Flows** | *3a. Required field missing / duplicate title:* system shows a validation error and the movie is not saved. |

> **Repeat this short template** for: Update/Delete/Search of Movie, Genre, Hall, Seat,
> Screening, Customer, Staff, Snack, Promotion, plus Login and Logout.

---

## 5. Input Design (Forms / Dialog Boxes) (part of I/O — 25 marks)

> The assignment says **hand sketches are enough**. Below is the field list for each
> form so your sketches are complete and consistent. Draw each as a labelled form.

**F1 — Movie Form**
Title | Genre (dropdown) | Duration (min) | Language | Rating/Classification (dropdown) |
Release Date | Synopsis | Poster (file) | Status (Now Showing / Coming Soon) →
Buttons: *Save*, *Clear*, *Delete*.

**F2 — Cinema Hall Form**
Hall Name | Type (2D / 3D / IMAX) | Number of Rows | Seats per Row | Total Capacity (auto) →
*Save*, *Configure Seats*, *Delete*.

**F3 — Screening (Showtime) Form**
Movie (dropdown) | Hall (dropdown) | Date | Start Time | End Time (auto from duration) |
Base Price | Format (2D/3D/IMAX) → *Save*, *Clear*, *Delete*.

**F4 — Customer Registration Form**
First Name | Last Name | Email | Phone | Password | Confirm Password → *Register*, *Cancel*.

**F5 — Booking Form / Seat Selection Dialog**
Screening info (read-only) | Interactive Seat Map (Available / Selected / Booked) |
Selected seats list | Promotion code | Total amount → *Confirm*, *Cancel*.

**F6 — Payment Dialog Box**
Amount Due (read-only) | Payment Method (Card / Cash / Mobile) | Card No. | Expiry | CVV →
*Pay*, *Cancel*.

**F7 — Login Dialog Box**
Username / Email | Password | Role (auto) → *Login*, *Cancel*.

**F8 — Snack Order Form**
Item (dropdown) | Quantity | Add line | Order lines list | Total → *Confirm*, *Cancel*.

---

## 6. Output Design (Screen / Paper) (part of I/O — 25 marks)

> Hand sketches are enough. Each output below should be drawn as a screen or printout.

**O1 — Now Showing screen:** grid of movie posters with title, rating, next showtimes.
**O2 — Seat map screen:** colour-coded seats (green = available, grey = booked, blue = selected).
**O3 — Booking confirmation / Ticket (printout):** cinema name/logo, movie title, date & time,
hall, seat number(s), price, booking reference, **QR code**.
**O4 — Payment receipt:** receipt no., date, items, amount, method, change.
**O5 — Sales Report (paper):** period, list of screenings with tickets sold and revenue,
grand total (very similar in spirit to the cost/benefit sheet in your assignment image).
**O6 — Hall Occupancy Report:** per screening, seats sold / capacity / occupancy %.
**O7 — Movie Performance Report:** per movie, total tickets, total revenue, ranking.

---

## 7. Database Design (Tables, Attributes, Data Types) (15 marks)

> PK = Primary Key, FK = Foreign Key.

### MOVIE
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| movie_id | INT (auto) | PK |
| title | VARCHAR(150) | |
| genre_id | INT | FK → GENRE |
| duration_min | INT | |
| language | VARCHAR(40) | |
| rating | VARCHAR(10) | |
| release_date | DATE | |
| synopsis | TEXT | |
| poster_url | VARCHAR(255) | |
| status | VARCHAR(20) | |

### GENRE
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| genre_id | INT (auto) | PK |
| name | VARCHAR(50) | |

### CINEMA_HALL
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| hall_id | INT (auto) | PK |
| name | VARCHAR(50) | |
| type | VARCHAR(20) | |
| capacity | INT | |

### SEAT
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| seat_id | INT (auto) | PK |
| hall_id | INT | FK → CINEMA_HALL |
| row_label | VARCHAR(2) | |
| seat_number | INT | |
| seat_type | VARCHAR(20) | |

### SCREENING
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| screening_id | INT (auto) | PK |
| movie_id | INT | FK → MOVIE |
| hall_id | INT | FK → CINEMA_HALL |
| show_date | DATE | |
| start_time | TIME | |
| end_time | TIME | |
| base_price | DECIMAL(8,2) | |
| format | VARCHAR(10) | |

### CUSTOMER
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| customer_id | INT (auto) | PK |
| first_name | VARCHAR(50) | |
| last_name | VARCHAR(50) | |
| email | VARCHAR(100) | |
| phone | VARCHAR(20) | |
| password_hash | VARCHAR(255) | |

### STAFF
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| staff_id | INT (auto) | PK |
| first_name | VARCHAR(50) | |
| last_name | VARCHAR(50) | |
| role | VARCHAR(20) | |
| username | VARCHAR(50) | |
| password_hash | VARCHAR(255) | |

### BOOKING
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| booking_id | INT (auto) | PK |
| customer_id | INT | FK → CUSTOMER |
| screening_id | INT | FK → SCREENING |
| booking_datetime | DATETIME | |
| status | VARCHAR(20) | |
| total_amount | DECIMAL(8,2) | |
| promotion_id | INT | FK → PROMOTION (nullable) |

### BOOKING_SEAT  *(links a booking to the seats it reserves)*
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| booking_seat_id | INT (auto) | PK |
| booking_id | INT | FK → BOOKING |
| seat_id | INT | FK → SEAT |
| price | DECIMAL(8,2) | |

### TICKET
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| ticket_id | INT (auto) | PK |
| booking_id | INT | FK → BOOKING |
| qr_code | VARCHAR(255) | |
| status | VARCHAR(20) | |
| issued_at | DATETIME | |

### PAYMENT
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| payment_id | INT (auto) | PK |
| booking_id | INT | FK → BOOKING |
| amount | DECIMAL(8,2) | |
| method | VARCHAR(20) | |
| status | VARCHAR(20) | |
| paid_at | DATETIME | |
| reference | VARCHAR(50) | |

### SNACK
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| snack_id | INT (auto) | PK |
| name | VARCHAR(50) | |
| category | VARCHAR(30) | |
| price | DECIMAL(8,2) | |

### SNACK_ORDER
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| order_id | INT (auto) | PK |
| customer_id | INT | FK → CUSTOMER |
| order_datetime | DATETIME | |
| total_amount | DECIMAL(8,2) | |

### SNACK_ORDER_ITEM
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| order_item_id | INT (auto) | PK |
| order_id | INT | FK → SNACK_ORDER |
| snack_id | INT | FK → SNACK |
| quantity | INT | |
| line_price | DECIMAL(8,2) | |

### PROMOTION
| Attribute | Data Type | Key |
|-----------|-----------|-----|
| promotion_id | INT (auto) | PK |
| code | VARCHAR(20) | |
| description | VARCHAR(100) | |
| discount_percent | DECIMAL(5,2) | |
| start_date | DATE | |
| end_date | DATE | |

### Relationships summary
- GENRE 1—* MOVIE · CINEMA_HALL 1—* SEAT · CINEMA_HALL 1—* SCREENING ·
  MOVIE 1—* SCREENING · CUSTOMER 1—* BOOKING · SCREENING 1—* BOOKING ·
  BOOKING 1—* BOOKING_SEAT *—1 SEAT · BOOKING 1—1 TICKET · BOOKING 1—* PAYMENT ·
  CUSTOMER 1—* SNACK_ORDER 1—* SNACK_ORDER_ITEM *—1 SNACK · PROMOTION 1—* BOOKING.

---

### How to assemble the final PDF
1. Put sections 1, 2, 4, 5, 6, 7 into Word/Excel as the assignment instructs
   (use cases table from `cinema_use_cases.csv` in Excel, then export to PDF).
2. Draw the use case diagram(s) in **StarUML** following section 3 and export as image.
3. Combine everything into one PDF named `YourNameSurnameAssignment1.pdf` with your
   name, student id and cohort on the first page.
