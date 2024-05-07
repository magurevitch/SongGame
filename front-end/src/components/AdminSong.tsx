import React, { useEffect, useState } from "react";
import { Song } from "../Models";

const AdminSong: React.FunctionComponent<{song: Song, updateSong: any}> = ({song, updateSong}) => {
    return <li>
        <input type="text" onChange={(e) => updateSong({song_title: e.target.value, artist: song.artist})} value={song.song_title} />
            -
        <input type="text" onChange={(e) => updateSong({song_title: song.song_title, artist: e.target.value})} value={song.artist} />
    </li>
}

export default AdminSong;