# `imports:snapshot`

```sh
rai imports:snapshot [OPTIONS] [schema:<col_name>=<type>, ...] [syntax:<option>=<value>, ...]
```

Load data from a CSV file into a RelationalAI model.
The CSV file may be local or hosted publicly on Azure or S3.

> [!IMPORTANT]
> `imports:snapshot` is only available for Azure-based models.

## Options

| Option | Type | Description |
| :------ | :--- | :------------ |
| `--source` | Text | The path to the local file or URL of the remote file to import. |
| `--model` | Text | The name of the [model](../python/Model/README.md) in which to import the data. |
| `--name` | Text | The name to assign to the resource in the model. Defaults to the file name, including the extension. |
| `--type` | Text | The file type. May be one of `"auto"` (default) or `"csv"`. |

## Arguments

<!-- markdownlint-disable no-inline-html -->

| Argument | Required | Description |
| :--------- | :--- | :------------ |
| `schema:<col_name>=<type>` | No | Set the type of the column named `<col_name>` to `<type>`.<br><br>`<type>` may be one of:<br><br>- `string`<br>- `boolean`<br>- `int`<br>- `float` |
| `syntax:header_row=<line_number>` | No | Set the line number of the header row in the CSV file. Defaults to `1`. The values `-1` and `0` indicate that the file has no header row. |
| `syntax:datarow=<line_number>` | No | Set the line number from which to begin parsing data from the CSV file. If missing, defaults to the first line after the header row. |
| `syntax:missingstrings=<string1>` | No | Set the string that represents missing (null) values in the CSV file. Defaults to `""`.  |
| `syntax:delim=<delimiter>` | No | Set the delimiter used in the CSV file. Defaults to `","`. |
| `syntax:quotechar=<char>` | No | Set the character used to quote fields in the CSV file. Defaults to `"`. |
| `syntax:escapechar=<char>` | No | Set the character used to escape the quote characters in the CSV file. Defaults to a backslash (`\`). |
| `syntax:decimalchar=<char>` | No | Set the character used to represent the decimal point in the CSV file. Defaults to a period (`.`). |
| `syntax:groupmark=<char>` | No | Set the character used to group digits in numbers. By default, group marks are not permitted in numbers. Set the group mark to the comma (`,`) to parse numbers such as `1,000.0`. |

<!-- markdownlint-enable no-inline-html -->

## Example

Run `rai imports:snapshot` without any arguments to use the built-in CLI prompts to select and upload a file.
After you select the model to use and the file to upload, you are asked to provide a resource name,
which defaults to the name of the file, and verify the file's schema:

```sh
$ rai imports:snapshot

---------------------------------------------------

▰▰▰▰ Models fetched

? Select a model: myModel

? Select a file: data/transactions.csv
? name: transactions.csv

  Field    Type     Ex.
 ────────────────────────────────
  id       String   TXN-00004052
  date     String   2023-10-12
  from     String   P-00013130
  to       String   P-00015417
  amount   Number   5214

? Use this schema for transactions.csv: Yes
▰▰▰▰ Snapshot for transactions.csv created

---------------------------------------------------
```

Use the `--source`, `--model`, and `--name` flags to load a file without interactively selecting the file, model, and resource name.
You must still interactively confirm the schema of the file:

```sh
$ rai imports:snapshot --source data/transactions.csv --model myModel --name transactions

---------------------------------------------------

  Field    Type     Ex.
 ────────────────────────────────
  id       String   TXN-00004052
  date     String   2023-10-12
  from     String   P-00013130
  to       String   P-00015417
  amount   Number   5214

? Use this schema for transactions: Yes
▰▰▰▰ Snapshot for transactions created

---------------------------------------------------
```

To change the default schema, pass additional command-line arguments of the form `schema:<column_name>=<type>`.
For example, to use `string` for the `amount` column, pass the arg `schema:amount=string`.
As usual, you are asked to verify the schema before the snapshot is uploaded:

```sh
$ rai imports:snapshot --source data/transactions.csv --model myModel --name transactions schema:amount=string

---------------------------------------------------

? name: transactions.csv

  Field    Type     Ex.
 ────────────────────────────────
  id       String   TXN-00004052
  date     String   2023-10-12
  from     String   P-00013130
  to       String   P-00015417
  amount   String   5214

? Use this schema for transactions: Yes
▰▰▰▰ Snapshot for transactions created

---------------------------------------------------
```

You may provide multiple `schema:*` arguments to customize the schema as needed.

Once you create the snapshot, you may add objects from the file to your model in
a [`model.read()`](../python/Model/read.md) context:

```python
import relationalai as rai

model = rai.Model("myModel")
Transaction = model.Type("Transaction")

# Create `Transaction` objects from the rows of the "transactions.csv" resource.
with model.read("transactions.csv") as row:
    # Columns, like `id`, are accessed as attributes of the `row` object.
    transaction = Transaction.add(id=row.id)
    # If a column name is a Python keyword, such as the `from` column, use `getattr()`.
    transaction.set(
        date=row.date,
        from_=getattr(row, "from"),
        to=row.to
    )
```

In the preceding example, `from` is a [Python keyword](https://docs.python.org/3/reference/lexical_analysis.html#keywords),
so accessing `row.from` raises a `SyntaxError`.
To circumvent this, rename the column in the file or use Python's built-in
[`getattr()`](https://docs.python.org/3/library/functions.html#getattr) function.

## See Also

[`imports:list`](./imports_list.md),
[`imports:delete`](./imports_delete.md),
and [`imports:stream`](./imports_stream.md).
