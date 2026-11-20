import csv


def read_sales(summary, error_file):
    """reads all sales in csv"""

    total_quantity = 0
    total_sales = 0.0
    invalid_sales = 0

    with open("sales.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)

        for line_number, row in enumerate(reader, start=2):

            if validate_sale(row):
                update_summary(summary, row)

                total_quantity += int(row[2])
                total_sales += float(row[3])

            else:
                reason = "invalid sale"

                log_error(error_file, line_number, row, reason)
                invalid_sales += 1

    return total_quantity, total_sales, invalid_sales

def validate_sale(row):
    """checks and validates the info"""

    if len(row) != 4:
        return False

    if row[0].strip() == "" or row[1].strip() == "":
        return False

    try:
        quantity = int(row[2])
        price = float(row[3])

    except ValueError:
        return False

    if quantity <= 0 or price < 0:
        return False

    return True


def update_summary(summary, row):
    """adds sales"""

    item = row[1]
    quantity = int(row[2])
    price = float(row[3])

    if item not in summary:
        summary[item] = {"Qty": 0, "Price Total": 0.0}

    summary[item]["Qty"] += quantity
    summary[item]["Price Total"] += price


def log_error(error_file, line_number, row, reason):
    """records the invalid sales in errors.log"""

    try:
        error_file.write(
            f"line {line_number} | {reason} | {','.join(row)}\n"
        )

    except OSError:
        print("could not write to the error log.")


def save_summary(summary):
    """saves sales to the csv file"""

    with open("sales_summary.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Item", "Qty", "Price Total"])

        for item in sorted(summary):
            writer.writerow([
                item,
                summary[item]["Qty"],
                f"{summary[item]['Price Total']:.2f}"
            ])


def display_totals(total_quantity, total_sales, invalid_sales):
    """display the sale total"""

    print("\nsales processing complete")
    print("-----------------------------")
    print(f"total items sold: {total_quantity}")
    print(f"sales total: ${total_sales:.2f}")
    print(f"invalid sales: {invalid_sales}")
    print("files created: sales_summary.csv, errors.log")


def main():
    """runs the program"""

    summary = {}

    with open("errors.log", "w") as error_file:
        total_quantity, total_sales, invalid_sales = read_sales(
            summary, error_file
        )

    save_summary(summary)

    display_totals(total_quantity, total_sales, invalid_sales)


if __name__ == "__main__":
    main()
