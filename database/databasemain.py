# Import the aiosqlite module for asynchronous database operations
import aiosqlite

async def connectdb() -> aiosqlite.connect:
    """
    Establishes and returns a connection to the database with a cursor.
    
    Returns:
        tuple: (db connection object, cursor object)
    """

    db = await aiosqlite.connect('database/base.db')
    sql = await db.cursor()

    return db, sql


async def createtables():
    """
    Creates the 'notes' table in the database if it doesn't already exist.
    Table structure:
        - note_id: Auto-incrementing primary key
        - note_title: Text field for note title
        - note_description: Text field for note content
    """

    db, sql = await connectdb()

    # Create notes table with auto-increment ID
    await sql.execute("""CREATE TABLE IF NOT EXISTS notes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_title TEXT,
        note_description TEXT
    )""")

    # Commit changes and close connection
    await db.commit()
    await db.close()