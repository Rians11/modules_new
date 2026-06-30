"""Generate a simple, Word-style Input & Output Design section (HTML -> PDF).
Plain black & white, like a basic Microsoft Word document."""

U = "________________"   # underscore field

HTML = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page { size: A4; margin: 2cm; }
body { font-family:'Calibri','Liberation Sans',Arial,sans-serif; color:#000; font-size:12pt; line-height:1.5; }
h1 { font-size:16pt; font-weight:bold; }
h2 { font-size:13pt; font-weight:bold; margin-top:18px; }
.box { border:1px solid #000; width:330px; margin:14px auto; padding:14px 22px; }
.box .ttl { text-align:center; font-weight:bold; margin-bottom:12px; letter-spacing:1px; }
.box .f { margin:7px 0; }
.box .b { text-align:center; margin-top:12px; font-weight:bold; }
table { border-collapse:collapse; width:100%; margin:8px 0 16px 0; }
th,td { border:1px solid #000; padding:5px 9px; text-align:left; font-size:11pt; }
th { font-weight:bold; }
.ticket { border:1px solid #000; width:300px; margin:10px auto; padding:14px 20px; }
.ticket .ttl { text-align:center; font-weight:bold; border-bottom:1px solid #000; padding-bottom:6px; margin-bottom:8px; }
.center { text-align:center; }
.pb { page-break-before: always; }
p.small { font-size:11pt; }
</style></head><body>

<h1>5. Input Design (Forms / Dialog Boxes)</h1>

<div class="box">
  <div class="ttl">LOGIN</div>
  <div class="f">Username : """ + U + """</div>
  <div class="f">Password : """ + U + """</div>
  <div class="b">[ Login ]</div>
</div>

<div class="box">
  <div class="ttl">ADD MOVIE</div>
  <div class="f">Title : """ + U + """</div>
  <div class="f">Genre : """ + U + """</div>
  <div class="f">Duration : """ + U + """</div>
  <div class="f">Language : """ + U + """</div>
  <div class="f">Rating : """ + U + """</div>
  <div class="b">[ Add ]&nbsp;&nbsp;[ Update ]&nbsp;&nbsp;[ Delete ]</div>
</div>

<div class="box">
  <div class="ttl">ADD SHOWTIME</div>
  <div class="f">Movie : """ + U + """</div>
  <div class="f">Cinema Hall : """ + U + """</div>
  <div class="f">Date : """ + U + """</div>
  <div class="f">Time : """ + U + """</div>
  <div class="f">Ticket Price : """ + U + """</div>
  <div class="b">[ Save ]</div>
</div>

<div class="box">
  <div class="ttl">BOOK TICKET</div>
  <div class="f">Customer Name : """ + U + """</div>
  <div class="f">Phone Number : """ + U + """</div>
  <div class="f">Showtime (Movie / Date / Time) : """ + U + """</div>
  <div class="f">Seat Number : """ + U + """</div>
  <div class="f">Payment Method : """ + U + """</div>
  <div class="b">[ Book ]</div>
</div>

<p class="small"><i>Note: the other data-entry forms (Add Genre, Add Cinema Hall, Add Staff,
Add Customer, Add Snack, Add Promotion) follow the same layout as the Add Movie form above.</i></p>

<h2>Dialog Boxes</h2>

<div class="box" style="width:380px">
  <div class="ttl">Confirm Booking</div>
  <div class="center">Would you confirm the booking of 2 seats for "Avengers" (15/04/2025, 17h00)?</div>
  <div class="b">[ Confirm ]&nbsp;&nbsp;[ Cancel ]</div>
</div>

<div class="box" style="width:380px">
  <div class="ttl">Delete Movie</div>
  <div class="center">Are you sure you want to delete this movie? This action is irreversible.</div>
  <div class="b">[ Yes (Delete) ]&nbsp;&nbsp;[ No ]</div>
</div>

<!-- ====================== OUTPUT ====================== -->
<h1 class="pb">6. Output Design (Screen / Paper)</h1>

<h2>Movie List</h2>
<table>
<tr><th>ID</th><th>Title</th><th>Genre</th><th>Duration</th><th>Rating</th></tr>
<tr><td>1</td><td>Avengers</td><td>Action</td><td>143 min</td><td>PG-13</td></tr>
<tr><td>2</td><td>The Rookie</td><td>Series</td><td>45 min</td><td>PG</td></tr>
<tr><td>3</td><td>Scream</td><td>Horror</td><td>114 min</td><td>18</td></tr>
<tr><td>4</td><td>Afterburn</td><td>Comedy</td><td>98 min</td><td>PG-13</td></tr>
</table>

<h2>Seat Map (plan of the room)</h2>
<p class="small">Rows A, B, C and columns 1-5. Colour code: Green = available, Red = sold, Blue = selected.</p>
<table style="width:auto">
<tr><th>&nbsp;</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><th>A</th><td>A1</td><td>A2</td><td>A3 (sold)</td><td>A4</td><td>A5</td></tr>
<tr><th>B</th><td>B1</td><td>B2 (sel)</td><td>B3 (sel)</td><td>B4 (sold)</td><td>B5</td></tr>
<tr><th>C</th><td>C1</td><td>C2</td><td>C3</td><td>C4</td><td>C5 (sold)</td></tr>
</table>

<h2>Booking Summary (before payment)</h2>
<table>
<tr><th>Film</th><th>Showtime</th><th>Seats</th><th>Quantity</th><th>Unit Price</th><th>Total</th></tr>
<tr><td>Avengers</td><td>15/04/2025 17h00 - Hall 4</td><td>B2, B3</td><td>2</td><td>20.00</td><td>40.00</td></tr>
</table>

<h2>Ticket (printout)</h2>
<div class="ticket">
  <div class="ttl">CINEMA MANAGEMENT SYSTEM</div>
  <div class="f">Movie : Avengers</div>
  <div class="f">Room : 4</div>
  <div class="f">Date : 15/04/2025</div>
  <div class="f">Time : 17h00</div>
  <div class="f">Seat : B2, B3</div>
  <div class="f">N&deg; Ticket : 10066</div>
</div>

<h2>Sales Report (paper)</h2>
<table>
<tr><th>Date</th><th>Movie</th><th>Tickets Sold</th><th>Revenue</th></tr>
<tr><td>15/04/2025</td><td>Avengers</td><td>120</td><td>2,400.00</td></tr>
<tr><td>15/04/2025</td><td>Scream</td><td>80</td><td>1,440.00</td></tr>
<tr><td>Total</td><td>&nbsp;</td><td>200</td><td>3,840.00</td></tr>
</table>

</body></html>"""

with open("IO_Design.html", "w") as f:
    f.write(HTML)
print("Saved IO_Design.html (Word style)")
