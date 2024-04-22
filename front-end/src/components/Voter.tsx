import React, { useEffect, useState } from "react";
import API from "./API";

const Voter = () => {
    const [songs, setSongs] = useState<string[]>([]);
    
    useEffect(() => {
        API.getAllSongs().then(response => setSongs(response.songs));
    }, []);

    return <div>
        {songs}
    </div>;
}

export default Voter;