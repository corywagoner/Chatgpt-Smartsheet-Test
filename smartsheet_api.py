from flask import Flask, request, jsonify
import smartsheet

app = Flask(__name__)

# 🔹 Replace with your actual SmartSheet API Key
SMARTSHEET_API_KEY = "F8632UO7roGYOs5ugDMFMO95IHPHlcvtfbcvg"
smart = smartsheet.Smartsheet(SMARTSHEET_API_KEY)

# 🔹 Replace with your actual SmartSheet ID
SHEET_ID = 628387936685956  # Get this from your SmartSheet URL

@app.route("/get_sheet", methods=["GET"])
def get_sheet():
    """ Retrieve all rows from a SmartSheet """
    sheet = smart.Sheets.get_sheet(SHEET_ID)
    data = [
        {col.title: cell.value for col, cell in zip(sheet.columns, row.cells)}
        for row in sheet.rows
    ]
    return jsonify(data)

@app.route("/update_cell", methods=["POST"])
def update_cell():
    """ Update a cell in SmartSheet """
    data = request.json
    row_id = data.get("row_id")
    column_id = data.get("column_id")
    new_value = data.get("value")

    updated_row = smartsheet.models.Row()
    updated_row.id = row_id
    updated_row.cells.append({"column_id": column_id, "value": new_value})

    smart.Sheets.update_rows(SHEET_ID, [updated_row])
    return jsonify({"message": "Cell updated successfully!"})

@app.route("/add_row", methods=["POST"])
def add_row():
    """ Add a new row to the SmartSheet """
    data = request.json
    new_row = smartsheet.models.Row()
    new_row.to_top = True  # Add row at the top

    for col_id, value in data["cells"].items():
        new_row.cells.append({"column_id": int(col_id), "value": value})

    smart.Sheets.add_rows(SHEET_ID, [new_row])
    return jsonify({"message": "Row added successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
