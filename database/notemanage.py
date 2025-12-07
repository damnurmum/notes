# Import database connection function and aiosqlite module
from database.databasemain import connectdb
import aiosqlite


async def getnotes() -> list or None:
    """
    Retrieves all notes from the database.
    
    Returns:
        list: List of dictionaries containing note data (note_id, note_title, note_description)
        None: If no notes are found in the database
    """
    notes = []

    # Connect to database
    db, sql = await connectdb()

    # Execute SELECT query to get all notes
    await sql.execute("SELECT * FROM notes")
    result = await sql.fetchall()

    # Close database connection
    await db.close()

    if result is not None:
    
        # Convert database records to dictionary format
        for note in result:
            notes.append(
                {
                    "note_id": note[0],
                    "note_title": note[1],
                    "note_description": note[2]
                }
            )

        return notes
    else:
        return None

async def searchnote(keyword: str) -> list or None:
    """
    Searches for notes matching a keyword in title or description.
    
    Args:
        keyword (str): The search term to look for in notes
        
    Returns:
        list: List of matching notes with note_id and note_title
        None: If no matches are found
    """
    db, sql = await connectdb()

    # Execute search query using LIKE operator for partial matches
    await sql.execute("SELECT note_id, note_title FROM notes WHERE note_title LIKE ? OR note_description LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    result = await sql.fetchall()
    
    # Close database connection
    await db.close()
    
    notes_id = []
    if result is not None:
        # Convert results to dictionary format
        for note in result:
            notes_id.append({"note_id": note[0], "note_title": note[1]})

        return notes_id
    
    else:
        return None

class Note:
    """
    Manages CRUD operations for individual notes.
    Provides methods to create, read, delete, and manage note data.
    """

    def __init__(self, note_id: int = None):
        """
        Initialize a Note object.
        
        Args:
            note_id (int, optional): The ID of an existing note. Defaults to None for new notes.
        """
        self.note_id = note_id

    async def create(self, note_title: str, note_description: str) -> int:
        """
        Creates a new note in the database.
        
        Args:
            note_title (str): The title of the note
            note_description (str): The content/description of the note
            
        Returns:
            int: The ID of the newly created note
        """

        db, sql = await connectdb()

        # Insert new note into database
        await sql.execute("INSERT INTO notes VALUES (NULL, ?, ?)", (str(note_title), str(note_description),))

        # Store the auto-generated note ID
        self.note_id = sql.lastrowid

        # Commit changes and close connection
        await db.commit()
        await db.close()

    async def delete(self) -> bool:
        """
        Deletes a note from the database by its ID.
        
        Returns:
            bool: True if deletion was successful, False if note_id is not set
        """

        if self.note_id is not None:
            db, sql = await connectdb()

            # Delete note where ID matches the current note_id
            await sql.execute("DELETE FROM notes WHERE note_id = ?", (self.note_id,))

            # Commit changes and close connection
            await db.commit()
            await db.close()

            return True
        else:
            return False
        
    async def get(self) -> dict:
        """
        Retrieves the complete data of a note by its ID.
        
        Returns:
            dict: Dictionary containing note_id, note_title, and note_description
            None: If the note is not found or note_id is not set
        """

        if self.note_id is not None:
            db, sql = await connectdb()

            # Query database for note with matching ID
            await sql.execute("SELECT * FROM notes WHERE note_id = ?", (self.note_id,))
            note = await sql.fetchone()
            await db.close()

            if note is not None:
                # Convert database record to dictionary format
                data = {
                    "note_id": note[0],
                    "note_title": note[1],
                    "note_description": note[2]
                }

                return dict(data)
            
            else:
                return None
        else:
            return None
        

    

                