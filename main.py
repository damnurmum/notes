# Import necessary modules and classes for note management
from database.notemanage import Note, getnotes, searchnote
from database.databasemain import createtables
import asyncio

# Initialize the database tables on startup
asyncio.run(createtables())


async def selectnote():
    """Function to select and manage a specific note"""
    answer = input("\nSelect your note to view content or delete it: ")

    if answer.isdigit():
        note = Note(answer)
        note_data = await note.get()
        if note_data is not None:
            # Display note title and content
            print("\n\nTitle: {note_title}\nContent: {note_description}".format(
                note_title = note_data['note_title'], 
                note_description = note_data['note_description']
                ))
                    
            print("[1] - Delete note.\n[2] - Return to main menu")

            answer = str(input("Select an option: "))
            if answer.isdigit():
                if int(answer) == 1:
                    # Delete the note from database
                    await note.delete()
                    print("\nYou successfully deleted your note")

                else:
                    pass
                    
        else:
            print("\nNote not found!")

async def mynotes():
    """Function to display all notes and allow selection"""
    notes = await getnotes()

    # Display all available notes with their IDs and titles
    for note in notes:
        print("[{note_id}] - {note_title}".format(note_id = note['note_id'], note_title = note['note_title']))

    await selectnote()




    
async def createnote():
    """Function to create a new note"""
    title = input("Enter note title - ")
    description = input("Enter note content - ")

    # Create new note in database
    note = Note()
    await note.create(title, description)

    print("\n\nYour note was successfully created")

async def searchnotes():
    """Function to search notes by keyword"""
    keyword = input("Enter a keyword to search: ")
    notes = await searchnote(keyword)

    if notes is not None:
        # Display search results
        for note in notes:
            print("[{note_id}] - {note_title}".format(note_id = note['note_id'], note_title = note['note_title']))

        answer = input("Enter the note number to view its content: ")
        if answer.isdigit():
            note = Note(int(answer))
            note_data = await note.get()
            # Display selected note details
            print("\n\nTitle: {note_title}\n\nContent: {note_description}".format(
                note_title = note_data['note_title'], 
                note_description = note_data['note_description']
            ))

async def main():
    """Main menu function with infinite loop for user interaction"""
    while True:
        # Display main menu options
        print('\n\n[1] My notes\n[2] Create note\n[3] Search notes\n\n')

        try:
            answer = int(input("Select an option to manage your notes: "))
        except ValueError:
            print("Invalid input, please enter a number.")
            continue

        if answer == 1:
            # Show all user notes
            await mynotes()            

        elif answer == 2:
            # Create a new note
            await createnote()

        elif answer == 3:
            # Search for notes by keyword
            await searchnotes()
        
        


                        
            
# Run the main application
asyncio.run(main())