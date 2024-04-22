import React, { useEffect, useState } from "react";
import API from "./API";

const ListAdder = () => {
    const [players, setPlayers] = useState<string[]>([]);
    const [formValues, setFormValues] = useState<{name: string, songs: string[]}>({name: "", songs: [""]})

    useEffect(() => {
        API.getAllPlayers().then(response => setPlayers(response.players));
    }, []);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (players.includes(formValues.name)) {
            console.log("Already submitted");
            return;
        }
        await API.addPlayerList(formValues.name, formValues.songs.filter(x => x));
        let newPlayers = await API.getAllPlayers();
        setPlayers(newPlayers.players);
    };

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        event.preventDefault();
        setFormValues({ ...formValues, name: event.target.value });
    };

    const handleSongsChange = (index: number) => (event: React.ChangeEvent<HTMLInputElement>) => {
        event.preventDefault();
        let songs = formValues.songs;
        songs[index] = event.target.value;
        if (!event.target.value) {
            songs = songs.filter(x => x);
            songs.push("");
        } else if (index+1 === songs.length) {
            songs.push("");
        }
        setFormValues({ ...formValues, songs });
    };

    return <div>
        Players who have already submitted: {players}
        <form onSubmit={handleSubmit}>
            <label>Name: <input type="text" key="name" onChange={handleNameChange} /></label>
            <label>Songs:</label>
            {
                formValues.songs.map((value, index) => <input type="text" key={`song${index}`} onChange={handleSongsChange(index)} value={value} />)
            }
            <button type="submit">Submit</button>
        </form>
    </div>;
}

export default ListAdder;