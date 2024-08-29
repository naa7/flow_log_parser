# Flow Log Parser

## Overview

The Flow Log Parser program is designed to parse a flow log file and map each row to a tag based on a lookup table. It then generates an output file with counts of matches for each tag and each port/protocol combination.

## Assumptions and Limitations

1. **Log Format**:

   - The program supports only the default flow log format as specified in the [AWS documentation](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html).
   - Only version 2 of the log format is supported. Logs of other versions or custom formats are not handled.

2. **Case Insensitivity**:

   - Matching between protocols and the lookup table is case insensitive.

3. **Lookup Table**:

   - The lookup table is assumed to be well-formed with the columns `dstport`, `protocol`, and `tag`.
   - Lines with fewer than 3 columns in the lookup table are skipped.
   - The lookup table is read as a CSV file with up to 10,000 mappings.

4. **Flow Log File**:

   - The flow log file is assumed to be a plain text file.
   - The file size can be up to 10 MB.
   - Empty lines in the flow log file are skipped.

5. **Protocols**:

   - The program maps protocol numbers to `tcp`, `udp`, and `icmp`. Other protocols are considered "Unknown" and will not be matched.

6. **Error Handling**:
   - Basic error handling is implemented to catch unexpected errors during file reading/writing and parsing.

## Installation and Running

1. **Requirements**:

   - Python 3.x
   - No additional libraries or packages are required beyond the Python standard library.

2. **Files**:

   - `flow_log.txt`: Input file containing flow log data.
   - `lookup_table.csv`: CSV file containing the lookup table with columns `dstport`, `protocol`, and `tag`.
   - `output.txt`: Output file where results will be written.

3. **Running the Program**:
   - Ensure that the `flow_log.txt`, `lookup_table.csv`, and `output.txt` files are in the same directory as the script.
   - Run the script using the following command:
     ```bash
     python flow_log_parser.py
     ```

## Tests

The following tests were performed to validate the program:

1. **Basic Functionality**:

   - Verified that the program correctly parses the sample flow log data and produces the expected counts in the output file.

2. **Case Insensitivity**:

   - Tested with varied case formats in the lookup table to ensure case-insensitive matching.

3. **Error Handling**:
   - Simulated missing or malformed files to ensure the program handles such errors gracefully.

## Analysis

1. **Performance**:

   - The program handles flow log files up to 10 MB efficiently by processing each line in a single pass and using dictionaries for lookups and counts.

2. **Scalability**:

   - While the current implementation handles the given constraints well, performance may be impacted if the file size or the number of mappings exceeds the defined limits.

3. **Future Improvements**:
   - Consider adding support for additional log formats or versions if required.
   - Enhance the error handling to provide more specific error messages.
