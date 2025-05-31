import os
import pandas as pd
import sys


def get_content_after_colon(text):
    """Extract content after the first colon in a string."""
    if ":" in text:
        return text.split(":", 1)[1].strip()
    return text.strip()


def get_content_after_dot(text):
    """Extract content after the first dot in a string."""
    if "." in text:
        return text.split(".", 1)[1].strip()
    return text.strip()


def extract_content_sections(text):
    """Extract the three sections from the response content."""
    # Remove any outer quotes if present
    text = text.strip('"')
    text = text.replace("\t", "")  # Remove \t characters
    text = text.replace("\\t", "")  # Remove \t characters
    text = text.replace('"', "")  # Remove escaped quotes
    text = text.replace('"', "")

    # Split by newline character
    if "\n\n" in text:
        sections = text.split("\n\n")
    elif "\\n" in text:
        sections = text.split("\\n")
    elif ";" in text:
        sections = text.split(";")
    else:
        raise ValueError("Unexpected format in text: {}".format(text))

    # Clean up sections
    sections = [section.strip() for section in sections if section.strip()]

    if not len(sections) == 3:
        print("--------------------")
        print("text:", text)
        print("Content sections:", sections)
        raise ValueError(
            "Expected three sections in the content, but found: {}".format(
                len(sections)
            )
        )

    # Parse each section
    title = get_content_after_colon(sections[0]).replace("\\", "").strip()
    tags = get_content_after_colon(sections[1]).replace("\\", "").strip()
    category = get_content_after_colon(sections[2]).replace("\\", "").strip()

    # ensure that the comma seperated tags are unique
    tags = ", ".join(sorted(set(tag.strip() for tag in tags.split(","))))

    title = get_content_after_dot(title)
    tags = get_content_after_dot(tags)
    category = get_content_after_dot(category)

    # if the length of the title is smaller than 3 words, then duplicate the title
    if len(title.split()) < 5:
        title = title + " - " + title

    return title, tags, category


def analyze_output_files(folder_path, output_file):
    """Process all text files in the specified folder and create a table."""
    results = []

    # Check if the directory exists
    if not os.path.isdir(folder_path):
        print(f"Directory not found: {folder_path}")
        return

    # Process each text file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)

            try:
                # Read the text file directly (one-liner)
                with open(file_path, "r") as f:
                    content = f.read().strip()

                # Extract the title, tags, and category
                title, tags, category = extract_content_sections(content)

                # Add to results
                results.append(
                    {
                        "Filename": file_name[:-13]
                        + ".jpeg",  # Remove the last 13 characters from the filename _response.txt
                        "Description": title,
                        "Keywords": tags,
                        "Categories": category,
                        "Editorial": "no",
                        "Mature content": "no",
                        "illustration": "no",
                    }
                )

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Create a DataFrame and display as a table
    if results:
        df = pd.DataFrame(results)

        # Display the table
        # print(df.to_string(index=False))
        print("\nAnalysis Results:")
        print(df.shape)

        # Optional: Save to CSV
        # folder_name = os.path.basename(folder_path)
        # csv_path = os.path.join(os.path.dirname(folder_path), f"{folder_name}_output_analysis.csv")
        csv_path = output_file
        df.to_csv(csv_path, index=False)
        print(f"\nResults saved to {csv_path}")
    else:
        print("No results found.")


if __name__ == "__main__":
    # Get argument from command line via argparser package
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze output files and create a summary table."
    )
    parser.add_argument(
        "--folder_path", help="Folder containing output files to analyze"
    )
    parser.add_argument(
        "--output_file", default="6_image_tags.csv", help="Output CSV file name"
    )
    args = parser.parse_args()
    folder_path = args.folder_path
    output_file_name = args.output_file

    output_file_path = os.path.join(os.path.dirname(folder_path), output_file_name)
    print(f"Analyzing output files in: {folder_path}")
    analyze_output_files(folder_path, output_file_path)
    print(f"Output CSV file: {output_file_path}")
