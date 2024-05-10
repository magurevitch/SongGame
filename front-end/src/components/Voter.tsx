import React, { useEffect, useState } from "react";
import API from "./API";
import { Song } from "../Models";

const Voter = () => {
    const [songs, setSongs] = useState<Song[]>([]);
    const [chosenSongs, setChosenSongs] = useState<Set<Song>>(new Set());
    
    useEffect(() => {
        API.getAllSongs().then(response => setSongs(response.songs));
    }, []);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        await API.vote(Array.from(chosenSongs));
        console.log("vote cast");
    };

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        let index: number = parseInt(event.target.value);
        if(event.target.checked) {
            chosenSongs.add(songs[index]);
        } else {
            chosenSongs.delete(songs[index]);
        }
        setChosenSongs(chosenSongs);
    };

    return <form onSubmit={handleSubmit}>
        {songs.map((song,index) => <label>
            <input type="checkbox" key={index} value={index} onChange={handleChange}/>
            {song.song_title} - {song.artist}
            <br/>
        </label>)}
        <button type="submit">Submit</button>
    </form>;
}

export default Voter;