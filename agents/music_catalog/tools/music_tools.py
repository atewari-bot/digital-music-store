from langchain_core.tools import tool
from da.db import get_chinook_db
import ast
import logging

@tool
def get_albums_by_artist(artist: str) -> str:
    """
    Returns a list of albums by the specified artist.
    
    Args:
        artist (str): The name of the artist to search for.
        
    Returns:
        list[dict]: A list of albums that match the specified artist.
    """
    try:
        if not artist or not artist.strip():
            return "Error: Artist name cannot be empty."
        
        # Execute the query to get albums by the artist from Album and Artist tables
        # `db.run` is a utility from LangChain to execute SQL queries
        # `include_columns=True` indicates that the result should include column names
        # Note: Album table has Title column, not Name
        result = get_chinook_db().run(
            f"""
            SELECT Album.Title, Artist.Name as ArtistName
            FROM Album
            JOIN Artist ON Album.ArtistId = Artist.ArtistId
            WHERE Artist.Name like '%{artist}%'
            """,
            include_columns=True,
        )
        return result if result else f"No albums found for artist '{artist}'"
    except Exception as e:
        logging.error(f"Error in get_albums_by_artist: {e}")
        return f"Error retrieving albums for artist '{artist}': {str(e)}"

@tool
def get_tracks_by_artist(artist: str) -> str:
    """
    Returns a list of tracks by the specified artist.
    
    Args:
        artist (str): The name of the artist to search for.
        
    Returns:
        list[dict]: A list of tracks that match the specified artist.
    """
    try:
        if not artist or not artist.strip():
            return "Error: Artist name cannot be empty."
        
        # Execute the query to get tracks by the artist from Track, Album, and Artist tables
        result = get_chinook_db().run(
            f"""
            SELECT Track.Name as SongName, Artist.Name as ArtistName
            FROM Album
            LEFT JOIN Track ON Track.AlbumId = Album.AlbumId
            LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
            WHERE Artist.Name like '%{artist}%'
            """,
            include_columns=True,
        )
        return result if result else f"No tracks found for artist '{artist}'"
    except Exception as e:
        logging.error(f"Error in get_tracks_by_artist: {e}")
        return f"Error retrieving tracks for artist '{artist}': {str(e)}"

@tool
def get_songs_by_genre(genre: str) -> list:
    """
    Returns a list of songs by the specified genre.
    
    Args:
        genre (str): The name of the genre to search for.
        
    Returns:
        list[dict]: A list of songs that match the specified genre.
    """
    try:
        if not genre or not genre.strip():
            return ["Error: Genre name cannot be empty."]
        
        # Execute the query to get songs by the genre from Track and Genre tables
        db = get_chinook_db()
        # First, get the GenreId for the specified genre
        genre_id_query = f"Select GenreId from Genre where Name like '%{genre}%'"
        genre_id_result = db.run(genre_id_query, include_columns=True)

        # If no genre is found, return an empty list
        if not genre_id_result or not genre_id_result[0]:
            return [f"No genre found for '{genre}'"]
        
        # Safely evaluate the result to get the genre_ids
        genre_ids = ast.literal_eval(genre_id_result)

        # Extract the GenreId from the result - validate it's numeric
        try:
            genre_id_list = ", ".join([str(int(genre_id['GenreId'])) for genre_id in genre_ids])
        except (ValueError, KeyError) as e:
            logging.error(f"Error parsing genre IDs: {e}")
            return [f"Error processing genre '{genre}': Invalid genre ID format"]

        # Now, query the Track table for songs with the specified GenreId
        songs = db.run(
            f"""
            SELECT Track.Name as SongName, Artist.Name as ArtistName
            FROM Track
            LEFT JOIN Album ON Track.AlbumId = Album.AlbumId
            LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
            WHERE Track.GenreId IN ({genre_id_list})
            GROUP BY Artist.Name
            LIMIT 10;
            """,
            include_columns=True,
        )

        # If no songs are found, return a message
        if not songs:
            return [f"No songs found for genre '{genre}'"]
        
        formatted_songs = ast.literal_eval(songs)
        logging.debug(f"Found {len(formatted_songs)} songs for genre '{genre}'")
        return [
            {
                "Song": str(song["SongName"]),
                "Artist": str(song["ArtistName"])
            } for song in formatted_songs
        ]
    except Exception as e:
        logging.error(f"Error in get_songs_by_genre: {e}")
        return [f"Error retrieving songs for genre '{genre}': {str(e)}"]

@tool
def check_for_songs(song_title: str) -> str:
    """
    Checks if songs with the specified title exist in the catalog.
    
    Args:
        song_title (str): The title of the song to check.
        
    Returns:
        str: A message indicating whether the song exists or not.
    """
    try:
        if not song_title or not song_title.strip():
            return "Error: Song title cannot be empty."
        
        # Execute the query to check if the song exists in the Track table
        result = get_chinook_db().run(
            f"""
            SELECT Track.Name, Album.Title, Artist.Name as ArtistName
            FROM Track
            LEFT JOIN Album ON Track.AlbumId = Album.AlbumId
            LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
            WHERE Track.Name like '%{song_title}%'
            LIMIT 20
            """,
            include_columns=True,
        )
        
        if not result:
            return f"No songs found with title '{song_title}'"
        
        return result
    except Exception as e:
        logging.error(f"Error in check_for_songs: {e}")
        return f"Error checking for songs with title '{song_title}': {str(e)}"

def get_music_tools():
    """
    Returns a list of music-related tools.
    
    This function provides a list of tools that can be used to interact with the music catalog,
    including searching for albums, tracks, and genres.
    
    Returns:
        list: A list of music-related tools.
    """
    return [
        get_albums_by_artist,
        get_tracks_by_artist,
        get_songs_by_genre,
        check_for_songs
    ]