import React, { useEffect, useState } from "react";
import API from "./API";

const ListAdder = () => {
    const [players, setPlayers] = useState<string[]>()

    useEffect(() => {
        API.getAllPlayers().then(response => setPlayers(response.players));
    }, [])

    return <div>
        {players}
    </div>;
}

export default ListAdder;