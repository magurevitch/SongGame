import React, { useEffect, useState } from "react";
import API from "./API";

const ListAdder = () => {
    const [players, setPlayers] = useState<string[]>([]);
    const [songs, setSongs] = useState<string[]>([]);

    useEffect(() => {
        console.log({songs, players});
    }, [songs, players]);

    useEffect(() => {
        API.getAllPlayers().then(response => setPlayers(response.players));
        API.getAllSongs().then(response => setSongs(response.songs));
    }, []);

    return <div>
        {players}
        {songs}
    </div>;
}

export default ListAdder;