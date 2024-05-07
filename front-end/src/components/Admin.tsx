import React, { useEffect, useState } from "react";
import API from "./API";
import Phase from "../Phase";
import AdminSong from "./AdminSong";

const Admin: React.FunctionComponent<{setPhase: any}> = ({setPhase}) => {
    const [players, setPlayers] = useState<string[]>([]);
    const [songs, setSongs] = useState<string[]>([]);

    useEffect(() => {
        API.getAllPlayers().then(response => setPlayers(response.players));
        API.getAllSongs().then(response => setSongs(response.songs));
    }, []);

    return <div>
        <div>Players: {players.join(", ")}</div>
        <div>Songs: 
            <ol>
                {songs.map(song => <AdminSong song={song} />)}
            </ol>
        </div>
        <div>
            {[Phase.ADD_LIST, Phase.VOTE, Phase.SCORE].map(phase =>
                <button onClick={async () => {
                    await API.changeGamePhase(phase)
                    setPhase(phase);
                }}>
                    Start {Phase[phase]}
                </button>
            )}
        </div>
    </div>;
}

export default Admin;