import sys
import struct
import os
import subprocess

ELF_MAGIC = b"\x7fELF"


class ELFFile:
    def __init__(self, path):
        self.path = path
        self.data = None
        self.header = None
        self.is_64bit = False
        self.entry_point = 0
        self.load()

    def load(self):
        with open(self.path, "rb") as f:
            self.data = f.read()
            if len(self.data) < 64:
                raise ValueError(f"{self.path} is too small to be a valid ELF file.")
            self.parse_header()

    def parse_header(self):
        if self.data[:4] != ELF_MAGIC:
            raise ValueError(f"{self.path} is not a valid ELF file.")

        if self.data[4] == 2:
            self.is_64bit = True
            try:
                self.header = struct.unpack("16sHHIQQQIHHHHHH", self.data[0:0x40])
                self.entry_point = self.header[3]
            except struct.error as e:
                raise ValueError(f"Error unpacking header of {self.path}: {e}")
        else:
            raise ValueError(f"{self.path} is not a 64-bit ELF file.")

    def get_entry_point(self):
        return self.entry_point

    def get_data(self):
        return self.data


def create_combined_binary(bin1, bin2, output_path):
    bin1_data = bin1.get_data()
    bin2_data = bin2.get_data()

    wrapper_code = f"""
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>

unsigned char bin1[] = {{ {', '.join(str(b) for b in bin1_data)} }};
unsigned char bin2[] = {{ {', '.join(str(b) for b in bin2_data)} }};

void write_bin(const char* filename, unsigned char* data, size_t size) {{
    FILE *f = fopen(filename, "wb");
    fwrite(data, size, 1, f);
    fclose(f);
}}

int main() {{
    write_bin("bin1", bin1, {len(bin1_data)});
    write_bin("bin2", bin2, {len(bin2_data)});

    // Make the binaries executable
    chmod("bin1", 0755);
    chmod("bin2", 0755);

    // Execute the binaries
    if (fork() == 0) {{
        execl("./bin1", "bin1", NULL);
    }}
    printf(" ");
    if (fork() == 0) {{
        execl("./bin2", "bin2", NULL);
    }}

    // Wait for both child processes
    wait(NULL);
    wait(NULL);
    
    remove("bin1");
    remove("bin2");

    return 0;
}}
"""
    with open("wrapper.c", "w") as f:
        f.write(wrapper_code)

    subprocess.run(["gcc", "wrapper.c", "-o", output_path], check=True)

    os.remove("wrapper.c")


def main():
    if len(sys.argv) != 3:
        print("Usage: injector <binary1> <binary2>")
        sys.exit(1)

    bin1_path = sys.argv[1]
    bin2_path = sys.argv[2]

    bin1 = ELFFile(bin1_path)
    bin2 = ELFFile(bin2_path)

    output_path = "combined_binary"

    create_combined_binary(bin1, bin2, output_path)


if __name__ == "__main__":
    main()
