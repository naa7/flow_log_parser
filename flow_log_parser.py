import csv


class FlowLogParser:
    def __init__(self, flow_log_file, lookup_table_file, output_file):
        self.flow_log_file = flow_log_file
        self.lookup_table_file = lookup_table_file
        self.output_file = output_file

    def load_lookup_table(self):
        lookup_table = {}

        try:
            with open(self.lookup_table_file, "r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if len(row) < 3:
                        continue

                    dstport = int(row["dstport"])
                    protocol = row["protocol"].lower()
                    tag = row["tag"]

                    if (dstport, protocol) not in lookup_table:
                        lookup_table[(dstport, protocol)] = []

                    lookup_table[(dstport, protocol)].append(tag)

        except Exception as e:
            print(f"Unexpected error while loading lookup table: {e}")
            raise

        return lookup_table

    def parse_flow_log(self, lookup_table):
        tags_count = {}
        port_protocol_count = {}
        protocol_map = {"6": "tcp", "17": "udp", "1": "icmp"}

        try:
            with open(self.flow_log_file, "r") as file:

                for line in file:
                    if len(line.strip()) == 0:
                        continue

                    parts = line.split()

                    if parts[0] != "2":
                        continue

                    dstport = int(parts[6])
                    protocol_num = parts[7]
                    protocol = protocol_map.get(protocol_num, "Unknown")
                    tags = lookup_table.get((dstport, protocol), ["Untagged"])

                    for tag in tags:
                        tags_count[tag] = tags_count.get(tag, 0) + 1

                    port_protocol_count[(dstport, protocol)] = (
                        port_protocol_count.get((dstport, protocol), 0) + 1
                    )

        except Exception as e:
            print(f"Unexpected error while parsing flow log: {e}")
            raise

        return tags_count, port_protocol_count

    def write_output(self, tags_count, port_protocol_count):
        try:
            with open(self.output_file, "w") as file:

                file.write("Tag Counts:\n")
                file.write("Tag,Count\n")

                for tag, count in tags_count.items():
                    file.write(f"{tag},{count}\n")

                file.write("\nPort/Protocol Combination Counts:\n")
                file.write("Port,Protocol,Count\n")

                for (port, protocol), count in port_protocol_count.items():
                    file.write(f"{port},{protocol},{count}\n")

        except Exception as e:
            print(f"Unexpected error while writing output: {e}")
            raise

    def run(self):
        try:
            lookup_table = self.load_lookup_table()
            tags_count, port_protocol_count = self.parse_flow_log(lookup_table)
            self.write_output(tags_count, port_protocol_count)

        except Exception as e:
            print(f"Error: {e}")


def main():
    flow_log_file = "flow_log.txt"
    lookup_table_file = "lookup_table.csv"
    output_file = "output.txt"

    parser = FlowLogParser(flow_log_file, lookup_table_file, output_file)
    parser.run()


if __name__ == "__main__":
    main()
