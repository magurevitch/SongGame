import React, { useEffect, useState } from "react";
import API from "./API";

type Song = {
    song: string;
    artist: string;
}

const ListAdder = () => {
    const [players, setPlayers] = useState<string[]>([]);
    const [formValues, setFormValues] = useState<{name: string, songs: Song[]}>({name: "", songs: [{song: "", artist: ""}]})

    useEffect(() => {
        API.getAllPlayers().then(response => setPlayers(response.players));
    }, []);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (players.includes(formValues.name)) {
            console.log("Already submitted");
            return;
        }
        await API.addPlayerList(formValues.name, formValues.songs.filter(x => x.song).map(x => `${x.song} - ${x.artist || "Unknown"}`));
        let newPlayers = await API.getAllPlayers();
        setPlayers(newPlayers.players);
    };

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        event.preventDefault();
        setFormValues({ ...formValues, name: event.target.value });
    };

    const handleSongsChange = (index: number, isArtist: boolean) => (event: React.ChangeEvent<HTMLInputElement>) => {
        event.preventDefault();
        let songs = formValues.songs;
        if(isArtist) {
            songs[index].artist = event.target.value;
        } else {
            songs[index].song = event.target.value;
        }
        if (!songs[index].song) {
            songs = songs.filter(x => x.song);
            songs.push({song: "", artist: ""});
        } else if (index+1 === songs.length) {
            songs.push({song: "", artist: ""});
        }
        setFormValues({ ...formValues, songs });
    };

    return <div>
        Players who have already submitted: {players.join(", ")}
        <br/>
        <form onSubmit={handleSubmit}>
            <label>Name: <input type="text" key="name" onChange={handleNameChange} /></label>
            <br/>
            <label>Songs - Artists:</label>
            {
                formValues.songs.map((value, index) => <div>
                    <input type="text" key={`song${index}`} onChange={handleSongsChange(index, false)} value={value.song} />
                    -
                    <input type="text" key={`artist${index}`} onChange={handleSongsChange(index, true)} value={value.artist} />
                </div>)
            }
            <button type="submit">Submit</button>
        </form>
    </div>;
}

export default ListAdder;