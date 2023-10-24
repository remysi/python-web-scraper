import os


# Creates a .txt file out of given string and removes all whitespace in it
def all_text_to_txt_file(text):
    with open('pageText.txt', 'w', encoding='utf-8') as file:
        cleaned_text = ''.join(text.split())
        file.write(cleaned_text)


# Creates a .txt file out of given list of links and removes all whitespace in it
def list_of_links_to_txt_file(links):
    with open('pageLinks.txt', 'w', encoding='utf-8') as file:
        for link in links:
            cleaned_link = ''.join(link.split())
            file.write(cleaned_link + '\n')


# Creates a .txt file of one link also requires a name of the file to be created when called
def link_to_txt_file(file_name, subdirectory, link):

    # Folder structure
    parent_directory = 'scraper files'

    # Main directory is created if it doesn't exist yet
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    # Subdirectory path is created from parent directory name and given subdirectory name
    subdirectory_path = os.path.join(parent_directory, subdirectory)

    # Subdirectories are created if they don't exist
    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path)

    # File path is made by joining subdirectory path and file name together
    file_path = os.path.join(subdirectory_path, file_name)

    # Navigates to wanted directory and creates a new .txt file and writes to it if there is not a file already with
    # the same name
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(link)