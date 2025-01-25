# Jinja2 HTML template for the PNR details report
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PNR Details</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>PNR Details</h1>
    <table>
        <tr><th>Train Number</th><td>{{ train_number }}</td></tr>
        <tr><th>Train Name</th><td>{{ train_name }}</td></tr>
        <tr><th>Boarding Date</th><td>{{ boarding_date }}</td></tr>
        <tr><th>From</th><td>{{ from_ }}</td></tr>
        <tr><th>To</th><td>{{ to }}</td></tr>
        <tr><th>Reserved Upto</th><td>{{ reserved_upto }}</td></tr>
        <tr><th>Boarding Point</th><td>{{ boarding_point }}</td></tr>
        <tr><th>Class</th><td>{{ class_ }}</td></tr>
        <tr><th>S. No.</th><td>{{ s_no }}</td></tr>
        <tr><th>Booking Status</th><td>{{ booking_status }}</td></tr>
        <tr><th>Current Status</th><td>{{ current_status }}</td></tr>
        <tr><th>Coach Position</th><td>{{ coach_position }}</td></tr>
    </table>
</body>
</html>
"""
