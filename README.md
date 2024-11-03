# Code Injector

## Introduction

This project involves developing a "binary injector" that merges two programs into one. The primary objective is to inject a target program into another program, making the final executable run both in sequence.

By understanding binary headers and entry points, the tool merges the functionality of two binaries into one.

## Supported Formats

- **ELF** for Linux systems
  
## Setup

   We are not allowed to push binaries so complation is necessary...

   ```bash
   gcc bin.c -o bin_c
   gcc helloworld.c -o helloworld_c
   ```

## Usage

1. **Prepare two binaries**: The first binary is the target which is to be executed first. The second binary is the one being injected. `I have supplied bin_c and helloworld_c both compiled from C, only files that are a certain size will work for my code but any short code compiled from C will be fine`

2. **Inject the second binary into the first**:

   To use the below command as you see it you will have to compile the `injector.py`, but it is not a necessity.

   ```bash
   ./injector <target_binary> <second_binary>
   ```

   For example:

   ```bash
   python3 injector.py helloworld_c bin_c
   ```

3. **Execution**: After injecting, run the combined binary:

   ```bash
   ./combined_binary
   ```

   Output example:

   ```bash
   01
   hello world
   ```

The output demonstrates that the original target program (`bin`) runs, followed by the injected program's output (`helloworld`).

## Technical Details

- The injector modifies the entry point of the target program, allowing execution of both the original binary and the injected binary.
- It reads the binary headers of the target and adjusts them to include the injected binary's code.
