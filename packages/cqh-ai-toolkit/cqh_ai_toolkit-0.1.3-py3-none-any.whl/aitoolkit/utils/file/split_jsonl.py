def split_jsonl(
    input_file: str, num_parts: int = 15, prefix: str = "part", buffer_size: int = 8192
):
    """
    Splits a JSONL file into multiple sequential parts.
    All parts except the last will have equal size (total_lines // num_parts).
    Any extra lines will be placed in the last part.
    Example:
        100 lines split into 3 parts:
        - Part 1: 33 lines
        - Part 2: 33 lines
        - Part 3: 34 lines (33 + 1 extra)
    """
    with open(input_file, "r", encoding="utf-8") as f:
        total_lines = sum(1 for _ in f)

    if total_lines == 0:
        raise ValueError("Input file is empty")

    base_lines = total_lines // num_parts

    try:
        current_part = 0
        current_line = 0
        output_file = None

        with open(input_file, "r", encoding="utf-8", buffering=buffer_size) as f:
            filename = (
                f"{prefix}{str(current_part + 1).zfill(len(str(num_parts)))}.jsonl"
            )
            output_file = open(filename, "w", encoding="utf-8", buffering=buffer_size)

            for line_number, line in enumerate(f, 1):
                if current_part < num_parts - 1 and current_line >= base_lines:
                    output_file.close()
                    current_part += 1
                    current_line = 0

                    filename = f"{prefix}{str(current_part + 1).zfill(len(str(num_parts)))}.jsonl"
                    output_file = open(
                        filename, "w", encoding="utf-8", buffering=buffer_size
                    )

                output_file.write(line)
                current_line += 1

                if line_number % 10000 == 0:
                    print(
                        f"Processed {line_number}/{total_lines} lines "
                        f"({(line_number / total_lines) * 100:.1f}%)"
                    )

    finally:
        if output_file:
            output_file.close()
