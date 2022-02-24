
import argparse

def main():
    parser = argparse.ArgumentParser(description = "Arguments for Reddit scraping")
    parser.add_argument("--input", type = str, help = "Name of input file")
    parser.add_argument("--output", type = str, help = "Name of output file")
    parser.add_argument("--num_sent", type = int, help = "Number of sentences to subset")
    args = parser.parse_args()

    counter = 0

    input_file = open(args.input, encoding = "utf-8")
    output_file = open(args.output, "w", encoding = "utf-8")
    
    while counter < args.num_sent:
        line = input_file.readline()
        output_file.write(line)
        counter += 1
        

if __name__ == '__main__':
    main()


