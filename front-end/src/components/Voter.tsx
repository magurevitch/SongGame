import React, { useEffect, useState } from "react";
import API from "./API";

const Voter = () => {
    const [songs, setSongs] = useState<string[]>([]);
    const [chosenSongs, setChosenSongs] = useState<Set<string>>(new Set());
    
    useEffect(() => {
        API.getAllSongs().then(response => setSongs(response.songs));
    }, []);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        await API.vote(Array.from(chosenSongs));
        console.log("vote cast");
    };

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if(event.target.checked) {
            chosenSongs.add(event.target.value);
        } else {
            chosenSongs.delete(event.target.value);
        }
        setChosenSongs(chosenSongs);
    };

    return <form onSubmit={handleSubmit}>
        {songs.map(song => <label>
            <input type="checkbox" key={song} value={song} onChange={handleChange}/>
            {song}
            <br/>
        </label>)}
        <button type="submit">Submit</button>
    </form>;
}

export default Voter;